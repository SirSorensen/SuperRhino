class Queue:
    def __init__(self):
        """Initialize an empty queue using a list."""
        self.queue = []

    def enqueue(self, item):
        """Add an item to the end of the queue."""
        self.queue.append(item)

    def dequeue(self):
        """Remove and return the first item from the queue."""
        if not self.is_empty():
            return self.queue.pop(0)  # Removes the first element (FIFO)
        return None  # Return None if queue is empty

    def peek(self):
        """Return the first item without removing it."""
        if not self.is_empty():
            return self.queue[0]
        return None

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.queue) == 0

    def size(self):
        """Return the number of items in the queue."""
        return len(self.queue)

def list_to_queue(xs : list) -> Queue:
    queue = Queue()
    for x in xs:
        queue.enqueue(x)
    return queue

