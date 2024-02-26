// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from tobii_glasses_pkg:msg/EyeData.idl
// generated code does not contain a copyright notice
#include "tobii_glasses_pkg/msg/detail/eye_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `name`
#include "rosidl_runtime_c/string_functions.h"

bool
tobii_glasses_pkg__msg__EyeData__init(tobii_glasses_pkg__msg__EyeData * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    tobii_glasses_pkg__msg__EyeData__fini(msg);
    return false;
  }
  // pupil_center
  // pupil_diameter
  // gaze_direction
  return true;
}

void
tobii_glasses_pkg__msg__EyeData__fini(tobii_glasses_pkg__msg__EyeData * msg)
{
  if (!msg) {
    return;
  }
  // status
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // pupil_center
  // pupil_diameter
  // gaze_direction
}

bool
tobii_glasses_pkg__msg__EyeData__are_equal(const tobii_glasses_pkg__msg__EyeData * lhs, const tobii_glasses_pkg__msg__EyeData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // pupil_center
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->pupil_center[i] != rhs->pupil_center[i]) {
      return false;
    }
  }
  // pupil_diameter
  if (lhs->pupil_diameter != rhs->pupil_diameter) {
    return false;
  }
  // gaze_direction
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->gaze_direction[i] != rhs->gaze_direction[i]) {
      return false;
    }
  }
  return true;
}

bool
tobii_glasses_pkg__msg__EyeData__copy(
  const tobii_glasses_pkg__msg__EyeData * input,
  tobii_glasses_pkg__msg__EyeData * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // pupil_center
  for (size_t i = 0; i < 3; ++i) {
    output->pupil_center[i] = input->pupil_center[i];
  }
  // pupil_diameter
  output->pupil_diameter = input->pupil_diameter;
  // gaze_direction
  for (size_t i = 0; i < 3; ++i) {
    output->gaze_direction[i] = input->gaze_direction[i];
  }
  return true;
}

tobii_glasses_pkg__msg__EyeData *
tobii_glasses_pkg__msg__EyeData__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tobii_glasses_pkg__msg__EyeData * msg = (tobii_glasses_pkg__msg__EyeData *)allocator.allocate(sizeof(tobii_glasses_pkg__msg__EyeData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(tobii_glasses_pkg__msg__EyeData));
  bool success = tobii_glasses_pkg__msg__EyeData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
tobii_glasses_pkg__msg__EyeData__destroy(tobii_glasses_pkg__msg__EyeData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    tobii_glasses_pkg__msg__EyeData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
tobii_glasses_pkg__msg__EyeData__Sequence__init(tobii_glasses_pkg__msg__EyeData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tobii_glasses_pkg__msg__EyeData * data = NULL;

  if (size) {
    data = (tobii_glasses_pkg__msg__EyeData *)allocator.zero_allocate(size, sizeof(tobii_glasses_pkg__msg__EyeData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = tobii_glasses_pkg__msg__EyeData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        tobii_glasses_pkg__msg__EyeData__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
tobii_glasses_pkg__msg__EyeData__Sequence__fini(tobii_glasses_pkg__msg__EyeData__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      tobii_glasses_pkg__msg__EyeData__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

tobii_glasses_pkg__msg__EyeData__Sequence *
tobii_glasses_pkg__msg__EyeData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tobii_glasses_pkg__msg__EyeData__Sequence * array = (tobii_glasses_pkg__msg__EyeData__Sequence *)allocator.allocate(sizeof(tobii_glasses_pkg__msg__EyeData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = tobii_glasses_pkg__msg__EyeData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
tobii_glasses_pkg__msg__EyeData__Sequence__destroy(tobii_glasses_pkg__msg__EyeData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    tobii_glasses_pkg__msg__EyeData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
tobii_glasses_pkg__msg__EyeData__Sequence__are_equal(const tobii_glasses_pkg__msg__EyeData__Sequence * lhs, const tobii_glasses_pkg__msg__EyeData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!tobii_glasses_pkg__msg__EyeData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
tobii_glasses_pkg__msg__EyeData__Sequence__copy(
  const tobii_glasses_pkg__msg__EyeData__Sequence * input,
  tobii_glasses_pkg__msg__EyeData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(tobii_glasses_pkg__msg__EyeData);
    tobii_glasses_pkg__msg__EyeData * data =
      (tobii_glasses_pkg__msg__EyeData *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!tobii_glasses_pkg__msg__EyeData__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          tobii_glasses_pkg__msg__EyeData__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!tobii_glasses_pkg__msg__EyeData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
