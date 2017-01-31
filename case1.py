import diagnostics

# example file
import gcd

#  Cosistency in this example is defined as having a common prime factor
#  Given an inconsistent set of numbers, we are using the diagnostics approach to find the minium inconsistent subset

tax = diagnostics.lattice([])

tax.allJustifications([24,54,12,5,9,17],gcd.has_common_prime)

