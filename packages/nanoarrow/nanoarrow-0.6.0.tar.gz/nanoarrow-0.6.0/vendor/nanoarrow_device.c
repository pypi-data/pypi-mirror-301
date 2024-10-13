// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

#include <errno.h>
#include <inttypes.h>

#include "nanoarrow.h"
#include "nanoarrow_device.h"

ArrowErrorCode ArrowDeviceCheckRuntime(struct ArrowError* error) {
  const char* nanoarrow_runtime_version = ArrowNanoarrowVersion();
  const char* nanoarrow_ipc_build_time_version = NANOARROW_VERSION;

  if (strcmp(nanoarrow_runtime_version, nanoarrow_ipc_build_time_version) != 0) {
    ArrowErrorSet(error, "Expected nanoarrow runtime version '%s' but found version '%s'",
                  nanoarrow_ipc_build_time_version, nanoarrow_runtime_version);
    return EINVAL;
  }

  return NANOARROW_OK;
}

static void ArrowDeviceArrayInitDefault(struct ArrowDevice* device,
                                        struct ArrowDeviceArray* device_array,
                                        struct ArrowArray* array) {
  memset(device_array, 0, sizeof(struct ArrowDeviceArray));
  device_array->device_type = device->device_type;
  device_array->device_id = device->device_id;
  ArrowArrayMove(array, &device_array->array);
}

