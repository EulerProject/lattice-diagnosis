# lattice-diagnosis
A model-based diagnostics toolset that given a set of inconsistent rules (policies) finds the minimal inconsistent subset(s) of it. 
There are two example cases in the current repository:
- Case1.py: Input: a set of integers; Diagnostic Function: a set of integers with no common factor is inconsistent
- Case2.py: Input: a provenance graph, a set of integrity rules for a valid graph, a set of customization rules for sanitizing the graph stated as a set of DLV rules. Diagnostic Function: a set of customization rules violating one (or more) integrity rule is inconsistent. 

