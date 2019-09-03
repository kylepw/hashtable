#!/usr/bin/env python
import hashlib
from random import randrange


def get_index(max=None):
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
        return f'Node {{{self.key}:{self.value}}} -> {self.next}'


class HashTable:
    def __init__(self):
        # array with linked nodes at each index
        self.db = []
        # Map hash value to array index
        self.hash_map = {}

    def read(self, key):
        pass

    def write(self, key=None, value=None):
        if key is None:
            return None
        hash_key = to_hash(key)
        if hash_key in self.hash_map:
            node = self._get_node(index=self.hash_map[hash_key], key=key)
        # Map hash to random index
        index = get_index(len(self.db)+1)
        node = self._write_node(index, key, value)
        self.hash_map[hash_key] = index

        return node

    def _get_node(self, index, key):
        """Return :obj:`Node` at array[index] with `key`"""
        node = self.db[index]
        if node.key == key:
            return node
        while (node):
            if node.key == key:
                return node
            node = node.next
        return node

    def _append_node(self, index, key, value):
        node = self.db[index]
        while (node.next):
            node = node.next
        node.next = Node(key, value)
        return node.next

    def _write_node(self, index, key, value):
        """Overwrite or append node value"""
        node = self._get_node(index, key)
        if node:
            node.value = value
        else:
            node = self._append_node(index, key, value)
        return node

