#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Steering file for semi-official MC production of madgraph signal samples
with beam backgrounds (BGx1) from pre-generated LHE files.
"""

__author__ = "Sam Cunliffe"

import basf2 as b2
import random
from beamparameters import add_beamparameters
from simulation import add_simulation
from L1trigger import add_tsim
from reconstruction import add_reconstruction
from mdst import add_mdst_output
from ROOT import Belle2
import glob

# the LHE output from magraph assume its in CWD
mg_outputdir = "decay"

# configure the LHE reader
lhereader = b2.register_module("LHEInput")
lhereader.param("makeMaster", True)
lhereader.param("runNum", 0)  # set me!!!
lhereader.param("expNum", 1003)  # realistic phase 3
lhereader.param(
    "inputFileList", [mg_outputdir + "/Events/run_01/unweighted_events.lhe"]
)
lhereader.param("useWeights", False)
lhereader.param("nInitialParticles", 2)
lhereader.param("nVirtualParticles", 0)
lhereader.param("boost2Lab", True)  # generation is in centre of mass system (see steering card)
lhereader.param("wrongSignPz", True)  # because Belle II convention is different to LEP etc
b2.print_params(lhereader)

# set database conditions
b2.conditions.prepend_globaltag("mc_production_MC14a")

# create path
main = b2.create_path()

# add beamparameters
add_beamparameters(main, "Y4S")

# read in generated events
main.add_module(lhereader)

# detector simulation
background_subblocks = glob.glob(
    "/pnfs/desy.de/belle/local/belle/MC/prerelease-05-00-00a/DB00001021/BG15/phase31/beambg/BGx1/sub*"
)
bgfiles_eph3 = glob.glob(random.choice(background_subblocks) + "/*.root")
print("INFO background files are here:", bgfiles_eph3)
add_simulation(main, bkgfiles=bgfiles_eph3)

# trigger simulation
add_tsim(main, Belle2Phase="Phase3")

# reconstruction
add_reconstruction(main)

# Finally add mdst output
add_mdst_output(
    main, filename="mdst.root", additionalBranches=["KlIds", "KLMClustersToKlIds"]
)

# process events and print call statistics
b2.process(main)
print(b2.statistics)
