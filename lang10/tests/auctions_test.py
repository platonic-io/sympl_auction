import pytest
from assembly_client.api.contracts import ContractRef

AUCTION = ContractRef('auction', '1.0.0', 10)

class TestAuction():

    @pytest.fixture
    def reset_publish(self, network):
        network.reset(sympl_version=10)
        network.publish([AUCTION])

    @pytest.fixture
    def key_alias(self, network):
        return network.register_key_alias()

    @pytest.fixture
    def auction(self, network, reset_publish, key_alias):
        return network[key_alias].auction['10-1.0.0']

    # General auction tests

    def test_auction_life_cycle(self, auction):
        assert len(auction.get_auctions()) == 0

        new_auction = auction.create_auction(product_description='stamps collection',
                                              initial_price='200')

        assert new_auction['product_description'] == 'stamps collection'
        assert len(auction.get_auctions()) == 1

        auction.bid(id=new_auction['id'], amount='210')
        auction.bid(id=new_auction['id'], amount='220')

        assert new_auction['closed'] == False

    def test_cannot_bid_expired_auction(self, auction):
        new_auction = auction.create_auction(product_description='stamps collection',
                                              initial_price='200')

        auction.close_auction(id=new_auction['id'])

        with pytest.raises(Exception):
            auction.bid(id=new_auction['id'], amount='210')


    def test_bid_must_propose_higher_price(self, auction):
        new_auction = auction.create_auction(product_description='stamps collection',
                                              initial_price='200')
        with pytest.raises(Exception):
            auction.bid(id=new_auction['id'], amount='199')

        auction.bid(id=new_auction['id'], amount='210')

        with pytest.raises(Exception):
            auction.bid(id=new_auction['id'], amount='210')

        with pytest.raises(Exception):
            auction.bid(id=new_auction['id'], amount='205')


    def test_close_auction_returns_winning_bid(self, auction):
        new_auction = auction.create_auction(product_description='stamps collection',
                                             initial_price='200')
        auction.bid(id=new_auction['id'], amount='210')
        winning_bid = auction.close_auction(id=new_auction['id'])

        assert winning_bid['amount'] == '210'

    # Silent auction tests

    def test_admin_creation(self, network, auction, reset_publish):
        ka1 = network.register_key_alias()
        ka2 = network.register_key_alias()

        admin = auction.create_admin(new_admin=ka1)
        assert ka1 != ka2
        assert admin['id'] == ka1

        with pytest.raises(Exception):
            auction.create_admin(new_admin=ka2)

    def test_silent_auction_admin(self, auction, key_alias):
        auction.create_admin(new_admin=key_alias)
        new_auction = auction.create_auction(product_description='stamps collection',
                                            initial_price='200',
                                            silent=True)

        assert new_auction['product_description'] == 'stamps collection' 
    
    def test_silent_auction_non_admin(self, reset_publish, auction):
        with pytest.raises(Exception):
            auction.create_auction(product_description='stamps collection',
                                    initial_price='200',
                                    silent=True)

    def test_add_member(self, reset_publish, network, auction, key_alias):
        auction.create_admin(new_admin=key_alias)
        ka1 = network.register_key_alias()
    
