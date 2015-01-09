#!/usr/bin/python
import os
import shutil
import sys

IGNORE_PATTERNS = ('.myvcs','^.git')

def overriteDirectory(src, dest):

	currentDirContent = os.listdir(src)
	versionDirContent = os.listdir(dest)

	for item in currentDirContent:
		itempath = os.path.join(src,item)
		if item == '.myvcs':
			continue
		if os.path.isdir(itempath):
			shutil.rmtree(itempath)
		if(os.path.isfile(itempath)):
			os.remove(itempath)

	for item in versionDirContent:
		itempath = os.path.join(dest, item)
		localpath = os.path.join(src, item)
		
		if os.path.isdir(itempath):
			shutil.copytree(itempath, localpath)
		if(os.path.isfile(itempath)):
			shutil.copyfile(itempath, localpath)	

def copy(arguments):
	print "here"
	src = os.getcwd()
	dest = os.path.join(src, ".myvcs")
	if os.path.exists(dest):
		shutil.rmtree(dest)
	shutil.copytree(src, dest)

def snapshot(arguments):
	src = os.getcwd()
	base = os.path.join(src, '.myvcs');
	counter = 1
	while(os.path.exists(os.path.join(base, str(counter)))):
		counter += 1
	dest = os.path.join(base, str(counter))
	shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

def checkout(arguments):
	version = int(arguments[0])
	src = os.getcwd()
	base = os.path.join(src, ".myvcs")
	dest = os.path.join(base, str(version))

	if not os.path.isdir(dest):
		print "Error"
		return

	overriteDirectory(os.getcwd(), dest)
	
	

def latest(arguments):
	src = os.getcwd()
	base = os.path.join(src, '.myvcs');
	counter = 1
	while(os.path.exists(os.path.join(base, str(counter)))):
		counter += 1
	counter -= 1
	dest = os.path.join(base, str(counter))
	overriteDirectory(src, dest)


function_map = { 
    'copy': copy,
    'snapshot' : snapshot,
    'checkout' : checkout,
    'latest' : latest
}

if __name__ == "__main__":
	#print os.getcwd()
	command = sys.argv[1]
	if command not in function_map:
		print 'error : unknown command'
	else:
		function = function_map[command]
		function(sys.argv[2:])
