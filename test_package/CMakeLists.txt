project(test_package)
cmake_minimum_required(VERSION 2.8.11)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules")
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/build/") # for conan

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR}/)
  include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
  include(${CMAKE_BINARY_DIR}/conan_paths.cmake OPTIONAL)
  conan_basic_setup(
    # prevent conan_basic_setup from resetting cmake variables
    TARGETS
    KEEP_RPATHS
    # see https://github.com/conan-io/conan/issues/6012
    NO_OUTPUT_DIRS
  )
else()
  message (FATAL_ERROR "must use conan")
endif()

if(NOT TARGET CONAN_PKG::cling_conan)
  message(FATAL_ERROR "Use CONAN_PKG::cling_conan from conan")
endif()

message (STATUS "CONAN_CLING_CONAN_ROOT=${CONAN_CLING_CONAN_ROOT}")
message (STATUS "CONAN_LIB_DIRS_CLING_CONAN=${CONAN_LIB_DIRS_CLING_CONAN}")
message (STATUS "CONAN_BUILD_DIRS_CLING_CONAN=${CONAN_BUILD_DIRS_CLING_CONAN}")
message (STATUS "CONAN_INCLUDE_DIRS_CLING_CONAN=${CONAN_INCLUDE_DIRS_CLING_CONAN}")

find_path(CLING_Interpreter_INCLUDE_DIR ClingOptions.h
          HINTS 
                ${CONAN_CLING_CONAN_ROOT}
                ${CONAN_LIB_DIRS_CLING_CONAN}
                ${CONAN_BUILD_DIRS_CLING_CONAN}
                ${CONAN_INCLUDE_DIRS_CLING_CONAN}
                ${CONAN_CLING_CONAN_ROOT}/include/cling/Interpreter
                # fallback to system one
                ${CLING_DIR}/src/tools/cling/include/cling/Interpreter
                ${CLING_DIR}/llvm_src/tools/cling/include/cling/Interpreter
                $ENV{CLING_PREFIX}/include/cling/Interpreter
                ${CLING_PREFIX}/include/cling/Interpreter
                /usr/include/cling/Interpreter
                /usr/local/include/cling/Interpreter
                /opt/local/include/cling/Interpreter
          NO_DEFAULT_PATH)

message(STATUS "[cling] CLING_Interpreter_INCLUDE_DIR: ${CLING_Interpreter_INCLUDE_DIR}")

find_path(LLVMConfig_DIR LLVMConfig.cmake
          HINTS 
                ${CONAN_CLING_CONAN_ROOT}
                ${CONAN_LIB_DIRS_CLING_CONAN}
                ${CONAN_BUILD_DIRS_CLING_CONAN}
                ${CONAN_INCLUDE_DIRS_CLING_CONAN}
                ${CONAN_CLING_CONAN_ROOT}/lib/cmake/llvm
                # fallback to system one
                ${CLING_DIR}/src/tools/cling/include/cling/Interpreter
                ${CLING_DIR}/llvm_src/tools/cling/include/cling/Interpreter
                $ENV{CLING_PREFIX}/include/cling/Interpreter
                ${CLING_PREFIX}/include/cling/Interpreter
                ${CLING_Interpreter_INCLUDE_DIR}/../../../../../../build/lib/cmake/llvm
                /usr/include/cling/Interpreter
                /usr/local/include/cling/Interpreter
                /opt/local/include/cling/Interpreter
          NO_DEFAULT_PATH)

message(STATUS "[cling] LLVMConfig_DIR: ${LLVMConfig_DIR}")

include(
  ${LLVMConfig_DIR}/LLVMConfig.cmake
)

if(LLVM_BINARY_DIR)
  message(STATUS "[cling] LLVM_BINARY_DIR: ${LLVM_BINARY_DIR}")
else()
  message(FATAL_ERROR "[cling] LLVM_BINARY_DIR not found: ${LLVM_BINARY_DIR}")
endif()

list(APPEND CLING_DEFINITIONS LLVMDIR="${LLVM_BINARY_DIR}")

find_package( Threads REQUIRED )
message(STATUS "CMAKE_THREAD_LIBS_INIT = ${CMAKE_THREAD_LIBS_INIT}")

message(STATUS "CMAKE_DL_LIBS = ${CMAKE_DL_LIBS}")

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} PUBLIC
    CONAN_PKG::cling_conan
    Threads::Threads
    ${CMAKE_DL_LIBS}
    #LIBDL::LIBDL
    #${DLIB_LIB_DIR}/libdlib.so
    #tinfo
    #ncurses
)

target_compile_options(${PROJECT_NAME} PRIVATE
  -fno-rtti)

target_compile_definitions(${PROJECT_NAME} PUBLIC
  ${CLING_DEFINITIONS}
)

# POSITION_INDEPENDENT_CODE for -fPIC
set_property(TARGET ${PROJECT_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)

if(MSVC)
  set_target_properties(${PROJECT_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS 1)
  set_property(TARGET ${PROJECT_NAME} APPEND_STRING PROPERTY LINK_FLAGS
              "/EXPORT:?setValueNoAlloc@internal@runtime@cling@@YAXPEAX00D_K@Z
              /EXPORT:?setValueNoAlloc@internal@runtime@cling@@YAXPEAX00DM@Z
              /EXPORT:cling_runtime_internal_throwIfInvalidPointer")
endif()

set_target_properties( ${PROJECT_NAME} PROPERTIES
  OUTPUT_NAME ${PROJECT_NAME}
  CXX_STANDARD 17
  CXX_EXTENSIONS OFF
  CMAKE_CXX_STANDARD_REQUIRED ON
  RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib )
