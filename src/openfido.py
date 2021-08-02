"""OpenFIDO API

Syntax: openfido [OPTIONS] FUNCTION [...]

Options:
	-h|--help      output this help
	-q|--quiet     enables less output
	-v|--verbose   enables more output
	--version      output version number

Authentication methods:

	./github_auth.py file:
		token=<your-token>

	GITHUB_TOKEN environment variable:
		% export GITHUB_TOKEN=<your-token>

	$HOME/.github/access-token file:
		<your-token>
"""

__version__ = "0.0.1"

import os, sys, glob, pydoc, warnings, subprocess, signal
import requests, shutil, importlib, pandas, docker
from pygit2 import Repository

sys.path.append(".")
sys.path.append(os.getenv("HOME")+"/.openfido")
sys.path.append("/usr/local/bin")

try:
	from openfido_config import *
except:
	pass

# get authorization token
try:
	import github_auth as authentication_token
except:
	# template class using environment variable
	class authentication_token:
		token = os.getenv('GITHUB_TOKEN',None)
	if not authentication_token.token:
		# try reading file $HOME/.github/access-token
		try:
			token_file = f"{os.getenv('HOME','')}/.github/access-token"
			_fh = open(token_file,"r")
			authentication_token.token = _fh.read()
		except Exception as exc:
			pass
	pass

# default streams
def error(msg,exit=None):
	print(msg,file=sys.stderr)
	if exit:
		sys.exit(exit)
def silent(msg,exit=None):
	if exit:
		sys.exit(exit)
default_streams = {"output":silent, "warning":warnings.warn, "error":error, "verbose":silent, "quiet":silent}
command_streams = {"output":print, "warning":warnings.warn, "error":error, "verbose":silent, "quiet":silent}

#
# FUNCTION VALIDATE
#
callable_functions = ["config","help","index","info","install","show","update","run","server","pipeline","workflow"]
def is_valid(function):
	return function in callable_functions

#
# CONFIG FUNCTION
#
def config(options=[], config=[], stream=default_streams):
	"""Syntax: openfido config [show|get VARIABLE|set VARIABLE VALUE]

	The `config` function manages the openfido configuration file.  There are three possible locations
	for the file `openfido_config.py`, and they are used in the following order of precedence:
		1. `./openfido_config.py`
		2. `$HOME/.openfido/openfido_config.py`
		3. `/usr/local/share/openfido_config.py`
	"""
	if len(options) == 0:
		options = ["show"]
	if options[0] == "show" and len(options) == 1:
		result = {
			"verbose" : config.verbose,
			"quiet" : config.quiet,
			"orgname" : config.orgname,
			"branch" : config.branch,
			"cache" : config.cache,
			"apiurl" : config.apiurl,
			"rawurl" : config.rawurl,
			"giturl" : config.giturl,
			"traceback_file" : "openfido.err"		
		}
		for key,value in result.items():
			if type(value) is str:
				stream["output"](f"{key}=\"{value}\"")
			else:
				stream["output"](f"{key}={value}")
		return result
	elif options[0] == "get" and len(options) == 2:
		stream["output"](getattr(config,options[1]))
	elif options[0] == "set" and len(options) in (3,4):
		result = {
			"verbose" : config.verbose,
			"quiet" : config.quiet,
			"orgname" : config.orgname,
			"branch" : config.branch,
			"cache" : config.cache,
			"apiurl" : config.apiurl,
			"rawurl" : config.rawurl,
			"giturl" : config.giturl,	
			"traceback_file" : config.traceback_file
		}
		#TODO
		if options[1] in ["-l","--local"]:
			cfgfile = "./openfido_config.py"
			options = options[1:]
		else:
			cfgfile = os.getenv("HOME")+"/.openfido/openfido_config.py"
		if len(options) < 3:
			raise Exception(f"missing value")
		if not options[1] in result.keys():
			raise Exception(f"'{options[1]}' is not a valid configuration variables")
		for key, value in result.items():
			if options[1] == key:
				if type(value) is str:
					result[key] = options[2]
				elif type(value) == type(eval(options[2])):
					result[key] = eval(options[2])
				else:
					raise Exception(f"'{options[2]}' is not a valid type for variable '{key}'")
		with open(cfgfile,"w") as fh:
			for key,value in result.items():
				if type(value) is str:
					print(f"{key}=\"{value}\"",file=fh)
				else:
					print(f"{key}={value}",file=fh)
		return result
	else:
		raise Exception(f"'options={options}' is not valid")
