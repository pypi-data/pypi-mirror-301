import json
import os
import argparse
from typing import List, Union, Tuple
import random

import bisect
import math

import itertools

from prettytable import PrettyTable
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def bubble_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def insertion_sort(arr: List[int]) -> List[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def selection_sort(arr: List[int]) -> List[int]:
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def heap_sort(arr: List[int]) -> List[int]:
    def heapify(arr: List[int], n: int, i: int):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

def shell_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def counting_sort(arr: List[int]) -> List[int]:
    max_val = max(arr)
    min_val = min(arr)
    range_of_values = max_val - min_val + 1
    count = [0] * range_of_values
    output = [0] * len(arr)

    for i in arr:
        count[i - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1

    return output

def radix_sort(arr: List[int]) -> List[int]:
    def counting_sort_for_radix(arr: List[int], exp: int) -> List[int]:
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = arr[i] // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    return arr

def bucket_sort(arr: List[int]) -> List[int]:
    max_val = max(arr)
    min_val = min(arr)
    bucket_range = (max_val - min_val) / len(arr)
    buckets = [[] for _ in range(len(arr) + 1)]

    for num in arr:
        bucket_index = int((num - min_val) // bucket_range)
        if bucket_index == len(arr):
            bucket_index -= 1
        buckets[bucket_index].append(num)

    sorted_arr = []
    for bucket in buckets:
        insertion_sort(bucket)
        sorted_arr.extend(bucket)

    return sorted_arr

# Новые алгоритмы сортировки

def comb_sort(arr: List[int]) -> List[int]:
    gap = len(arr)
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True

        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False

    return arr

def cocktail_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        swapped = False

        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        if not swapped:
            break

        swapped = False
        end = end - 1

        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        start = start + 1

    return arr

def gnome_sort(arr: List[int]) -> List[int]:
    index = 0
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

def cycle_sort(arr: List[int]) -> List[int]:
    for cycle_start in range(0, len(arr) - 1):
        item = arr[cycle_start]
        pos = cycle_start

        for i in range(cycle_start + 1, len(arr)):
            if arr[i] < item:
                pos += 1

        if pos == cycle_start:
            continue

        while item == arr[pos]:
            pos += 1

        arr[pos], item = item, arr[pos]

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(arr)):
                if arr[i] < item:
                    pos += 1

            while item == arr[pos]:
                pos += 1

            arr[pos], item = item, arr[pos]

    return arr

def pigeonhole_sort(arr: List[int]) -> List[int]:
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1

    holes = [0] * size

    for x in arr:
        holes[x - min_val] += 1

    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + min_val
            i += 1

    return arr

def strand_sort(arr: List[int]) -> List[int]:
    def merge_lists(a: List[int], b: List[int]) -> List[int]:
        result = []
        while a and b:
            if a[0] <= b[0]:
                result.append(a.pop(0))
            else:
                result.append(b.pop(0))
        result.extend(a)
        result.extend(b)
        return result

    result = []
    while arr:
        sublist = [arr.pop(0)]
        i = 0
        while i < len(arr):
            if arr[i] > sublist[-1]:
                sublist.append(arr.pop(i))
            else:
                i += 1
        result = merge_lists(result, sublist)
    return result

def pancake_sort(arr: List[int]) -> List[int]:
    def flip(arr: List[int], k: int):
        left = 0
        while left < k:
            arr[left], arr[k] = arr[k], arr[left]
            k -= 1
            left += 1

    for i in range(len(arr) - 1, 0, -1):
        max_idx = 0
        for j in range(1, i + 1):
            if arr[j] > arr[max_idx]:
                max_idx = j
        if max_idx != i:
            flip(arr, max_idx)
            flip(arr, i)
    return arr

def bogo_sort(arr: List[int]) -> List[int]:
    def is_sorted(arr: List[int]) -> bool:
        return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))

    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

