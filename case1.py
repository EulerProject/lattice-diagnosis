import diagnostics
import diaglattice
import re
# example file
import gcd

#  Cosistency in this example is defined as having a common prime factor
#  Given an inconsistent set of numbers, we are using the diagnostics approach to find the minium inconsistent subset
inputRules = list()
tax = diagnostics.lattice([])

inputFile = open('in3.txt', 'r')
lines = inputFile.readlines()
for line in lines:
    inputRules.append(line.strip())
tax.allJustifications(inputRules,gcd.has_common_prime)


# get articulations from input
art = inputRules
art = map(int, art)
allMIS = set()
fMIS = open('MIS.txt', "r")
lines = fMIS.readlines()
for line in lines:
    aMISString = re.match("(.*)\[(.*)\](.*)", line).group(2).split("&")
    #aMISString = list(map(int, aMISString))
    nMISString = []
    for a in aMISString:
        nMISString.append(art.index(int(a)))
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
