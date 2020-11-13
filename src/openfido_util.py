"""OpenFIDO utilities
"""

import os, csv, json, pandas, inspect

def csv_quote(c):
	"""Special data type for CSV quoting"""
	opts = {
		"all" : csv.QUOTE_ALL,
		"minimal" : csv.QUOTE_MINIMAL,
		"nonnumeric" : csv.QUOTE_NONNUMERIC,
		"none" : csv.QUOTE_NONE,
		}
	if c.lower() in opts.keys():
		return opts[c.lower()]
	else:
		raise Exception(f"'{c}' is not a valid CSV quoting option")

#
# This defines all the I/O formats supported by OpenFIDO using dataframe
#
format_options = {
	"/dev/stdin" : "csv", # specify the default file type for stdin
	"/dev/stdout" : "csv", # specify the default file type for stdout
	"csv" : { # CSV file type information
		"read" : { # read options data types
			"sep" : [str],
			"delimiter" : [str],
			"header" : [list,str,bool],
			"names" : [list],
			"index_col" : [None,int,bool,str],
			"usecols" : [list],
			"prefix" : [bool],
			"mangle_dup_cols" : [bool],
			"dtype" : [dict,str],
			"engine" : [str],
			"converters" : [dict],
			"true_values" : [list],
			"false_values" : [list],
			"skipinitialspaces" : [bool],
			"skiprows" : [int,list],
			"nrows" : [int],
			"na_values" : [float,str,list,dict],
			"keep_default_na" : [bool],
			"na_filter" : [bool],
			"verbose" : [bool],
			"skip_blank_lines" : [bool],
			"parse_dates" : [bool,list,dict],
			"infer_datetime_format" : [bool],
			"keep_date_col" : [bool],
			# "date_parser" : [function],
			"dayfirst" : [bool],
			"cache_dates" : [bool],
			"compression" : [str],
			"thousands" : [str],
			"decimal" : [str],
			"lineterminator" : [str],
			"quoting" : [csv_quote],
			"quotechar" : [str],
			"doublequote" : [bool],
			"escapechar" : [None,str],
			"comment" : [str],
			"dialect" : [str],
			"error_bad_lines" : [bool],
			"warn_bad_lines" : [bool],
			"delim_whitespaces" : [bool],
			"low_memory" : [bool],
			"memory_map" : [bool],
			"float_precision" : [str],
		},
		"write" : { # write option data types
			"sep" : [str],
			"na_rep" : [str],
			"float_format" : [None,str],
			"header" : [bool,list,str],
			"index" : [bool],
			"encoding" : [str],
			"compression" : [str],
			"quoting" : [csv_quote],
			"quotechar" : [str],
			"line_terminator" : [str],
			"date_format" : [None,str],
			"doublequote" : [bool],
			"escapechar" : [None,str],
			"decimal" : [str],
		},
		"call" : { # read/write callables
			"read" : lambda file,options: pandas.read_csv(file,**options),
			"write" : lambda data,file,options: data.to_csv(file,**options),
		},
		"default" : { # default options for read and write calls
			"read" : {
				"header" : None,
			},
			"write" : {
				"header" : False,
				"index" : False,
			},
		},
	},
	"json" : { # JSON file type information
		"read" : { # read options data types
			"orient" : [str],
			"typ" : [str],
			"dtype" : [dict,bool],
			"convert_axes" : [None,bool],
			"convert_dates" : [list,bool],
			"keep_default_dates" : [bool],
			"precise_float" : [bool],
			"date_unit" : [None,str],
			"encoding" : [str],
			"lines" : [bool],
			"compression" : [None,str],
		},
		"write" : { # write options data types
			"orient" : [str],
			"data_format" : [None,str],
			"double_precision" : [int],
			"force_ascii" : [bool],
			"date_unit" : [str],
			"lines" : [bool],
			"compression" : [None,str],
			"index" : [bool],
			"indent" : [int],
			# TODO
		},
		"call" : { # read/write calls
			"read" : lambda file,options: pandas.read_json(file,**options),
			"write" : lambda data,file,options: data.to_json(file,**options),
		},
		"default" : { # read/read default options
			"read" : {
			},
			"write" : {
				"indent" : 1,
				"date_unit" : "s",
			},
		},
	}
}

def get_help(function):
	"""Obtain the help text for an OpenFIDO function"""
	import importlib.util as lib
	spec = lib.spec_from_file_location(function.replace("/__init__.py",""),function)
	mod = lib.module_from_spec(spec)
	spec.loader.exec_module(mod)
	return mod.__doc__

def get_cardinalities(function):
	"""Get I/O cardinalities of an openfido function
	Valid cardinalities:

		None   No I/O file expected
		0      Any number is allowed
		N      Exactly N are required
		-N     At least one and up to N are allowed
	"""
	specs = {}
	with open(function.replace("__init__.py","openfido.json"),"r") as fh:
		specs = json.load(fh)
	if "inputs" not in specs.keys() or "outputs" not in specs.keys():
		raise Exception(f"function does not have cardinalities specified in openfido.json")
	return {"inputs":specs["inputs"], "outputs":specs["outputs"]}

