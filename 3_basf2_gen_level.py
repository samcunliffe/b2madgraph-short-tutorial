#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make an ntuple of generator-level physics quantities from a madgraph
ee --> gamma alp; alp --> gamma gamma signal sample.
"""

__author__ = "Sam Cunliffe"

from basf2 import create_path, register_module, print_params, process, statistics
from beamparameters import add_beamparameters
from modularAnalysis import (
    variablesToNtuple,
    reconstructDecay,
    fillParticleListsFromMC,
    matchMCTruth,
)
from variables import variables as vm
import pdg
import os
import subprocess

# register the particles so they are known to the framework
pdg.add_particle("beam", 55, 999.0, 999.0, 0, 0)
pdg.add_particle("alp", 9000006, 999.0, 999.0, 0, 0)

# where we put the output (you might need to be clever with this as to where you put your output)
mg_outputdir = "decay"

# look for the zipped ouput
if os.path.isfile(mg_outputdir + "/Events/run_01/unweighted_events.lhe.gz"):
    # ... then we need to unzip it
    subprocess.run(["gunzip", mg_outputdir + "/Events/run_01/unweighted_events.lhe.gz"])

# now look for the unzipped output
if not os.path.isfile(mg_outputdir + "/Events/run_01/unweighted_events.lhe"):
    raise FileNotFound(
        "Can't find LHE output, expected at: "
        + mg_outputdir
        + "/Events/run_01/unweighted_events.lhe"
    )

# configure the LHE reader
lhereader = register_module("LHEInput")
lhereader.param("runNum", 0)
lhereader.param("makeMaster", True)
lhereader.param("expNum", 1003)  # realistic phase 3
lhereader.param(
    "inputFileList", [mg_outputdir + "/Events/run_01/unweighted_events.lhe"]
)
lhereader.param("useWeights", False)
lhereader.param("nInitialParticles", 2)
lhereader.param("nVirtualParticles", 0)
lhereader.param("boost2Lab", True)  # generation is in centre of mass system (see steering card)
lhereader.param("wrongSignPz", True)  # because Belle II convention is different to LEP etc
print_params(lhereader)

# open read in LHE madgraph events
main = create_path()
main.add_module("Progress")
add_beamparameters(main, "Y4S")
main.add_module(lhereader)

# generator level
fillParticleListsFromMC(
    [("gamma:gen", ""), ("alp:gen", ""),], addDaughters=True, path=main
)

reconstructDecay("beam:gen -> alp:gen gamma:gen", "", path=main)

# info to write out
variables = ["E", "px", "py", "pz", "pt", "p", "theta", "cosTheta", "phi"]
cmsvariables = []
for v in variables:
    vm.addAlias(v + "CM", "useCMSFrame(%s)" % v)
    cmsvariables += [v + "CM"]

variables = ["InvM", "M"] + variables + cmsvariables


# dump to root analysis ntuple file
variablesToNtuple("alp:gen", variables, "alps", "gen_tuple.root", path=main)
variablesToNtuple("gamma:gen", variables, "photons", "gen_tuple.root", path=main)

beamvariables = []
for v in variables:
    vm.addAlias("alp_%s" % v, "daughter(0, %s)" % v)
    vm.addAlias("gammaR_%s" % v, "daughter(1, %s)" % v)
    beamvariables += ["alp_%s" % v, "gammaR_%s" % v]

variablesToNtuple("beam:gen", beamvariables, "beam", "gen_tuple.root", path=main)

process(main)
print(statistics)
