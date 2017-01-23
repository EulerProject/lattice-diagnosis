#  Input: a set of positive integers
#  Problem: check if the input set numbers have a common prime factor (GCD > 1)


def gcd(a,b):
    while b:
        (a, b) = (b, a % b)
    return a

def gcd_list(Xs):
    # return reduce(lambda x,y:gcd(x,y),Xs)
    result = Xs[0]
    for x in Xs[1:]:
        result = gcd(result,x)
    return result

def has_common_prime(Xs):
    return gcd_list(Xs) > 1

if __name__ == "__main__":
    L1 = [24,54,12]
    L2 = [24,54,12,5]

    print L1, gcd_list(L1), has_common_prime(L1)
    print L2, gcd_list(L2), has_common_prime(L2)



