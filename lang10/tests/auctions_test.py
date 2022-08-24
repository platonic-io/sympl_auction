import pytest
from assembly_client.api.contracts import ContractRef

VERSION = '1.0.4'
AUCTION = ContractRef('auction', VERSION, 10)

class TestAuction():

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
    def auction(self, network, reset_publish, key_alias):
        return network[key_alias].auction['10-'+VERSION]

    @pytest.fixture
    def bidder(self, network, reset_publish, other_key_alias):
        return network[other_key_alias].auction['10-'+VERSION]

#### General auction tests

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


    def test_close_auction_returns_winning_bid(self, auction, bidder):
        new_auction = auction.create_auction(product_description='stamps collection',
                                             initial_price='200')
        auction.bid(id=new_auction['id'], amount='210')
        winning_bid = auction.close_auction(id=new_auction['id'])

        assert winning_bid['amount'] == '210'

        with pytest.raises(Exception):
            bidder.close_auction(id=new_auction['id'])

#### Silent auction tests

    def test_create_admin(self, network, auction, bidder, key_alias, reset_publish):
        admin1 = auction.create_admin(new_admin=key_alias)
        assert admin1['id'] == key_alias

        ka = network.register_key_alias()
        admin2 = auction.create_admin(new_admin=ka)
        assert admin2['id'] == ka

        with pytest.raises(Exception):
            auction.create_admin(new_admin=key_alias)
        with pytest.raises(Exception):
            bidder.create_admin(new_admin=ka)

    def test_create_silent_auction(self, auction, bidder, key_alias):
        auction.create_admin(new_admin=key_alias)
        new_auction = auction.create_auction(product_description='stamps collection',
                                            initial_price='200',
                                            silent=True)

        assert new_auction['product_description'] == 'stamps collection' 

        with pytest.raises(Exception):
            bidder.create_auction(product_description='stamps collection',
                                    initial_price='200',
                                    silent=True)
    
    def test_add_member(self, auction, bidder, key_alias, other_key_alias, reset_publish):
        auction.create_admin(new_admin=key_alias)
        new_auction = auction.create_auction(product_description='stamps collection',
                                            initial_price='200',
                                            silent=True)

        creator_list = auction.get_auctions()
        assert len(creator_list) == 1

        non_member_list = bidder.get_auctions()
        assert non_member_list == []

        auction.add_member(new_member=other_key_alias, id=new_auction['id'])
        member_list = bidder.get_auctions()
        assert member_list == creator_list

    def test_silent_bid(self, auction, bidder, key_alias, other_key_alias, reset_publish):
        auction.create_admin(new_admin=key_alias)
        new_auction = auction.create_auction(product_description='stamps collection',
                                            initial_price='200',
                                            silent=True)

        with pytest.raises(Exception):
            bidder.bid(id=new_auction['id'], amount='210')                                         

        auction.add_member(new_member=other_key_alias, id=new_auction['id'])
        bid = bidder.bid(id=new_auction['id'], amount='210')
        auction = auction.get_auctions()[0]
        assert bid == auction['last_bid']
