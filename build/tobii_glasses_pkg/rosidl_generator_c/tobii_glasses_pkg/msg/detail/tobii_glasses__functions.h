// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from tobii_glasses_pkg:msg/TobiiGlasses.idl
// generated code does not contain a copyright notice

#ifndef TOBII_GLASSES_PKG__MSG__DETAIL__TOBII_GLASSES__FUNCTIONS_H_
#define TOBII_GLASSES_PKG__MSG__DETAIL__TOBII_GLASSES__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "tobii_glasses_pkg/msg/rosidl_generator_c__visibility_control.h"

#include "tobii_glasses_pkg/msg/detail/tobii_glasses__struct.h"

/// Initialize msg/TobiiGlasses message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * tobii_glasses_pkg__msg__TobiiGlasses
 * )) before or use
 * tobii_glasses_pkg__msg__TobiiGlasses__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__TobiiGlasses__init(tobii_glasses_pkg__msg__TobiiGlasses * msg);

/// Finalize msg/TobiiGlasses message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__TobiiGlasses__fini(tobii_glasses_pkg__msg__TobiiGlasses * msg);

/// Create msg/TobiiGlasses message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * tobii_glasses_pkg__msg__TobiiGlasses__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
tobii_glasses_pkg__msg__TobiiGlasses *
tobii_glasses_pkg__msg__TobiiGlasses__create();

/// Destroy msg/TobiiGlasses message.
/**
 * It calls
 * tobii_glasses_pkg__msg__TobiiGlasses__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__TobiiGlasses__destroy(tobii_glasses_pkg__msg__TobiiGlasses * msg);

/// Check for msg/TobiiGlasses message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__TobiiGlasses__are_equal(const tobii_glasses_pkg__msg__TobiiGlasses * lhs, const tobii_glasses_pkg__msg__TobiiGlasses * rhs);

/// Copy a msg/TobiiGlasses message.
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
tobii_glasses_pkg__msg__TobiiGlasses__copy(
  const tobii_glasses_pkg__msg__TobiiGlasses * input,
  tobii_glasses_pkg__msg__TobiiGlasses * output);

/// Initialize array of msg/TobiiGlasses messages.
/**
 * It allocates the memory for the number of elements and calls
 * tobii_glasses_pkg__msg__TobiiGlasses__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__init(tobii_glasses_pkg__msg__TobiiGlasses__Sequence * array, size_t size);

/// Finalize array of msg/TobiiGlasses messages.
/**
 * It calls
 * tobii_glasses_pkg__msg__TobiiGlasses__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__fini(tobii_glasses_pkg__msg__TobiiGlasses__Sequence * array);

/// Create array of msg/TobiiGlasses messages.
/**
 * It allocates the memory for the array and calls
 * tobii_glasses_pkg__msg__TobiiGlasses__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
tobii_glasses_pkg__msg__TobiiGlasses__Sequence *
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__create(size_t size);

/// Destroy array of msg/TobiiGlasses messages.
/**
 * It calls
 * tobii_glasses_pkg__msg__TobiiGlasses__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
void
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__destroy(tobii_glasses_pkg__msg__TobiiGlasses__Sequence * array);

/// Check for msg/TobiiGlasses message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_tobii_glasses_pkg
bool
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__are_equal(const tobii_glasses_pkg__msg__TobiiGlasses__Sequence * lhs, const tobii_glasses_pkg__msg__TobiiGlasses__Sequence * rhs);

/// Copy an array of msg/TobiiGlasses messages.
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
tobii_glasses_pkg__msg__TobiiGlasses__Sequence__copy(
  const tobii_glasses_pkg__msg__TobiiGlasses__Sequence * input,
  tobii_glasses_pkg__msg__TobiiGlasses__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // TOBII_GLASSES_PKG__MSG__DETAIL__TOBII_GLASSES__FUNCTIONS_H_
