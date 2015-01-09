#!/usr/bin/python
import os
import shutil
import sys

IGNORE_PATTERNS = ('.myvcs','^.git')

def overriteDirectory(src, dest):

	if not os.path.isdir(dest):
		print "Error"
		return

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

def getcurrentversion():
	src = os.getcwd()
	dest = os.path.join(os.getcwd(), ".myvcs")
	f = open(os.path.join(dest, "head"),"r+")
	s = f.readline()
	f.close()
	return int(s)

def updateversion(version_num):
	src = os.getcwd()
	dest = os.path.join(os.getcwd(), ".myvcs")
	f = open(os.path.join(dest, "head"),"w")
	f.write(str(version_num))
	f.close()


def copy(arguments):
	init = str(0)
	src = os.getcwd()
	dest = os.path.join(src, ".myvcs")
	if os.path.exists(dest):
		shutil.rmtree(dest)
	shutil.copytree(src, dest)
	f = open(os.path.join(dest, "head"),"w")
	f.write(init)
	f.close()

def snapshot(arguments):
	src = os.getcwd()
	base = os.path.join(src, '.myvcs');
	counter = 1
	while(os.path.exists(os.path.join(base, str(counter)))):
		counter += 1
	dest = os.path.join(base, str(counter))
	shutil.copytree(src, dest, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))
	updateversion(counter)

def checkout(arguments):
	version = int(arguments[0])
	src = os.getcwd()
	base = os.path.join(src, ".myvcs")
	dest = os.path.join(base, str(version))

	if not os.path.isdir(dest):
		print "Error"
		return

	overriteDirectory(os.getcwd(), dest)
	updateversion(version)
	

def latest(arguments):
	src = os.getcwd()
	base = os.path.join(src, '.myvcs');
	counter = 1
	while(os.path.exists(os.path.join(base, str(counter)))):
		counter += 1
	counter -= 1
	dest = os.path.join(base, str(counter))
	overriteDirectory(src, dest)
	updateversion(counter)

def init(arguments=None):
	init = str(0)
	dest = os.path.join(os.getcwd(), ".myvcs")
	if os.path.exists(dest):
		shutil.rmtree(dest)
	os.mkdir(dest)
	f = open(os.path.join(dest, "head"),"w")
	f.write(init)
	f.close()

def current(arguments):
	print getcurrentversion()

def log():
	return

function_map = { 
	'init' : init,
    'copy': copy,
    'snapshot' : snapshot,
    'checkout' : checkout,
    'latest' : latest,
    'current' : current,
    'log' : log
}

if __name__ == "__main__":
	#print os.getcwd()
	command = sys.argv[1]
	if command not in function_map:
		print 'error : unknown command'
	else:
		function = function_map[command]
		function(sys.argv[2:])
