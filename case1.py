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
tax.allJustifications([24,2,4,45],gcd.has_common_prime)
lat = diaglattice.DiagnosticLattice('MIS.txt')
lat.genLattice()

f = open('out.dot', 'w')
fullLatStr = lat.fullLatViz()
f.write(fullLatStr)
f.close()