static ArrowErrorCode ArrowDeviceCpuBufferInitAsync(struct ArrowDevice* device_src,
                                                    struct ArrowBufferView src,
                                                    struct ArrowDevice* device_dst,
                                                    struct ArrowBuffer* dst,
                                                    void* stream) {
  if (device_dst->device_type != ARROW_DEVICE_CPU ||
      device_src->device_type != ARROW_DEVICE_CPU) {
    return ENOTSUP;
  }

  if (stream != NULL) {
    return EINVAL;
  }

  ArrowBufferInit(dst);
  dst->allocator = ArrowBufferAllocatorDefault();
  NANOARROW_RETURN_NOT_OK(ArrowBufferAppend(dst, src.data.as_uint8, src.size_bytes));
  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCpuBufferMove(struct ArrowDevice* device_src,
                                               struct ArrowBuffer* src,
                                               struct ArrowDevice* device_dst,
                                               struct ArrowBuffer* dst) {
  if (device_dst->device_type != ARROW_DEVICE_CPU ||
      device_src->device_type != ARROW_DEVICE_CPU) {
    return ENOTSUP;
  }

  ArrowBufferMove(src, dst);
  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCpuBufferCopy(struct ArrowDevice* device_src,
                                               struct ArrowBufferView src,
                                               struct ArrowDevice* device_dst,
                                               struct ArrowBufferView dst, void* stream) {
  if (device_dst->device_type != ARROW_DEVICE_CPU ||
      device_src->device_type != ARROW_DEVICE_CPU) {
    return ENOTSUP;
  }

  if (stream != NULL) {
    return EINVAL;
  }

  memcpy((uint8_t*)dst.data.as_uint8, src.data.as_uint8, dst.size_bytes);
  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCpuSynchronize(struct ArrowDevice* device,
                                                void* sync_event, void* stream,
                                                struct ArrowError* error) {
  switch (device->device_type) {
    case ARROW_DEVICE_CPU:
      if (sync_event != NULL || stream != NULL) {
        ArrowErrorSet(error, "sync_event and stream must be NULL for ARROW_DEVICE_CPU");
        return EINVAL;
      } else {
        return NANOARROW_OK;
      }
    default:
      ArrowErrorSet(error, "Expected CPU device but got device type %d",
                    (int)device->device_id);
      return ENOTSUP;
  }
}

static void ArrowDeviceCpuRelease(struct ArrowDevice* device) { device->release = NULL; }

struct ArrowDevice* ArrowDeviceCpu(void) {
  static struct ArrowDevice* cpu_device_singleton = NULL;
  if (cpu_device_singleton == NULL) {
    cpu_device_singleton = (struct ArrowDevice*)ArrowMalloc(sizeof(struct ArrowDevice));
    ArrowDeviceInitCpu(cpu_device_singleton);
  }

  return cpu_device_singleton;
}

void ArrowDeviceInitCpu(struct ArrowDevice* device) {
  device->device_type = ARROW_DEVICE_CPU;
  device->device_id = -1;
  device->array_init = NULL;
  device->array_move = NULL;
  device->buffer_init = &ArrowDeviceCpuBufferInitAsync;
  device->buffer_move = &ArrowDeviceCpuBufferMove;
  device->buffer_copy = &ArrowDeviceCpuBufferCopy;
  device->synchronize_event = &ArrowDeviceCpuSynchronize;
  device->release = &ArrowDeviceCpuRelease;
  device->private_data = NULL;
}

struct ArrowDevice* ArrowDeviceResolve(ArrowDeviceType device_type, int64_t device_id) {
  NANOARROW_UNUSED(device_id);
  if (device_type == ARROW_DEVICE_CPU) {
    return ArrowDeviceCpu();
  }

  if (device_type == ARROW_DEVICE_METAL) {
    struct ArrowDevice* default_device = ArrowDeviceMetalDefaultDevice();
    if (device_id == default_device->device_id) {
      return default_device;
    }
  }

  if (device_type == ARROW_DEVICE_CUDA || device_type == ARROW_DEVICE_CUDA_HOST) {
    return ArrowDeviceCuda(device_type, device_id);
  }

  return NULL;
}

ArrowErrorCode ArrowDeviceArrayInitAsync(struct ArrowDevice* device,
                                         struct ArrowDeviceArray* device_array,
                                         struct ArrowArray* array, void* sync_event,
                                         void* stream) {
  if (device->array_init != NULL) {
    return device->array_init(device, device_array, array, sync_event, stream);
  }

  // Sync event and stream aren't handled by the fallback implementation
  if (sync_event != NULL || stream != NULL) {
    return EINVAL;
  }

  ArrowDeviceArrayInitDefault(device, device_array, array);
  return NANOARROW_OK;
}

ArrowErrorCode ArrowDeviceBufferInitAsync(struct ArrowDevice* device_src,
                                          struct ArrowBufferView src,
                                          struct ArrowDevice* device_dst,
                                          struct ArrowBuffer* dst, void* stream) {
  int result = device_dst->buffer_init(device_src, src, device_dst, dst, stream);
  if (result == ENOTSUP) {
    result = device_src->buffer_init(device_src, src, device_dst, dst, stream);
  }

  return result;
}

ArrowErrorCode ArrowDeviceBufferMove(struct ArrowDevice* device_src,
                                     struct ArrowBuffer* src,
                                     struct ArrowDevice* device_dst,
                                     struct ArrowBuffer* dst) {
  int result = device_dst->buffer_move(device_src, src, device_dst, dst);
  if (result == ENOTSUP) {
    result = device_src->buffer_move(device_src, src, device_dst, dst);
  }

  return result;
}

ArrowErrorCode ArrowDeviceBufferCopyAsync(struct ArrowDevice* device_src,
                                          struct ArrowBufferView src,
                                          struct ArrowDevice* device_dst,
                                          struct ArrowBufferView dst, void* stream) {
  int result = device_dst->buffer_copy(device_src, src, device_dst, dst, stream);
  if (result == ENOTSUP) {
    result = device_src->buffer_copy(device_src, src, device_dst, dst, stream);
  }

  return result;
}

struct ArrowBasicDeviceArrayStreamPrivate {
  struct ArrowDevice* device;
  struct ArrowArrayStream naive_stream;
};

static int ArrowDeviceBasicArrayStreamGetSchema(
    struct ArrowDeviceArrayStream* array_stream, struct ArrowSchema* schema) {
  struct ArrowBasicDeviceArrayStreamPrivate* private_data =
      (struct ArrowBasicDeviceArrayStreamPrivate*)array_stream->private_data;
  return private_data->naive_stream.get_schema(&private_data->naive_stream, schema);
}

static int ArrowDeviceBasicArrayStreamGetNext(struct ArrowDeviceArrayStream* array_stream,
                                              struct ArrowDeviceArray* device_array) {
  struct ArrowBasicDeviceArrayStreamPrivate* private_data =
      (struct ArrowBasicDeviceArrayStreamPrivate*)array_stream->private_data;

  struct ArrowArray tmp;
  NANOARROW_RETURN_NOT_OK(
      private_data->naive_stream.get_next(&private_data->naive_stream, &tmp));
  int result = ArrowDeviceArrayInit(private_data->device, device_array, &tmp, NULL);
  if (result != NANOARROW_OK) {
    ArrowArrayRelease(&tmp);
    return result;
  }

  return NANOARROW_OK;
}

static const char* ArrowDeviceBasicArrayStreamGetLastError(
    struct ArrowDeviceArrayStream* array_stream) {
  struct ArrowBasicDeviceArrayStreamPrivate* private_data =
      (struct ArrowBasicDeviceArrayStreamPrivate*)array_stream->private_data;
  return private_data->naive_stream.get_last_error(&private_data->naive_stream);
}

static void ArrowDeviceBasicArrayStreamRelease(
    struct ArrowDeviceArrayStream* array_stream) {
  struct ArrowBasicDeviceArrayStreamPrivate* private_data =
      (struct ArrowBasicDeviceArrayStreamPrivate*)array_stream->private_data;
  ArrowArrayStreamRelease(&private_data->naive_stream);
  ArrowFree(private_data);
  array_stream->release = NULL;
}

ArrowErrorCode ArrowDeviceBasicArrayStreamInit(
    struct ArrowDeviceArrayStream* device_array_stream,
    struct ArrowArrayStream* array_stream, struct ArrowDevice* device) {
  struct ArrowBasicDeviceArrayStreamPrivate* private_data =
      (struct ArrowBasicDeviceArrayStreamPrivate*)ArrowMalloc(
          sizeof(struct ArrowBasicDeviceArrayStreamPrivate));
  if (private_data == NULL) {
    return ENOMEM;
  }

  private_data->device = device;
  ArrowArrayStreamMove(array_stream, &private_data->naive_stream);

  device_array_stream->device_type = device->device_type;
  device_array_stream->get_schema = &ArrowDeviceBasicArrayStreamGetSchema;
  device_array_stream->get_next = &ArrowDeviceBasicArrayStreamGetNext;
  device_array_stream->get_last_error = &ArrowDeviceBasicArrayStreamGetLastError;
  device_array_stream->release = &ArrowDeviceBasicArrayStreamRelease;
  device_array_stream->private_data = private_data;
  return NANOARROW_OK;
}

void ArrowDeviceArrayViewInit(struct ArrowDeviceArrayView* device_array_view) {
  memset(device_array_view, 0, sizeof(struct ArrowDeviceArrayView));
}

void ArrowDeviceArrayViewReset(struct ArrowDeviceArrayView* device_array_view) {
  ArrowArrayViewReset(&device_array_view->array_view);
  device_array_view->device = NULL;
}

ArrowErrorCode ArrowDeviceArrayViewSetArrayMinimal(
    struct ArrowDeviceArrayView* device_array_view, struct ArrowDeviceArray* device_array,
    struct ArrowError* error) {
  // Resolve device
  struct ArrowDevice* device =
      ArrowDeviceResolve(device_array->device_type, device_array->device_id);
  if (device == NULL) {
    ArrowErrorSet(error,
                  "Can't resolve device with type %" PRId32 " and identifier %" PRId64,
                  device_array->device_type, device_array->device_id);
    return EINVAL;
  }

  // Set the device array device
  device_array_view->device = device;

  // Populate the array_view
  NANOARROW_RETURN_NOT_OK(ArrowArrayViewSetArrayMinimal(&device_array_view->array_view,
                                                        &device_array->array, error));

  // Populate the sync_event
  device_array_view->sync_event = device_array->sync_event;

  return NANOARROW_OK;
}

// Walks the tree of arrays to count the number of buffers with unknown size
// and the number of bytes we need to copy from a device buffer to find it.
static ArrowErrorCode ArrowDeviceArrayViewWalkUnknownBufferSizes(
    struct ArrowArrayView* array_view, int64_t* offset_buffer_size) {
  switch (array_view->storage_type) {
    case NANOARROW_TYPE_STRING:
    case NANOARROW_TYPE_BINARY:
    case NANOARROW_TYPE_LARGE_STRING:
    case NANOARROW_TYPE_LARGE_BINARY:
      if (array_view->length == 0 || array_view->buffer_views[1].size_bytes == 0) {
        array_view->buffer_views[2].size_bytes = 0;
      } else if (array_view->buffer_views[2].size_bytes == -1) {
        *offset_buffer_size += array_view->layout.element_size_bits[1] / 8;
      }
      break;
    default:
      break;
  }

  // Recurse for children
  for (int64_t i = 0; i < array_view->n_children; i++) {
    NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewWalkUnknownBufferSizes(
        array_view->children[i], offset_buffer_size));
  }

  // ...and for dictionary
  if (array_view->dictionary != NULL) {
    NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewWalkUnknownBufferSizes(
        array_view->dictionary, offset_buffer_size));
  }

  return NANOARROW_OK;
}

// Walks the tree of arrays and launches an async copy of the relevant
// item in the array's offset buffer to the temporary buffer we've just
// allocated to collect these values.
static ArrowErrorCode ArrowDeviceArrayViewResolveUnknownBufferSizesAsync(
    struct ArrowDevice* device, struct ArrowArrayView* array_view,
    uint8_t** offset_value_dst, void* stream) {
  int64_t offset_plus_length = array_view->offset + array_view->length;

  struct ArrowBufferView src_view;
  struct ArrowBufferView dst_view;

  switch (array_view->storage_type) {
    case NANOARROW_TYPE_STRING:
    case NANOARROW_TYPE_BINARY:
      if (array_view->buffer_views[2].size_bytes == -1) {
        src_view.data.as_int32 =
            array_view->buffer_views[1].data.as_int32 + offset_plus_length;
        src_view.size_bytes = sizeof(int32_t);
        dst_view.data.as_uint8 = *offset_value_dst;
        dst_view.size_bytes = sizeof(int32_t);

        NANOARROW_RETURN_NOT_OK(ArrowDeviceBufferCopyAsync(
            device, src_view, ArrowDeviceCpu(), dst_view, stream));

        (*offset_value_dst) += sizeof(int32_t);
      }
      break;
    case NANOARROW_TYPE_LARGE_STRING:
    case NANOARROW_TYPE_LARGE_BINARY:
      if (array_view->buffer_views[2].size_bytes == -1) {
        src_view.data.as_int64 =
            array_view->buffer_views[1].data.as_int64 + offset_plus_length;
        src_view.size_bytes = sizeof(int64_t);
        dst_view.data.as_uint8 = *offset_value_dst;
        dst_view.size_bytes = sizeof(int64_t);

        NANOARROW_RETURN_NOT_OK(ArrowDeviceBufferCopyAsync(
            device, src_view, ArrowDeviceCpu(), dst_view, stream));

        (*offset_value_dst) += sizeof(int64_t);
      }
      break;
    default:
      break;
  }

  // Recurse for children
  for (int64_t i = 0; i < array_view->n_children; i++) {
    NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewResolveUnknownBufferSizesAsync(
        device, array_view->children[i], offset_value_dst, stream));
  }

  // ...and for dictionary
  if (array_view->dictionary != NULL) {
    NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewResolveUnknownBufferSizesAsync(
        device, array_view->dictionary, offset_value_dst, stream));
  }

  return NANOARROW_OK;
}