def setup_io(inputs,outputs,function=None):
	"""Setup the I/O for an OpenFIDO function

	This should always be called first in a function.
	"""
	if not function:
		frame = inspect.stack()[1]
		function = frame[0].f_code.co_filename
	cards = get_cardinalities(function)
	specs = {"inputs":inputs,"outputs":outputs}
	for key,card in cards.items():
		spec = specs[key]
		if card == None: # nothing expect expected
			if spec:
				raise Exception("unexpected input(s)")
		elif card > 0: # fixed number
			if len(spec) != card:
				raise Exception(f"incorrect number of {key}s (expected {card}, got {len(spec)})")
			break
		elif card < 0: # minimum number
			if len(inputs) < card:
				raise Exception("missing input(s)")
			break
		elif card != 0: # any number
			raise Exception(f"invalid input cardinality '{card}'")

def has_extension(file,ext):
	"""Verifies that the file has the specified extension"""
	return file[-1-len(ext):] == "."+ext

def read_input(file,options):
	"""Read the input file using the file format's read options"""
	if not file:
		raise Exception("missing input")
	for ftype in format_options.keys():
		if file == ftype or has_extension(file,ftype):
			if file == ftype: ftype = format_options[file]
			options = get_read_options(ftype,options)
			return format_options[ftype]["call"]["read"](file,options)
	raise Exception(f"{file} is not in a supported input format")

def write_output(data,file,options):
	"""Write the output file using the file format's write options"""
	if not file:
		raise Exception("missing output")
	for ftype in format_options.keys():
		if file == ftype or has_extension(file,ftype):
			if file == ftype: ftype = format_options[file]
			options = get_write_options(ftype,options)
			format_options[ftype]["call"]["write"](data,file,options)
			return None
	raise Exception(f"{file} is not in a supported input format")

def hold(df,order=0,axis=0,inplace=True):
	"""Perform hold on dataframe

	Parameters:
		df (dataframe)   Data on which to perform hold
		order (int)      Order of hold (default 0)
		axis (int)       Axis over which to hold (default 0=rows, 1=columns)

	A hold fills is missing values based on previous values.  A zero-order hold
	simply copies the previous value. A first-order hold extrapolates from the
	slope of the previous two values.

	The axis determines which was the series are applied.  Axis 0 means the series
	are taken in row-wise, meaning the each column is an independent series.  Axis 1
	means the series are taken column-wise, meaning that each row is an independent
	series.

	Note that hold cannot be applied in cases where needed initial values are null.
	"""

	# make a copy if not inplace
	if not inplace:
		df = df.copy(deep=True)

	# use transpose to handle column-wise series
	if axis==1: 
		return hold(df.transpose(),order=order,axis=0).transpose()

	# iterate over series containing nulls
	for col in df.columns[df.isnull().any()]:
		d = df[col]

		# refuse to apply hold if initial value(s) are null
		if np.isnan(d.iloc[0:order].any()):
			raise Exception(f"unable to hold on series '{col}' with initial NaN value")

		# find index of null values
		index = d.index[d.apply(np.isnan)]

		# iterate over null values copying previous values
		if order == 0:
			for i in index:
				d.iloc[index] = d.iloc[i-1]
		elif order == 1:
			for i in index:
				d.iloc[index] = 2.0*d.iloc[i-1] - d.iloc[i-2]
		else:
			raise Exception("order={order} is not valid")
	return df
	
def get_option(name,value,types):
	"""CSV and JSON option handler

	This function convert a string to a valid kwarg option.

	Example:
		my_options["orient"] = get_option("orient","index",json_read_options)
	"""
	for jot in types:
		if jot is str:
			return value
		if jot in (int,float):
			try:
				return value
			except:
				pass
		if jot is bool:
			if value.lower() == "true":
				return True
			elif value.lower() == "false":
				return False
			else:
				raise Exception(f"'{name}={value}' is not valid")
		if jot is None and value.lower in ("none","null","nul"):
			return None
		if jot is list and value.find(',') >= 0:
			try:
				return value.split(',')
			except:
				pass
		if jot is dict:
			try:
				items = value.split(',')
				result = {}
				for item in items:
					specs = item.split(":")
					result[specs[0]] = specs[1]
				return result
			except:
				pass
		if jot is csv_quote:
			try:
				return csv_quote(value)
			except:
				pass
	raise Exception(f"'{name}={value}' is not a valid option for type '{type}'")

def get_read_options(ftype,options):
	"""Get the file type's read options"""
	result = format_options[ftype]["default"]["read"]
	for option in options:
		tag = f"--{ftype}-read-"
		if option.find(tag) == 0:
			specs = option.split("=")
			if len(specs) < 2:
				raise Exception(f"'{option}' is not valid") 
			name = specs[0][len(tag):]
			if name not in format_options[ftype]["read"].keys():
				raise Exception(f"'{option}' is not valid")
			value = specs[1]	
			result[name] = get_option(name,value,format_options[ftype]["read"][name])
	return result

def get_write_options(ftype,options):
	"""Get the file type's write options"""
	result = format_options[ftype]["default"]["write"]
	for option in options:
		tag = f"--{ftype}-write-"
		if option.find(tag) == 0:
			specs = option.split("=")
			if len(specs) < 2:
				raise Exception(f"'{option}' is not valid") 
			name = specs[0][len(tag):]
			if name not in format_options[ftype]["write"].keys():
				raise Exception(f"'{options}' is not valid")
			value = specs[1]	
			result[name] = get_option(name,value,format_options[ftype]["write"][name])
	return result
