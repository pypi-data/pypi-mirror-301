# ___license_placeholder___###

if(STEPS_ENABLE_ERROR_ON_WARNING)
  add_options(ALL_LANGUAGES ALL_BUILDS -Werror)
endif()

add_definitions(-DENABLE_ASSERTLOG=1)

set(lib_soversion "${VERSION_MAJOR}.${VERSION_MINOR}")
set(lib_version "${lib_soversion}.${VERSION_PATCH}")

add_subdirectory(steps/math)
add_subdirectory(steps/geom)
add_subdirectory(steps/model)
add_subdirectory(steps/rng)
add_subdirectory(steps/solver)
add_subdirectory(steps/tetexact)
add_subdirectory(steps/tetode)
add_subdirectory(steps/util)
add_subdirectory(steps/wmdirect)
add_subdirectory(steps/wmrk4)
add_subdirectory(steps/wmrssa)

# enable below to turn on MPI profiling
if(USE_MPI)
  add_subdirectory(steps/mpi)
  if(USE_MPI_PROFILING)
    add_definitions(-DMPI_PROFILING=1)
  endif()
endif()

# ==============================================================================
# ==============================

add_library(libsteps_static STATIC $<TARGET_OBJECTS:stepswmrssa>)
set_target_properties(libsteps_static PROPERTIES OUTPUT_NAME steps)
target_link_libraries(
  libsteps_static
  PUBLIC stepsutil
         stepsmath
         stepsgeom
         stepsrng
         stepsmodel
         stepssolver
         stepstetexact
         stepstetode
         stepswmdirect
         stepswmrk4
         ${libsteps_link_libraries})
if(USE_MPI)
  target_link_libraries(libsteps_static PUBLIC stepstetopsplit)
  target_link_libraries(libsteps_static PUBLIC stepstetvesicle)
  if(STEPS_USE_DIST_MESH)
    target_link_libraries(libsteps_static PUBLIC stepsdist)
  endif()
endif()

add_library(libsteps SHARED $<TARGET_OBJECTS:stepswmrssa>)
target_link_libraries(
  libsteps
  PUBLIC stepsutil
         stepsmath
         stepsgeom
         stepsrng
         stepsmodel
         stepssolver
         stepstetexact
         stepstetode
         stepswmdirect
         stepswmrk4
         ${libsteps_link_libraries})
if(USE_MPI)
  target_link_libraries(libsteps PUBLIC stepstetopsplit)
  target_link_libraries(libsteps PUBLIC stepstetvesicle)
  if(STEPS_USE_DIST_MESH)
    target_link_libraries(libsteps PUBLIC stepsdist)
  endif()
endif()

set_target_properties(libsteps PROPERTIES VERSION "${lib_version}" SOVERSION "${lib_soversion}")
set_target_properties(libsteps PROPERTIES OUTPUT_NAME steps)

# ==========================================================================
# Installation of the headers and shared lib
#
option(INSTALL_DEV_LIBS "Install steps lib and headers which are required for development only" OFF)

if(INSTALL_DEV_LIBS)
  install(
    TARGETS libsteps
    RUNTIME DESTINATION bin COMPONENT lib
    ARCHIVE DESTINATION lib COMPONENT lib
    LIBRARY DESTINATION lib COMPONENT lib)
endif()
