docker build -t ethenv -f tests/docker/Dockerfile .
docker run -it -d --name ethnode ethenv
docker exec -ti ethnode bash -c "nohup parity --chain dev --geth --jsonrpc-interface 0.0.0.0 --rpcport 8008 --rpccorsdomain=* --rpcapi eth,net,parity,parity_pubsub,rpc,traces,web3,personal & sleep 5;" 

docker exec -ti ethnode bash -c "python3 -W ignore E2E_Crowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_CappedCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_MintedCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_PausableCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_RefundableCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_TimedCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_WhitelistedCrowdsale.py"

docker rm ethnode --force

