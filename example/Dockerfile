FROM ethereum/client-go:v1.10.1

# ARG ACCOUNT_PASSWORD
ARG NODE_TYPE SIGNER_ONE SIGNER_TWO SIGNER_THREE

COPY . /tmp

RUN geth init /tmp/genesis.json && \
    rm -f ~/.ethereum/geth/nodekey && \
    cp /tmp/$SIGNER_ONE ~/.ethereum/keystore && \
    cp /tmp/$SIGNER_TWO ~/.ethereum/keystore && \
    cp /tmp/$SIGNER_THREE ~/.ethereum/keystore

ENTRYPOINT ["geth"]