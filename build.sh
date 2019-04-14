#!/usr/bin/env bash

set -u
set -e

TARGETS='	
./contracts/crowdsales/Crowdsale.sol
./contracts/crowdsales/distribution/FinalizableCrowdsale.sol
./contracts/crowdsales/distribution/RefundableCrowdsale.sol
./contracts/crowdsales/emission/MintedCrowdsale.sol
./contracts/crowdsales/validation/CappedCrowdsale.sol
./contracts/crowdsales/validation/TimedCrowdsale.sol
./contracts/crowdsales/validation/WhitelistCrowdsale.sol
'

for SOLIDITY_FILE in $TARGETS
do
    echo compiling "$SOLIDITY_FILE"
#    TEMP="bin/`basename $SOLIDITY_FILE`"
    TEMP=temp.sol
    python3 solc_precompile.py "$SOLIDITY_FILE" > "$TEMP"
    solc --optimize-runs 200 --optimize --bin --abi --overwrite -o bin "$TEMP"
done

echo all contracts were compiled

