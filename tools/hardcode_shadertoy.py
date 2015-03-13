# hardcode_shadertoy.py

from __future__ import print_function
import sys
import os

header = """/* GENERATED FILE - DO NOT EDIT!
 * Created by hardcode_shaders.py.
 *
 */
"""

passthruVert = """
#version 330
in vec4 vPosition;
void main()
{
    gl_Position = vPosition;
}
"""
imageHeader = """
#version 330
uniform vec3 iResolution; // viewport resolution (in pixels)
uniform float iGlobalTime; // shader playback time (in seconds)
out vec4 glFragColor;
"""
imageFooter = """
void main()
{
    vec4 fragcol = vec4(0.);
    mainImage(fragcol, gl_FragCoord.xy);
    glFragColor = fragcol;
}
"""

soundHeader = """
#version 330
// shadertoy.com effect.js line 77
//#extension GL_OES_standard_derivatives : enable
uniform vec4      iDate;                 // (year, month, day, time in seconds)
uniform float     iSampleRate;           // sound sample rate (i.e., 44100)
uniform float     iBlockOffset;
//uniform float     iChannelTime[4];
//uniform vec3      iChannelResolution[4];
out vec4 glFragColor;
"""
soundFooter= """
void main()
{
    float t = iBlockOffset + (gl_FragCoord.x + gl_FragCoord.y*512.0)/44100.0;

    vec2 y = mainSound( t );

    vec2 v  = floor((0.5+0.5*y)*65536.0);
    vec2 vl =   mod(v,256.0)/255.0;
    vec2 vh = floor(v/256.0)/255.0;
    glFragColor = vec4(vl.x,vh.x,vl.y,vh.y);
}

"""

def generateSourceFile():
	"""
	Output a hardcoded C++ source file with shaders as strings.
	"""
	shaderPath = "shaders/"
	autogenDir = "autogen/"
	sourceFileOut = autogenDir + "g_shaders.h"

	# Write a small comment if no shaders directory.
	if not os.path.isdir(shaderPath):
		print("Directory", shaderPath, "does not exist.")
		with open(sourceFileOut,'w') as outStream:
			print("/* Directory", shaderPath, "does not exist. */", file=outStream,)
		return

	# Create autogen/ if it's not there.
	if not os.path.isdir(autogenDir):
		os.makedirs(autogenDir)

	tab = "    "
	decl = "const char* "
	newline = "\\n"
	quote = "\""

	with open(sourceFileOut,'w') as outStream:
		print(header, file=outStream)
		print("#include <map>", file=outStream)

		shaderList = [
			(imageHeader, 'image.frag', imageFooter),
			(soundHeader, 'sound.frag', soundFooter),
			(passthruVert, 'passthru.vert', None)
			]
		for shaderTup in shaderList:
			lines = shaderTup[0].splitlines()
			shaderName = shaderTup[1]
			if shaderName is not None:
				file = shaderPath + shaderName
				try:
					lines.extend(open(file).read().splitlines())
					lines.extend(shaderTup[2].splitlines())
				except:
					pass
			varname = shaderName.replace(".","_")
			print("\n" + decl + varname + " = ", file=outStream)
			for l in lines:
				if l != "":
					l = l.replace('"', '\\"')
					print(tab + quote + l + newline + quote, file=outStream)
			print(";", file=outStream)

		mapvar = "g_shaderMap"
		print("\n", file=outStream)
		print("std::map<std::string, std::string> " + mapvar + ";", file=outStream)
		print("\n", file=outStream)

		print("void initShaderList() {", file=outStream)
		for shaderTup in shaderList:
			fname = shaderTup[1]
			varname = fname.replace(".","_")
			print(tab + mapvar + "[\"" + fname + "\"] = " + varname + ";", file=outStream)
		print("}", file=outStream)


#
# Main: enter here
#
def main(argv=None):
	# TODO: create directory if it doesn't exist
	generateSourceFile()


if __name__ == "__main__":
	sys.exit(main())