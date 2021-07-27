#!/bin/bash

. /cvmfs/belle.cern.ch/tools/b2setup release-05-02-12

export MGPATH=$BELLE2_EXTERNALS_DIR/Linux_x86_64/common/bin/mg5_aMC
export MODELPATH=$BELLE2_RELEASE_DIR/generators/madgraph/models/ALP_UFO
echo $MODELPATH

cp $BELLE2_RELEASE_DIR/generators/madgraph/cards/run_card.dat .
