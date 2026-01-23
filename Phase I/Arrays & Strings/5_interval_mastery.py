"""
Filename: interval_mastery.py
Focus: Mastering the Overlapping Intervals pattern.
Key Idea: Sort by start time, then compare the current interval's start 
with the previous interval's end.
"""

import heapq

# =============================================================================
# PATTERN: Overlapping Intervals
# Logic: 1. Sort intervals by start time.
#        2. Iterate and compare: If current.start <= previous.end, they overlap.
# =============================================================================

def merge_intervals(intervals):
    """
    Problem: Merge all overlapping intervals.
    Logic: Sort by start. If current interval overlaps with the last merged 
    interval, update the end of the last merged interval to be the max of both.
    """
    if not intervals: return []
    
    # Step 1: Sort by start time O(N log N)
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for i in range(1, len(intervals)):
        curr_start, curr_end = intervals[i]
        prev_end = merged[-1][1]
        
        # If overlap exists
        if curr_start <= prev_end:
            merged[-1][1] = max(prev_end, curr_end)
        else:
            merged.append(intervals[i])
            
    return merged



def insert_interval(intervals, new_interval):
    """
    Problem: Insert a new interval into a sorted list and merge if necessary.
    Logic: 
    1. Add all intervals ending before the new one starts.
    2. Merge all overlapping intervals with the new one.
    3. Add the remaining intervals.
    """
    res = []
    i = 0
    n = len(intervals)
    new_start, new_end = new_interval
    
    # 1. Add intervals that come strictly before
    while i < n and intervals[i][1] < new_start:
        res.append(intervals[i])
        i += 1
        
    # 2. Merge overlapping intervals
    while i < n and intervals[i][0] <= new_end:
        new_start = min(new_start, intervals[i][0])
        new_end = max(new_end, intervals[i][1])
        i += 1
    res.append([new_start, new_end])
    
    # 3. Add remaining
    while i < n:
        res.append(intervals[i])
        i += 1
        
    return res

def meeting_rooms_ii(intervals):
    """
    Problem: Find minimum number of conference rooms required.
    Logic: Use a Min-Heap to track the end times of meetings currently in rooms.
    If a new meeting starts after the earliest meeting ends, reuse that room.
    """
    import heapq
    if not intervals: return 0
    
    intervals.sort(key=lambda x: x[0])
    # Heap stores the end times of meetings
    rooms = [] 
    
    for start, end in intervals:
        # If the room with the earliest end time is free
        if rooms and start >= rooms[0]:
            heapq.heappop(rooms)
        
        heapq.heappush(rooms, end)
        
    return len(rooms)



def interval_intersection(list1, list2):
    """
    Problem: Find the intersection of two sets of sorted intervals.
    Logic: Two Pointers. The intersection starts at max(s1, s2) 
    and ends at min(e1, e2). Increment the pointer of the interval that ends first.
    """
    i = j = 0
    res = []
    
    while i < len(list1) and j < len(list2):
        # Find overlap boundaries
        start = max(list1[i][0], list2[j][0])
        end = min(list1[i][1], list2[j][1])
        
        if start <= end:
            res.append([start, end])
            
        # Move pointer of the interval that finishes first
        if list1[i][1] < list2[j][1]:
            i += 1
        else:
            j += 1
            
    return res

# =============================================================================
# STAFF SIGNAL: Sweep Line Algorithm
# =============================================================================
"""
Filename: interval_mastery_advanced.py
Focus: Advanced Overlapping Intervals & Multi-list merging.
"""

class Interval:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f"[{self.start}, {self.end}]"

# =============================================================================
# PROBLEM: Employee Free Time
# Logic: We are looking for the gaps between the merged working hours of 
# all employees. Instead of merging all and then finding gaps, we use a 
# Min-Heap to process the "earliest" work intervals across all employees.
# =============================================================================

def employee_free_time(schedule):
    """
    Problem: Find the common free time for all employees.
    Logic: 
    1. Use a Min-Heap to track the smallest start time across all employee schedules.
    2. Track the 'anchor' (the end time of the last processed work interval).
    3. If the next interval starts AFTER the anchor, the gap in between is free time.
    Complexity: O(N log K) where N is total intervals and K is number of employees.
    """
    min_heap = []
    
    # 1. Push the first interval of each employee into the heap
    # Format: (start_time, employee_index, interval_index)
    for i, employee_schedule in enumerate(schedule):
        if employee_schedule:
            heapq.heappush(min_heap, (employee_schedule[0].start, i, 0))
    
    res = []
    # Initialize 'anchor' with the start of the earliest meeting
    if not min_heap:
        return []
    
    # Get the very first start time to initialize our tracking
    anchor = min_heap[0][0]
    
    while min_heap:
        start, emp_idx, interval_idx = heapq.heappop(min_heap)
        
        # 2. Logic Check: Is there a gap between anchor and current start?
        if start > anchor:
            res.append(Interval(anchor, start))
        
        # 3. Update the anchor to the furthest end time seen so far
        anchor = max(anchor, schedule[emp_idx][interval_idx].end)
        
        # 4. Push the next interval of the same employee into the heap
        if interval_idx + 1 < len(schedule[emp_idx]):
            next_interval = schedule[emp_idx][interval_idx + 1]
            heapq.heappush(min_heap, (next_interval.start, emp_idx, interval_idx + 1))
            
    return res

# =============================================================================
# STAFF SIGNAL: Sweep Line / Event Processing
# =============================================================================

def min_meeting_rooms_sweep_line(intervals):
    """
    Problem: Meeting Rooms II (Sweep Line Alternative).
    Logic: Treat starts and ends as separate events. 
    +1 when a meeting starts, -1 when it ends.
    The max value of the running sum is the number of rooms needed.
    """
    events = []
    for start, end in intervals:
        events.append((start, 1))  # Meeting starts
        events.append((end, -1))   # Meeting ends
    
    # Sort events. If times are equal, process end (-1) before start (+1)
    events.sort()
    
    curr_rooms = 0
    max_rooms = 0
    for time, type in events:
        curr_rooms += type
        max_rooms = max(max_rooms, curr_rooms)
        
    return max_rooms



# =============================================================================
# Example Usage for Employee Free Time
# =============================================================================
if __name__ == "__main__":
    # Employee 1: [[1,3], [6,7]], Employee 2: [[2,4]], Employee 3: [[2,5], [9,12]]
    sched = [
        [Interval(1, 3), Interval(6, 7)],
        [Interval(2, 4)],
        [Interval(2, 5), Interval(9, 12)]
    ]
    
    # Expected: Gap between 5 and 6, and Gap between 7 and 9
    print(f"Free Time Slots: {employee_free_time(sched)}")