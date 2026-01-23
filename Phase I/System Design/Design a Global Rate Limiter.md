# Distributed Rate Limiter System Design

## Overview
A distributed rate limiter controls the rate of requests across multiple servers to prevent abuse and ensure fair resource allocation.

## Key Topics (Phase I)

### 1. **Functional Requirements**
- Limit requests per user/IP within a time window
- Support multiple rate limit policies
- Return 429 (Too Many Requests) when exceeded
- Track request counts across distributed systems

### 2. **Non-Functional Requirements**
- **Scalability**: Handle millions of requests per second
- **Low Latency**: Minimal overhead (<5ms per request)
- **High Availability**: Resilient to node failures
- **Consistency**: Accurate rate limit enforcement

### 3. **System Architecture**
- Distributed cache (Redis) for fast counters
- Multiple rate limiter servers
- Load balancer for request distribution
- Database for persistent policies

### 4. **Algorithms**
- **Token Bucket**: Smooth burst handling
- **Sliding Window**: Accurate counting
- **Leaky Bucket**: Fixed rate output

### 5. **Data Flow**
```
Client → Load Balancer → Rate Limiter → Backend Service
                              ↓
                          Redis Cache
```

### 6. **Challenges & Solutions**
- **Race Conditions**: Use Lua scripts in Redis
- **Network Partitions**: Fallback strategies
- **Synchronization**: Consistent hashing for distribution

### 7. **Estimated Capacity**
- Throughput: 1M+ RPS
- Latency: <5ms
- Storage: ~1GB per 1M users


## Engineering Justification (The "Staff Interview" Talk Track)

If an interviewer at Meta asks why you built it this way, highlight these Architectural Decisions:

### Atomic State Management

By using Lua, we avoid the "Phantom Read" problem where two nodes see 1 token remaining and both try to grab it. The logic is encapsulated within the Redis engine.

### Network Efficiency

By implementing `batch_size`, we reduced the network I/O and CPU overhead on the Redis cluster by 99% (assuming a batch of 100). This is how you scale to billions of events.

### Thread Safety

The combination of `_registry_lock` and per-ticker `_local_locks` ensures that we don't have race conditions within a single multi-threaded Python process, while also avoiding a "Global Interpreter Lock" bottleneck for different tickers.

---

### Load Balancing Strategies for Rate Limiting

While L7 is the intuitive choice, the most robust answer for a high-scale system is a Hybrid Approach, and often L4 is preferred for the immediate front of a dedicated Rate Limiter. Here is why your instinct for L7 is partially correct, but why L4 often wins at the Staff scale.

#### 1. The Case for Layer 4 (TCP/UDP)
If you are designing a high-performance Global Rate Limiter that must handle millions of requests per second with sub-millisecond overhead:
- **Speed**: L4 doesn't look at the HTTP payload or terminate TLS (SSL). It just forwards packets. This means lower latency.
- **Throughput**: A single L4 LB can handle significantly more connections than an L7 LB because it doesn't have to perform expensive string parsing or JSON inspection.
- **The "Protection" Argument**: If you are being DDOSed, you want your LB to be as "dumb" and fast as possible to drop or distribute traffic before it hits the application layer.

#### 2. The Case for Layer 7 (Application)
You would use an L7 LB in front of the Rate Limiter if your limiting logic is highly granular:
- **Attribute-based Limiting**: If you need to rate limit based on a User-ID in a JSON body, a specific API-Key in a header, or a JWT claim.
- **Path-based Routing**: If you want different rate-limiting clusters for /payments (strict) vs /search (loose).
- **TLS Termination**: If you want the LB to decrypt the traffic so the Rate Limiter can see the contents.

#### 3. The "Staff Engineer" Recommendation: The Two-Tier Design
In a production-grade system (like those at Stripe or AWS), you rarely use just one. You use a Tiered Load Balancing strategy:
- **Tier 1**: L4 Load Balancer (e.g., AWS NLB or Google Maglev)
    - **Job**: Highly available entry point. It distributes traffic based on IP/Port across a fleet of Tier 2 proxies.
    - **Why**: It handles the massive raw traffic volume and provides a single stable IP.
    
- **Tier 2**: L7 Proxy / Edge Gateway (e.g., Envoy, Nginx, or an API Gateway)
    - **Job**: This is where the Rate Limiting Logic actually lives or is called from.
    - **Mechanism**: The L7 proxy receives the request, extracts the API-Key, and makes a high-speed call to a sidecar or a Redis-backed Rate Limiter service.

#### Summary of the Trade-off

| Decision | Use L4 if... | Use L7 if... |
|----------|---------------|---------------|
| Priority | Extreme Throughput & Low Latency. | Granular Routing & Header Inspection. |
| Overhead | Minimal (Packet forwarding). | Significant (SSL handshake + Header parsing). |
| Complexity | Lower. | Higher (Requires managing certificates/rules). |

#### Staff Interview Tip:
If an interviewer asks this, start by asking: "What is our scale and what are we limiting on?" If we limit on IP address, suggest L4. If we limit on User Session/API Key, suggest L7, but mention that we might put an L4 in front of it to handle the raw connection volume and provide high availability.

