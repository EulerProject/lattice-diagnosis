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


import sys
import os
import sets
import collections
import operator
import re

class DiagnosticLattice:
    
    def __init__(self, allMIS, art, legend = True):
        self.inputFile = 'in.txt'
        self.art = []
        self. legend = legend
        self.art = art
        self.allMCS = set()
        self.otherRed = set()
        self.allGreen = set()
        self.otherGreen = set()
        self.nodesBin = set()
        self.edgesBin = []
        self.latVizNodes = {}
        self.latVizEdges = {}
        self.allMIS = allMIS
    
    def findSupSets(self, aFrozenset, setOfFronzensets):
        supSets = set()
        for fronzenset in setOfFronzensets:
            if len(aFrozenset) < len(fronzenset):
                if aFrozenset.issubset(fronzenset):
                    supSets.add(fronzenset)
        return supSets

    def isPower2(self, num):
        return num != 0 and ((num & (num - 1)) == 0)
    
    def turnBin(self, num, power):
        binRep = []
        for p in range(power):
            if num & 1 << p:
                binRep.append(p)
        return frozenset(binRep)
                
    def createUncoloredLat(self, numOfArts):
        numOfNodes = 2**numOfArts
        nodes = []
        edges = []
        for i in range(numOfNodes):
            nodes.append(i)
            self.nodesBin.add(self.turnBin(i, numOfArts))
        for i in nodes:
            for j in nodes:
                if i<j and self.isPower2(i^j):
                    edges.append([i,j])
        for edge in edges:
            self.edgesBin.append([self.turnBin(edge[0], numOfNodes), self.turnBin(edge[1], numOfNodes)])
    def eliminate_subsets(self, sequence_of_sets):
        """Return a list of the elements of `sequence_of_sets`, removing all
        elements that are subsets of other elements.  Assumes that each
        element is a set or frozenset and that no element is repeated."""
        # The code below does not handle the case of a sequence containing
        # only the empty set, so let's just handle all easy cases now.
        if len(sequence_of_sets) <= 1:
            return list(sequence_of_sets)
        # We need an indexable sequence so that we can use a bitmap to
        # represent each set.
        if not isinstance(sequence_of_sets, collections.Sequence):
            sequence_of_sets = list(sequence_of_sets)
        # For each element, construct the list of all sets containing that
        # element.
        sets_containing_element = {}
        for i, s in enumerate(sequence_of_sets):
            for element in s:
                try:
                    sets_containing_element[element] |= 1 << i
                except KeyError:
                    sets_containing_element[element] = 1 << i
        # For each set, if the intersection of all of the lists in which it is
        # contained has length != 1, this set can be eliminated.
        out = [s for s in sequence_of_sets
               if s and self.isPower2(reduce(
                   operator.and_, (sets_containing_element[x] for x in s)))]
        return out
       
    
    def genLattice(self):
        self.createUncoloredLat(len(self.art)) 
        # find other red or green nodes
        for aMIS in self.allMIS:
            supSets = self.findSupSets(aMIS, self.nodesBin)
            self.otherRed.update(supSets)
        self.allGreen = self.nodesBin.difference(self.otherRed).difference(self.allMIS)        
        self.allMCS = set(self.eliminate_subsets(self.allGreen))
        self.otherGreen = self.allGreen.difference(self.allMCS)
    # generate the full lattice
    def fullLatViz(self):
        #self.genLattice()
        self.art = map(str, self.art)
        artMap = {k+1: v for k, v in enumerate(self.art)}
        outstr = ""
        outstr += "digraph{\n"
        outstr += "rankdir=BT\n"
        outstr += 'node[fontname="Helvetica"]\n\n'
        if self.legend:
            # add nodes
            outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=filled]\n'
            for solidRed in self.allMIS:
                label = ','.join(str(s+1) for s in solidRed)
                outstr += '"' + label +'"\n'
            outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=solid penwidth=0.4]\n'
            for otherRed in self.otherRed:
                label = ','.join(str(s+1) for s in otherRed)
                outstr += '"' + label +'"\n'
            outstr += 'node[shape=box color="#006400" fillcolor="#A0FFA0" style="rounded,filled"]\n'
            for solidGreen in self.allMCS:
                if len(solidGreen) == 0:
                    outstr += '"None"\n'
                else:
                    label = ','.join(str(s+1) for s in solidGreen)
                    outstr += '"' + label +'"\n'
            outstr += 'node[shape=box color="#006400" style=rounded penwidth=0.4]\n'
            for otherGreen in self.otherGreen:
                if len(otherGreen) == 0:
                    outstr += '"None"\n'
                else:
                    label = ','.join(str(s+1) for s in otherGreen)
                    outstr += '"' + label +'"\n'
            
            # add edges
            outstr += '\nedge[style=dotted penwidth=0.4]\n\n'
            for edge in self.edgesBin:
                # red dotted eddges
                if (edge[0] in self.allMIS or edge[0] in self.otherRed) \
                    and (edge[1] in self.allMIS or edge[1] in self.otherRed):
                    start = ','.join(str(s+1) for s in edge[0])
                    end = ','.join(str(s+1) for s in edge[1])
                    outstr += '"' + start + '" -> "' + end +'" [color="#CC0000"]\n'
                if (edge[0] in self.allMCS or edge[0] in self.otherGreen) \
                    and (edge[1] in self.allMCS or edge[1] in self.otherGreen):
                    if len(edge[0]) == 0:
                        start = 'None'
                    else:
                    # green dotted edges
                        start = ','.join(str(s+1) for s in edge[0])
                    end = ','.join(str(s+1) for s in edge[1])
                    outstr += '"' + start + '" -> "' + end +'" [dir=back color="#006400"]\n'
                if (edge[0] in self.allMCS or edge[0] in self.otherGreen) \
                    and (edge[1] in self.allMIS or edge[1] in self.otherRed):
                    if len(edge[0]) == 0:
                        start = 'None'
                    else:
                        start = ','.join(str(s+1) for s in edge[0])
                    end = ','.join(str(s+1) for s in edge[1])
                    outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#C0C0C0" penwidth=1 style=solid]\n'
            # add legend
            artsLabels = ""
            for art in self.art:
                artsLabels += "<TR> \n <TD>" + str(self.art.index(art)+1) + "</TD> \n <TD>" + art + "</TD> \n </TR> \n"
            outstr += "node[shape=plaintext fontsize=12 color=black] \n"
            outstr += '{rank=top Legend [label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="2"> \n'
            outstr += artsLabels
            outstr += "</TABLE> \n >] } \n"
            outstr += 'Legend -> "None" [style=invis]\n'

        else:
            # add nodes
            outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=filled]\n'
            for solidRed in self.allMIS:
                label = ','.join(artMap[s+1] for s in solidRed)
                outstr += '"' + label +'"\n'
            outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=solid penwidth=0.4]\n'
            for otherRed in self.otherRed:
                label = ','.join(artMap[s+1] for s in otherRed)
                outstr += '"' + label +'"\n'
            outstr += 'node[shape=box color="#006400" fillcolor="#A0FFA0" style="rounded,filled"]\n'
            for solidGreen in self.allMCS:
                if len(solidGreen) == 0:
                    outstr += '"None"\n'
                else:
                    label = ','.join(artMap[s+1] for s in solidGreen)
                    outstr += '"' + label +'"\n'
            outstr += 'node[shape=box color="#006400" style=rounded penwidth=0.4]\n'
            for otherGreen in self.otherGreen:
                if len(otherGreen) == 0:
                    outstr += '"None"\n'
                else:
                    label = ','.join(artMap[s+1] for s in otherGreen)
                    outstr += '"' + label +'"\n'
            
            # add edges
            outstr += '\nedge[style=dotted penwidth=0.4]\n\n'
            for edge in self.edgesBin:
                # red dotted eddges
                if (edge[0] in self.allMIS or edge[0] in self.otherRed) \
                    and (edge[1] in self.allMIS or edge[1] in self.otherRed):
                    start = ','.join(artMap[s+1] for s in edge[0])
                    end = ','.join(artMap[s+1] for s in edge[1])
                    outstr += '"' + start + '" -> "' + end +'" [color="#CC0000"]\n'
                if (edge[0] in self.allMCS or edge[0] in self.otherGreen) \
                    and (edge[1] in self.allMCS or edge[1] in self.otherGreen):
                    if len(edge[0]) == 0:
                        start = 'None'
                    else:
                    # green dotted edges
                        start = ','.join(artMap[s+1] for s in edge[0])
                    end = ','.join(artMap[s+1] for s in edge[1])
                    outstr += '"' + start + '" -> "' + end +'" [dir=back color="#006400"]\n'
                if (edge[0] in self.allMCS or edge[0] in self.otherGreen) \
                    and (edge[1] in self.allMIS or edge[1] in self.otherRed):
                    if len(edge[0]) == 0:
                        start = 'None'
                    else:
                        start = ','.join(artMap[s+1] for s in edge[0])
                    end = ','.join(artMap[s+1] for s in edge[1])
                    outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#C0C0C0" penwidth=1 style=solid]\n'           
        outstr += "}"
        return outstr
    
    def reducedLatViz(self):
        self.genLattice()
        outstr = ""
        outstr += "digraph{\n"
        outstr += "rankdir=BT\n"
        outstr += 'node[fontname="Helvetica"]\n\n'
        
        # add nodes
        if len(self.otherRed) > 0:
            outstr += '"AllOtherRed" [shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=solid penwidth=0.4]\n'
        if len(self.otherGreen) > 0:
            outstr += '"AllOtherGreen" [shape=box color="#006400" style=rounded penwidth=0.4]\n'
        outstr += 'node[shape=octagon color="#FF0000" fillcolor="#FFB0B0" style=filled]\n'
        for solidRed in self.allMIS:
            label = ','.join(str(s+1) for s in solidRed)
            outstr += '"' + label +'"\n'
        outstr += 'node[shape=box color="#006400" fillcolor="#A0FFA0" style="rounded,filled"]\n'
        for solidGreen in self.allMCS:
            if len(solidGreen) == 0:
                outstr += '"None"\n'
            else:
                label = ','.join(str(s+1) for s in solidGreen)
                outstr += '"' + label +'"\n'
        # add edges
        outstr += '\nedge[style=dotted penwidth=0.4]\n\n'
        if len(self.otherRed) > 0:
            for solidRed in self.allMIS:
                start = ','.join(str(s+1) for s in solidRed)
                end = 'AllOtherRed'
                outstr += '"' + start + '" -> "' + end +'" [color="#CC0000",label='+str(len(self.art)-len(solidRed))+']\n'
        if len(self.otherGreen) > 0:
            for solidGreen in self.allMCS:
                start = 'AllOtherGreen'
                if len(solidGreen) == 0:
                    end = '"None"\n'
                else:
                    end = ','.join(str(s+1) for s in solidGreen)
                outstr += '"' + start + '" -> "' + end +'" [dir=back color="#006400",label='+str(len(solidGreen))+']\n'
        for edge in self.edgesBin:
            if edge[0] in self.allMCS and edge[1] in self.allMIS:
                if len(edge[0]) == 0:
                    start = 'None'
                else:
                    start = ','.join(str(s+1) for s in edge[0])
                end = ','.join(str(s+1) for s in edge[1])
                outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#C0C0C0" penwidth=1 style=solid]\n'
        if len(self.otherGreen) > 0:
            for mis in self.allMIS:
                start = 'AllOtherGreen'
                end = ','.join(str(s+1) for s in mis)
                outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#C0C0C0" penwidth=1 style=solid label='+str(len(mis))+']\n'
        if len(self.otherRed) > 0:
            for mcs in self.allMCS:
                start = ','.join(str(s+1) for s in mcs)
                end = 'AllOtherRed'
                outstr += '"' + start + '" -> "' + end +'" [arrowhead=none color="#C0C0C0" penwidth=1 style=solid label='+str(len(self.art)-len(mcs))+']\n'
        # add legend
        artsLabels = ""
        for art in self.art:
            artsLabels += "<TR> \n <TD>" + str(self.art.index(art)+1) + "</TD> \n <TD>" + art + "</TD> \n </TR> \n"
        outstr += "node[shape=plaintext fontsize=12 color=black fillcolor=white] \n"
        outstr += '{rank=top Legend [label=< \n <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="2"> \n'
        outstr += artsLabels
        outstr += "</TABLE> \n >] } \n"
        if len(self.otherGreen) > 0:
            outstr += 'Legend -> "AllOtherGreen" [style=invis]\n'
        else:
            outstr += 'Legend -> "None" [style=invis]\n'
  
        outstr += "}"
        return outstr
    

