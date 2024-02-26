// generated from
// rosidl_typesupport_c/resource/rosidl_typesupport_c__visibility_control.h.in
// generated code does not contain a copyright notice

#ifndef TOBII_GLASSES_PKG__MSG__ROSIDL_TYPESUPPORT_C__VISIBILITY_CONTROL_H_
#define TOBII_GLASSES_PKG__MSG__ROSIDL_TYPESUPPORT_C__VISIBILITY_CONTROL_H_

#ifdef __cplusplus
extern "C"
{
#endif

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
  #ifdef __GNUC__
    #define ROSIDL_TYPESUPPORT_C_EXPORT_tobii_glasses_pkg __attribute__ ((dllexport))
    #define ROSIDL_TYPESUPPORT_C_IMPORT_tobii_glasses_pkg __attribute__ ((dllimport))
  #else
    #define ROSIDL_TYPESUPPORT_C_EXPORT_tobii_glasses_pkg __declspec(dllexport)
    #define ROSIDL_TYPESUPPORT_C_IMPORT_tobii_glasses_pkg __declspec(dllimport)
  #endif
  #ifdef ROSIDL_TYPESUPPORT_C_BUILDING_DLL_tobii_glasses_pkg
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_tobii_glasses_pkg ROSIDL_TYPESUPPORT_C_EXPORT_tobii_glasses_pkg
  #else
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_tobii_glasses_pkg ROSIDL_TYPESUPPORT_C_IMPORT_tobii_glasses_pkg
  #endif
#else
  #define ROSIDL_TYPESUPPORT_C_EXPORT_tobii_glasses_pkg __attribute__ ((visibility("default")))
  #define ROSIDL_TYPESUPPORT_C_IMPORT_tobii_glasses_pkg
  #if __GNUC__ >= 4
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_tobii_glasses_pkg __attribute__ ((visibility("default")))
  #else
    #define ROSIDL_TYPESUPPORT_C_PUBLIC_tobii_glasses_pkg
  #endif
#endif

#ifdef __cplusplus
}
#endif

#endif  // TOBII_GLASSES_PKG__MSG__ROSIDL_TYPESUPPORT_C__VISIBILITY_CONTROL_H_