#
# HELP FUNCTION
#
def help(options=[], config=[], stream=default_streams):
	"""Syntax: openfido help [COMMAND]

	The `help` function displays help information using the python help facility.
	"""
	mod = sys.modules[__name__]
	if not options:
		stream["output"](mod.__doc__)
		stream["output"]("Functions:")
		for entry in callable_functions:
			call = getattr(mod,entry)
			text = pydoc.render_doc(call,renderer=pydoc.plaintext).split("\n")[3].strip()
			stream["output"](f"\t{text.replace('Syntax: ','')}")
		stream["output"]("")
	elif not type(options) is list:
		raise Exception("help options must be a list")
	elif len(options) > 1:
		raise Exception("help is only available on one command at a time")
	elif is_valid(options[0]):
		call = getattr(mod,options[0])
		text = pydoc.render_doc(call,renderer=pydoc.plaintext).split("\n")[3:]
		for line in text:
			stream["output"](line.strip())
		return text
	else:
		raise Exception(f"help on '{options[0]}' not available or command not found")

#
# LIST FUNCTION
#
def index(options=[], config=[], stream=default_streams):
	"""Syntax: openfido index [PATTERN]

	The `index` function lists the contents of the public openfido product library.
	"""
	headers = {}
	if authentication_token.token:
		headers = {"Authorization": f"token {authentication_token.token.strip()}"}
	else:
		stream["verbose"]("using unauthenticated access")
	apiurl = config.apiurl
	orgname = config.orgname
	branch = config.branch
	rawurl = config.rawurl
	url = f"{apiurl}/orgs/{orgname}/repos"
	data = requests.get(url,headers=headers,params={}).json()
	if not data:
		raise Exception(f"unable to reach repo list for org '{orgname}' at {apiurl}")
	elif not type(data) is list:
		raise Exception(f"API error for org '{orgname}' at {url}: response ({type(data)}) = {data}")
	if authentication_token.token:
		stream["verbose"]("access token ok")
	repos = dict(zip(list(map(lambda r:r['name'],data)),data))
	if len(options) > 0:
		result = []
		for option in options:
			for repo in list(repos.keys()):
				if repo in result:
					continue
				pos = repo.find(option[option[0]=='^':])
				if pos < 0:
					continue
				url = f"{rawurl}/{orgname}/{repo}/{branch}/openfido.json"
				try:
					manifest = requests.get(url).json()
					if manifest["application"] == "openfido" and ( option[0] != '^' or pos == 0 ):
						result.append(repo)
				except:
					pass
	else:
		result = []
		for repo in list(repos.keys()):
			url = f"{rawurl}/{orgname}/{repo}/{branch}/openfido.json"
			try:
				manifest = requests.get(url).json()
				if manifest["application"] == "openfido":
					result.append(repo)
			except:
				pass

	for name in sorted(result):
		stream["output"](name)
	return result

#
# INFO FUNCTION
#
def info(options=[], config=[], stream=default_streams):
	"""Syntax: openfido info PRODUCT

	The `info` function displays information about a public openfido product.
	"""
	if len(options) == 0:
		raise Exception("product name is required")
	elif len(options) > 1:
		raise Exception("only one product name is allowed")
	name = options[0]
	cache = config.cache
	path = f"{cache}/{name}/__init__.py"
	print("path: ", path)
	if os.path.exists(path):
		stream["verbose"](f"examining {path}")
		spec = importlib.util.spec_from_file_location(name,path)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		text = pydoc.render_doc(module,renderer=pydoc.plaintext).split("\n")
		for line in text:
			stream["output"](line)
		return text


