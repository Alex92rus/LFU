import logging


class Dl_node:

    def __init__(self, value):
        self.prev = None
        self.value = value
        self.next = None


class DLinkedlist:

    def __init__(self, value):
        self.head = Dl_node(value)
        self.tail = self.head

    def add(self, value):
        self.tail.next = Dl_node(value)
        self.tail.next.prev = self.tail
        self.tail = self.tail.next

    def print(self):
        current = self.head
        print("None<->", end="")
        while current:
            print(f"{current.value}<->", end="")
            current = current.next
        print("End Of List", end="")

    def delete_head(self):
        if self.head is not None:
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None
            else:
                self.tail = None
        else:
            print("Empty List")


class LFUCache:

    def __init__(self, capacity):
        self.min_node = None
        self.capacity = capacity
        self.value_map = {}
        self.frequency_map = {}
        self.key_doubly_list_map = {}

    def retrieve(self, key):
        if key in self.value_map:  # is the key in the cache map
            try:
                node: Dl_node = self.frequency_map[key]
                dict_keys: set = self.key_doubly_list_map[node]
                dict_keys.remove(key)  # remove the key from its frequency sibling keys
                if len(dict_keys) == 0:  # if the key was alone with this frequency, remove the frequency from the list
                    if node.next is not None and node.next.value == node.value + 1:
                        next_set: set = self.key_doubly_list_map[node.next]
                        next_set.add(key)
                        node.next.prev = node.prev
                        node.prev.next = node.next
                        self.frequency_map[key] = node.next
                    else:  # reuse the same node just update its frequency
                        node.value += 1
                        dict_keys.add(key)
                else:
                    if node.next is not None and node.next.value == node.value + 1:
                        next_set: set = self.key_doubly_list_map[node.next]
                        next_set.add(key)
                        self.frequency_map[key] = node.next
                    else:
                        tmp_next = Dl_node(node.value + 1)
                        tmp_next.next = node.next
                        tmp_next.prev = node
                        node.next = tmp_next
                        self.frequency_map[key] = tmp_next
                        self.key_doubly_list_map[tmp_next] = {key}
            except Exception as ex:
                logging.log(logging.WARN, 'The Initialisation of the LFUis  incorrect')
                raise Exception('Invalid Setup of LRU')
            return self.value_map[key]
        else:
            return None

    def write(self, key, value):
        if key not in self.frequency_map:
            if self.min_node is None:
                self.min_node = Dl_node(0)
                self.key_doubly_list_map[self.min_node] = set()
            if len(self.value_map.keys()) == self.capacity:
                min_set: set = self.key_doubly_list_map[self.min_node]
                evict_key = min_set.pop()
                self.frequency_map.pop(evict_key)
                self.value_map.pop(evict_key)
            self.value_map[key] = value
            if self.min_node.value == 0:
                min_set: set = self.key_doubly_list_map[self.min_node]
                min_set.add(key)
                self.frequency_map[key] = self.min_node
            else:
                new_node = Dl_node(0)
                tmp_node = self.min_node
                if self.key_doubly_list_map[self.min_node] is None or len(self.key_doubly_list_map[self.min_node]) == 0:
                    tmp_node = self.min_node.next
                new_node.next = tmp_node
                tmp_node.prev = new_node
                self.min_node = new_node
                self.key_doubly_list_map[self.min_node] = {key}
                self.frequency_map[key] = new_node
        else:
            self.value_map[key] = value

    def print(self):
        current = self.min_node
        print("None<->", end="")
        while current:
            print(f"{current.value}<->", end="")
            current = current.next
        print("End Of List")



if __name__ == '__main__':
    dl_list = DLinkedlist(5)
    dl_list.add(6)
    dl_list.add(7)
    dl_list.print()
    dl_list.delete_head()
    print()
    dl_list.print()

    a_cache: LFUCache = LFUCache(3)
    a_cache.write(10, 'a')
    a_cache.write(20, 'b')
    a_cache.write(30, 'c')
    a_cache.retrieve(30)
    a_cache.retrieve(30)
    a_cache.retrieve(30)
    a_cache.retrieve(20)
    a_cache.retrieve(20)
    a_cache.retrieve(10)
    a_cache.retrieve(20)
    a_cache.retrieve(20)
    a_cache.retrieve(20)
    a_cache.retrieve(20)
    a_cache.retrieve(20)
    a_cache.print()
    a_cache.write(50, 'c')
    a_cache.retrieve(50)
    a_cache.retrieve(30)
    a_cache.print()




































