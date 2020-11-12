"""OpenFIDO utilities
"""

import os, csv, json, pandas, inspect

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
	return file[-1-len(ext):] == "."+ext

def read_input(file,options):
	if not file:
		raise Exception("missing input")
	elif file == "/dev/stdin" or has_extension(file,"csv"):
		return pandas.read_csv(file,**get_read_options(file,options))
	elif has_extension(file,"json"):
		return pandas.read_json(file,**get_read_options(file,options))
	else:
		raise Exception(f"{file} is not in a supported input format")

def write_output(data,file,options):
	if not file:
		raise Exception("missing output")
	elif file == "/dev/stdout" or has_extension(file,"csv"):
		data.to_csv(file,**get_write_options(file,options))
	elif has_extension(file,"json"):
		data.to_json(file,**get_write_options(file,options))
	else:
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
		elif jot is bool:
			if value == "True":
				return True
			elif value == "False":
				return False
			else:
				raise Exception(f"'{name}={value}' is not valid")
		elif jot is None and value.lower in ("none","null","nul"):
			return None
		elif jot is list and value.find(',') >= 0:
			try:
				return value.split(',')
			except:
				pass
		elif jot is dict:
			try:
				items = value.split(',')
				result = {}
				for item in items:
					specs = item.split(":")
					result[specs[0]] = specs[1]
				return result
			except:
				pass
		elif jot is csv_quote:
			try:
				return csv_quote(value)
			except:
				pass
		else:
			raise Exception(f"'{jot}' is not a valid option type")
	raise Exception(f"'{name}' is not a valid option")

def get_read_options(file,options):
	result = {}
	if has_extension(file,"json"):
		for option in options:
			tag = "--json-read-"
			if option.find(tag) == 0:
				specs = option.split("=")
				if len(specs) < 2:
					raise Exception(f"'{option}' is not valid") 
				name = specs[0][len(tag):]
				if name not in json_read_options.keys():
					raise Exception(f"'{option}' is not valid")
				value = specs[1]	
				result[name] = get_option(name,value,json_read_options[name])
	elif file == "/dev/stdin" or has_extension(file,"csv"):
		result["header"] = None
		for option in options:
			tag = "--csv-read-"
			if option.find(tag) == 0:
				specs = option.split("=")
				if len(specs) < 2:
					raise Exception(f"'{option}' is not valid") 
				name = specs[0][len(tag):]
				if name not in csv_read_options.keys():
					raise Exception(f"'{option}' is not valid")
				value = specs[1]	
				result[name] = get_option(name,value,csv_read_options[name])
	# print(f"get_read_options(file='{file}',options={options}) --> {result}")
	return result

def get_write_options(file,options):
	result = {}
	if has_extension(file,"json"):
		result["indent"] = 4
		for option in options:
			tag = "--json-write-"
			if option.find(tag) == 0:
				specs = option.split("=")
				if len(specs) < 2:
					raise Exception(f"'{option}' is not valid") 
				name = specs[0][len(tag):]
				if name not in json_write_options.keys():
					raise Exception(f"'{options}' is not valid")
				value = specs[1]	
				result[name] = get_option(name,value,json_write_options[name])
	elif file == "/dev/stdout" or has_extension(file,"csv"):
		result["header"] = False
		result["index"] = False
		for option in options:
			tag = "--csv-write-"
			if option.find(tag) == 0:
				specs = option.split("=")
				if len(specs) < 2:
					raise Exception(f"'{option}' is not valid") 
				name = specs[0][len(tag):]
				if name not in csv_write_options.keys():
					raise Exception(f"'{option}' is not valid")
				value = specs[1]	
				result[name] = get_option(name,value,csv_write_options[name])
	# print(f"get_write_options(file='{file}',options={options}) --> {result}")
	return result

json_read_options = {
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
}

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

csv_read_options = {
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
	"float_precision" : [str]
}

csv_write_options = {
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
}


