//
// Created by hariharan on 8/8/22.
//

#ifndef BRAHMA_INTERCEPTOR_H
#define BRAHMA_INTERCEPTOR_H

#include <brahma/brahma_config.hpp>
/* Internal Headers */
#include <brahma/logging.h>
/* External Headers */
#include <gotcha/gotcha.h>

#include <cstdarg>
#include <memory>

#define GOTCHA_BINDING_MACRO(fname)                                 \
  bindings[binding_index].name = #fname;                            \
  bindings[binding_index].wrapper_pointer = (void*)fname##_wrapper; \
  bindings[binding_index].function_handle = &fname##_handle;        \
  binding_index++;

#define GOTCHA_MACRO_TYPEDEF(name, ret, args, args_val, class_name) \
  typedef ret(*name##_fptr) args;                                   \
  inline ret name##_wrapper args {                                  \
    return class_name::get_instance()->name args_val;               \
  }                                                                 \
  gotcha_wrappee_handle_t get_##name##_handle();
#define GOTCHA_MACRO_TYPEDEF_OPEN(name, ret, args, args_val, start, \
                                  class_name)                       \
  typedef ret(*name##_fptr) args;                                   \
  inline ret name##_wrapper args {                                  \
    va_list _args;                                                  \
    va_start(_args, start);                                         \
    int mode = va_arg(_args, int);                                  \
    va_end(_args);                                                  \
    ret v = class_name::get_instance()->name args_val;              \
    return v;                                                       \
  }                                                                 \
  gotcha_wrappee_handle_t get_##name##_handle();

#define GOTCHA_MACRO_TYPEDEF_EXECL(name, ret, args, args_val, start, \
                                   class_name)                       \
  typedef ret(*name##_fptr) args;                                    \
  inline ret name##_wrapper args {                                   \
    va_list _args;                                                   \
    va_start(_args, start);                                          \
    char* val = va_arg(_args, char*);                                \
    va_end(_args);                                                   \
    ret v = class_name::get_instance()->name args_val;               \
    return v;                                                        \
  }                                                                  \
  gotcha_wrappee_handle_t get_##name##_handle();

#define GOTCHA_MACRO(name, ret, args, args_val, class_name) \
  gotcha_wrappee_handle_t name##_handle;                    \
  gotcha_wrappee_handle_t get_##name##_handle() { return name##_handle; }

#define BRAHMA_WRAPPER(name) name##_wrapper;

#define BRAHMA_UNWRAPPED_FUNC(name, ret, args)                                 \
  BRAHMA_LOG_INFO("[BRAHMA]\tFunction %s() not wrapped. Calling Original.\n",  \
                  #name);                                                      \
  name##_fptr name##_wrappee = (name##_fptr)gotcha_get_wrappee(name##_handle); \
  ret result = name##_wrappee args;

#define BRAHMA_UNWRAPPED_FUNC_VOID(name, args)                                 \
  BRAHMA_LOG_INFO("[BRAHMA]\tFunction %s() not wrapped. Calling Original.\n",  \
                  #name);                                                      \
  name##_fptr name##_wrappee = (name##_fptr)gotcha_get_wrappee(name##_handle); \
  name##_wrappee args;
#define BRAHMA_MAP_OR_FAIL(func_)                               \
  auto __real_##func_ =                                         \
      (func_##_fptr)gotcha_get_wrappee(get_##func_##_handle()); \
  assert(__real_##func_ != NULL)

size_t count_posix();
size_t count_stdio();
size_t count_mpiio();
size_t count_mpi();
int update_posix(gotcha_binding_t*& bindings, size_t& binding_index);

int update_stdio(gotcha_binding_t*& bindings, size_t& binding_index);

int update_mpiio(gotcha_binding_t*& bindings, size_t& binding_index);
int update_mpi(gotcha_binding_t*& bindings, size_t& binding_index);

extern int brahma_bind_functions();
extern int brahma_get_binding(gotcha_binding_t*& bindings,
                              size_t& binding_count);

#endif  // BRAHMA_INTERCEPTOR_H
