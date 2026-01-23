"""
Concurrency: Asyncio/GIL/Locking Patterns
Focus: Jul 3 - Jul 9, 2026
"""

import asyncio
import threading
from threading import Lock, RLock, Semaphore, Event
from queue import Queue

# GIL (Global Interpreter Lock) Understanding
def cpu_bound_task(n):
    """CPU-bound task: GIL limits true parallelism"""
    pass

def io_bound_task(url):
    """I/O-bound task: Good candidate for threading/asyncio"""
    pass

# Threading Primitives
class ThreadSafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = Lock()
    
    def increment(self):
        """Thread-safe increment using lock"""
        pass
    
    def decrement(self):
        """Thread-safe decrement using lock"""
        pass

# Reader-Writer Lock Pattern
class ReaderWriterLock:
    def __init__(self):
        self.readers = 0
        self.writers = 0
        self.read_lock = Lock()
        self.write_lock = Lock()
    
    def acquire_read(self):
        """Acquire read lock (multiple readers allowed)"""
        pass
    
    def release_read(self):
        """Release read lock"""
        pass
    
    def acquire_write(self):
        """Acquire write lock (exclusive)"""
        pass
    
    def release_write(self):
        """Release write lock"""
        pass

# Asyncio Patterns
async def fetch_data(url):
    """Simulate async I/O operation"""
    pass

async def concurrent_fetches(urls):
    """Fetch multiple URLs concurrently using asyncio"""
    pass

# Deadlock Prevention
def resource_allocation(resources):
    """Allocate resources safely to avoid deadlock"""
    pass

# Producer-Consumer Pattern
class ProducerConsumer:
    def __init__(self, buffer_size):
        self.queue = Queue(maxsize=buffer_size)
    
    def producer(self, item):
        """Thread-safe producer"""
        pass
    
    def consumer(self):
        """Thread-safe consumer"""
        pass
