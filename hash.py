#!/usr/bin/env python
import hashlib
from random import randrange


def gen_index(max=None):
    """Generate random integer from 0 to max"""
    if max is None:
        return None
    return randrange(max)
    
def to_hash(key, length=10):
    """Convert :obj:`str` to hash `int` value"""
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % (10 ** length)


class Node:
    """Linked-list node"""
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node

    def __repr__(self):
        return f'Node {{{self.key}: {self.value}}}'

class LinkedList:
    """Linked-list of nodes"""
    def __init__(self, head=None):
        self.head = head

    def __repr__(self):
        return f'Linked-list: {{{self.head.key}: {self.head.value}}} -> {self.head.next}'

    def get(self, key):
        """Return :obj:`Node` with `key`"""
        node = self.head
        if node.key == key:
            return node
        while (node):
            if node.key == key:
                return node
            node = node.next
        return node

    def _append(self, key, value):
        node = self.head
        while (node.next):
            node = node.next
        node.next = Node(key, value)
        return node.next

    def set(self, key, value):
        """Overwrite or append node value"""
        node = self.get(key)
        if node:
            node.value = value
        else:
            node = self._append(key, value)
        return node

class HashTable:
    """
        Example of hash table.

        Get 'value' of 'key':
        - Convert 'key' to hash value
        - At array index associated with hash value
        - Traverse linked list until 'key' node found
        - Return value of node

        Set 'value' of 'key':
        - Convert 'key' to hash value
        - Find array index associated with hash value
        - If no array index, map an index to hash value
        - Traverse linked list until 'key' node found
        - Set new value
        - If not found, append new node to end of linked list
    """
    def __init__(self):
        # array of linked-lists
        self.db = []
        # Map hash values to array indexes
        self.hash_map = {}

    def _get_list(self, index):
        """Return :obj:`LinkedList` or None"""
        try:
            return self.db[index]
        except IndexError:
            return None

    def get(self, key):
        hash_key = to_hash(key)
        print(self.hash_map)
        if hash_key not in self.hash_map:
            return None
        index = self.hash_map[hash_key]
        lst = self._get_list(index)
        if lst and lst.get(key):
            return lst.get(key).value

    def set(self, key=None, value=None):
        if key is None:
            return None
        hash_key = to_hash(key)
        if hash_key in self.hash_map:
            lst = self._get_list(index=self.hash_map[hash_key])
            node = lst.set(key, value)
        else:
            # Map hash to random index
            index = gen_index(len(self.db)+1)
            lst = self._get_list(index)
            if not lst:
                self.db.append(LinkedList())
                lst = self.db[-1]
            node = lst.set(key, value)
            self.hash_map[hash_key] = index
        return node
