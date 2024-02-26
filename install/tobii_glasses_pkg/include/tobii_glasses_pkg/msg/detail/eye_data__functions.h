// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from tobii_glasses_pkg:msg/EyeData.idl
// generated code does not contain a copyright notice

#ifndef TOBII_GLASSES_PKG__MSG__DETAIL__EYE_DATA__FUNCTIONS_H_
#define TOBII_GLASSES_PKG__MSG__DETAIL__EYE_DATA__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "tobii_glasses_pkg/msg/rosidl_generator_c__visibility_control.h"

#include "tobii_glasses_pkg/msg/detail/eye_data__struct.h"

/// Initialize msg/EyeData message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * tobii_glasses_pkg__msg__EyeData
 * )) before or use
 * tobii_glasses_pkg__msg__EyeData__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__EyeData__init(tobii_glasses_pkg__msg__EyeData * msg);

/// Finalize msg/EyeData message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__EyeData__fini(tobii_glasses_pkg__msg__EyeData * msg);

/// Create msg/EyeData message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * tobii_glasses_pkg__msg__EyeData__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
tobii_glasses_pkg__msg__EyeData *
tobii_glasses_pkg__msg__EyeData__create();

/// Destroy msg/EyeData message.
/**
 * It calls
 * tobii_glasses_pkg__msg__EyeData__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__EyeData__destroy(tobii_glasses_pkg__msg__EyeData * msg);

/// Check for msg/EyeData message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__EyeData__are_equal(const tobii_glasses_pkg__msg__EyeData * lhs, const tobii_glasses_pkg__msg__EyeData * rhs);

/// Copy a msg/EyeData message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__EyeData__copy(
  const tobii_glasses_pkg__msg__EyeData * input,
  tobii_glasses_pkg__msg__EyeData * output);

/// Initialize array of msg/EyeData messages.
/**
 * It allocates the memory for the number of elements and calls
 * tobii_glasses_pkg__msg__EyeData__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__EyeData__Sequence__init(tobii_glasses_pkg__msg__EyeData__Sequence * array, size_t size);

/// Finalize array of msg/EyeData messages.
/**
 * It calls
 * tobii_glasses_pkg__msg__EyeData__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__EyeData__Sequence__fini(tobii_glasses_pkg__msg__EyeData__Sequence * array);

/// Create array of msg/EyeData messages.
/**
 * It allocates the memory for the array and calls
 * tobii_glasses_pkg__msg__EyeData__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
tobii_glasses_pkg__msg__EyeData__Sequence *
tobii_glasses_pkg__msg__EyeData__Sequence__create(size_t size);

/// Destroy array of msg/EyeData messages.
/**
 * It calls
 * tobii_glasses_pkg__msg__EyeData__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__EyeData__Sequence__destroy(tobii_glasses_pkg__msg__EyeData__Sequence * array);

/// Check for msg/EyeData message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__EyeData__Sequence__are_equal(const tobii_glasses_pkg__msg__EyeData__Sequence * lhs, const tobii_glasses_pkg__msg__EyeData__Sequence * rhs);

/// Copy an array of msg/EyeData messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__EyeData__Sequence__copy(
  const tobii_glasses_pkg__msg__EyeData__Sequence * input,
  tobii_glasses_pkg__msg__EyeData__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // TOBII_GLASSES_PKG__MSG__DETAIL__EYE_DATA__FUNCTIONS_H_