def stooge_sort(arr: List[int]) -> List[int]:
    def stooge(arr: List[int], i: int, h: int):
        if i >= h:
            return

        if arr[i] > arr[h]:
            arr[i], arr[h] = arr[h], arr[i]

        if h - i + 1 > 2:
            t = (h - i + 1) // 3
            stooge(arr, i, h - t)
            stooge(arr, i + t, h)
            stooge(arr, i, h - t)

    stooge(arr, 0, len(arr) - 1)
    return arr

def tim_sort(arr: List[int]) -> List[int]:
    min_run = 32
    n = len(arr)

    for i in range(0, n, min_run):
        insertion_sort(arr[i:min(i + min_run, n)])

    size = min_run
    while size < n:
        for start in range(0, n, size * 2):
            midpoint = start + size - 1
            end = min((start + size * 2 - 1), (n-1))
            merged_array = merge(
                left=arr[start:midpoint + 1],
                right=arr[midpoint + 1:end + 1])
            arr[start:start + len(merged_array)] = merged_array

        size *= 2

    return arr

def comb_sort(arr: List[int]) -> List[int]:
    gap = len(arr)
    shrink = 1.3
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True

        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False

    return arr

def shell_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

    return arr

def counting_sort(arr: List[int]) -> List[int]:
    max_val = max(arr)
    min_val = min(arr)
    range_of_values = max_val - min_val + 1
    
    count = [0] * range_of_values
    output = [0] * len(arr)

    for i in arr:
        count[i - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1

    return output

def introsort(arr: List[int]) -> List[int]:
    def introsort_helper(arr: List[int], start: int, end: int, depth_limit: int):
        size = end - start
        if size < 16:
            insertion_sort_range(arr, start, end)
        elif depth_limit == 0:
            heapsort_range(arr, start, end)
        else:
            pivot = partition(arr, start, end)
            introsort_helper(arr, start, pivot, depth_limit - 1)
            introsort_helper(arr, pivot + 1, end, depth_limit - 1)

    def insertion_sort_range(arr: List[int], start: int, end: int):
        for i in range(start + 1, end):
            key = arr[i]
            j = i - 1
            while j >= start and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    def heapsort_range(arr: List[int], start: int, end: int):
        def sift_down(arr: List[int], start: int, end: int, root: int):
            while True:
                child = 2 * (root - start) + 1 + start
                if child >= end:
                    break
                if child + 1 < end and arr[child] < arr[child + 1]:
                    child += 1
                if arr[root] >= arr[child]:
                    break
                arr[root], arr[child] = arr[child], arr[root]
                root = child

        for i in range((end - start - 2) // 2 + start, start - 1, -1):
            sift_down(arr, start, end, i)

        for i in range(end - 1, start, -1):
            arr[start], arr[i] = arr[i], arr[start]
            sift_down(arr, start, i, start)

    def partition(arr: List[int], start: int, end: int) -> int:
        pivot = arr[end - 1]
        i = start - 1
        for j in range(start, end - 1):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[end - 1] = arr[end - 1], arr[i + 1]
        return i + 1

    max_depth = 2 * math.floor(math.log2(len(arr)))
    introsort_helper(arr, 0, len(arr), max_depth)
    return arr

def bitonic_sort(arr: List[int]) -> List[int]:
    def compare_and_swap(arr: List[int], i: int, j: int, direction: int):
        if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
            arr[i], arr[j] = arr[j], arr[i]

    def bitonic_merge(arr: List[int], low: int, count: int, direction: int):
        if count > 1:
            k = count // 2
            for i in range(low, low + k):
                compare_and_swap(arr, i, i + k, direction)
            bitonic_merge(arr, low, k, direction)
            bitonic_merge(arr, low + k, k, direction)

    def bitonic_sort_recursive(arr: List[int], low: int, count: int, direction: int):
        if count > 1:
            k = count // 2
            bitonic_sort_recursive(arr, low, k, 1)
            bitonic_sort_recursive(arr, low + k, k, 0)
            bitonic_merge(arr, low, count, direction)

    def pad_to_power_of_two(arr: List[int]) -> List[int]:
        n = len(arr)
        next_power_of_two = 2 ** math.ceil(math.log2(n))
        return arr + [float('inf')] * (next_power_of_two - n)

    padded_arr = pad_to_power_of_two(arr)
    bitonic_sort_recursive(padded_arr, 0, len(padded_arr), 1)
    return [x for x in padded_arr if x != float('inf')]

def odd_even_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    sorted = False
    while not sorted:
        sorted = True
        for i in range(1, n-1, 2):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                sorted = False
        for i in range(0, n-1, 2):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                sorted = False
    return arr

def tree_sort(arr: List[int]) -> List[int]:
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    def insert(root, val):
        if root is None:
            return Node(val)
        if val < root.val:
            root.left = insert(root.left, val)
        else:
            root.right = insert(root.right, val)
        return root

    def inorder(root, result):
        if root:
            inorder(root.left, result)
            result.append(root.val)
            inorder(root.right, result)

    root = None
    for num in arr:
        root = insert(root, num)
    
    result = []
    inorder(root, result)
    return result

def patience_sort(arr: List[int]) -> List[int]:
    piles = []
    for num in arr:
        new_pile = [num]
        i = bisect.bisect_left(piles, new_pile)
        if i != len(piles):
            piles[i].append(num)
        else:
            piles.append(new_pile)
    
    result = []
    while piles:
        smallest_pile = min(piles, key=lambda x: x[-1])
        result.append(smallest_pile.pop())
        if not smallest_pile:
            piles.remove(smallest_pile)
    
    return result[::-1]

def smooth_sort(arr: List[int]) -> List[int]:
    def down_heap(arr, k, n):
        new_elem = arr[k]
        while k <= n // 2:
            child = 2 * k
            if child < n and arr[child] < arr[child + 1]:
                child += 1
            if new_elem >= arr[child]:
                break
            arr[k] = arr[child]
            k = child
        arr[k] = new_elem

    def heap_sort(arr):
        n = len(arr)
        for i in range(n // 2 - 1, -1, -1):
            down_heap(arr, i, n - 1)
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            down_heap(arr, 0, i - 1)

    heap_sort(arr)
    return arr

def tournament_sort(arr: List[int]) -> List[int]:
    def create_tournament(arr):
        n = len(arr)
        tournament = [0] * (2 * n)
        for i in range(n):
            tournament[n + i] = i
        for i in range(n - 1, 0, -1):
            tournament[i] = tournament[2 * i] if arr[tournament[2 * i]] < arr[tournament[2 * i + 1]] else tournament[2 * i + 1]
        return tournament

    def adjust_tournament(tournament, arr, index):
        n = len(arr)
        while index > 1:
            index = index // 2
            left = tournament[2 * index]
            right = tournament[2 * index + 1]
            tournament[index] = left if arr[left] < arr[right] else right

    n = len(arr)
    tournament = create_tournament(arr)
    result = []
    for _ in range(n):
        winner = tournament[1]
        result.append(arr[winner])
        arr[winner] = float('inf')
        adjust_tournament(tournament, arr, n + winner)
    return result

def library_sort(arr: List[int]) -> List[int]:
    def insert(arr, gaps, item):
        i = bisect.bisect_left(arr, item)
        if i < len(arr) and arr[i] == 0:
            arr[i] = item
        else:
            while i < len(arr) and arr[i] != 0:
                i += 1
            if i == len(arr):
                arr.append(item)
                gaps.append(0)
            else:
                arr[i] = item
        return i

    n = len(arr)
    sorted_arr = [0] * (2 * n)
    gaps = [0] * (2 * n)
    for i in range(0, n, 2):
        sorted_arr[i] = arr[i // 2]
    
    for i in range(1, n, 2):
        insert(sorted_arr, gaps, arr[i // 2])
    
    return [x for x in sorted_arr if x != 0]

def block_sort(arr: List[int]) -> List[int]:
    def insertion_sort(arr, left, right):
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    def merge(arr, left, mid, right):
        left_arr = arr[left:mid+1]
        right_arr = arr[mid+1:right+1]
        i = j = 0
        k = left
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1

    block_size = 32
    for i in range(0, len(arr), block_size):
        insertion_sort(arr, i, min(i + block_size - 1, len(arr) - 1))
    
    curr_size = block_size
    while curr_size < len(arr):
        for start in range(0, len(arr), curr_size * 2):
            mid = start + curr_size - 1
            end = min(start + curr_size * 2 - 1, len(arr) - 1)
            merge(arr, start, mid, end)
        curr_size *= 2
    
    return arr

def double_selection_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    for i in range(n // 2):
        min_idx = i
        max_idx = i
        for j in range(i + 1, n - i):
            if arr[j] < arr[min_idx]:
                min_idx = j
            if arr[j] > arr[max_idx]:
                max_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if max_idx == i:
            max_idx = min_idx
        if max_idx != n - i - 1:
            arr[n - i - 1], arr[max_idx] = arr[max_idx], arr[n - i - 1]
    return arr

def spaghetti_sort(arr: List[int]) -> List[int]:
    if not arr:
        return arr
    max_val = max(arr)
    spaghetti = [[] for _ in range(max_val + 1)]
    for num in arr:
        spaghetti[num].append(num)
    return [num for bucket in spaghetti for num in bucket]

def brick_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    sorted = False
    while not sorted:
        sorted = True
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted = False
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted = False
    return arr

def cycle_sort_optimized(arr: List[int]) -> List[int]:
    for cycle_start in range(len(arr) - 1):
        item = arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, len(arr)):
            if arr[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(arr)):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
    return arr

def exchange_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr

def permutation_sort(arr: List[int]) -> List[int]:
    return list(min(itertools.permutations(arr)))

def sleep_sort(arr: List[int]) -> List[int]:
    import threading
    import time
    
    result = []
    def add_to_result(x):
        time.sleep(x * 0.1)
        result.append(x)
    
    threads = []
    for i in arr:
        thread = threading.Thread(target=add_to_result, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return result

def tag_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    tagged = [(arr[i], i) for i in range(n)]
    tagged.sort(key=lambda x: x[0])
    for i in range(n):
        arr[i] = tagged[i][0]
    return arr

def binary_insertion_sort(arr: List[int]) -> List[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        left, right = 0, i - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] < key:
                left = mid + 1
            else:
                right = mid - 1
        for j in range(i - 1, left - 1, -1):
            arr[j + 1] = arr[j]
        arr[left] = key
    return arr

def franceschini_sort(arr: List[int]) -> List[int]:
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = sort(arr[:mid])
        right = sort(arr[mid:])
        return merge(left, right)

    return sort(arr)

def j_sort(arr: List[int]) -> List[int]:
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def slow_sort(arr: List[int]) -> List[int]:
    def slow_sort_recursive(arr, i, j):
        if i >= j:
            return
        m = (i + j) // 2
        slow_sort_recursive(arr, i, m)
        slow_sort_recursive(arr, m + 1, j)
        if arr[m] > arr[j]:
            arr[m], arr[j] = arr[j], arr[m]
        slow_sort_recursive(arr, i, j - 1)

    slow_sort_recursive(arr, 0, len(arr) - 1)
    return arr

def read_numbers(file_path: str) -> List[int]:
    _, ext = os.path.splitext(file_path)
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        numbers = [int(num.strip()) for num in content.replace('\n', ',').split(',') if num.strip()]
    elif ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as f:
            numbers = json.load(f)
    else:
        raise ValueError("Неподдерживаемый формат файла. Используйте .txt или .json")
    return numbers

def write_to_file(numbers: List[int], file_path: str, output_format: str = 'json') -> None:
    if output_format == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"sorted_numbers": numbers}, f, indent=2)
    elif output_format == 'pretty_json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"sorted_numbers": numbers}, f, indent=2)
    else:
        formatted_output = format_output(numbers, output_format)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_output)

def format_output(numbers: List[int], output_format: str) -> str:
    if output_format == 'brackets':
        return f"[{', '.join(map(str, numbers))}]"
    elif output_format == 'curly_braces':
        return f"{{{', '.join(map(str, numbers))}}}"
    elif output_format == 'parentheses':
        return f"({', '.join(map(str, numbers))})"
    elif output_format == 'no_commas':
        return ' '.join(map(str, numbers))
    elif output_format == 'spaces':
        return ' '.join(map(str, numbers))
    elif output_format == 'vertical':
        return '\n'.join(map(str, numbers))
    elif output_format == 'horizontal':
        return ' '.join(map(str, numbers))
    elif output_format == 'csv':
        return ','.join(map(str, numbers))
    elif output_format == 'tab_separated':
        return '\t'.join(map(str, numbers))
    elif output_format == 'json':
        json_str = json.dumps({"sorted_numbers": numbers}, indent=2)
        return highlight(json_str, JsonLexer(), TerminalFormatter())
    elif output_format == 'pretty_json':
        json_str = json.dumps({"sorted_numbers": numbers}, indent=2)
        return highlight(json_str, JsonLexer(), TerminalFormatter())
    elif output_format == 'bullet_points':
        return '\n'.join(f'• {num}' for num in numbers)
    elif output_format == 'numbered_list':
        return '\n'.join(f'{i+1}. {num}' for i, num in enumerate(numbers))
    elif output_format == 'html_list':
        return f"<ul>\n{''.join(f'  <li>{num}</li>\n' for num in numbers)}</ul>"
    elif output_format == 'xml':
        return f"<numbers>\n{''.join(f'  <number>{num}</number>\n' for num in numbers)}</numbers>"
    elif output_format == 'yaml':
        return '- ' + '\n- '.join(map(str, numbers))
    elif output_format == 'markdown_table':
        table = PrettyTable()
        table.field_names = ["Index", "Number"]
        for i, num in enumerate(numbers):
            table.add_row([i+1, num])
        return table.get_string()
    elif output_format == 'latex_array':
        return f"\\begin{{array}}{{c}}\n{' \\\\ '.join(map(str, numbers))}\n\\end{{array}}"
    elif output_format == 'binary':
        return ' '.join(format(num, '08b') for num in numbers)
    elif output_format == 'hexadecimal':
        return ' '.join(format(num, '02X') for num in numbers)
    elif output_format == 'scientific_notation':
        return ' '.join(f'{num:.2e}' for num in numbers)
    elif output_format == 'percentage':
        max_num = max(numbers)
        return ' '.join(f'{(num/max_num)*100:.2f}%' for num in numbers)
    else:
        raise ValueError(f"Неподдерживаемый формат вывода: {output_format}")
    
def allsort():
    algorithms = [
        'merge', 'quick', 'bubble', 'insertion', 'selection', 'heap', 'shell',
        'counting', 'radix', 'bucket', 'comb', 'cocktail', 'gnome', 'cycle',
        'pigeonhole', 'strand', 'pancake', 'bogo', 'stooge', 'tim',
        'intro', 'bitonic', 'odd_even', 'tree', 'patience', 'smooth',
        'tournament', 'library', 'block', 'double_selection', 'spaghetti',
        'brick', 'cycle_optimized', 'exchange', 'permutation', 'sleep',
        'tag', 'binary_insertion', 'franceschini', 'j_sort', 'slow'
    ]
    print("Available sorting algorithms:")
    for algo in algorithms:
        print(f"- {algo}")

def allformat():
    output_formats = [
        'brackets', 'curly_braces', 'parentheses', 'no_commas', 'spaces',
        'vertical', 'horizontal', 'csv', 'tab_separated', 'json', 'pretty_json',
        'bullet_points', 'numbered_list', 'html_list', 'xml', 'yaml',
        'markdown_table', 'latex_array', 'binary', 'hexadecimal',
        'scientific_notation', 'percentage'
    ]
    print("Available output formats:")
    for fmt in output_formats:
        print(f"- {fmt}")

def sort_numbers(numbers: List[int], algorithm: str, output_format: str, output_path: str = None) -> Tuple[List[int], str]:
    algorithms = {
        'merge': merge_sort,
        'quick': quick_sort,
        'bubble': bubble_sort,
        'insertion': insertion_sort,
        'selection': selection_sort,
        'heap': heap_sort,
        'shell': shell_sort,
        'counting': counting_sort,
        'radix': radix_sort,
        'bucket': bucket_sort,
        'comb': comb_sort,
        'cocktail': cocktail_sort,
        'gnome': gnome_sort,
        'cycle': cycle_sort,
        'pigeonhole': pigeonhole_sort,
        'strand': strand_sort,
        'pancake': pancake_sort,
        'bogo': bogo_sort,
        'stooge': stooge_sort,
        'tim': tim_sort,
        'comb': comb_sort,
        'shell': shell_sort,
        'counting': counting_sort,
        'intro': introsort,
        'bitonic': bitonic_sort,
        'odd_even': odd_even_sort,
        'tree': tree_sort,
        'patience': patience_sort,
        'smooth': smooth_sort,
        'tournament': tournament_sort,
        'library': library_sort,
        'block': block_sort,
        'double_selection': double_selection_sort,
        'spaghetti': spaghetti_sort,
        'brick': brick_sort,
        'cycle_optimized': cycle_sort_optimized,
        'exchange': exchange_sort,
        'permutation': permutation_sort,
        'sleep': sleep_sort,
        'tag': tag_sort,
        'binary_insertion': binary_insertion_sort,
        'franceschini': franceschini_sort,
        'j_sort': j_sort,
        'slow': slow_sort
    }

    if algorithm not in algorithms:
        raise ValueError(f"Unsupported algorithm. Choose from: {', '.join(algorithms.keys())}")

    sorted_numbers = algorithms[algorithm](numbers)
    formatted_output = format_output(sorted_numbers, output_format)

    if output_path:
        with open(output_path, 'w') as f:
            f.write(formatted_output)
        print(f"Sorted list saved to {output_path}")

    return sorted_numbers, formatted_output

def main():
    parser = argparse.ArgumentParser(description="Sorting library")
    parser.add_argument("input", nargs='?', help="Input numbers or path to the input file")
    parser.add_argument("algorithm", nargs='?', choices=[
        "merge", "quick", "bubble", "insertion", "selection", "heap", "shell",
        "counting", "radix", "bucket", "comb", "cocktail", "gnome", "cycle",
        "pigeonhole", "strand", "pancake", "bogo", "stooge", "tim",
        "intro", "bitonic", "odd_even", "tree", "patience", "smooth",
        "tournament", "library", "block", "double_selection", "spaghetti",
        "brick", "cycle_optimized", "exchange", "permutation", "sleep",
        "tag", "binary_insertion", "franceschini", "j_sort", "slow"
    ], help="Sorting algorithm to use")
    parser.add_argument("--output_format", default="brackets", choices=[
        'brackets', 'curly_braces', 'parentheses', 'no_commas', 'spaces', 'vertical',
        'horizontal', 'csv', 'tab_separated', 'json', 'pretty_json', 'bullet_points',
        'numbered_list', 'html_list', 'xml', 'yaml', 'markdown_table', 'latex_array',
        'binary', 'hexadecimal', 'scientific_notation', 'percentage'
    ], help="Output format")
    parser.add_argument("--output_file", help="Path to the output file (optional)")
    parser.add_argument("--allsort", action="store_true", help="Show all available sorting algorithms")
    parser.add_argument("--allformat", action="store_true", help="Show all available output formats")

    args = parser.parse_args()

    if args.allsort:
        allsort()
        return

    if args.allformat:
        allformat()
        return

    if not args.input or not args.algorithm:
        parser.print_help()
        return

    try:
        # Check if input is a file or a list of numbers
        if os.path.isfile(args.input):
            numbers = read_numbers(args.input)
        else:
            numbers = [int(x) for x in args.input.split(',')]
        
        sorted_numbers, formatted_output = sort_numbers(numbers, args.algorithm, args.output_format, args.output_file)
        
        if not args.output_file:
            print(formatted_output)
    except ValueError as e:
        print(f"Error: {str(e)}")
        if "algorithm" in str(e):
            print("\nAvailable sorting algorithms:")
            allsort()
        elif "output format" in str(e):
            print("\nAvailable output formats:")
            allformat()
        else:
            print("\nAvailable sorting algorithms:")
            allsort()
            print("\nAvailable output formats:")
            allformat()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()