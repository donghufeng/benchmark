cmake_minimum_required(VERSION 3.15 FATAL_ERROR)

project(benchmark)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(ThirdPartyPath ${PROJECT_SOURCE_DIR}/third_party)
set(VenvPath ${PROJECT_SOURCE_DIR}/venv)
find_package(pybind11)

# QuEST
LINK_DIRECTORIES(${VenvPath}/lib)
pybind11_add_module(quest_test ${PROJECT_SOURCE_DIR}/ccsrc/quest_test.cpp)
target_include_directories(quest_test PUBLIC ${ThirdPartyPath}/QuEST/QuEST/include)
target_link_libraries(quest_test PUBLIC -lQuEST)
set_target_properties(quest_test PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/benchmark)
