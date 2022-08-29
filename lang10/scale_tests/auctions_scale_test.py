import pytest
import time
from assembly_client.api.contracts import ContractRef

AUCTION = ContractRef('auction_genesis', '1.0.1', 10)

name_str = "stamps collection #{index}"
price_str="{price}"
i = 0

def do_an_auction(auction, key_alias, bidder, second_bidder, other_key_alias, third_key_alias):
    new_auction = auction.create_auction(product_description='stamps collection',
                                         initial_price='100',
                                         silent=True)
    auction.add_member(new_member=third_key_alias, id=new_auction['id'])
    auction.add_member(new_member=other_key_alias, id=new_auction['id'])
    max_n = 20
    for idx in range(1, max_n):
        bidder.bid(id=new_auction['id'], amount=price_str.format(price=100+idx))
    for idx in range(max_n+2, max_n*2):
        second_bidder.bid(id=new_auction['id'], amount=price_str.format(price=100+idx))
    winning_bid = auction.close_auction(id=new_auction['id'])
    assert winning_bid['amount'] == price_str.format(price=100 + (max_n*2) -1)

class TestScaleAuction():

    @pytest.fixture
    def reset_publish(self, network):
        # network.reset(sympl_version=10)
        # network.publish([AUCTION])
        pass

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
        return network[key_alias].auction_genesis['10-1.0.1']

    @pytest.fixture
    def bidder(self, network, reset_publish, other_key_alias):
        return network[other_key_alias].auction_genesis['10-1.0.1']

    @pytest.fixture
    def second_bidder(self, network, reset_publish, third_key_alias):
        return network[third_key_alias].auction_genesis['10-1.0.1']

    #### Scale auction tests
    def test_scale_auctions_creation(self, auction, key_alias, bidder, second_bidder, other_key_alias, third_key_alias, benchmark):
        auction.create_admin(new_admin=key_alias)
        benchmark.pedantic(do_an_auction, args=(auction, key_alias, bidder, second_bidder, other_key_alias, third_key_alias), iterations=10, rounds=10)
