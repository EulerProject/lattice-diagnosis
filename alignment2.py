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
#       alignment.py
#
#  Alignment Module:
#    We define the alignment class here for taxonomy alignment
#    and dataset integration
#


import os
import sets
import itertools
import string
import sys
import copy
from operator import itemgetter
from shutil import copyfile


class diagnostic:

    def __init__(self, args):
        self.articulations = []                # set of articulations
        self.fixedCnt = 0                      # # of fixes /repairs
        self.artIndex = []                     # articulations string with index

    # return consistent or ambiguous
    def diagnosisAskOracle(self, artSet, flag):
        return flag(artSet)
            

    def allJustifications(self, artSet, flag):
        s = sets.Set()
        curpath = sets.Set()
        allpaths = sets.Set()
        self.computeAllJust(artSet, s, curpath, allpaths, flag)
        
    def computeAllJust(self, artSet, justSet, curpath, allpaths, flag):
        # prepare the internal files
        #f = open(self.misinternalfiles, "a")
        f = open("MIS.txt","w")

        
        # prepare cashed path
        for path in allpaths:
            if path.issubset(curpath):
                return
        
        # ask oracle question
        if self.diagnosisAskOracle(artSet, flag):
            allpaths.add(curpath)
            return
                            
        # prepare the justification set
        j = sets.Set()
        for s in justSet:
            if len(s.intersection(curpath)) == 0:
                j = s
                
        # check the justification set
        if len(j) == 0:
            j = self.computeOneJust(artSet, flag)
            if len(j) != 0:
                lj = list(j)
                if len(lj) > 1:
                    print "************************************"
                    f.write("MIS "+str(self.fixedCnt)+": [",)
                    print "Min inconsistent subset ",self.fixedCnt,": [",
                    for i in range(len(lj)-1):
                        print lj[i],
                        f.write(",")
                        print ",",
                        # Parisa: Temp change
                        f.write(str(lj[i]))
                        #f.write(self.artIndex.index(lj[i].strip()).__str__())
                        #f.write(self.artIndex.index(lj[i].string.strip()).__str__())
                        #print lj[i].ruleNum,":",lj[i].string,
                    print lj[-1],
                    f.write(str(lj[-1]))

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
            self.computeAllJust(tmpart, justSet, tmpcur, allpaths, flag)
        

    def computeOneJust(self, artSet, flag):
        if self.diagnosisAskOracle(artSet, flag):
            return sets.Set()
        return self.computeJust(sets.Set(), artSet, flag)

    # s is consistent, f is inconsistent
    def computeJust(self, s, f, flag):
        if len(f) <= 1:
            return f
        f1 = copy.copy(f)
        f2 = sets.Set()
        for i in range(len(f) /2):
            f2.add(f1.pop())
        if not self.diagnosisAskOracle(s.union(f1), flag):
            return self.computeJust(s, f1, flag)
        if not self.diagnosisAskOracle(s.union(f2), flag):
            return self.computeJust(s, f2, flag)
        sl = self.computeJust(s.union(f1), f2, flag)
        sr = self.computeJust(s.union(sl), f1, flag)
        return sl.union(sr)                   
        
