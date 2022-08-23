import pytest
import time
from assembly_client.api.contracts import ContractRef
from assembly_client.api import node_api_client

AUCTION = ContractRef('auction', '1.0.0', 10)

name_str = "stamps collection #{index}"
price_str="{price}"
i = 0


def async_call(  network, key_alias, contract_ref, function, kwargs):
        """
        calls the specified contract function on a node
        :param key_alias: key_alias to invoke as
        :param contract_ref: contract to call
        :param function: function to invoke
        :param kwargs: dictionary of arguments to the contract, will be json serialized
        :return: the result of the call as a value or job object
        """
        session = network.node_sessions[network.alias_locations[key_alias]]

        # if this clientside does not post, it'll be the value read, otherwise a job
        result = node_api_client.call(
            session,
            key_alias,
            contract_ref,
            function,
            kwargs,
            query_tx_index=network.query_tx_index,
        )

def do_an_auction(auction, key_alias, bidder, second_bidder, other_key_alias, third_key_alias, network):
    new_auction = auction.create_auction(product_description='stamps collection',
                                         initial_price='100',
                                         silent=True)

    auction.add_member(new_member=third_key_alias, id=new_auction['id'])
    auction.add_member(new_member=other_key_alias, id=new_auction['id'])
    max_n = 20
    for idx in range(1, max_n * 2):
        if idx < max_n:
          async_call(network, other_key_alias, AUCTION, "bid", {"id": new_auction['id'], "amount" :price_str.format(price=100+idx)})
        else:
        #bidder.bid(id=new_auction['id'], amount=price_str.format(price=100+idx))
#    for idx in range(max_n+2, max_n*2):
         async_call(network,third_key_alias, AUCTION, "bid", {"id": new_auction['id'], "amount" :price_str.format(price=100+idx)})
#        second_bidder.bid(id=new_auction['id'], amount=price_str.format(price=100+idx))
    keep_waiting = True
    while keep_waiting: 
      time.sleep(0.005)
      # import pdb
      # pdb.set_trace()
      keep_waiting = not(str(auction.last_bid_for_auction(id=new_auction["id"])) == price_str.format(price=100 + (max_n*2) -1))
    winning_bid = auction.close_auction(id=new_auction['id'])
    assert winning_bid['amount'] == price_str.format(price=100 + (max_n*2) -1)

class TestScaleAuction():

    @pytest.fixture
    def reset_publish(self, network):
        network.reset(sympl_version=10)
        network.publish([AUCTION])

    @pytest.fixture
    def key_alias(self, network):
        return network.register_key_alias()

    @pytest.fixture
    def other_key_alias(self, network):
        return network.register_key_alias()

    @pytest.fixture
    def third_key_alias(self, network):
        return network.register_key_alias()

    @pytest.fixture
    def auction(self, network, reset_publish, key_alias):
        return network[key_alias].auction['10-1.0.0']

    @pytest.fixture
    def bidder(self, network, reset_publish, other_key_alias):
        return network[other_key_alias].auction['10-1.0.0']

    @pytest.fixture
    def second_bidder(self, network, reset_publish, third_key_alias):
        return network[third_key_alias].auction['10-1.0.0']

    #### Scale auction tests
    def test_scale_auctions_creation(self, auction, key_alias, bidder, second_bidder, other_key_alias, third_key_alias, network, benchmark):
        auction.create_admin(new_admin=key_alias)
        benchmark.pedantic(do_an_auction, args=(auction, key_alias, bidder, second_bidder, other_key_alias, third_key_alias, network), iterations=3, rounds=3)
