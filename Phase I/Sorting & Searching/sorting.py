def bubble_sort(nums): 
    #NOTE: it's stable sorting algorithm
    #At every pass the largest element comes at the end
    for i in range(len(nums)):
        for j in range(len(nums) - i - 1):
            if nums[j]>nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


def selection_sort_using_min(nums):
    #NOTE: it's unstable sorting algorithm
    for i in range(len(nums)):
        #At every pass the min element is in it's right position
        min_ix = i
        for j in range(i + 1, len(nums)):
            if nums[min_ix] > nums[j]:
                min_ix = j
        
        nums[i], nums[min_ix] = nums[min_ix], nums[i]
    return nums

def selection_sort_using_max(nums):
    #NOTE: it's unstable sorting algorithm
    for i in reversed(range(len(nums))):
        #At every pass the max element is put in it's right position
        max_ix = i
        for j in range(i):
            if nums[j] > nums[max_ix]:
                max_ix = j
        nums[max_ix], nums[i] = nums[i], nums[max_ix]
    return nums

def insertion_sort(nums):
    # Note: i + 1 is the element we are currently "inserting"
    for i in range(len(nums) - 1):
        # Start at i + 1 and move left as long as the element is smaller
        for j in range(i + 1, 0, -1):
            if nums[j] < nums[j - 1]:
                nums[j], nums[j - 1] = nums[j - 1], nums[j]
            else:
                # If it's not smaller, the left portion is already sorted
                break
    return nums
        
