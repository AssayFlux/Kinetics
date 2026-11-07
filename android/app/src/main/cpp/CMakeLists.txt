cmake_minimum_required(VERSION 3.22.1)
project(kinetics_native LANGUAGES C CXX)

add_library(kinetics_rust STATIC IMPORTED)
set_target_properties(kinetics_rust PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/../../../../../native-rust/target/aarch64-linux-android/release/libkinetics_rust.a"
)

add_library(kinetics_native SHARED kinetics_native.cpp)
target_compile_features(kinetics_native PRIVATE cxx_std_17)
target_link_options(kinetics_native PRIVATE "-Wl,-z,max-page-size=16384")
target_link_libraries(kinetics_native PRIVATE kinetics_rust)