#
# INSTALL FUNCTION
#
def install(options=[], config=[], stream=default_streams):
	"""Syntax: openfido [OPTIONS] install [-d|--dryrun] PRODUCT ...

	The `install` command installs one or more public openfido products on the local system.
	"""
	headers = {}
	if authentication_token.token:
		headers = {"Authorization": f"token {authentication_token.token.strip()}"}
	else:
		stream["verbose"]("using unauthenticated access")
	apiurl = config.apiurl
	cache = config.cache
	orgname = config.orgname
	branch = config.branch
	rawurl = config.rawurl
	giturl = config.giturl
	url = f"{apiurl}/orgs/{orgname}/repos"
	data = requests.get(url,headers=headers,params={}).json()
	if not data:
		raise Exception(f"unable to reach repo list for org '{orgname}' at {apiurl}")
	elif not type(data) is list:
		raise Exception(f"API error for org '{orgname}' at {url}: response ({type(data)}) = {data}")
	if authentication_token.token:
		stream["verbose"]("access token ok")
	repos = dict(zip(list(map(lambda r:r['name'],data)),data))
	dryrun = os.system
	failed = []
	done = []
	for option in options:
		if option[0] == '-':
			if option in ['-d','--dry-run']:
				dryrun = stream["output"]
			else:
				raise Exception(f"option '{option}' is invalid")
	for name in options:
		if name[0] == '-':
			continue
		elif not name in repos.keys():
			stream["error"](f"'{name}' not found in openfido repository")
			failed.append(name)
		else:
			repo = repos[name]
			url = f"{rawurl}/{orgname}/{name}/{branch}/openfido.json"
			data = requests.get(url)
			try:
				manifest = data.json()
			except:
				manifest = None
			if not manifest:
				stream["error"](f"manifest read failed: url={url}, status_code={data.status_code}, headers={data.headers}, body=[{data.text}]") 
			if not "application" in manifest.keys() or manifest["application"] != "openfido":
				stream["error"](f"tool '{name}' is not an openfido application")
				failed.append(name)
			elif not "valid" in manifest.keys() or not manifest["valid"]:
				stream["warning"](f"tool '{name}' is not valid")
				failed.append(name)
			else:
				if not "version" in manifest.keys():
					stream["warning"](f"tool '{name}' has no version")
				if not "tooltype" in manifest.keys() or manifest["tooltype"] not in ("pipeline","workflow"):
					stream["warning"](f"tool '{name}' type is missing or invalid")
				stream["verbose"](f"{name}: {manifest['tooltype']} version {manifest['version']} is valid")
				source = f"{giturl}/{orgname}/{name}"
				target = f"{cache}/{name}"
				if os.path.exists(target):
					repo = Repository(target)
					existing_branch = repo.head.name.split("/")[-1]
					if branch == existing_branch:
						pass
					else:
						stream["warning"](f"'{name}' is already installed in branch '{existing_branch}'. Repo branch will be switched to '{branch}'")
						remove([name],config,stream)
						if dryrun(f"git clone -q {source} {target} -b {branch} --depth 1") != 0:
							failed.append(name)
						else:
							stream["verbose"](f"'{name}' cloned ok")
							done.append(name)
					done.append(name)
				elif os.system(f"git clone -q {source} {target} -b {branch} --depth 1") != 0:
					stream["error"](f"unable to clone '{name}' into openfido cache '{cache}'")
					failed.append(name)
				else:
					stream["verbose"](f"'{name}' cloned ok")
					done.append(name)
				# TODO: implement installation
				# done.append(name)
	return {"ok":len(done), "errors":len(failed), "done":done, "failed": failed}

#
# SHOW FUNCTION
#
def show(options=[], config=[], stream=default_streams):
	"""Syntax: openfido [OPTIONS] show PATTERN ...
	
	The `show` function prints out the products with names that match PATTERN.
	"""
	if not options:
		options = ["*"]
	cache = config.cache
	for pattern in options:
		for path in glob.iglob(f"{cache}/{pattern}"):
			name = path.split("/")[-1]
			if not os.path.exists(f"{path}/openfido.json"):
				raise Exception(f"'{cache}/{name}' not found")
			sys.path.append(f"{cache}/{name}")
			if not os.path.exists(f"{path}/__init__.py"):
				raise Exception(f"'{path}/__init__.py' not found")
			spec = importlib.util.spec_from_file_location(name,f"{path}/__init__.py")
			module = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(module)
			if not hasattr(module,"main") or not callable(module.main):
				raise Exception(f"'{name}/__init__.py' missing callable main")
			stream["output"](name)

