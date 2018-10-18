class Cons:
    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

    def to_array(self):
        return [self.head] + (self.tail.to_array() if self.tail is not None else [])

    @classmethod
    def from_array(cls, arr):
        if len(arr) == 0:
            return None

        head = Cons(arr[0])
        current = head
        for val in arr[1:]:
            current.tail = Cons(val)
            current = current.tail

        return head

    def filter(self, fn):
        # TODO: construct new algebraic list containing only elements
        #      that satisfy the predicate.
        return Cons.from_array(list(filter(fn, self.to_array())))

    def map(self, fn):
        # TODO: construct a new algebraic list containing all elements
        #      resulting from applying the mapper function to a list.
        return Cons.from_array(list(map(fn, self.to_array())))