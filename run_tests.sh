docker build -t fintechframework -f tests/docker/Dockerfile .
docker run -it -d --name ethnode fintechframework

docker exec -ti ethnode bash -c "nohup geth --dev --rpc --rpccorsdomain 'http://localhost:8545' --rpcapi='db,eth,net,web3,personal,web3' --targetgaslimit '9000000' --allow-insecure-unlock & sleep 3;"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_Crowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_CappedCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_MintedCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_PausableCrowdsale.py"
#docker exec -ti ethnode bash -c "python3 -W ignore E2E_RefundableCrowdsale.py"
#docker exec -ti ethnode bash -c "python3 -W ignore E2E_TimedCrowdsale.py"
docker exec -ti ethnode bash -c "python3 -W ignore E2E_WhitelistedCrowdsale.py"


docker rm ethnode --force