## Implementation

### Python Code

```python
import time
import threading
import redis
from typing import Dict, Optional

class FinalDistributedRateLimiter:
    """
    A high-performance, distributed rate limiter using the Token Bucket algorithm.
    
    Features: 
    - Atomic Lua scripting for thread/process safety.
    - Local Batch Leasing to reduce network latency.
    - Sharded locking to minimize local thread contention.
    """

    # The Lua script is stored as a class constant to be loaded once.
    LUA_TOKEN_BUCKET = """
    local key = KEYS[1]
    local max_capacity = tonumber(ARGV[1])
    local refill_rate = tonumber(ARGV[2])
    local tokens_to_consume = tonumber(ARGV[3])
    local now = tonumber(ARGV[4])

    -- Get current state
    local state = redis.call('HMGET', key, 'tokens', 'last_update')
    local curr_tokens = tonumber(state[1]) or max_capacity
    local last_update = tonumber(state[2]) or now

    -- Calculate refill
    local time_passed = math.max(0, now - last_update)
    local refill = time_passed * refill_rate
    local new_tokens = math.min(max_capacity, curr_tokens + refill)

    -- Check if enough tokens exist for the batch
    if new_tokens >= tokens_to_consume then
        new_tokens = new_tokens - tokens_to_consume
        redis.call('HMSET', key, 'tokens', new_tokens, 'last_update', now)
        return 1 -- Success
    else
        return 0 -- Refused
    end
    """

    def __init__(self, redis_client: redis.Redis, batch_size: int = 100):
        """
        Initialize the rate limiter.
        
        Args:
            redis_client: Redis connection instance
            batch_size: Number of tokens to lease per Redis call
        """
        self.redis = redis_client
        self.batch_size = batch_size
        
        # Local state for the "Multiplier Effect" (Leasing)
        self._local_counts: Dict[str, int] = {}
        self._local_locks: Dict[str, threading.Lock] = {}
        self._registry_lock = threading.Lock()
        
        # Pre-register script for performance (EVALSHA)
        self._lua_sha = self.redis.script_load(self.LUA_TOKEN_BUCKET)

    def _get_lock(self, ticker: str) -> threading.Lock:
        """Sharded locking to ensure high-concurrency safety per ticker."""
        if ticker not in self._local_locks:
            with self._registry_lock:
                if ticker not in self._local_locks:
                    self._local_locks[ticker] = threading.Lock()
                    self._local_counts[ticker] = 0
        return self._local_locks[ticker]

    def allow_request(self, ticker: str, limit: int = 1000, refill_rate: int = 100) -> bool:
        """
        Main entry point. Checks local lease first, then goes to Redis.
        limit: Max tokens the global bucket can hold.
        refill_rate: Tokens added per second globally.
        """
        lock = self._get_lock(ticker)
        
        with lock:
            # Step 1: Check Local Lease (Nanoseconds latency)
            if self._local_counts[ticker] > 0:
                self._local_counts[ticker] -= 1
                return True

            # Step 2: Local lease empty, fetch a Batch from Redis (2ms latency)
            # We use time.time() here; in a Staff system, consider Redis TIME command for sync.
            now = time.time()
            
            try:
                # Atomically request a 'batch_size' of tokens
                success = self.redis.evalsha(
                    self._lua_sha, 1, f"rl:{ticker}", 
                    limit, refill_rate, self.batch_size, now
                )
                
                if success:
                    # We consumed 'batch_size' tokens, use 1 now, store the rest
                    self._local_counts[ticker] = self.batch_size - 1
                    return True
            except redis.exceptions.NoScriptError:
                # Fallback if script is flushed from Redis cache
                self._lua_sha = self.redis.script_load(self.LUA_TOKEN_BUCKET)
                return self.allow_request(ticker, limit, refill_rate)
            
            return False
```

---

## Example Usage: Reuters Financial Data Feed

```python
if __name__ == "__main__":
    # Setup Redis Connection
    r_client = redis.Redis(host='localhost', port=6379, db=0)
    
    # Initialize the Staff-level Limiter
    # 100 tokens per batch means we only talk to Redis once every 100 requests.
    limiter = FinalDistributedRateLimiter(r_client, batch_size=100)

    # Simulation
    ticker = "AAPL"
    for i in range(105):
        if limiter.allow_request(ticker, limit=500, refill_rate=50):
            print(f"Request {i+1}: Allowed")
        else:
            print(f"Request {i+1}: Rate Limited")
```

---

## Key Design Principles

### Token Bucket Algorithm

The token bucket algorithm is a widely-used rate limiting technique:
- Tokens accumulate at a fixed rate (refill_rate)
- Each request consumes one token
- If no tokens remain, the request is rejected
- The bucket has a maximum capacity (limit)

### Batch Leasing Optimization

Instead of fetching one token at a time from Redis, we fetch batches:
- Reduces Redis network round trips
- 99% reduction in overhead for batch_size=100
- Maintains accuracy while improving throughput

### Thread Safety Model

The implementation ensures thread-safety through:
- Per-ticker locks to avoid contention across different rate limits
- Registry lock to safely initialize new ticker entries
- Lua scripting for atomic operations at the Redis level