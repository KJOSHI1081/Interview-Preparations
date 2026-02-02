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
    56. Merge Intervals

    Problem: Merge all overlapping intervals.
    
    Given an array of intervals where intervals[i] = [starti, endi],
      merge all overlapping intervals, and return an array of the 
      non-overlapping intervals that cover all the intervals in the input.
    Example 1:

    Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]
    Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
    Example 2:

    Input: intervals = [[1,4],[4,5]]
    Output: [[1,5]]
    Explanation: Intervals [1,4] and [4,5] are considered overlapping.
    Example 3:

    Input: intervals = [[4,7],[1,4]]
    Output: [[1,7]]
    Explanation: Intervals [1,4] and [4,7] are considered overlapping.

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
    57. Insert Interval
    Problem: 
    
    You are given an array of non-overlapping intervals intervals where 
    intervals[i] = [starti, endi] represent the start and the end of the ith interval and intervals
      is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] 
      that represents the start and end of another interval.

    Insert newInterval into intervals such that intervals is still sorted in ascending order by starti 
    and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).
    Return intervals after the insertion. 
    Note that you don't need to modify intervals in-place. You can make a new array and return it. 

    Example 1:

    Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
    Output: [[1,5],[6,9]]
    Example 2:

    Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
    Output: [[1,2],[3,10],[12,16]]
    Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].
    Insert a new interval into a sorted list and merge if necessary.
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

def meeting_rooms_ii(intervals,use_heap=False):
    """
    LeetCode #253: Meeting Rooms II.
    Problem: Find minimum number of conference rooms required.
        Given an array of meeting time intervals consisting of start and end times [[s1,e1],[s2,e2],...], 
        where s_i < e_i, find the minimum number of conference rooms required to hold all meetings.
        
        Example Walkthrough
        Input: intervals = [[0, 30], [5, 10], [15, 20]]

        Time 0: Meeting 1 starts [0, 30]. Rooms needed: 1
        Time 5: Meeting 2 starts [5, 10]. It overlaps with Meeting 1. Rooms needed: 2
        Time 10: Meeting 2 ends. One room becomes free. Rooms in use: 1
        Time 15: Meeting 3 starts [15, 20]. Meeting 1 is still going, 
            but Meeting 2's room is now empty. We reuse that room. Rooms in use: 2
        Time 20: Meeting 3 ends.
        Time 30: Meeting 1 ends.

        Result: The maximum number of simultaneous meetings was 2.
    Logic: Use a Min-Heap to track the end times of meetings currently in rooms.
    If a new meeting starts after the earliest meeting ends, reuse that room.
    """

    if not use_heap:
        sorted_starts = sorted(intervals, key=lambda x: x[0])
        sorted_ends = sorted(intervals, key=lambda x: x[1])
        s_i, e_i = 0, 0
        res = 0
        count = 0
        while s_i < len(sorted_starts):
            if sorted_starts[s_i] < sorted_ends[e_i]:
                count += 1
                s_i += 1
            else:
                count -= 1
                e_i += 1
            res = max(res, count)
        
        return res



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
    986. Interval List Intersections

    Problem: Find the intersection of two sets of sorted intervals.

    Input: firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]
    Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]

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

def employee_free_time(schedule, use_heap=False):
    """
    Problem: Find the common free time for all employees.
    Logic: 
    1. Use a Min-Heap to track the smallest start time across all employee schedules.
    2. Track the 'anchor' (the end time of the last processed work interval).
    3. If the next interval starts AFTER the anchor, the gap in between is free time.
    Complexity: O(N log K) where N is total intervals and K is number of employees.
    """

    if not use_heap:
        composite_calender = []
        #Flattening the calendar that includes all the employee schedule
        for emp_schedule in schedule:
            for interval in emp_schedule:
                composite_calender.append(interval)
        #Sorting them by their start time     
        composite_calender.sort(key=lambda x: x.start)

        #Using prev_end as initial farthest busiest end
        prev_end = composite_calender[0].end
        free_times = []
        for i in range(1, len(composite_calender)):
            curr = composite_calender[i]
            #check if any gap available
            if curr.start > prev_end:
                free_times.append(Interval(curr.start, prev_end))
            #update the farthest busiest end
            prev_end = max(prev_end, curr.end)
        return free_times




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