// After synchronizing the stream with the CPU to ensure that all of the
// buffer sizes have been copied to the our temporary buffer, relay them
// back to the appropriate buffer view so that the buffer copier can
// do its thing.
static void ArrowDeviceArrayViewCollectUnknownBufferSizes(
    struct ArrowArrayView* array_view, uint8_t** offset_value_dst) {
  switch (array_view->storage_type) {
    case NANOARROW_TYPE_STRING:
    case NANOARROW_TYPE_BINARY:
      if (array_view->buffer_views[2].size_bytes == -1) {
        int32_t size_bytes_32;
        memcpy(&size_bytes_32, *offset_value_dst, sizeof(int32_t));
        array_view->buffer_views[2].size_bytes = size_bytes_32;
        (*offset_value_dst) += sizeof(int32_t);
      }
      break;
    case NANOARROW_TYPE_LARGE_STRING:
    case NANOARROW_TYPE_LARGE_BINARY:
      if (array_view->buffer_views[2].size_bytes == -1) {
        memcpy(&array_view->buffer_views[2].size_bytes, *offset_value_dst,
               sizeof(int64_t));
        (*offset_value_dst) += sizeof(int64_t);
      }
      break;
    default:
      break;
  }

  // Recurse for children
  for (int64_t i = 0; i < array_view->n_children; i++) {
    ArrowDeviceArrayViewCollectUnknownBufferSizes(array_view->children[i],
                                                  offset_value_dst);
  }

  // ...and for dictionary
  if (array_view->dictionary != NULL) {
    ArrowDeviceArrayViewCollectUnknownBufferSizes(array_view->dictionary,
                                                  offset_value_dst);
  }
}

static ArrowErrorCode ArrowDeviceArrayViewEnsureBufferSizesAsync(
    struct ArrowDeviceArrayView* device_array_view, void* stream,
    struct ArrowError* error) {
  // Walk the tree of arrays to check for buffers whose size we don't know
  int64_t temp_buffer_length_bytes_required = 0;
  NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewWalkUnknownBufferSizes(
      &device_array_view->array_view, &temp_buffer_length_bytes_required));

  // If there are no such arrays (e.g., there are no string or binary arrays in the tree),
  // we don't have to do anything extra
  if (temp_buffer_length_bytes_required == 0) {
    return NANOARROW_OK;
  }

  // Ensure that the stream provided waits on the array's sync event
  NANOARROW_RETURN_NOT_OK(device_array_view->device->synchronize_event(
      device_array_view->device, device_array_view->sync_event, stream, error));

  // Allocate a buffer big enough to hold all the offset values we need to
  // copy from the GPU
  struct ArrowBuffer buffer;
  ArrowBufferInit(&buffer);
  NANOARROW_RETURN_NOT_OK(
      ArrowBufferResize(&buffer, temp_buffer_length_bytes_required, 0));

  uint8_t* cursor = buffer.data;
  int result = ArrowDeviceArrayViewResolveUnknownBufferSizesAsync(
      device_array_view->device, &device_array_view->array_view, &cursor, stream);
  if (result != NANOARROW_OK) {
    ArrowBufferReset(&buffer);
    return result;
  }

  NANOARROW_DCHECK(cursor == (buffer.data + buffer.size_bytes));

  // Synchronize the stream with the CPU
  result = device_array_view->device->synchronize_event(device_array_view->device, NULL,
                                                        stream, error);

  // Collect the values from the temporary buffer
  cursor = buffer.data;
  ArrowDeviceArrayViewCollectUnknownBufferSizes(&device_array_view->array_view, &cursor);
  NANOARROW_DCHECK(cursor == (buffer.data + buffer.size_bytes));
  ArrowBufferReset(&buffer);

  return result;
}