#
# UPDATE FUNCTION
#
def update(options=[], config=[], stream=default_streams):
	"""Syntax: openfido [OPTIONS] update [-d|--dryrun] PRODUCT ...

	The `update` function brings one or more products on the local system up to date with the 
	most recent public versions.
	"""
	dryrun = os.system
	cache = config.cache
	done = []
	failed = []
	for option in options:
		if option[0] == '-':
			if option in ['-d','--dry-run']:
				dryrun = stream["output"]
			else:
				raise Exception(f"option '{option}' is invalid")
	for name in options:
		if name[0] != '-':
			if os.path.exists(f"{cache}/{name}"):
				stream["verbose"](f"updating {cache}/{name}")
				dryrun(f"cd {cache}/{name} && git pull")
				done.append(name)
			else:
				stream["warning"](f"'{name}' not found")
				failed.append(name)
	return {"ok":len(done), "errors":len(failed), "done":done, "failed": failed}

#
# REMOVE FUNCTION
#
def remove(options=[], config=[], stream=default_streams):
	"""Syntax: openfido [OPTIONS] remove [-d|--dryrun] PRODUCT ...

	The `remove` function removes one or more products from the local system.
	"""
	dryrun = os.system
	cache = config.cache
	done = []
	failed = []
	for option in options:
		if option[0] == '-':
			if option in ['-d','--dry-run']:
				dryrun = stream["output"]
			else:
				raise Exception(f"option '{option}' is invalid")
	for name in options:
		if name[0] != '-':
			if cache[0] != '/':
				stream["error"](f"unable to remove a folder without an absolute path")
				failed.append(name)
			elif os.path.exists(f"{cache}/{name}/.git"):
				stream["verbose"](f"removing {cache}/{name}")
				dryrun(f"rm -rf '{cache}/{name}'")
				done.append(name)
			else:
				stream["warning"](f"'{name}' not found or not an openfido product")
				failed.append(name)
	return {"ok":len(done), "errors":len(failed), "done":done, "failed": failed}

#
# RUN FUNCTION
#
def run(options=[], config=[], stream=command_streams):
	"""Syntax: openfido [OPTIONS] run PRODUCT [OPTIONS ...] INPUTFILES [OUTPUTFILES]

	The `run` function runs an openfido product on the local system.
	"""
	if not options:
		raise Exception("missing package name")
	name = options[0]
	cache = config.cache
	branch = config.branch
	path = f"{cache}/{name}"
	if not os.path.exists(f"{path}/openfido.json"):
		raise Exception(f"'{cache}/{name}' not found")
	if not install([name],config,stream)["ok"]:
		raise Exception(f"unable to install '{name}' in branch '{branch}' into openfido cache '{cache}'")
	sys.path.append(f"{cache}/{name}")
	if not os.path.exists(f"{path}/__init__.py"):
		raise Exception(f"'{path}/__init__.py' not found")
	spec = importlib.util.spec_from_file_location(name,f"{path}/__init__.py")
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	if hasattr(module,"openfido") and callable(module.openfido):
		return module.openfido(options,stream)
	if not hasattr(module,"main") or not callable(module.main):
		raise Exception(f"'{name}/__init__.py' missing callable main")
	inputs = []
	outputs = []
	flags = []
	for n in range(1,len(options)):
		if options[n][0] == '-' or "=" in options[n]: 
			flags.append(options[n])
		elif not inputs:
			inputs = options[n].split(',')
		elif not outputs:
			outputs = options[n].split(',')
		else:
			raise Exception(f"option {options[n]} unexpected")
	if not inputs:
		inputs = ["/dev/stdin"]
	if not outputs:
		outputs = ["/dev/stdout"]
	# inputs will be the name of input file
	# outputs will be the name of output files
	return module.main(inputs=inputs,outputs=outputs,options=flags)

#
# SERVER FUNCTION
#
def server(options=[], config=[], stream=command_streams):
	"""Syntax: openfido [OPTIONS] server [start|stop|restart|status|update|open]

	The `server` function controls the local openfido server running on docker.
	"""
	if len(options) == 0:
		raise Exception("missing server command")
	elif len(options) > 1:
		raise Exception("too many server commands")
	else:
		subprocess.run(["/usr/local/bin/openfido-server",options[0]])

#
# PIPELINE FUNCTION
#
pipeline_filename = ".pipelines.csv"
def readlocal_pipelines(pipeline_csv=pipeline_filename):
	try:
		data = pandas.read_csv(pipeline_csv,dtype=str)
	except:
		data = pandas.DataFrame()
	return data

def addlocal_pipeline(data,row):
	item = pandas.DataFrame(row)
	if len(data) == 0:
		return item
	else:
		return pandas.concat([data.set_index(['name']),item.set_index(['name'])],verify_integrity=True).reset_index()

