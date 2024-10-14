#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "grape_engine" for configuration "Release"
set_property(TARGET grape_engine APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(grape_engine PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/grape_engine"
  )

list(APPEND _cmake_import_check_targets grape_engine )
list(APPEND _cmake_import_check_files_for_grape_engine "${_IMPORT_PREFIX}/bin/grape_engine" )

# Import target "gs_proto" for configuration "Release"
set_property(TARGET gs_proto APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(gs_proto PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgs_proto.so"
  IMPORTED_SONAME_RELEASE "libgs_proto.so"
  )

list(APPEND _cmake_import_check_targets gs_proto )
list(APPEND _cmake_import_check_files_for_gs_proto "${_IMPORT_PREFIX}/lib/libgs_proto.so" )

# Import target "gs_util" for configuration "Release"
set_property(TARGET gs_util APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(gs_util PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "grape-lite;vineyard_client;vineyard_basic;vineyard_io;vineyard_graph;vineyard_malloc;vineyard_llm_cache;Boost::system;Boost::filesystem;Boost::context;Boost::program_options;Boost::regex;Boost::thread"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libgs_util.so"
  IMPORTED_SONAME_RELEASE "libgs_util.so"
  )

list(APPEND _cmake_import_check_targets gs_util )
list(APPEND _cmake_import_check_files_for_gs_util "${_IMPORT_PREFIX}/lib/libgs_util.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
