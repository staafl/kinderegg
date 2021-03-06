CMAKE_MINIMUM_REQUIRED( VERSION 2.6 )
PROJECT( kinderegg )

INCLUDE(cmake_modules/InvokePython.cmake)
INVOKEPYTHON( "tools/hardcode_shadertoy.py" )
# Python script will dump generated headers to autogen/
INCLUDE_DIRECTORIES("autogen/")

# GLFW, SDL, SFML
SET( GL_FRAMEWORK "SDL" CACHE STRING "Which OpenGL windowing framework to use" )

SET( USE_CORE_CONTEXT TRUE CACHE BOOL "Use Core Context" )
IF( USE_CORE_CONTEXT )
    ADD_DEFINITIONS(-DUSE_CORE_CONTEXT)
ENDIF()

#
# Platform-dependent section
#
IF( WIN32 )
    MESSAGE(STATUS "MSVC_VERSION=${MSVC_VERSION}")
    # 1600 = VS 10.0
    # 1700 = VS 11.0
    # 1800 = VS 12.0

    #
    # Custom Windows include and link dirs for my machine:
    #
    SET( LIBS_HOME "C:/lib" CACHE STRING "Location of support libraries Glut, Glew and others"  )

    SET( GLM_ROOT "${LIBS_HOME}/glm-0.9.5.4/glm" CACHE STRING "glm root" )
    INCLUDE_DIRECTORIES( "${GLM_ROOT}" )
    ADD_DEFINITIONS( -DGLM_FORCE_RADIANS )

    IF( GL_FRAMEWORK STREQUAL "GLFW" )
        MESSAGE("Using GLFW Framework.")
        IF( MSVC_VERSION STREQUAL "1600" ) # VS 2010
            SET( GLFW3_ROOT "${LIBS_HOME}/glfw-3.1.bin.WIN32" CACHE STRING "glfw root" )
            LINK_DIRECTORIES( "${GLFW3_ROOT}/lib-vc2010" )
        ELSEIF( MSVC_VERSION STREQUAL "1700" )
            SET( GLFW3_ROOT "${LIBS_HOME}/glfw-3.1.bin.WIN32" CACHE STRING "glfw root" )
            LINK_DIRECTORIES( "${GLFW3_ROOT}/lib-vc2012" )
        ELSEIF( MSVC_VERSION STREQUAL "1800" )
            SET( GLFW3_ROOT "${LIBS_HOME}/glfw-3.1.bin.WIN32" CACHE STRING "glfw root" )
            LINK_DIRECTORIES( "${GLFW3_ROOT}/lib-vc2013" )
        ENDIF()
        INCLUDE_DIRECTORIES( "${GLFW3_ROOT}/include" )
        SET( FRAMEWORK_LIBS glfw3.lib )
    ELSEIF( GL_FRAMEWORK STREQUAL "SDL" )
        MESSAGE("Using SDL2 Framework.")
        SET( SDL2_ROOT "${LIBS_HOME}/SDL2-2.0.3" CACHE STRING "SDL2 root" )
        INCLUDE_DIRECTORIES( "${SDL2_ROOT}/include" )
        LINK_DIRECTORIES   ( "${SDL2_ROOT}/lib/x86" )
        SET( FRAMEWORK_LIBS SDL2.lib )
    ELSEIF( GL_FRAMEWORK STREQUAL "SFML" )
        SET( SFML_ROOT "${LIBS_HOME}/SFML-2.2" CACHE STRING "SFML root" )
        INCLUDE_DIRECTORIES( "${SFML_ROOT}/include" )
        LINK_DIRECTORIES   ( "${SFML_ROOT}/lib" )
        SET( FRAMEWORK_LIBS sfml-main.lib sfml-system.lib sfml-window.lib )
    ELSE()
        MESSAGE("Unknown GL_FRAMEWORK: choose GLFW or SDL.")
    ENDIF()

    SET( GLEW_ROOT "${LIBS_HOME}/glew-1.12.0" CACHE STRING "glew root" )
    INCLUDE_DIRECTORIES( "${GLEW_ROOT}/include" )
    LINK_DIRECTORIES   ( "${GLEW_ROOT}/lib/Release/Win32" )
    ADD_DEFINITIONS( -DGLEW_STATIC )

    SET( PLATFORM_LIBS
        ${FRAMEWORK_LIBS}
        opengl32.lib glu32.lib glew32s.lib
        Winmm.lib
        ws2_32.lib
        )

    ADD_DEFINITIONS( /W4 -D_CRT_SECURE_NO_WARNINGS )

    # These lines will silence some linker warnings on VS2010,
    # but also remove debug info from the debug build.
    #SET( CMAKE_EXE_LINKER_FLAGS /NODEFAULTLIB:\"libcmt.lib\" )
    #SET( CMAKE_EXE_LINKER_FLAGS_DEBUG /NODEFAULTLIB:\"msvcrt.lib\" )
