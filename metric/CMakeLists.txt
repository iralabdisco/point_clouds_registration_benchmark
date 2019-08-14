cmake_minimum_required (VERSION 2.8)
project(point_cloud_registration_benchmark)

find_package(PCL 1.7 REQUIRED)


set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14")

include_directories(${PCL_INCLUDE_DIRS})
#link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_library(${PROJECT_NAME}_metric INTERFACE)
target_include_directories(${PROJECT_NAME}_metric INTERFACE .)

install(FILES metric.hpp DESTINATION include)
