#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Steering file for quick minimalist analysis of ALP signal mdst files.
"""

__author__ = "Sam Cunliffe"

import basf2 as b2
import modularAnalysis as ma
import pdg

# register the particles so they are known to the framework
pdg.add_particle("beam", 55, 999.0, 999.0, 0, 0)
pdg.add_particle("alp", 9000006, 999.0, 999.0, 0, 0)

# standard basf2 analysis stuff
path = b2.Path()
ma.inputMdst("default", "mdst.root", path)
ma.fillParticleList("gamma:sam", "E > 0.02", path=path)
ma.reconstructDecay("alp:gg -> gamma:sam gamma:sam", "", path=path)
ma.reconstructDecay("beam:ggg -> alp:gg gamma:sam", "9 < InvM < 11", path=path)

ma.matchMCTruth("beam:ggg", path)

ma.variablesToNtuple(
    "beam:ggg", ["daughter(0, InvM)", "isSignal"], "reco", "analysis_tuple.root", path
)

b2.process(path)
print(b2.statistics)
