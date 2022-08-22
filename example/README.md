## Steps to create a private Geth network with PoA consensus

1. install Geth client: https://geth.ethereum.org/docs/install-and-build/installing-geth#macos-via-homebrew
2. update `genesis.json` and `setup.py (config)`
3. delete any existing Geth docker image/container
4. navigate to the same directory of `setup.py`
5. > python setup.py
6. > docker-compose up -d
7. check cluster with Docker