import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.utils.queue_manager import QueueManager

def test_enqueue_and_dequeue():
    """
    Test that verifies the enqueue and dequeue operations of the QueueManager.

    This test checks that items can be added to the queue until it reaches the maximum size,
    and that items are dequeued in the correct order (FIFO). It also verifies that the queue 
    does not allow more items than its maximum size.
    """
    q = QueueManager(max_size=2)
    assert q.is_empty()  # Verify the queue is initially empty
    assert q.enqueue("a")  # Enqueue an item
    assert q.enqueue("b")  # Enqueue another item
    assert not q.enqueue("c")  # Ensure the queue does not accept a third item
    assert q.is_full()  # Verify the queue is full
    assert q.dequeue() == "a"  # Dequeue and check the first item
    assert q.dequeue() == "b"  # Dequeue and check the second item
    assert q.is_empty()  # Verify the queue is empty again

def test_dequeue_empty_queue():
    """
    Test that verifies the behavior when attempting to dequeue from an empty queue.

    This test ensures that when the queue is empty, the dequeue operation returns None.
    """
    q = QueueManager(max_size=1)
    assert q.dequeue() is None  # Dequeue from an empty queue should return None

def test_queue_size_limit():
    """
    Test that verifies the size limit of the queue.

    This test checks that the queue does not exceed the specified maximum size and behaves 
    correctly when items are added beyond the limit. It also verifies that the queue is resized 
    properly after dequeuing an item.
    """
    q = QueueManager(max_size=3)
    for i in range(5):
        q.enqueue(i)  # Add items to the queue, exceeding the max size
    assert q.is_full()  # Verify the queue is full
    assert q.dequeue() == 0  # Verify the first item is dequeued
    assert not q.is_full()  # Verify the queue is no longer full after dequeuing an item
