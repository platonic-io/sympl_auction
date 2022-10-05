#!/usr/bin/env bash

set -eo pipefail
top_dir=$(git rev-parse --show-toplevel)

# Start local network, create a key alias and store it
sym local-network start
sym network cka > /tmp/ka_out
key_alias=$(cat /tmp/ka_out)

# Publish version 1.0.0
sym network publish -d $top_dir/lang10/contracts/1.0.0/

# Wait for the network to be "ready"
#sleep 10

# Create an auction
curl --request POST --header "Symbiont-Key-Alias: $key_alias" \
--url http://localhost:8888/api/v1/contracts/auction/10-1.0.0/create_auction \
--header 'Content-Type: application/json' --silent --data '{"product_description":"stamps", "initial_price":5, "silent":false}'

sleep 5
# Make sure it's been created, get the Identifier
auction_id=$(curl --request POST --header "Symbiont-Key-Alias: $key_alias" \
--url http://localhost:8888/api/v1/contracts/auction/10-1.0.0/get_auctions \
--header 'Content-Type: application/json' --silent --data '{}' | jq -r '.data.result[0].id')

# Retrieve it
# Should get something like: {"data":{"result":{"closed": false, "creator": "KA-2916552819566653", "id": "AUC-C9hGiijUGVqcRwcEYNdouaqz7r7jcsvzmzhDj8iYHCgNSsYgJgRgnnHF", "initial_price": "5", "last_bid": null, "product_description": "stamps"},"last_tx_index":7}}%
EXPECTED_AUCTION=$(curl --request POST --header "Symbiont-Key-Alias: $key_alias" \
--url http://localhost:8888/api/v1/contracts/auction/10-1.0.0/get_auction_by_id \
--header 'Content-Type: application/json' --silent --data "{\"id\":\"$auction_id\"}")

echo ">>> Received $EXPECTED_AUCTION"

# Publish version 2.0.0
sym network publish -d $top_dir/lang10/contracts/2.0.0/

# Retrieve our previously created auction - where is it!?
RECEIVED_AUCTION=$(curl --request POST --header "Symbiont-Key-Alias: $key_alias" \
--url http://localhost:8888/api/v1/contracts/auction/10-2.0.0/get_auction_by_id \
--header 'Content-Type: application/json' --silent --data "{\"id\":\"$auction_id\"}")

# We expect received auction to be the same as expected auction, ie. to have been migrated
echo ">>> Retrieved (post-upgrade) $RECEIVED_AUCTION"

sym local-network stop
[[ $(echo "$RECEIVED_AUCTION" | jq .data.result.id) == $(echo "$EXPECTED_AUCTION" | jq .data.result.id) ]] && \
[[ $(echo "$RECEIVED_AUCTION" | jq .data.result.creator) == $(echo "$EXPECTED_AUCTION" | jq .data.result.creator) ]] && \
[[ $(echo "$RECEIVED_AUCTION" | jq .data.result.last_bid) == $(echo "$EXPECTED_AUCTION" | jq .data.result.last_bid) ]] && \
[[ $(echo "$RECEIVED_AUCTION" | jq .data.result.product_description) == $(echo "$EXPECTED_AUCTION" | jq .data.result.product_description) ]] && \
echo "Successful migration" || return 1
