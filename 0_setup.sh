#!/bin/bash

. /cvmfs/belle.cern.ch/tools/b2setup release-05-02-12

export MODELPATH=$BELLE2_RELEASE_DIR/generators/madgraph/models/ALP_UFO
echo $MODELPATH

cp $BELLE2_RELEASE_DIR/generators/madgraph/cards/run_card.dat .
