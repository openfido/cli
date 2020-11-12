"""OpenFIDO Library Documentation: TODO

NAME
    TODO - TODO

DESCRIPTION
    TODO

    INPUTS

      TODO

    OUTPUTS

      TODO
"""

# main is required for openfido to be able to call this product
def main(inputs,outputs,options):

	# load the openfido utility module
	import openfido_util as of

	# setup the input and output file lists
	of.setup_io(inputs,outputs)

	# stage the results
	result = {}

	# process the input files
	for file in inputs:

		# read the input
		TODO = of.read_input(file,options)

	# process the output files
	for file in outputs:

		# write the output
		of.write_output(TODO,file,options)

		# prepare the return dict
		result[file] = TODO

	# return the result to the caller
	return result
