# Copyright (c) 2014 University of California, Davis
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#       diagnostics.py
#

import sets
import string
import copy

class lattice:

    def __init__(self, args):
        self.fixedCnt = 0                      # # of fixes /repairs
        self.internalfile = open("MIS.txt","w+")  # prepare internal file
    def allJustifications(self, artSet, diagnosisOracle):
        s = sets.Set()
        curpath = sets.Set()
        allpaths = sets.Set()
        self.computeAllJust(artSet, s, curpath, allpaths, diagnosisOracle)
        
    def computeAllJust(self, artSet, justSet, curpath, allpaths, diagnosisOracle):
        f = self.internalfile

        # prepare cashed path
        for path in allpaths:
            if path.issubset(curpath):
                return
        
        # ask oracle question
        if diagnosisOracle(artSet):
            allpaths.add(curpath)
            return
                            
        # prepare the justification set
        j = sets.Set()
        for s in justSet:
            if len(s.intersection(curpath)) == 0:
                j = s
                
        # check the justification set
        if len(j) == 0:
            j = self.computeOneJust(artSet, diagnosisOracle)
            if len(j) != 0:
                lj = list(j)
                f.write("MIS "+str(self.fixedCnt)+": [",)
                print "Min inconsistent subset ",self.fixedCnt,": [",
                for i in range(len(lj)):
                    if i != 0:
                        f.write(",")
                        print ",",
                    f.write(str(lj[i]))
                    print lj[i],
                f.write("]\n")
                print "]"
                print "************************************"
                self.fixedCnt += 1
                
        # update justification set
        if len(j) != 0:
            justSet.add(frozenset(j))
            # justSet.add(j)
        for a in j:
            tmpcur = copy.copy(curpath)
            tmpcur.add(a)
            tmpart = copy.copy(artSet)
            tmpart.remove(a)
            self.computeAllJust(tmpart, justSet, tmpcur, allpaths, diagnosisOracle)

    def computeOneJust(self, artSet, diagnosisOracle):
        if diagnosisOracle(artSet):
            return sets.Set()
        return self.computeJust(sets.Set(), artSet, diagnosisOracle)

    # s is consistent, f is inconsistent
    def computeJust(self, s, f, diagnosisOracle):
        if len(f) <= 1:
            return f
        f1 = copy.copy(f)
        f2 = sets.Set()
        for i in range(len(f) /2):
            f2.add(f1.pop())
        if not diagnosisOracle(s.union(f1)):
            return self.computeJust(s, f1, diagnosisOracle)
        if not diagnosisOracle(s.union(f2)):
            return self.computeJust(s, f2, diagnosisOracle)
        sl = self.computeJust(s.union(f1), f2, diagnosisOracle)
        sr = self.computeJust(s.union(sl), f1, diagnosisOracle)
        return sl.union(sr)                   
        
