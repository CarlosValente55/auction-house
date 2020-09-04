from utils import TextOperator, logger
from auction import Auction


class AuctionHouse():
    def __init__(self):
        self.text_operator = TextOperator()
        self.instruction = None
        self.list_of_auctions = []

    def startAuction(self):
        """
        This method is responsible for starting the auction by iterating through the instructions.
        """
        for line in self.text_operator.read_lines():
            logger(line)
            self.instruction = line
            self.read_actions()
            # Iterate through every close_time of every auction
            for expiring_bid in self.list_of_auctions:
                # If the current timestamp is equal to the close_time of an auction
                if expiring_bid['expiring_auction_timestamp'] == self.instruction[0]:
                    self.close_auction(expiring_bid['auctions'])
                    break

    def read_actions(self):
        """
        This method is reading the type of instruction and deciding what to do with each of them.

        -For selling instructions it will create an object of type Auction() and added to a structure list_of_auctions.

        -For bidding instructions it will find the Auction object and make a bid on it.
        """
        # For Selling instructions
        if len(self.instruction) == 6:
            # Append a new auction to the list of auctions
            auction = Auction(timestamp=self.instruction[0], user_id=self.instruction[1],
                              item=self.instruction[3], reserve_price=self.instruction[4], close_time=self.instruction[5])
            self.add_auctions(self.instruction[5], auction)
        # For Bidding instructions
        elif len(self.instruction) == 5:
            # Find the auction to bid
            auction = self.find_auction(self.instruction[3])
            if auction is not None:
                auction.bid(self.instruction)

    def close_auction(self, auctions):
        """
        This method closes the auction of each
        """
        for auction in auctions:
            auction.winning_bid['price_paid'] = auction.solve_price_paid()
            self.export_auction(auction.winning_bid)

        self.remove_auctions(self.instruction[0])

    def find_auction(self, item):
        """
        This method finds an auction by the item which is the unique identifier.

        Arguments:
        -item; string id
        Returns:
        -auction object; if found
        -None; if not found
        """
        for auction in self.list_of_auctions:
            for find_auction in auction["auctions"]:
                if item == find_auction.item:
                    return find_auction

    def add_auctions(self, timestamp, auction):
        """
        This method updates the list_of_auctions by inserting an auction in the 
        list of auctions corresponding to the expiring auction timestamp.

        Arguments:
        -timestamp; string
        -auction; auction object
        """
        if self.list_of_auctions == []:
            self.list_of_auctions.append(
                dict(expiring_auction_timestamp=timestamp, auctions=[auction]))
        else:
            for index, expiring_bids in enumerate(self.list_of_auctions):
                # If the expiring auction timestamp is already stored
                if expiring_bids['expiring_auction_timestamp'] == timestamp:
                    self.list_of_auctions[index]['auctions'].append(auction)
                    break
                else:
                    self.list_of_auctions.append(
                        dict(expiring_auction_timestamp=timestamp, auctions=[auction]))
                    break

    def remove_auctions(self, timestamp):
        """
        This method removes all the actions that are expired.

        Arguments:
        -timestamp; string
        Returns:
        -True; if the timestamp matches any expriring_auction_timestamp
        -False;
        """
        for index, expiring_bid in enumerate(self.list_of_auctions):
            if expiring_bid['expiring_auction_timestamp'] == timestamp:
                del self.list_of_auctions[index]
                return True
        return False

    def export_auction(self, auction):
        self.text_operator.write_line(auction)


if __name__ == "__main__":
    startAuction = AuctionHouse()
    startAuction.startAuction()
