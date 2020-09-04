import unittest
from auction import Auction


class TestAuction(unittest.TestCase):
    def setUp(self):
        self.auction1 = Auction(timestamp=2, user_id=1,
                                item="pc1", reserve_price=150, close_time=20)

    def tearDown(self):
        pass

    def test_selling_details(self):
        # Testing selling details
        self.assertEqual(self.auction1.item, "pc1")
        self.assertEqual(self.auction1.selling_details["timestamp"], 2)
        self.assertEqual(self.auction1.selling_details["user_id"], 1)
        self.assertEqual(self.auction1.selling_details["reserve_price"], 150)
        self.assertEqual(self.auction1.selling_details["close_time"], 20)

    def test_bid(self):
        # Test Bidding 0
        instruction1 = [12, '8', 'BID', 'pc1', '0']
        self.assertFalse(self.auction1.bid(instruction1))


        instruction2 = [15, '8', 'BID', 'pc1', '6']
        self.assertTrue(self.auction1.bid(instruction2))

        # Testing Bidding lower than the the current highest bid
        instruction3 = [16, '8', 'BID', 'pc1', '5']
        self.assertFalse(self.auction1.bid(instruction3))

        instruction4 = [16, '8', 'BID', 'pc1', '20']
        self.assertTrue(self.auction1.bid(instruction4))

        # Testing Bidding after closing time
        instruction5 = [22, '8', 'BID', 'pc1', '15']
        self.assertFalse(self.auction1.bid(instruction5))

        # Test if winning_details fields were correctly affected
        self.assertEqual(self.auction1.winning_bid['lowest_bid'], 6)
        self.assertEqual(self.auction1.winning_bid['highest_bid'], 20)
        self.assertEqual(self.auction1.winning_bid['total_bid_count'], 2)
        self.assertEqual(
            self.auction1.winning_bid['price_paid'].queue, [20, 6, 0])

    def test_solve_price_paid(self):
        #Test no bids made
        self.assertEqual(self.auction1.solve_price_paid(),0)
        #Test one bid made
        self.auction1.winning_bid['price_paid'].enqueue(0)
        self.auction1.winning_bid['price_paid'].enqueue(10)
        self.assertEqual(self.auction1.solve_price_paid(),0.0)
        #Test more than one bid
        self.auction1.winning_bid['price_paid'].enqueue(0)
        self.auction1.winning_bid['price_paid'].enqueue(10)
        self.auction1.winning_bid['price_paid'].enqueue(150)
        self.assertEqual(self.auction1.solve_price_paid(),10)        

if __name__ == '__main__':
    unittest.main()
