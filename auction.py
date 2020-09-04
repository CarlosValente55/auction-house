class Auction():
    def __init__(self, **attribs):
        self.item = attribs['item']
        self.price_paid = Queue(3) #Creates a Queue of max size 3
        self.price_paid.enqueue(0)
        self.selling_details = dict(timestamp=attribs['timestamp'],
                                    user_id=attribs['user_id'],
                                    reserve_price=attribs['reserve_price'],
                                    close_time=attribs['close_time'])
        self.winning_bid = dict(
            close_time=self.selling_details['close_time'], item=self.item, user_id=None, status=None, price_paid=self.price_paid, total_bid_count=0, highest_bid=None, lowest_bid=None)

    def bid(self, instruction):
        """
        This method handles the bidding functionality.
        Validates a bid and also checks if the bid status is already defined.

        Arguments:
        -instruction; the current instruction.
        Returns:
        -True; if it's a valid bid.
        -False; if it's an invalid bid.
        """
        bid_price=float(instruction[4])
        # If the bid is on time
        if self.selling_details['close_time'] > instruction[0]:
            # If the current bid is higher than the last bid made by a user
            if bid_price > self.winning_bid['price_paid'].peek():
                self.winning_bid['total_bid_count'] += 1
                self.winning_bid['highest_bid'] = bid_price
                self.winning_bid['price_paid'].enqueue(
                        bid_price)
                self.winning_bid['user_id'] = instruction[1]
                # If it's the first bid than it's the lowest bid
                if self.winning_bid['lowest_bid'] is None:
                    self.winning_bid['lowest_bid'] = bid_price

                return True

            else:
                return False

        return False

    def solve_price_paid(self):
        """
        This method analyses the queue of prices.
        The queue has max size of 3.
        Returns:
            -0.00
            -reserve_price 
            -the second element of the queue which is equivalent to the second highest
            valid bid
        """
        # Calculates the queue size
        price_paid_size = self.winning_bid['price_paid'].size()
        # If no bid was made
        if price_paid_size == 1:
            self.winning_bid['status'] = "UNSOLD"
            return self.winning_bid['price_paid'].peek()
        # If one bid was made
        elif price_paid_size == 2:
            # If the bid made is equal or higher than the reserve
            if self.winning_bid['price_paid'].peek() >= float(self.selling_details['reserve_price']):
                self.winning_bid['status'] = "SOLD"
                return self.selling_details['reserve_price']
            else:
                self.winning_bid['status'] = "UNSOLD"
                self.winning_bid['user_id'] = None
                return 0.00
        # If more than one bid was made
        elif price_paid_size == 3:
            # If the last bid is equal or higher than the reserve
            if self.winning_bid['price_paid'].peek() >= float(self.selling_details['reserve_price']):
                self.winning_bid['status'] = "SOLD"
                self.winning_bid['price_paid'].dequeue()
                return self.winning_bid['price_paid'].dequeue()
            else:
                self.winning_bid['status'] = "UNSOLD"
                self.winning_bid['user_id'] = None
                return 0.00


# Fixed Sized Queue Implementation
class Queue:
    def __init__(self, queue_size):
        self.queue = []
        self.queue_size = queue_size

    def peek(self):
        return self.queue[0]

    def enqueue(self, item):
        if self.queue_size == self.size():
            self.dequeue()
        self.queue.insert(0, item)

    def dequeue(self):
        return self.queue.pop()

    def size(self):
        return len(self.queue)
