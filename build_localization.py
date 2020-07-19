import json
import os
import sys
import argparse
import codecs
import re
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-b', dest='base', type=str)
parser.add_argument('-s', dest='source', type=str)
parser.add_argument('-d', dest='destination', type=str)
parser.add_argument('--debug', dest='debug', action='store_true')
args = parser.parse_args()

base = args.base
source = args.source
destination = args.destination
debug = args.debug

stringRule = r"(\S+)\s*=\s*(\".*?\"|\S+)"
commentRule = r"^/"

def getKeyValues(file):
	keyvalues = {}

	for line in codecs.open(file, encoding='utf-8'):
		if len(line) < 8:
			continue

		if re.search(commentRule, line):
			continue

		array = re.findall(stringRule, line)

		if len(array) != 1:
			print('len(array) != 1')
			print(line)
			print(array)
			if debug == False:
				exit(1)
			continue

		keyvalue = array[0]

		if len(keyvalue) != 2:
			print('len(keyvalue) != 2')
			print(line)
			print(keyvalue)
			if debug == False:
				exit(1)
			continue

		key = keyvalue[0][1:-1]
		value = keyvalue[1][1:-1]

		if '"' + key + '"' not in line or '"' + value + '"' not in line:
			print('"' + key + '" not in line or "' + value + '" not in line')
			print(line)
			print(keyvalue)
			if debug == False:
				exit(1)
			continue

		keyvalues[key] = value

	return keyvalues

def replaceKeyValues(base, source):
	for key, value in source.items():
		base[key] = value

	return base

def writeToFile(filename, dict):
	path, file = os.path.split(filename)
	Path(path).mkdir(parents=True, exist_ok=True)
	with open(filename, mode='wt', encoding='utf-8') as file:
		for key, value in dict.items():
			file.write('"' + key + '" = "' + value + '";\n')

def checkPath(path, language):
	file = Path(path)
	if not file.is_file():
		return False

	return True

languages = ["en", "de", "es", "fr", "it", "ja", "ko", "pt-PT", "pt", "ru", "zh-Hans"]

for language in languages:
	if debug == True:
		print(language)

	filename = language + ".lproj/Localizable.strings"
	basePath = base + "/" + filename
	sourcePath = source + "/" + filename
	destinationPath = destination + "/" + filename

	if not checkPath(basePath, language) or not checkPath(sourcePath, language):
		if debug == True:
			print('language ' + language + ' not found!!')
		continue

	if debug == True:
		print('Get base KeyValues')
	baseKeyValues = getKeyValues(basePath)

	if debug == True:
		print('Get source KeyValues')
	sourceKeyValues = getKeyValues(sourcePath)

	if basePath == sourcePath:
		writeToFile(destinationPath, baseKeyValues)
	else:
		result = replaceKeyValues(baseKeyValues, sourceKeyValues)
		writeToFile(destinationPath, result)












