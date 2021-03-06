# - Config file for the dashel package
# It defines the following variables
# dashel_INCLUDE_DIRS - include directories for dashel
# dashel_LIBRARIES - libraries to link against

# Dependencies of Dashel
if (WIN32)
	set(EXTRA_LIBS winspool ws2_32 setupapi)
else (WIN32)
	# only if we build static library we need to link the add_dependencies
	# of Dashel to the final versions
	set (NO_LINK_DASHEL_DEPS ON)
	if (NOT NO_LINK_DASHEL_DEPS)
		if (APPLE)
			find_library(COREFOUNDATION_LIBRARY CoreFoundation)
			find_library(IOKIT_LIBRARY IOKit)
			mark_as_advanced(COREFOUNDATION_LIBRARY)
			mark_as_advanced(IOKIT_LIBRARY)
			find_library(POLL_LIBRARY poll)
			set(EXTRA_LIBS ${COREFOUNDATION_LIBRARY} ${IOKIT_LIBRARY} ${POLL_LIBRARY})
		else (APPLE)
			# look for libudev
			find_path(UDEV_INCLUDE_DIR libudev.h)
			find_library(UDEV_LIBS udev)
			if (UDEV_INCLUDE_DIR AND UDEV_LIBS)
				message(STATUS "libudev found")
				include_directories(${UDEV_INCLUDE_DIR})
				set(EXTRA_LIBS ${UDEV_LIBS})
				add_definitions(-DUSE_LIBUDEV)
			else ()
				find_package(PkgConfig)
				pkg_check_modules(HAL hal)
				if (${HAL_FOUND})
					message(STATUS "hal found")
					include_directories(${HAL_INCLUDE_DIRS})
					set(EXTRA_LIBS ${HAL_LIBRARIES})
					add_definitions(-DUSE_HAL)
				endif (${HAL_FOUND})
			endif ()
		endif (APPLE)
	endif ()
endif (WIN32)

# Standard search
find_path(DASHEL_INCLUDE_DIR dashel/dashel.h CMAKE_FIND_ROOT_PATH_BOTH)
SET(dashel_INCLUDE_DIRS ${DASHEL_INCLUDE_DIR})
find_library(DASHEL_LIBRARY dashel CMAKE_FIND_ROOT_PATH_BOTH)
SET(dashel_LIBRARIES ${DASHEL_LIBRARY} ${EXTRA_LIBS})