ArrowErrorCode ArrowDeviceArrayViewSetArrayAsync(
    struct ArrowDeviceArrayView* device_array_view, struct ArrowDeviceArray* device_array,
    void* stream, struct ArrowError* error) {
  // Populate the array view with all information accessible from the CPU
  NANOARROW_RETURN_NOT_OK(
      ArrowDeviceArrayViewSetArrayMinimal(device_array_view, device_array, error));

  NANOARROW_RETURN_NOT_OK(
      ArrowDeviceArrayViewEnsureBufferSizesAsync(device_array_view, stream, error));

  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceArrayViewCopyInternal(struct ArrowDevice* device_src,
                                                       struct ArrowArrayView* src,
                                                       struct ArrowDevice* device_dst,
                                                       struct ArrowArray* dst,
                                                       void* stream) {
  // Currently no attempt to minimize the amount of memory copied (i.e.,
  // by applying offset + length and copying potentially fewer bytes)
  dst->length = src->length;
  dst->offset = src->offset;
  dst->null_count = src->null_count;

  for (int i = 0; i < NANOARROW_MAX_FIXED_BUFFERS; i++) {
    if (src->layout.buffer_type[i] == NANOARROW_BUFFER_TYPE_NONE) {
      break;
    }

    NANOARROW_RETURN_NOT_OK(ArrowDeviceBufferInitAsync(
        device_src, src->buffer_views[i], device_dst, ArrowArrayBuffer(dst, i), stream));
  }

  for (int64_t i = 0; i < src->n_children; i++) {
    NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewCopyInternal(
        device_src, src->children[i], device_dst, dst->children[i], stream));
  }

  if (src->dictionary != NULL) {
    NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewCopyInternal(
        device_src, src->dictionary, device_dst, dst->dictionary, stream));
  }

  return NANOARROW_OK;
}

ArrowErrorCode ArrowDeviceArrayViewCopyAsync(struct ArrowDeviceArrayView* src,
                                             struct ArrowDevice* device_dst,
                                             struct ArrowDeviceArray* dst, void* stream) {
  // Ensure src has all buffer sizes defined
  NANOARROW_RETURN_NOT_OK(ArrowDeviceArrayViewEnsureBufferSizesAsync(src, stream, NULL));

  struct ArrowArray tmp;
  NANOARROW_RETURN_NOT_OK(ArrowArrayInitFromArrayView(&tmp, &src->array_view, NULL));

  int result = ArrowDeviceArrayViewCopyInternal(src->device, &src->array_view, device_dst,
                                                &tmp, stream);
  if (result != NANOARROW_OK) {
    ArrowArrayRelease(&tmp);
    return result;
  }

  // If we are copying to the CPU, we need to synchronize the stream because we
  // can't populate a sync event for a CPU array.
  if (device_dst->device_type == ARROW_DEVICE_CPU) {
    result = src->device->synchronize_event(src->device, NULL, stream, NULL);
    if (result != NANOARROW_OK) {
      ArrowArrayRelease(&tmp);
      return result;
    }

    stream = NULL;
  }

  result = ArrowArrayFinishBuilding(&tmp, NANOARROW_VALIDATION_LEVEL_MINIMAL, NULL);
  if (result != NANOARROW_OK) {
    ArrowArrayRelease(&tmp);
    return result;
  }

  result = ArrowDeviceArrayInitAsync(device_dst, dst, &tmp, NULL, stream);
  if (result != NANOARROW_OK) {
    ArrowArrayRelease(&tmp);
    return result;
  }

  return result;
}

ArrowErrorCode ArrowDeviceArrayMoveToDevice(struct ArrowDeviceArray* src,
                                            struct ArrowDevice* device_dst,
                                            struct ArrowDeviceArray* dst) {
  // Can always move from the same device to the same device
  if (src->device_type == device_dst->device_type &&
      src->device_id == device_dst->device_id) {
    ArrowDeviceArrayMove(src, dst);
    return NANOARROW_OK;
  }

  struct ArrowDevice* device_src = ArrowDeviceResolve(src->device_type, src->device_id);
  if (device_src == NULL) {
    return EINVAL;
  }

  // See if the source knows how to move
  int result;
  if (device_src->array_move != NULL) {
    result = device_src->array_move(device_src, src, device_dst, dst);
    if (result != ENOTSUP) {
      return result;
    }
  }

  // See if the destination knows how to move
  if (device_dst->array_move != NULL) {
    NANOARROW_RETURN_NOT_OK(device_dst->array_move(device_src, src, device_dst, dst));
  }

  return NANOARROW_OK;
}

#if !defined(NANOARROW_DEVICE_WITH_CUDA)
struct ArrowDevice* ArrowDeviceCuda(ArrowDeviceType device_type, int64_t device_id) {
  NANOARROW_UNUSED(device_type);
  NANOARROW_UNUSED(device_id);

  return NULL;
}
#endif

#if !defined(NANOARROW_DEVICE_WITH_METAL)
struct ArrowDevice* ArrowDeviceMetalDefaultDevice(void) {
  return NULL;
}

ArrowErrorCode ArrowDeviceMetalInitDefaultDevice(struct ArrowDevice* device,
                                                 struct ArrowError* error) {
  NANOARROW_UNUSED(device);

  ArrowErrorSet(error, "nanoarrow_device not built with Metal support");
  return ENOTSUP;
}

