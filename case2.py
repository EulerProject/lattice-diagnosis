import diagnostics
import diaglattice
import re
# example file
import prob

tax = diagnostics.lattice([])
inputRules = []
inputFile = open('ur.dlv', 'r')
lines = inputFile.readlines()
for line in lines:
    inputRules.append(line.strip())
tax.allJustifications(inputRules,prob.diag)


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

