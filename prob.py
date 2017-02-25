#  Input: ProPub's rules; Integrity rules for a valid graph
#  A provenance graph stated as a set of DLV rules
# Usage: python prob.py pg.dlv propub_swallow.dlv
import sys
import subprocess


def exe(c):
    command = 'dlv -silent ' + c
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    lst = out[1:-2].strip().split(', ')
    return lst


def diag(ur):
    f = open('ureq.dlv', 'w')
    for r in ur:
        f.write(r +'\n')
    f.close()
    ICRules = ['nc', 'nfs', 'wc', 'nfs']
    lst = exe('ureq.dlv pg.dlv propub_swallow.dlv')
    for l in lst:
        r  = l.split('(')[0]
        if r in ICRules:
            return False
    return True

if __name__ == "__main__":
    f = open('ur.dlv', 'r')
    reqs = f.readlines()
    if diag(reqs):
        print 'Consistent'
    else:
        print 'Inconsistent'
