# Auction smart contract

## Introduction

This smart contract repository is a sample `symPL` contract as is used in the [Auction walkthrough](https://iportal.symbiont.io/sdk_docs/docs/walkthroughs/auctions/auctions/index/index.html) 
of Symbiont's SDK documentation. Hereby included are:
- the smart contract `auction.sympl`
- the contract definition `contract.yaml`
- A pytest test to validate the smart contract `test/auctions_test.py`

## Contributing 

Anyone is welcome to contribute to this repository, be it in the form of features, bug fixes, documentation or additional
tests. 
Please create a branch of your own and submit for merge via merge request. A codeowner will be assigned your merge request
and provide feedback/merge it. 

## Running tests

Requirements:
- Install the [pytest plugin](https://iportal.symbiont.io/sdk_docs/docs/testing/index/index.html)
- Have a mock-network running (we recommend using `sym` to get a mock network up and running quickly)

Steps: 
- Change directory to the root of this repository
- Run the following command:
```shell
pytest test/auctions_test.py --network-config=~/.symbiont/assembly-dev/mock-network/default/network-config.json --contract-path=./
```

