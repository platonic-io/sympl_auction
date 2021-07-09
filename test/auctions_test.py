import pytest
from assembly.lang_8 import ContractRef

AUCTION = ContractRef('auction', '1.0.0', 8)

class TestAuction():

    @pytest.fixture
    def reset_publish(self, network):
        network.reset(sympl_version=8)
        network.publish([AUCTION])

    @pytest.fixture
    def key_alias(self, network):
        return network.register_key_alias()

    @pytest.fixture
    def auction(self, network, reset_publish, key_alias):
        return network[key_alias].auction['8-1.0.0']

    def test_auction_life_cycle(self, auction):
        assert len(auction.get_auctions()) == 0

        new_auction = auction.create_auction(id='1',
                                              product_description='stamps collection',
                                              initial_price='200',
                                              days='3')

        assert new_auction['product_description'] == 'stamps collection'
        assert len(auction.get_auctions()) == 1

        auction.bid(bidder='Brooke', product_id='1', amount='210')
        auction.bid(bidder='Bradley', product_id='1', amount='220')

        auction.pass_day()

        new_auction = auction.get_auction(id='1')
        assert auction.get_auction(id='1')['days'] == '2'

        auction.pass_day()
        assert auction.get_auction(id='1')['days'] == '1'

        auction.pass_day()
        assert auction.get_auction(id='1')['days'] == '0'

        auction.pass_day()
        assert auction.get_auction(id='1')['days'] == '0'


    def test_cannot_bid_expired_auction(self, auction):
        new_auction = auction.create_auction(id='1',
                                              product_description='stamps collection',
                                              initial_price='200',
                                              days='3')
        auction.pass_day()
        auction.pass_day()
        auction.pass_day()
        auction.pass_day()

        with pytest.raises(Exception):
            auction.bid(bidder='Brooke', product_id='1', amount='210')


    def test_bid_must_propose_higher_price(self, auction):
        new_auction = auction.create_auction(id='1',
                                              product_description='stamps collection',
                                              initial_price='200',
                                              days='3')
        with pytest.raises(Exception):
            auction.bid(bidder='Brooke', product_id='1', amount='199')

        auction.bid(bidder='Brooke', product_id='1', amount='210')

        with pytest.raises(Exception):
            auction.bid(bidder='Bradley', product_id='1', amount='210')

        with pytest.raises(Exception):
            auction.bid(bidder='Bradley', product_id='1', amount='205')
