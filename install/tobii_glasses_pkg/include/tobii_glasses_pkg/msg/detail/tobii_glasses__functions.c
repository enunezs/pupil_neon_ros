// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from tobii_glasses_pkg:msg/TobiiGlasses.idl
// generated code does not contain a copyright notice
#include "tobii_glasses_pkg/msg/detail/tobii_glasses__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `camera_image`
#include "sensor_msgs/msg/detail/image__functions.h"
// Member `right_eye`
// Member `left_eye`
#include "tobii_glasses_pkg/msg/detail/eye_data__functions.h"

bool
tobii_glasses_pkg__msg__TobiiGlasses__init(tobii_glasses_pkg__msg__TobiiGlasses * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    tobii_glasses_pkg__msg__TobiiGlasses__fini(msg);
    return false;
  }
  // camera_image
  if (!sensor_msgs__msg__Image__init(&msg->camera_image)) {
    tobii_glasses_pkg__msg__TobiiGlasses__fini(msg);
    return false;
  }
  // gaze_position
  // gaze_position_3d
  // right_eye
  if (!tobii_glasses_pkg__msg__EyeData__init(&msg->right_eye)) {
    tobii_glasses_pkg__msg__TobiiGlasses__fini(msg);
    return false;
  }
  // left_eye
  if (!tobii_glasses_pkg__msg__EyeData__init(&msg->left_eye)) {
    tobii_glasses_pkg__msg__TobiiGlasses__fini(msg);
    return false;
  }
  // acelerometer
  // gyroscope
  return true;
}

void
tobii_glasses_pkg__msg__TobiiGlasses__fini(tobii_glasses_pkg__msg__TobiiGlasses * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // camera_image
  sensor_msgs__msg__Image__fini(&msg->camera_image);
  // gaze_position
  // gaze_position_3d
  // right_eye
  tobii_glasses_pkg__msg__EyeData__fini(&msg->right_eye);
  // left_eye
  tobii_glasses_pkg__msg__EyeData__fini(&msg->left_eye);
  // acelerometer
  // gyroscope
}

bool
tobii_glasses_pkg__msg__TobiiGlasses__are_equal(const tobii_glasses_pkg__msg__TobiiGlasses * lhs, const tobii_glasses_pkg__msg__TobiiGlasses * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // camera_image
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->camera_image), &(rhs->camera_image)))
  {
    return false;
  }
  // gaze_position
  for (size_t i = 0; i < 2; ++i) {
    if (lhs->gaze_position[i] != rhs->gaze_position[i]) {
      return false;
    }
  }
  // gaze_position_3d
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->gaze_position_3d[i] != rhs->gaze_position_3d[i]) {
      return false;
    }
  }
  // right_eye
  if (!tobii_glasses_pkg__msg__EyeData__are_equal(
      &(lhs->right_eye), &(rhs->right_eye)))
  {
    return false;
  }
  // left_eye
  if (!tobii_glasses_pkg__msg__EyeData__are_equal(
      &(lhs->left_eye), &(rhs->left_eye)))
  {
    return false;
  }
  // acelerometer
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->acelerometer[i] != rhs->acelerometer[i]) {
      return false;
    }
  }
  // gyroscope
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->gyroscope[i] != rhs->gyroscope[i]) {
      return false;
    }
  }
  return true;
}

bool
tobii_glasses_pkg__msg__TobiiGlasses__copy(
  const tobii_glasses_pkg__msg__TobiiGlasses * input,
  tobii_glasses_pkg__msg__TobiiGlasses * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // camera_image
  if (!sensor_msgs__msg__Image__copy(
      &(input->camera_image), &(output->camera_image)))
  {
    return false;
  }
  // gaze_position
  for (size_t i = 0; i < 2; ++i) {
    output->gaze_position[i] = input->gaze_position[i];
  }
  // gaze_position_3d
  for (size_t i = 0; i < 3; ++i) {
    output->gaze_position_3d[i] = input->gaze_position_3d[i];
  }
  // right_eye
  if (!tobii_glasses_pkg__msg__EyeData__copy(
      &(input->right_eye), &(output->right_eye)))
  {
    return false;
  }
  // left_eye
  if (!tobii_glasses_pkg__msg__EyeData__copy(
      &(input->left_eye), &(output->left_eye)))
  {
    return false;
  }
  // acelerometer
  for (size_t i = 0; i < 3; ++i) {
    output->acelerometer[i] = input->acelerometer[i];
  }
  // gyroscope
  for (size_t i = 0; i < 3; ++i) {
    output->gyroscope[i] = input->gyroscope[i];
  }
  return true;
}

tobii_glasses_pkg__msg__TobiiGlasses *
tobii_glasses_pkg__msg__TobiiGlasses__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tobii_glasses_pkg__msg__TobiiGlasses * msg = (tobii_glasses_pkg__msg__TobiiGlasses *)allocator.allocate(sizeof(tobii_glasses_pkg__msg__TobiiGlasses), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(tobii_glasses_pkg__msg__TobiiGlasses));
  bool success = tobii_glasses_pkg__msg__TobiiGlasses__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
tobii_glasses_pkg__msg__TobiiGlasses__destroy(tobii_glasses_pkg__msg__TobiiGlasses * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    tobii_glasses_pkg__msg__TobiiGlasses__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__init(tobii_glasses_pkg__msg__TobiiGlasses__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tobii_glasses_pkg__msg__TobiiGlasses * data = NULL;

  if (size) {
    data = (tobii_glasses_pkg__msg__TobiiGlasses *)allocator.zero_allocate(size, sizeof(tobii_glasses_pkg__msg__TobiiGlasses), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = tobii_glasses_pkg__msg__TobiiGlasses__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        tobii_glasses_pkg__msg__TobiiGlasses__fini(&data[i - 1]);
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
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__fini(tobii_glasses_pkg__msg__TobiiGlasses__Sequence * array)
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
      tobii_glasses_pkg__msg__TobiiGlasses__fini(&array->data[i]);
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

tobii_glasses_pkg__msg__TobiiGlasses__Sequence *
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  tobii_glasses_pkg__msg__TobiiGlasses__Sequence * array = (tobii_glasses_pkg__msg__TobiiGlasses__Sequence *)allocator.allocate(sizeof(tobii_glasses_pkg__msg__TobiiGlasses__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = tobii_glasses_pkg__msg__TobiiGlasses__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__destroy(tobii_glasses_pkg__msg__TobiiGlasses__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    tobii_glasses_pkg__msg__TobiiGlasses__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__are_equal(const tobii_glasses_pkg__msg__TobiiGlasses__Sequence * lhs, const tobii_glasses_pkg__msg__TobiiGlasses__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!tobii_glasses_pkg__msg__TobiiGlasses__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__copy(
  const tobii_glasses_pkg__msg__TobiiGlasses__Sequence * input,
  tobii_glasses_pkg__msg__TobiiGlasses__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(tobii_glasses_pkg__msg__TobiiGlasses);
    tobii_glasses_pkg__msg__TobiiGlasses * data =
      (tobii_glasses_pkg__msg__TobiiGlasses *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!tobii_glasses_pkg__msg__TobiiGlasses__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          tobii_glasses_pkg__msg__TobiiGlasses__fini(&data[i]);
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
    if (!tobii_glasses_pkg__msg__TobiiGlasses__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
