# parse_shadertoy_json.py

from __future__ import print_function
import json
import os
import sys
import shutil
import requests
from PIL import Image

def deleteGeneratedFiles():
    """Delete old versions of generated files."""
    autogenDir = os.path.join('..', 'autogen')
    shadersDir = os.path.join('..', 'shaders')
    files = [
        os.path.join(autogenDir, 'g_textures.h'),
        os.path.join(autogenDir, 'g_shaders.h'),
        os.path.join(shadersDir, 'image.frag'),
        os.path.join(shadersDir, 'sound.frag')]
    for f in files:
        try:
            os.remove(f)
        except:
            pass


def dumpReadmeFile(info, dir):
    readmeFileOut = os.path.join(dir, 'README.txt')
    with open(readmeFileOut,'w') as outStream:
        print("Title: " + info['name'], file=outStream)
        print("Author: " + info['username'], file=outStream)
        print('',file=outStream)
        print("Tags: " + ', '.join(info['tags']), file=outStream)
        print('',file=outStream)
        print("Description: " + info['description'], file=outStream)
        print('',file=outStream)
        print('Generated from https://www.shadertoy.com/view/{0} by kinderegg.'.format(info['id']),file=outStream)


textureHeader = """/*
 * Generated by parse_shadertoy_json.py
 */
"""
def dumpTextureFiles(dir, renderpass, name):
    """Write texture data to binary files in output dir and dimensions to generated header.
    Also write the shadertoy name to the header."""

    texFileOut = os.path.join('..', 'autogen', 'g_textures.h')
    texDir = os.path.join('..', 'textures')
    with open(texFileOut,'w') as outStream:
        print(textureHeader, file=outStream)
        print('char* shadername = "{0}";'.format(name), file=outStream)
        pass_id = 0
        print('int texdims[] = {', file=outStream)
        for r in renderpass:
            # Pull out textures
            print("  Pass ")
            print(r['inputs'])
            tex_id = 0
            for i in range(4):
                inp = r['inputs']
                w = 0
                h = 0
                d = 0
                # Texture dimensions - write to C source header
                if i < len(inp):
                    t = inp[i]
                    texfile = os.path.basename(t['src'])
                    print("MOO")
                    img = Image.open(os.path.join(texDir,texfile))
                    px = img.load()
                    w = img.size[0]
                    h = img.size[1]
                    m = img.mode
                    if m == 'L':
                        d = 1
                    elif m == 'RGB':
                        d = 3
                    elif m == 'RGBA':
                        d = 4
                    else:
                        print('Unknown mode: ' + m)
                arrayname = 'tex' + str(pass_id) + str(i)
                print(arrayname)
                texline = '{0}, {1}, {2},'
                print(texline.format(w,h,d), file=outStream)

                # Texture data - store to files in prod dir
                pixels = []
                if i < len(inp):
                    for j in range(img.size[1]):
                        for k in range(img.size[0]):
                            p = px[k,j]
                            if isinstance(p,int):
                                pixels.append(p)
                            elif isinstance(p,tuple):
                                for ch in p:
                                    pixels.append(ch)
                    # Write pixels array to binary file
                    binFile = os.path.join(dir, arrayname)
                    print("writing " + str(len(pixels)) + " bytes to " + binFile)
                    print(pixels[0:10])
                    pxByteArray = bytearray(pixels)
                    with open(binFile,'wb') as pxBinOut:
                        pxBinOut.write(pxByteArray)

                tex_id += 1
            pass_id += 1
        print('};', file=outStream)


def dumpShaderFiles(renderpass):
    """Save shader source to ../shaders/ for hardcoding by CMake."""
    shaderDir = os.path.join('..', 'shaders')
    for r in renderpass:
        shfile = r['type'] + ".frag"
        src = r['code']
        # TODO some retroactive refactoring
        #src = src.replace("main", "mainImage")
        #src = src.replace("gl_FragColor", "glFragColor")
        with open(os.path.join(shaderDir, shfile),'w') as outStream:
            print(src, file=outStream)
        print(shfile + ": " + str(len(src)) + " bytes written.")


def getShadertoyJsonFromSite(id):
    """Send a request to Shadertoy.com for the given shadertoy id.
    Store your API key in the filename below.
    """
    apikey = "xxxxxx"
    with open('apikey.txt','r') as keystr:
        apikey = keystr.read()
    req = 'https://www.shadertoy.com/api/v1/shaders/{0}?key={1}'
    req = req.format(id, apikey)
    r = requests.get(req)
    print(r)
    return r.json()


def getShadertoyJsonFromFile(filename):
    """Load json from a file on disk."""
    try:
        j = json.loads(open(filename).read())
        return j
    except:
        pass


def invokeBuild(dir):
    """Invoke CMake which in turn invokes designated compiler to build the executable."""
    cmakepath = 'C:/Program Files (x86)/CMake/bin/'
    if not os.path.exists(cmakepath):
        cmakepath = 'C:/Program Files (x86)/CMake 2.8/bin/'
    cmakepath += 'cmake'
    cmakepath = '"' + cmakepath + '"' # Wrap in quotes for Windows shell
    slnpath = '../build'
    os.chdir(slnpath)
    cmds = [
        cmakepath + ' ..',
        cmakepath + ' --build . --config Release --clean-first',]
    for c in cmds:
        print(c)
        os.system(c)


def copyExecutable(dir, name):
    """Copy the built exe to the output directory."""
    kepath = "./Release"
    keexe = "kinderegg.exe" # specified in CMakeLists.txt
    shutil.copyfile(
        os.path.join(kepath, keexe),
        os.path.join('..', 'tools', dir, name+'.exe'))
    # Copy SDL2.dll to output dir
    sdlpath = 'C:/lib/SDL2-2.0.3'
    sdllibpath = 'lib/x86'
    sdldllname = 'SDL2.dll'
    shutil.copyfile(
        os.path.join(sdlpath, sdllibpath, sdldllname),
        os.path.join('..', 'tools', dir, sdldllname))


#
# Main: enter here
#
def main(argv=None):
    # https://www.shadertoy.com/api/v1/shaders/query/string?key=appkey
    # Broken examples:
    # ldXXDj - Pirates by iq
    # XsX3RB - Volcanic by iq
    # MdB3Rc
#    if len(sys.argv) <= 1:
#        print("Usage:")
#        print("    python parse_shadertoy_json.py <jsonfile>")
#        print("    python parse_shadertoy_json.py <id>")
#        quit()
#    id = sys.argv[1]
#    j = getShadertoyJsonFromFile(id)
#    if j is None:
#        print("File " + id + " not found.")
#        j = getShadertoyJsonFromSite(id)
#
#    if 'Error' in j:
#        print(j['Error'])
#    else:
#        print('Success')
#        info = j['Shader']['info']
#        # Sanitize name
#        import string
#        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
#        info['name'] = ''.join(c for c in info['name'] if c in valid_chars)
#        name = info['name']
#        proddir = 'prods'
#        if not os.path.exists(proddir):
#            os.mkdir(proddir)
#        dir = os.path.join('prods', name)
#        if not os.path.exists(dir):
#            os.mkdir(dir)
#        dumpReadmeFile(info, dir)
#        renderpass = j['Shader']['renderpass']
#        deleteGeneratedFiles()
#        dumpShaderFiles(renderpass)
#        print("hi")
#        dumpTextureFiles(dir, renderpass, name)
#        print("there")
#        invokeBuild(dir)
        invokeBuild(dir)
#       copyExecutable(dir, name)
#        print(id)
#        print(name + " by " + info['username'])


if __name__ == "__main__":
    sys.exit(main())
