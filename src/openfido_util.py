"""OpenFIDO utilities
"""

import os, csv

def csv_quote(c):
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

def get_option(name,value,types):
	for jot in types:
		if jot is str:
			return value
		elif jot is bool:
			if value == "True":
				return True
			elif value == "False":
				return False
			else:
				raise Exception(f"'{name}={value}' is not valie")
		elif jot is None:
			return None
		elif jot is list:
			return value.split(',')
		elif jot is dict:
			items = value.split(',')
			result = {}
			for item in items:
				specs = item.split(":")
				result[specs[0]] = specs[1]
			return result
		elif jot is csv_quote:
			return csv_quote(value)
		else:
			raise Exception(f"'{jot}' is not a valid option type")
	raise Exception(f"'{name}' is not a valid option")

json_options = {
	"orient" : "columns",
	"typ" : "frame",
	"dtype" : None,
	"convert_axes" : True,
	"convert_dates" : True,
	"keep_default_dates" : True,
	"precise_float" : False,
	"date_unit" : None,
	"encoding" : "utf-8",
	"lines" : False,
	"compression" : "infer",
}

json_option_types = {
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

csv_options = {
	"sep" : ",",
	"na_rep" : "",
	"float_format" : None,
	"header" : False,
	"index" : False,
	"encoding" : "utf-8",
	"compression" : "infer",
	"quoting" : "minimal",
	"quotechar" : '"',
	"line_terminator" : os.linesep,
	"date_format" : None,
	"doublequote" : True,
	"escapechar" : None,
	"decimal" : ".",
}

csv_option_types = {
	"sep" : [str],
	"na_rep" : [str],
	"float_format" : [str,None],
	"header" : [list,str,bool],
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


