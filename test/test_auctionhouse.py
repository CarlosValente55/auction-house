import unittest
from auctionhouse import AuctionHouse

from auction import Auction
class TestAuctionHouse(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.auctionhouse = AuctionHouse()
        self.mock_auction= MockAuction(item='pc_1')
        self.mock_auction1= MockAuction(item='pc_2')

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_read_actions(self):
        pass
    def test_close_auction(self):
        pass
    
    def test_find_auction(self):
        self.auctionhouse.list_of_auctions=[dict(expiring_auction_timestamp=3,auctions=[self.mock_auction,self.mock_auction1]),dict(timestamp=4,auctions=[self.mock_auction1])]
        
        self.assertEqual(self.auctionhouse.find_auction('pc_1'),self.mock_auction)

        self.assertEqual(self.auctionhouse.find_auction('pc_3'),None)
    
    def test_add_and_remove_auctions(self):
        #Test add the first auction
        self.auctionhouse.list_of_auctions=[]
        self.auctionhouse.add_auctions(4,self.mock_auction)
        self.assertEqual(self.auctionhouse.list_of_auctions,[dict(expiring_auction_timestamp=4,auctions=[self.mock_auction])])

        #Test add the second auction
        self.auctionhouse.add_auctions(5,self.mock_auction1)

        self.assertEqual(self.auctionhouse.list_of_auctions,[dict(expiring_auction_timestamp=4,auctions=[self.mock_auction]),dict(expiring_auction_timestamp=5,auctions=[self.mock_auction1])])

        #Test remove auctions
        self.assertTrue(self.auctionhouse.remove_auctions(4))
        #Test with inexistent expiring bid timestamp
        self.assertFalse(self.auctionhouse.remove_auctions(6))
        

        
class MockAuction:
    def __init__(self,**attribs):
        self.item=attribs['item']