ArrowErrorCode ArrowDeviceMetalInitBuffer(struct ArrowBuffer* buffer) {
  NANOARROW_UNUSED(buffer);
  return ENOTSUP;
}

ArrowErrorCode ArrowDeviceMetalAlignArrayBuffers(struct ArrowArray* array) {
  NANOARROW_UNUSED(array);
  return ENOTSUP;
}
#endif
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

#if defined(NANOARROW_DEVICE_WITH_CUDA)

#include <inttypes.h>

#include <cuda.h>

#include "nanoarrow_device.h"

static inline void ArrowDeviceCudaSetError(CUresult err, const char* op,
                                           struct ArrowError* error) {
  if (error == NULL) {
    return;
  }

  const char* name = NULL;
  CUresult err_result = cuGetErrorName(err, &name);
  if (err_result != CUDA_SUCCESS || name == NULL) {
    name = "name unknown";
  }

  const char* description = NULL;
  err_result = cuGetErrorString(err, &description);
  if (err_result != CUDA_SUCCESS || description == NULL) {
    description = "description unknown";
  }

  ArrowErrorSet(error, "[%s][%s] %s", op, name, description);
}

#define _NANOARROW_CUDA_RETURN_NOT_OK_IMPL(NAME, EXPR, OP, ERROR) \
  do {                                                            \
    CUresult NAME = (EXPR);                                       \
    if (NAME != CUDA_SUCCESS) {                                   \
      ArrowDeviceCudaSetError(NAME, OP, ERROR);                   \
      return EIO;                                                 \
    }                                                             \
  } while (0)

#define NANOARROW_CUDA_RETURN_NOT_OK(EXPR, OP, ERROR)                                    \
  _NANOARROW_CUDA_RETURN_NOT_OK_IMPL(_NANOARROW_MAKE_NAME(cuda_err_, __COUNTER__), EXPR, \
                                     OP, ERROR)

#if defined(NANOARROW_DEBUG)
#define _NANOARROW_CUDA_ASSERT_OK_IMPL(NAME, EXPR, EXPR_STR)           \
  do {                                                                 \
    const CUresult NAME = (EXPR);                                      \
    if (NAME != CUDA_SUCCESS) NANOARROW_PRINT_AND_DIE(NAME, EXPR_STR); \
  } while (0)