ELSEIF( APPLE )
    ADD_DEFINITIONS( -D_MACOS )

    SET(CMAKE_CXX_FLAGS "-fno-rtti")

    INCLUDE_DIRECTORIES ( /System/Library/Frameworks )
    FIND_LIBRARY(COCOA_LIBRARY Cocoa)
    FIND_LIBRARY(IOKIT_LIBRARY IOKit)
    FIND_LIBRARY(GLUT_LIBRARY GLUT )
    FIND_LIBRARY(OpenGL_LIBRARY OpenGL )
    MARK_AS_ADVANCED (COCOA_LIBRARY
                      GLUT_LIBRARY
                      IOKIT_LIBRARY
                      OpenGL_LIBRARY)
    INCLUDE_DIRECTORIES( "/opt/local/include/" )
    LINK_DIRECTORIES   ( "/opt/local/lib" )

    SET( LIBS_HOME "~/Development/" )

    SET( GLM_ROOT "${LIBS_HOME}/glm-0.9.5.4/glm" CACHE STRING "glm root" )
    INCLUDE_DIRECTORIES( "${GLM_ROOT}" )
    ADD_DEFINITIONS( -DGLM_FORCE_RADIANS )

    SET( GLFW3_ROOT "${LIBS_HOME}/glfw-3.1/" )
    INCLUDE_DIRECTORIES( "${GLFW3_ROOT}/include" )
    LINK_DIRECTORIES   ( "${GLFW3_ROOT}/lib" )

    IF( USE_OCULUSSDK )
        SET( OCULUSSDK_ROOT "${LIBS_HOME}/OculusSDK" )
        INCLUDE_DIRECTORIES( "${OCULUSSDK_ROOT}/LibOVR/Include" )
        INCLUDE_DIRECTORIES( "${OCULUSSDK_ROOT}/LibOVR/Src" )
        LINK_DIRECTORIES   ( "${OCULUSSDK_ROOT}/LibOVR/Lib/Mac/Debug/" )
        ADD_DEFINITIONS( -DOVR_OS_MAC )
        ADD_DEFINITIONS( -DUSE_OCULUSSDK )
    ENDIF( USE_OCULUSSDK )

    FIND_LIBRARY(COCOA_LIBRARY Cocoa)
    FIND_LIBRARY(IOKIT_LIBRARY IOKit)

    MARK_AS_ADVANCED (COCOA_LIBRARY
                      IOKIT_LIBRARY
                      )
    # Todo - build OVR with RTTI support
    SET(CMAKE_CXX_FLAGS "-fno-rtti -framework CoreVideo")

    #SET( PLATFORM_LIBS libovr.a ${COCOA_LIBRARY} ${IOKIT_LIBRARY} )
    SET( PLATFORM_LIBS
        ${FRAMEWORK_LIBS}
        ${COCOA_LIBRARY}
        ${IOKIT_LIBRARY}
        ${GLUT_LIBRARY}
        ${OpenGL_LIBRARY}
        -lGLEW
        -lglfw3
        -lovr
        )
        # TODO: SDL2 or glfw

ELSEIF( UNIX )
    ADD_DEFINITIONS( -D_LINUX )
    SET( LIBS_HOME "~/lib" )
    
    ADD_DEFINITIONS( -D_DEBUG )
    SET(CMAKE_CXX_FLAGS "-ggdb")
    SET(CMAKE_CXX_FLAGS_DEBUG "-ggdb")

    SET( GLM_ROOT "${LIBS_HOME}/glm-0.9.5.4/glm" CACHE STRING "glm root" )
    INCLUDE_DIRECTORIES( "${GLM_ROOT}" )
    ADD_DEFINITIONS( -DGLM_FORCE_RADIANS )

    IF( GL_FRAMEWORK STREQUAL "GLFW" )
        MESSAGE("Using GLFW Framework.")
        SET( FRAMEWORK_LIBS -lglfw3 )
    ELSEIF( GL_FRAMEWORK STREQUAL "SDL" )
        MESSAGE("Using SDL2 Framework.")
        INCLUDE_DIRECTORIES( "/usr/include/SDL2" )
        LINK_DIRECTORIES   ( "/usr/local/lib/x86" )
        SET( FRAMEWORK_LIBS -lSDL2 )
    ELSE()
        MESSAGE("Unknown GL_FRAMEWORK: choose GLFW or SDL.")
    ENDIF()

    find_package(OpenGL REQUIRED)
    include_directories( ${OPENGL_INCLUDE_DIRS} )

    SET( PLATFORM_LIBS
        ${OVR_LIBS}
        -lGLEW
        -lGL
        -lGLU
        ${FRAMEWORK_LIBS}
        -pthread
        -lrt
        -lXrandr
        -lXxf86vm
        -lXi
        -lX11
        -lXinerama # GLFW 3.1
        -lXcursor # GLFW 3.1
        )
ENDIF()


#
# Platform-independent section
#
FILE( GLOB_RECURSE UTIL_SOURCE_FILES
    src/Util/*.cpp
    src/Util/*.h
    )

INCLUDE_DIRECTORIES("src")
INCLUDE_DIRECTORIES("src/util")

ADD_LIBRARY( Util ${UTIL_SOURCE_FILES} )

IF( GL_FRAMEWORK STREQUAL "GLFW" )
    ADD_EXECUTABLE( ${PROJECT_NAME} src/glfw_main.cpp ${SOURCE_FILES} )
ELSEIF( GL_FRAMEWORK STREQUAL "SDL" )
    ADD_EXECUTABLE( ${PROJECT_NAME} src/sdl_main.cpp ${SOURCE_FILES} )
ELSEIF( GL_FRAMEWORK STREQUAL "SFML" )
    ADD_EXECUTABLE( ${PROJECT_NAME} src/sfml_main.cpp ${SOURCE_FILES} )
ENDIF()

TARGET_LINK_LIBRARIES( ${PROJECT_NAME}
    Util
    ${PLATFORM_LIBS}
    )
