cmake_minimum_required(VERSION 3.3)  # minimum cmake version required 
project(spreadsheet) # Project name and can also specify version example # project(spreadsheet VERSION 1.0)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11") # specifing the cpp standard

set(BOOST_ROOT "./boost_1_77_0") # path where boost is installed
set(BOOSTROOT "./boost_1_77_0")  # path where boost is installed

find_package(Boost 1.77.0) # find boost package

if(NOT Boost_FOUND)
    message(FATAL_ERROR "Could not find boost!")
endif()

# if found do this
include_directories(${Boost_INCLUDE_DIRS})
include_directories("../streamulus/src")
include_directories(".")

add_definitions(-DUSE_MAIN)


add_executable(spreadsheet main.cpp)