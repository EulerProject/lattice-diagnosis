import sets

def allJustifications(artSet, flag):
    s = sets.Set()
    curpath = sets.Set()
    allpaths = sets.Set()
    computeAllJust(artSet, s, curpath, allpaths, flag)
    
def computeAllJust(artSet, justSet, curpath, allpaths, flag):
    # prepare the internal files
    if flag == 'Consistency':
        f = open(self.misinternalfiles, "a")
    elif flag == 'Ambiguity':
        f = open(self.masinternalfiles, "a")
    
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
            
            # Consistency output
            if flag == 'Consistency':
                # output mis
                if not reasoner[self.args['-r']] == reasoner["rcc1"]:
                    lj = list(j)
                    print "************************************"
                    f.write("MIS "+str(self.fixedCnt)+": [",)
                    print "Min inconsistent subset ",self.fixedCnt,": [",
                    for i in range(len(lj)):
                        if i != 0:
                            f.write(",")
                            print ",",
                        f.write(self.artIndex.index(lj[i].string.strip()).__str__())
                        print lj[i].ruleNum,":",lj[i].string,
                    f.write("]\n")
                    print "]"
                    print "************************************"
                    self.fixedCnt += 1
                else:
                    lj = list(j)
                    print "************************************"
                    f.write("MIS "+str(self.fixedCnt)+": [",)
                    print "Min inconsistent subset ",self.fixedCnt,": [",
                    for i in range(len(lj)):
                        if i != 0:
                            f.write(",")
                            print ",",
                        f.write(self.shawnarticulations.index(lj[i].strip()).__str__())
                        print lj[i],
                    f.write("]\n")
                    print "]"
                    print "************************************"
                    self.fixedCnt += 1
                    
            # Ambiguity output
            elif flag == 'Ambiguity':
                # output mas
                if not reasoner[self.args['-r']] == reasoner["rcc1"]:
                    lj = list(j)
                    tmplist = []
                    print "************************************"
                    f.write("MAS "+str(self.fixedCnt)+": [",)
                    print "Min articulation subset that makes unique PW ",self.fixedCnt,": [",
                    for i in range(len(lj)):
                        if i != 0:
                            f.write(",") 
                            print ",",
                        f.write(self.artIndex.index(lj[i].string.strip()).__str__())
                        print lj[i].ruleNum,":",lj[i].string,
                        
#                         # store for fourinone lattice
#                         tmplist.append(lj[i].string)
#     
#                     if flag == 'Consistency':
#                         if tmplist not in self.mis:
#                             self.mis.append(tmplist)
#                     else:
#                         if tmplist not in self.misANDmus:
#                             self.misANDmus.append(tmplist)
#                         
                    f.write("]\n")
                    print "]"
                    print "************************************"
                    self.fixedCnt += 1
                else:
                    lj = list(j)
                    print "************************************"
                    f.write("MAS "+str(self.fixedCnt)+": [",)
                    print "Min articulation subset that makes unique PW ",self.fixedCnt,": [",
                    for i in range(len(lj)):
                        if i != 0:
                            f.write(",")
                            print ",",
                        f.write(self.shawnarticulations.index(lj[i].strip()).__str__())
                        print lj[i],
                    f.write("]\n")
                    print "]"
                    print "************************************"
                    self.fixedCnt += 1
    
    # update justification set
    if len(j) != 0:
        justSet.add(j)
    for a in j:
        tmpcur = copy.copy(curpath)
        tmpcur.add(a)
        tmpart = copy.copy(artSet)
        tmpart.remove(a)
        self.computeAllJust(tmpart, justSet, tmpcur, allpaths, flag)
