from collections import deque
from src.core.utils.logger import get_logger 

logger = get_logger()

class QueueManager:
    """
    Manages a queue with a fixed maximum size. Supports enqueueing and dequeueing items, 
    and provides methods to check the queue's state and size.

    Args:
        max_size (int): The maximum number of items allowed in the queue (default is 5).
    """
    def __init__(self, max_size=5):
        """
        Initializes the QueueManager with a specified maximum size.

        Args:
            max_size (int): The maximum size of the queue.
        """
        self.queue = deque()
        self.max_size = max_size
        logger.info(f"QueueManager initialized with max size: {self.max_size}")

    def enqueue(self, item):
        """
        Adds an item to the queue. If the queue is full, the item will not be added.

        Args:
            item: The item to add to the queue.

        Returns:
            bool: Returns `True` if the item was successfully added, `False` if the queue is full.
        """
        if len(self.queue) >= self.max_size:
            logger.warning("Queue is full. Item not added.")
            return False
        self.queue.append(item)
        logger.debug(f"Item enqueued. Current queue size: {len(self.queue)}")
        return True

    def dequeue(self):
        """
        Removes and returns the first item from the queue.

        Returns:
            The dequeued item, or `None` if the queue is empty.
        """
        if self.queue:
            item = self.queue.popleft()
            logger.debug(f"Item dequeued. Current queue size: {len(self.queue)}")
            return item
        logger.debug("Queue is empty.")
        return None

    def is_empty(self):
        """
        Checks if the queue is empty.

        Returns:
            bool: `True` if the queue is empty, `False` otherwise.
        """
        return len(self.queue) == 0

    def is_full(self):
        """
        Checks if the queue is full.

        Returns:
            bool: `True` if the queue is full, `False` otherwise.
        """
        return len(self.queue) >= self.max_size

    def size(self):
        """
        Returns the current size of the queue.

        Returns:
            int: The current number of items in the queue.
        """
        return len(self.queue)

    def clear(self):
        """
        Clears all items from the queue.
        """
        self.queue.clear()
        logger.info("Queue cleared.")
