import diagnostics

# example file
import gcd

#  Cosistency in this example is defined as having a common prime factor
#  Given an inconsistent set of numbers, we are using the diagnostics approach to find the minium inconsistent subset



print diagnostics.computeAllJust([24,54,12,5],gcd.gcd)

