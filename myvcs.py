#!/usr/bin/python
import os
import shutil
import sys
import datetime
import filecmp
from filecmp import dircmp
import zipfile

IGNORE_PATTERNS = ('.myvcs','.git')

def compressDirectory(name,path):
	zip = zipfile.ZipFile(name, 'w')
	for root, dirs, files in os.walk(path):
		for file in files:
			zip.write(os.path.join(root, file))
	zip.close()
	return

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
	dest = os.path.join(os.getcwd(), ".myvcs")
	f = open(os.path.join(dest, "head"),"r+")
	s = f.readline()
	f.close()
	return int(s)

def updateversion(version_num):
	dest = os.path.join(os.getcwd(), ".myvcs")
	f = open(os.path.join(dest, "head"),"w")
	f.write(str(version_num))
	f.close()

def logSnap(message, parent):
	timestamp = str(datetime.datetime.now())
	version = str(getcurrentversion())
	dest = os.path.join(os.getcwd(), ".myvcs")
	f = open(os.path.join(dest, "log"), "a")
	s = " {0}# {1}|{2}|{3} \n".format(version, parent, timestamp, message)
	f.write(s)
	f.close()
	return

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
	parent = getcurrentversion()
	updateversion(counter)
	if not arguments:
		logSnap(" ", str(parent))
	elif str(arguments[0]) == '-m' and len(arguments) > 1 :
		message = ' '.join(arguments[1:])
		logSnap(message, str(parent))
	else:
		logSnap(" ", str(parent))

def checkout(arguments):
	version = int(arguments[0])
	dest = os.path.join(os.getcwd(), ".myvcs")
	dest = os.path.join(dest, str(version))

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

def log(arguments):
	dest = os.path.join(os.getcwd(), ".myvcs")
	logDictTree = {}
	try:	
		f = open(os.path.join(dest, "log"), "r")
		lines = f.readlines()
		for line in lines:
			version = line.split('#')[0]
			parent = (line.split('#')[1]).split('|')[0]
			parent = int(parent)
			version = int(version)
			logDictTree[version] = (parent, (line.split('#')[1]).split('|')[1:])
		currentVersion = getcurrentversion()
		print "Version: {0}|Time: {1}|Message: {2}".format(currentVersion, logDictTree[currentVersion][1][0], logDictTree[currentVersion][1][1])
		parent = logDictTree[currentVersion][0]
		while parent != 0:
			print "Version: {0}|Time: {1}|Message: {2}".format(parent, logDictTree[parent][1][0], logDictTree[parent][1][1])
			parent = logDictTree[parent][0]
	except:
		print "log empty"


def printDiffFiles(first, second, dcmp):
	for name in dcmp.diff_files:
		print "\033[1;31mFile {0} different in versions {1} and {2}\033[1;m".format(name, first, second)
	for name in dcmp.left_only:
		print "\033[1;33mFile/dir {0} only in version {1}\033[1;m".format(name, first)
	for name in dcmp.right_only:
		print "\033[1;34mFile/dir {0} only in version {1}\033[1;m".format(name, second)	
	#for name in dcmp.same_files:
	#	print "\033[1;30mFile {0} identical in versions {1} and {2}\033[1;m".format(name, first, second)
	for sub_dir in dcmp.subdirs.values():
		printDiffFiles(first, second, sub_dir)

def diff(arguments):
	if len(arguments)<2:
		print 'invalid input'
		return
	else:
		first = arguments[0]
		second = arguments[1]
		dest = os.path.join(os.getcwd(), ".myvcs")
		destfirst = os.path.join(dest, str(first))
		destsecond = os.path.join(dest, str(second))
		dcmp = dircmp(destfirst, destsecond)
		#dcmp.report()
		#dcmp.report_partial_closure()
		printDiffFiles(first, second, dcmp)

def status(arguments = None):
	first = getcurrentversion()
	destfirst = os.path.join(os.getcwd(), ".myvcs")
	destfirst = os.path.join(destfirst, str(first))
	destsecond = os.getcwd()
	print 'comparing: ' + destfirst  + ' ' + destsecond
	dcmp = dircmp(destfirst, destsecond, ignore = ['.git', '.myvcs'])
	printDiffFiles(first, 'current', dcmp)


def help(arguments = None):
	print 'hello'


function_map = { 
	'init' : init,
	'copy': copy,
	'snapshot' : snapshot,
	'checkout' : checkout,
	'latest' : latest,
	'current' : current,
	'log' : log,
	'diff' : diff,
	'help' : help,
	'status': status
}

if __name__ == "__main__":
	#print os.getcwd()
	command = sys.argv[1]
	if command not in function_map:
		print 'error : unknown command'
	else:
		function = function_map[command]
		function(sys.argv[2:])
