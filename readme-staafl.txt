- has to be in c:
- md build
- pip install pillow
- pip install requests
- set PATH=%PYTHON_HOME%;%PATH%
- https://github.com/Kitware/CMake/releases/download/v3.16.3/cmake-3.16.3-win32-x86.msi
- https://netcologne.dl.sourceforge.net/project/glew/glew/2.1.0/glew-2.1.0-win32.zip
    include to C:\Program Files (x86)\Microsoft Visual Studio\2019\Preview\VC\Tools\MSVC\14.20.27607\include
- https://www.libsdl.org/release/SDL2-devel-2.0.10-VC.zip
    include to C:\Program Files (x86)\Microsoft Visual Studio\2019\Preview\VC\Tools\MSVC\14.20.27607\include
    lib to lib
- tools\apikey.txt (shadertoy api key)
- autogen\g_textures.h (I can't figure out why this isn't regenerated currencly)
    maybe because of that stuff i commented out in parse_shadertoy_json.py
- tools\prods\molten bismuth\sdl2.dll

tools\hardcode_shadertoy.py
tools\parse_shadertoy_json.py
tools\apikey.txt