import diagnostics
import diaglattice

# example file
import gcd

#  Cosistency in this example is defined as having a common prime factor
#  Given an inconsistent set of numbers, we are using the diagnostics approach to find the minium inconsistent subset
inputRules = list()
tax = diagnostics.lattice([])

inputFile = open('in.txt', 'r')
lines = inputFile.readlines()
for line in lines:
    inputRules.append(line)
tax.allJustifications(map(int, inputRules),gcd.has_common_prime)
lat = diaglattice.DiagnosticLattice('MIS.txt', False)
lat.genLattice()

f = open('fullLattice.dot', 'w')
fullLatStr = lat.fullLatViz()
f.write(fullLatStr)
f.close()

f = open('reducedLattice.dot', 'w')
reducedLatStr = lat.reducedLatViz()
f.write(reducedLatStr)
f.close()
