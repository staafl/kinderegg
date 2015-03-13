# parse_shadertoy_json.py

from __future__ import print_function
import json
import os
from PIL import Image

jsonfile = "ldXXDj.txt"
#jsonfile = "4lX3RB.txt"
j = json.loads(open(jsonfile).read())

#print(json.dumps(j,indent=1))
info = j['Shader']['info']
print("Title: " + info['name'])
print("Author: " + info['username'])
print("Description: " + info['description'])
print("Tags: " + ', '.join(info['tags']))

renderpass = j['Shader']['renderpass']
for r in renderpass:
	print(r['type'])
	# Pull out textures
	for t in r['inputs']:
		texfile = os.path.basename(t['src'])
		print("    tex" + str(t['channel']) + ": " + texfile, end='')
		img = Image.open(texfile)
		px = img.load()
		print("    size: ", img.size, end='')
		for i in range(5):
			print(" " + str(px[i,0]), end='')
		print("")
		# TODO: Save to header
	print("    code: " + str(len(r['code'])) + " bytes")
	#print(r['code'])
	# TODO: Save to header