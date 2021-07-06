import pytest
from assembly.lang_8 import ContractRef

AUCTIONS = ContractRef('auctions', '1.0.0', 8)

class TestAuction():

    @pytest.fixture
    def reset_publish(self, network):
        network.reset(sympl_version=8)
        network.publish([AUCTIONS])

    @pytest.fixture
    def key_alias(self, network):
        return network.register_key_alias()

    @pytest.fixture
    def auctions(self, network, reset_publish, key_alias):
        return network[key_alias].auctions['8-1.0.0']

    def test_auction_life_cycle(self, auctions):
        assert len(auctions.get_auctions()) == 0

        new_auction = auctions.create_auction(id='1',
                                              product_description='stamps collection',
                                              initial_price='200',
                                              days='3')

        assert new_auction['product_description'] == 'stamps collection'
        assert len(auctions.get_auctions()) == 1

        auctions.bid(bider='Brooke', product_id='1', amount='210')
        auctions.bid(bider='Bradley', product_id='1', amount='220')

        auctions.pass_day()

        auction = auctions.get_auction(id='1')
        assert auctions.get_auction(id='1')['days'] == '2'

        auctions.pass_day()
        assert auctions.get_auction(id='1')['days'] == '1'

        auctions.pass_day()
        assert auctions.get_auction(id='1')['days'] == '0'

        auctions.pass_day()
        assert auctions.get_auction(id='1')['days'] == '0'


    def test_cannot_bid_expired_auction(self, auctions):
        new_auction = auctions.create_auction(id='1',
                                              product_description='stamps collection',
                                              initial_price='200',
                                              days='3')
        auctions.pass_day()
        auctions.pass_day()
        auctions.pass_day()
        auctions.pass_day()

        with pytest.raises(Exception):
            auctions.bid(bider='Brooke', product_id='1', amount='210')


    def test_bid_must_propose_higher_price(self, auctions):
        new_auction = auctions.create_auction(id='1',
                                              product_description='stamps collection',
                                              initial_price='200',
                                              days='3')
        with pytest.raises(Exception):
            auctions.bid(bider='Brooke', product_id='1', amount='199')

        auctions.bid(bider='Brooke', product_id='1', amount='210')

        with pytest.raises(Exception):
            auctions.bid(bider='Bradley', product_id='1', amount='210')

        with pytest.raises(Exception):
            auctions.bid(bider='Bradley', product_id='1', amount='205')
