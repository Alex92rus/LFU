# Efficient LFU Implementation with Sorting of Item Frequencies

## Overview
This repository contains an implementation of the Least Frequently Used (LFU) cache eviction algorithm with sorting. The LFU algorithm is a caching strategy that prioritizes items based on their frequency of use, ensuring that the least frequently used items are evicted first when the cache reaches its capacity.

## Features
- **Efficient Cache Management**: Utilizes a sorted data structure - doubly linked list, to keep track of item frequencies and read, add or evict the least frequently used items in O(1).
- **Configurable Cache Size**: Allows you to set the maximum size of the cache.
- **Thread Safety**: Ensures thread safety for concurrent access to the cache.

## Implementation

The implementation of the LRU cache is done in Python (3.12), using only built ins - there is no need to install requirements.txt
packages.

The main class - LFUCache has four methods in total, methods to read and write to the cache, a constructor and a printing function to display
what resides currently in the cache for debugging purpose.

- **constructor**: creates a LFU cache provided with a capacity.
- **retrieve method**: attempt to retrieve an item from the cache. This adds a unit (1) frequency to the key which is provided **only** if the key is already in the cache
- **write method**: writes a key, value pair item into the cache. This method excludes an item from the cache if the cache is full when the addition is called.

### Complexity

The LRU cache uses three data structures

- **value_map: dictionary**: Map which contains the items in the cache. Strings, numbers, and tuples work as keys, and any type can be a value.
Other types may or may not work correctly as keys, strings and tuples work cleanly since they are immutable.
- **frequency_map: dictionary**: Map which contains the frequencies for the keys in the cache.
- **key_doubly_list_map: dictionary**: a *doubly linked list* storing the sorted frequencies connected to a key set map storing the keys with the same frequency.

### Sorting

The frequencies are sorted in the doubly linked list which nodes are mapped as keys in the key_doubly_list_map: dictionary. Efficient sorting
can be achieved on the frequencies because at **every addition of a unit to a frequency we have to spend O(1) operations**.
Therefore, our sorting complexity is split across all the calls of the retrieve method.

Proving the following lemma:
At every addition of 1 there can be a maximum of 1 alteration in the frequencies:
1. Empty cache
starting a new frequency doubly linked list with a single frequency of 1 - O(1),
2. Addition of 1 to any of the keys having the kth frequency with the value of n:
 - 2.1 (n + 1) is not a frequency - add a new frequency node to the list between the kth and k+1 frequencies - O(1).
 - 2.2 (n + 1) is a frequency - move the key from the kth frequency to the k+1 frequency set = O(1).
 - if the key is the only with frequency of n - remove the kth frequency and relink the list - O(1).
 - 2.3 if the key is the only with frequency of n and (n + 1) is not a frequency increment the frequency of the node in place - O(1).

Using the above proof we can update the frequency list on every read operation.
Mind that here we take advantage of two constraints (updating a single number at a time, updating a number with only one value),
and in total the whole sorting would be O(c), where c is the number of
retrieve hit calls to the cache, which is equal to the sum of all frequencies in the cache.

When writing a new key, value into the cache, we define a object instance variable min_node to track the head of the list.
We evict a key from the set mapped to new_node if the capacity has already been reached.
We create the head of the doubly linked frequency list if it is the first item inserted in the cache, which will have a 0 frequency and 1 key.
We write the key, value pair in the cache value map, if the key is already there, the value is overridden to the new from te call.

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/Alex92rus/LFU
   python lfu_cache.py