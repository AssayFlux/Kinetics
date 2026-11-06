cmake_minimum_required(VERSION 3.20)
project(kinetics_molecule VERSION 0.1.0 LANGUAGES CXX)

option(KINETICS_BUILD_TESTS "Build native reference tests" ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(kinetics_molecule src/molecule.cpp)
target_include_directories(kinetics_molecule PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_features(kinetics_molecule PUBLIC cxx_std_17)
if(MSVC)
  target_compile_options(kinetics_molecule PRIVATE /W4 /permissive-)
else()
  target_compile_options(kinetics_molecule PRIVATE -Wall -Wextra -Wpedantic -Wconversion)
endif()

add_executable(kinetics-molecule-inspect src/inspect.cpp)
target_link_libraries(kinetics-molecule-inspect PRIVATE kinetics_molecule)

if(KINETICS_BUILD_TESTS)
  enable_testing()
  add_executable(kinetics_molecule_tests tests/test_molecule.cpp)
  target_link_libraries(kinetics_molecule_tests PRIVATE kinetics_molecule)
  target_compile_definitions(kinetics_molecule_tests PRIVATE
    KINETICS_FIXTURE_DIR="${CMAKE_CURRENT_SOURCE_DIR}/tests/fixtures")
  add_test(NAME kinetics_molecule_reference COMMAND kinetics_molecule_tests)
endif()
