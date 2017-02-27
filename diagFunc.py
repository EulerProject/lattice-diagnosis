import diagnostics
import diaglattice
import re
import sys
import optparse
import importlib

def diag(dfile, ifile):
    inputRules = list()
    tax = diagnostics.lattice([])
    diag = dfile
    diagFile = diag.split('.')[0]
    i = importlib.import_module(diagFile)
    diagOracle = getattr(i, diag.split('.')[1])
    inputFile =  open(ifile, 'r')
    lines = inputFile.readlines()
    for line in lines:

        inputRules.append(line.strip())
    tax.allJustifications(inputRules,diagOracle)


    # get articulations from input
    art = inputRules
    allMIS = set()
    fMIS = open('MIS.txt', "r")
    lines = fMIS.readlines()
    for line in lines:
        aMISString = re.match("(.*)\[(.*)\](.*)", line).group(2).split("&")
        #aMISString = list(map(int, aMISString))
        nMISString = []
        for a in aMISString:
            nMISString.append(art.index(a))
        aMIS = frozenset(map(int, nMISString))
        allMIS.add(aMIS)
    fMIS.close()
    lat = diaglattice.DiagnosticLattice(allMIS, art)
    #lat = diaglattice.DiagnosticLattice(allMIS, art, False)
    lat.genLattice()

    f = open('fullLattice.gv', 'w')
    fullLatStr = lat.fullLatViz()
    f.write(fullLatStr)
    f.close()

    f = open('reducedLattice.gv', 'w')
    reducedLatStr = lat.reducedLatViz()
    f.write(reducedLatStr)
    f.close()


def parse_options():
	# parse options
	parser = optparse.OptionParser(usage = "%prog [options]", version = "%prog 0.1")
	parser.add_option("-i","--inputfile",type="string",dest="ifile",
					  default=None,
					  help="input_file")
	parser.add_option("-d","--diagnostic_function",type="string",dest="dfile",
					  default=None,
					  help="diagnostics_function")
	(options,args) = parser.parse_args()
	return (options,args)
# MAIN 
if __name__ == '__main__':
	(options,args) = parse_options()
	if options.dfile == None or options.ifile == None:
            print 'Usage: diagFunc.py -d <diagnostics function> -i <input file>'
            sys.exit(1)
        diag(options.dfile, options.ifile)