#define NANOARROW_CUDA_ASSERT_OK(EXPR)                                                   \
  _NANOARROW_CUDA_ASSERT_OK_IMPL(_NANOARROW_MAKE_NAME(errno_status_, __COUNTER__), EXPR, \
                                 #EXPR)
#else
#define NANOARROW_CUDA_ASSERT_OK(EXPR) (void)(EXPR)
#endif

struct ArrowDeviceCudaPrivate {
  CUdevice cu_device;
  CUcontext cu_context;
};

struct ArrowDeviceCudaAllocatorPrivate {
  ArrowDeviceType device_type;
  int64_t device_id;
  // When moving a buffer from CUDA_HOST to CUDA, the pointer used to access
  // the data changes but the pointer needed to pass to cudaFreeHost does not
  void* allocated_ptr;
};

static void ArrowDeviceCudaDeallocator(struct ArrowBufferAllocator* allocator,
                                       uint8_t* ptr, int64_t old_size) {
  NANOARROW_UNUSED(ptr);
  NANOARROW_UNUSED(old_size);

  struct ArrowDeviceCudaAllocatorPrivate* allocator_private =
      (struct ArrowDeviceCudaAllocatorPrivate*)allocator->private_data;

  switch (allocator_private->device_type) {
    case ARROW_DEVICE_CUDA:
      cuMemFree((CUdeviceptr)allocator_private->allocated_ptr);
      break;
    case ARROW_DEVICE_CUDA_HOST:
      NANOARROW_CUDA_ASSERT_OK(cuMemFreeHost(allocator_private->allocated_ptr));
      break;
    default:
      break;
  }

  ArrowFree(allocator_private);
}

static ArrowErrorCode ArrowDeviceCudaAllocateBufferAsync(struct ArrowDevice* device,
                                                         struct ArrowBuffer* buffer,
                                                         int64_t size_bytes,
                                                         CUstream hstream) {
  struct ArrowDeviceCudaPrivate* private_data =
      (struct ArrowDeviceCudaPrivate*)device->private_data;

  NANOARROW_CUDA_RETURN_NOT_OK(cuCtxPushCurrent(private_data->cu_context),
                               "cuCtxPushCurrent", NULL);
  CUcontext unused;  // needed for cuCtxPopCurrent()

  struct ArrowDeviceCudaAllocatorPrivate* allocator_private =
      (struct ArrowDeviceCudaAllocatorPrivate*)ArrowMalloc(
          sizeof(struct ArrowDeviceCudaAllocatorPrivate));
  if (allocator_private == NULL) {
    NANOARROW_CUDA_ASSERT_OK(cuCtxPopCurrent(&unused));
    return ENOMEM;
  }

  CUresult err;
  void* ptr = NULL;
  const char* op = "";
  switch (device->device_type) {
    case ARROW_DEVICE_CUDA: {
      CUdeviceptr dptr = 0;

      // cuMemalloc requires non-zero size_bytes
      if (size_bytes > 0) {
        err = cuMemAllocAsync(&dptr, (size_t)size_bytes, hstream);
      } else {
        err = CUDA_SUCCESS;
      }

      ptr = (void*)dptr;
      op = "cuMemAlloc";
      break;
    }
    case ARROW_DEVICE_CUDA_HOST:
      err = cuMemAllocHost(&ptr, (size_t)size_bytes);
      op = "cuMemAllocHost";
      break;
    default:
      cuCtxPopCurrent(&unused);
      ArrowFree(allocator_private);
      return EINVAL;
  }

  if (err != CUDA_SUCCESS) {
    NANOARROW_CUDA_ASSERT_OK(cuCtxPopCurrent(&unused));
    ArrowFree(allocator_private);
    NANOARROW_CUDA_RETURN_NOT_OK(err, op, NULL);
  }

  allocator_private->device_id = device->device_id;
  allocator_private->device_type = device->device_type;
  allocator_private->allocated_ptr = ptr;

  buffer->data = (uint8_t*)ptr;
  buffer->size_bytes = size_bytes;
  buffer->capacity_bytes = size_bytes;
  buffer->allocator =
      ArrowBufferDeallocator(&ArrowDeviceCudaDeallocator, allocator_private);

  NANOARROW_CUDA_ASSERT_OK(cuCtxPopCurrent(&unused));
  return NANOARROW_OK;
}

struct ArrowDeviceCudaArrayPrivate {
  struct ArrowArray parent;
  CUevent cu_event;
};

static void ArrowDeviceCudaArrayRelease(struct ArrowArray* array) {
  struct ArrowDeviceCudaArrayPrivate* private_data =
      (struct ArrowDeviceCudaArrayPrivate*)array->private_data;

  if (private_data->cu_event != NULL) {
    NANOARROW_CUDA_ASSERT_OK(cuEventDestroy(private_data->cu_event));
  }

  ArrowArrayRelease(&private_data->parent);
  ArrowFree(private_data);
  array->release = NULL;
}

static ArrowErrorCode ArrowDeviceCudaArrayInitInternal(
    struct ArrowDevice* device, struct ArrowDeviceArray* device_array,
    struct ArrowArray* array, CUevent cu_event) {
  struct ArrowDeviceCudaArrayPrivate* array_private =
      (struct ArrowDeviceCudaArrayPrivate*)ArrowMalloc(
          sizeof(struct ArrowDeviceCudaArrayPrivate));
  if (array_private == NULL) {
    return ENOMEM;
  }

  memset(device_array, 0, sizeof(struct ArrowDeviceArray));
  device_array->array = *array;
  device_array->array.private_data = array_private;
  device_array->array.release = &ArrowDeviceCudaArrayRelease;
  ArrowArrayMove(array, &array_private->parent);

  device_array->device_id = device->device_id;
  device_array->device_type = device->device_type;

  if (cu_event != NULL) {
    array_private->cu_event = cu_event;
    device_array->sync_event = &array_private->cu_event;
  } else {
    array_private->cu_event = NULL;
    device_array->sync_event = NULL;
  }

  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCudaArrayInitAsync(struct ArrowDevice* device,
                                                    struct ArrowDeviceArray* device_array,
                                                    struct ArrowArray* array,
                                                    void* sync_event, void* stream) {
  struct ArrowDeviceCudaPrivate* private_data =
      (struct ArrowDeviceCudaPrivate*)device->private_data;

  NANOARROW_CUDA_RETURN_NOT_OK(cuCtxPushCurrent(private_data->cu_context),
                               "cuCtxPushCurrent", NULL);
  CUcontext unused;  // needed for cuCtxPopCurrent()

  CUevent cu_event;
  if (sync_event == NULL) {
    cu_event = NULL;
  } else {
    cu_event = *((CUevent*)sync_event);
  }

  // If the stream was passed, it means that we are required to ensure that
  // the event that is exported by the output array captures the work that
  // has been done on stream. If we were not given an event to take ownership of,
  // this means we need to create one.
  CUevent cu_event_tmp = NULL;
  CUresult err;

  if (stream != NULL && cu_event == NULL) {
    // Event is faster with timing disabled (a user can provide their
    // own event if they want timing enabled)
    err = cuEventCreate(&cu_event_tmp, CU_EVENT_DISABLE_TIMING);
    if (err != CUDA_SUCCESS) {
      NANOARROW_CUDA_ASSERT_OK(cuCtxPopCurrent(&unused));
      NANOARROW_CUDA_RETURN_NOT_OK(err, "cuEventCreate", NULL);
    }

    cu_event = cu_event_tmp;
  }

  if (stream != NULL) {
    err = cuEventRecord(cu_event, *((CUstream*)stream));
    if (err != CUDA_SUCCESS) {
      NANOARROW_CUDA_ASSERT_OK(cuCtxPopCurrent(&unused));
      if (cu_event_tmp != NULL) {
        NANOARROW_CUDA_ASSERT_OK(cuEventDestroy(cu_event_tmp));
      }

      NANOARROW_CUDA_RETURN_NOT_OK(err, "cuEventCreate", NULL);
    }
  }

  int result = ArrowDeviceCudaArrayInitInternal(device, device_array, array, cu_event);
  NANOARROW_CUDA_ASSERT_OK(cuCtxPopCurrent(&unused));
  if (result != NANOARROW_OK) {
    if (cu_event_tmp != NULL) {
      NANOARROW_CUDA_ASSERT_OK(cuEventDestroy(cu_event_tmp));
    }

    return result;
  }

  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCudaBufferCopyAsyncInternal(
    struct ArrowDevice* device_src, struct ArrowBufferView src,
    struct ArrowDevice* device_dst, struct ArrowBufferView dst, int* n_pop_context,
    struct ArrowError* error, CUstream hstream) {
  // Note: the device_src/sync event must be synchronized before calling these methods,
  // even though the cuMemcpyXXX() functions may do this automatically in some cases.

  if (device_src->device_type == ARROW_DEVICE_CPU &&
      device_dst->device_type == ARROW_DEVICE_CUDA) {
    struct ArrowDeviceCudaPrivate* dst_private =
        (struct ArrowDeviceCudaPrivate*)device_dst->private_data;
    NANOARROW_CUDA_RETURN_NOT_OK(cuCtxPushCurrent(dst_private->cu_context),
                                 "cuCtxPushCurrent", error);
    (*n_pop_context)++;

    NANOARROW_CUDA_RETURN_NOT_OK(
        cuMemcpyHtoDAsync((CUdeviceptr)dst.data.data, src.data.data,
                          (size_t)src.size_bytes, hstream),
        "cuMemcpyHtoD", error);

  } else if (device_src->device_type == ARROW_DEVICE_CUDA &&
             device_dst->device_type == ARROW_DEVICE_CUDA &&
             device_src->device_id == device_dst->device_id) {
    struct ArrowDeviceCudaPrivate* dst_private =
        (struct ArrowDeviceCudaPrivate*)device_dst->private_data;

    NANOARROW_CUDA_RETURN_NOT_OK(cuCtxPushCurrent(dst_private->cu_context),
                                 "cuCtxPushCurrent", error);
    (*n_pop_context)++;

    NANOARROW_CUDA_RETURN_NOT_OK(
        cuMemcpyDtoDAsync((CUdeviceptr)dst.data.data, (CUdeviceptr)src.data.data,
                          (size_t)src.size_bytes, hstream),
        "cuMemcpyDtoDAsync", error);

  } else if (device_src->device_type == ARROW_DEVICE_CUDA &&
             device_dst->device_type == ARROW_DEVICE_CUDA) {
    struct ArrowDeviceCudaPrivate* src_private =
        (struct ArrowDeviceCudaPrivate*)device_src->private_data;
    struct ArrowDeviceCudaPrivate* dst_private =
        (struct ArrowDeviceCudaPrivate*)device_dst->private_data;

    NANOARROW_CUDA_RETURN_NOT_OK(
        cuMemcpyPeerAsync((CUdeviceptr)dst.data.data, dst_private->cu_context,
                          (CUdeviceptr)src.data.data, src_private->cu_context,
                          (size_t)src.size_bytes, hstream),
        "cuMemcpyPeerAsync", error);

  } else if (device_src->device_type == ARROW_DEVICE_CUDA &&
             device_dst->device_type == ARROW_DEVICE_CPU) {
    struct ArrowDeviceCudaPrivate* src_private =
        (struct ArrowDeviceCudaPrivate*)device_src->private_data;

    NANOARROW_CUDA_RETURN_NOT_OK(cuCtxPushCurrent(src_private->cu_context),
                                 "cuCtxPushCurrent", error);
    (*n_pop_context)++;
    NANOARROW_CUDA_RETURN_NOT_OK(
        cuMemcpyDtoHAsync((void*)dst.data.data, (CUdeviceptr)src.data.data,
                          (size_t)src.size_bytes, hstream),
        "cuMemcpyDtoHAsync", error);

  } else if (device_src->device_type == ARROW_DEVICE_CPU &&
             device_dst->device_type == ARROW_DEVICE_CUDA_HOST) {
    memcpy((void*)dst.data.data, src.data.data, (size_t)src.size_bytes);

  } else if (device_src->device_type == ARROW_DEVICE_CUDA_HOST &&
             device_dst->device_type == ARROW_DEVICE_CUDA_HOST) {
    memcpy((void*)dst.data.data, src.data.data, (size_t)src.size_bytes);

  } else if (device_src->device_type == ARROW_DEVICE_CUDA_HOST &&
             device_dst->device_type == ARROW_DEVICE_CPU) {
    memcpy((void*)dst.data.data, src.data.data, (size_t)src.size_bytes);

  } else {
    return ENOTSUP;
  }

  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCudaBufferCopyAsync(struct ArrowDevice* device_src,
                                                     struct ArrowBufferView src,
                                                     struct ArrowDevice* device_dst,
                                                     struct ArrowBufferView dst,
                                                     void* stream) {
  if (stream == NULL) {
    return EINVAL;
  }

  CUstream hstream = *((CUstream*)stream);

  int n_pop_context = 0;
  struct ArrowError error;

  int result = ArrowDeviceCudaBufferCopyAsyncInternal(device_src, src, device_dst, dst,
                                                      &n_pop_context, &error, hstream);
  for (int i = 0; i < n_pop_context; i++) {
    CUcontext unused;
    NANOARROW_CUDA_ASSERT_OK(cuCtxPopCurrent(&unused));
  }

  return result;
}

static ArrowErrorCode ArrowDeviceCudaBufferInitAsync(struct ArrowDevice* device_src,
                                                     struct ArrowBufferView src,
                                                     struct ArrowDevice* device_dst,
                                                     struct ArrowBuffer* dst,
                                                     void* stream) {
  if (stream == NULL) {
    return EINVAL;
  }

  CUstream hstream = *((CUstream*)stream);

  struct ArrowBuffer tmp;

  switch (device_dst->device_type) {
    case ARROW_DEVICE_CUDA:
    case ARROW_DEVICE_CUDA_HOST:
      NANOARROW_RETURN_NOT_OK(
          ArrowDeviceCudaAllocateBufferAsync(device_dst, &tmp, src.size_bytes, hstream));
      break;
    case ARROW_DEVICE_CPU:
      ArrowBufferInit(&tmp);
      NANOARROW_RETURN_NOT_OK(ArrowBufferResize(&tmp, src.size_bytes, 0));
      break;
    default:
      return ENOTSUP;
  }

  struct ArrowBufferView tmp_view;
  tmp_view.data.data = tmp.data;
  tmp_view.size_bytes = tmp.size_bytes;
  int result =
      ArrowDeviceCudaBufferCopyAsync(device_src, src, device_dst, tmp_view, &hstream);
  if (result != NANOARROW_OK) {
    ArrowBufferReset(&tmp);
    return result;
  }

  ArrowBufferMove(&tmp, dst);
  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCudaSynchronize(struct ArrowDevice* device,
                                                 void* sync_event, void* stream,
                                                 struct ArrowError* error) {
  if (sync_event == NULL) {
    return NANOARROW_OK;
  }

  if (device->device_type != ARROW_DEVICE_CUDA &&
      device->device_type != ARROW_DEVICE_CUDA_HOST) {
    return ENOTSUP;
  }

  // Sync functions require a context to be set
  struct ArrowDeviceCudaPrivate* private_data =
      (struct ArrowDeviceCudaPrivate*)device->private_data;

  NANOARROW_CUDA_RETURN_NOT_OK(cuCtxPushCurrent(private_data->cu_context),
                               "cuCtxPushCurrent", NULL);
  CUcontext unused;  // needed for cuCtxPopCurrent()

  // Memory for cuda_event is owned by the ArrowArray member of the ArrowDeviceArray
  CUevent* cu_event = (CUevent*)sync_event;
  CUstream* cu_stream = (CUstream*)stream;
  CUresult err = CUDA_SUCCESS;
  const char* op = "";

  if (cu_stream == NULL && cu_event != NULL) {
    err = cuEventSynchronize(*cu_event);
    op = "cuEventSynchronize";
  } else if (cu_stream != NULL && cu_event == NULL) {
    err = cuStreamSynchronize(*cu_stream);
    op = "cuStreamSynchronize";
  } else if (cu_stream != NULL && cu_event != NULL) {
    err = cuStreamWaitEvent(*cu_stream, *cu_event, CU_EVENT_WAIT_DEFAULT);
    op = "cuStreamWaitEvent";
  }

  NANOARROW_ASSERT_OK(cuCtxPopCurrent(&unused));
  NANOARROW_CUDA_RETURN_NOT_OK(err, op, error);
  return NANOARROW_OK;
}

static ArrowErrorCode ArrowDeviceCudaArrayMove(struct ArrowDevice* device_src,
                                               struct ArrowDeviceArray* src,
                                               struct ArrowDevice* device_dst,
                                               struct ArrowDeviceArray* dst) {
  // Note that the case where the devices are the same is handled before this

  if (device_src->device_type == ARROW_DEVICE_CUDA_HOST &&
      device_dst->device_type == ARROW_DEVICE_CPU) {
    // Move: the array's release callback is responsible for cudaFreeHost or
    // deregistration (or perhaps this has been handled at a higher level).
    // We do have to wait on the sync event, though, because this has to be NULL
    // for a CPU device array.
    NANOARROW_RETURN_NOT_OK(
        ArrowDeviceCudaSynchronize(device_src, src->sync_event, NULL, NULL));
    ArrowDeviceArrayMove(src, dst);
    dst->device_type = device_dst->device_type;
    dst->device_id = device_dst->device_id;
    dst->sync_event = NULL;

    return NANOARROW_OK;
  }

  // TODO: We can theoretically also do a move from CUDA_HOST to CUDA

  return ENOTSUP;
}

static void ArrowDeviceCudaRelease(struct ArrowDevice* device) {
  struct ArrowDeviceCudaPrivate* private_data =
      (struct ArrowDeviceCudaPrivate*)device->private_data;
  NANOARROW_CUDA_ASSERT_OK(cuDevicePrimaryCtxRelease(private_data->cu_device));
  ArrowFree(device->private_data);
  device->release = NULL;
}

static ArrowErrorCode ArrowDeviceCudaInitDevice(struct ArrowDevice* device,
                                                ArrowDeviceType device_type,
                                                int64_t device_id,
                                                struct ArrowError* error) {
  switch (device_type) {
    case ARROW_DEVICE_CUDA:
    case ARROW_DEVICE_CUDA_HOST:
      break;
    default:
      ArrowErrorSet(error, "Device type code %" PRId32 " not supported", device_type);
      return EINVAL;
  }

  CUdevice cu_device;
  NANOARROW_CUDA_RETURN_NOT_OK(cuDeviceGet(&cu_device, (int)device_id), "cuDeviceGet",
                               error);

  CUcontext cu_context;
  NANOARROW_CUDA_RETURN_NOT_OK(cuDevicePrimaryCtxRetain(&cu_context, cu_device),
                               "cuDevicePrimaryCtxRetain", error);

  struct ArrowDeviceCudaPrivate* private_data =
      (struct ArrowDeviceCudaPrivate*)ArrowMalloc(sizeof(struct ArrowDeviceCudaPrivate));
  if (private_data == NULL) {
    NANOARROW_CUDA_ASSERT_OK(cuDevicePrimaryCtxRelease(cu_device));
    ArrowErrorSet(error, "out of memory");
    return ENOMEM;
  }

  device->device_type = device_type;
  device->device_id = device_id;
  device->array_init = &ArrowDeviceCudaArrayInitAsync;
  device->array_move = &ArrowDeviceCudaArrayMove;
  device->buffer_init = &ArrowDeviceCudaBufferInitAsync;
  device->buffer_move = NULL;
  device->buffer_copy = &ArrowDeviceCudaBufferCopyAsync;
  device->synchronize_event = &ArrowDeviceCudaSynchronize;
  device->release = &ArrowDeviceCudaRelease;

  private_data->cu_device = cu_device;
  private_data->cu_context = cu_context;
  device->private_data = private_data;

  return NANOARROW_OK;
}

struct ArrowDevice* ArrowDeviceCuda(ArrowDeviceType device_type, int64_t device_id) {
  CUresult err;
  int n_devices;

  static struct ArrowDevice* devices_singleton = NULL;
  if (devices_singleton == NULL) {
    err = cuInit(0);
    if (err != CUDA_SUCCESS) {
      return NULL;
    }

    err = cuDeviceGetCount(&n_devices);
    if (err != CUDA_SUCCESS) {
      return NULL;
    }

    if (n_devices == 0) {
      return NULL;
    }

    devices_singleton =
        (struct ArrowDevice*)ArrowMalloc(2 * n_devices * sizeof(struct ArrowDevice));
    if (devices_singleton == NULL) {
      return NULL;
    }

    int result = NANOARROW_OK;
    memset(devices_singleton, 0, 2 * n_devices * sizeof(struct ArrowDevice));

    for (int i = 0; i < n_devices; i++) {
      result =
          ArrowDeviceCudaInitDevice(devices_singleton + i, ARROW_DEVICE_CUDA, i, NULL);
      if (result != NANOARROW_OK) {
        break;
      }

      result = ArrowDeviceCudaInitDevice(devices_singleton + n_devices + i,
                                         ARROW_DEVICE_CUDA_HOST, i, NULL);
      if (result != NANOARROW_OK) {
        break;
      }
    }

    if (result != NANOARROW_OK) {
      for (int i = 0; i < n_devices; i++) {
        if (devices_singleton[i].release != NULL) {
          devices_singleton[i].release(&(devices_singleton[i]));
        }
      }

      ArrowFree(devices_singleton);
      devices_singleton = NULL;
      return NULL;
    }

  } else {
    err = cuDeviceGetCount(&n_devices);
    if (err != CUDA_SUCCESS) {
      return NULL;
    }
  }

  if (device_id < 0 || device_id >= n_devices) {
    return NULL;
  }

  switch (device_type) {
    case ARROW_DEVICE_CUDA:
      return devices_singleton + device_id;
    case ARROW_DEVICE_CUDA_HOST:
      return devices_singleton + n_devices + device_id;
    default:
      return NULL;
  }
}

#endif
