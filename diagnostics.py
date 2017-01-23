import sets

   
def computeAllJust(artSet, flag): # a recursive call but what does this actually do? 
    f = open("out.txt")
    s = sets.Set()
    curpath = sets.Set()
    allpaths = sets.Set()

    if not reasoner[self.args['-r']] == reasoner["rcc1"]:  # checking what reasoner is being used? 
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
            f.write(self.shawnarticulations.index(lj[i].strip()).__str__())  # this is the only line different in if and else!!
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
    computeAllJust(tmpart, justSet, tmpcur, allpaths, flag)