def writelocal_pipelines(data,pipeline_csv=pipeline_filename):
	data.to_csv(pipeline_csv,index=False,columns=data.columns)

def runlocal_pipepline(name,image_name,github,branch,entry,inputfolder,outputfolder):
	client = docker.from_env()
	try:
		client.get(image_name)
	except:
		client.images.pull(image_name)

	container = client.containers.run(image_name,
		command = f"sh -c 'git clone {github} -b {branch} --depth 1 /tmp/openfido ; cd /tmp/openfido ; export OPENFIDO_INPUT=/tmp/input ; export OPENFIDO_OUTPUT=/tmp/output ; source /tmp/openfido/{entry} 0</dev/null 1>/tmp/output/stdout 2>/tmp/output/stderr' ",
		auto_remove = True,
		volumes = {
			inputfolder : {"bind" : "/tmp/input", "mode" : "ro" },
			outputfolder : {"bind" : "/tmp/output", "mode" : "rw" },
		})

def pipeline(options=[], config=[], stream=command_streams):
	"""Syntax: openfido [OPTIONS] pipeline COMMAND [OPTIONS]

	The `pipeline` function is used to create and start pipeline operations.

	COMMAND:

		create [-l|--local] NAME DOCKER GITHUB BRANCH ENTRY [DESCRIPTION]
		start [-l|--local] NAME INPUTFOLDER OUTPUTFOLDER 
		delete [-l|--local] NAME
		list [-l|--local]
	"""
	if len(options) < 1:
		raise Exception("missing pipeline command")
	command = options[0]
	local = False
	args = []
	for option in options[1:]:
		if option[0] == '-':
			if option in ["-l","--local"]:
				local = True
			else:
				stream["error"](f"option '{option}' is not valid")
				return
		else:
			args.append(option)
	if command == "create":
		if len(args) < 5:
			raise Exception(f"missing one or more pipeline create arguments (args={args})")
		if len(args) > 6:
			raise Exception(f"too many pipeline create arguments (args={args})")
		pipeline = args[0]
		docker = args[1]
		github = args[2]
		branch = args[3]
		entry = args[4]
		if len(args) > 5:
			description = args[5]
		else:
			description = ""
		if local:
			data = readlocal_pipelines()
			data = addlocal_pipeline(data,{
				'name':[pipeline],
				'docker':[docker],
				'github':[github],
				'branch':[branch],
				'entry':[entry],
				'description':[description],
				})
			writelocal_pipelines(data)
		else:
			raise Exception(f"remote pipeline create not implemented yet (args={args})")
	elif command == "start":
		if len(args) < 3:
			raise Exception(f"missing one or more pipeline start arguments (args={args})")
		if len(args) > 3:
			raise Exception(f"too many pipeline start arguments (args={args})")
		pipeline = args[0]
		inputfolder = args[1]
		outputfolder = args[2]
		if local:
			data = readlocal_pipelines().set_index("name")
			spec = data.loc[pipeline]
			runlocal_pipepline(pipeline,spec["docker"],spec["github"],spec["branch"],spec["entry"],inputfolder,outputfolder)
		else:
			raise Exception(f"remote pipeline start not implemented yet (args={args})")
	elif command == "delete":
		if len(args) < 1:
			raise Exception(f"missing pipeline delete argument (args={args})")
		pipeline = args[0]
		if local:
			data = readlocal_pipelines().set_index("name")
			data = data.drop(pipeline)
			writelocal_pipelines(data.reset_index())
		else:
			raise Exception(f"remote pipeline delete not implemented yet (args={args})")
	elif command == "list":
		if local:
			data = readlocal_pipelines().set_index("name")
			for item in data.index:
				print(item)
		else:
			raise Exception(f"remote pipeline delete not implemented yet (args={args})")
	else:
		raise Exception(f"invalid pipeline command (command='{command}')")


#
# WORKFLOW FUNCTION
#
def workflow(options=[], config=[], stream=command_streams):
	"""Syntax: openfido [OPTIONS] workflow COMMAND [OPTIONS]

	The `pipeline` function is used to create and start pipeline operations.

	COMMAND:
	
		create [-l|--local] SPECFILE
		start  [-l|--local] NAME INPUTFOLDER OUTPUTFOLDER 
	"""
	raise Exception("workflow CLI not implemented yet")

