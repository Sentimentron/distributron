cmake_minimum_required(VERSION 2.8)

add_library (distributron socket.c)

enable_testing()

find_program( MEMORYCHECK_COMMAND valgrind )
set( MEMORYCHECK_COMMAND_OPTIONS "--trace-children=yes --leak-check=full" )

macro(_DTEST TEST)
  add_executable( test_${TEST} test_${TEST}.c )
  target_link_libraries(test_${TEST} distributron)

  add_test(test_${TEST} test_${TEST})

  set(memcheck_command "${CMAKE_MEMORYCHECK_COMMAND}
    ${CMAKE_MEMORYCHECK_COMMAND_OPTIONS}")
  separate_arguments(memcheck_command)
  #add_test(memcheck_${TEST} ${memcheck_command} test_${TEST})
endmacro()

_dtest("puck")
