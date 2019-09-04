#!/usr/bin/env python
from random import randrange


def gen_index(max=None):
    """Generate random integer from 0 to max"""
    if max is None:
        return None
    return randrange(max)

def to_hash(key, length=10):
    """Convert :obj:`str` to hash `int` value"""
    try:
        return abs(hash(key)) % (10 ** length)
    except TypeError:
        return abs(hash(str(key))) % (10 ** length)


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
        return f'Linked-list: {{{self.head}}} -> ...'

    def get(self, key):
        """Return :obj:`Node` with `key`"""
        node = self.head
        if node is None:
            return None
        if node.key == key:
            return node
        while (node):
            if node.key == key:
                return node
            node = node.next
        return node

    def _append(self, key, value):
        node = self.head
        if node is None:
            self.head = Node(key, value)
            return self.head
        else:
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
        Example of simple hash table implementation.

        (Reference: Cracking the Coding Interview p.88)
        >>> from hash import HashTable
        >>> t = HashTable()
        >>> t.get('hey')
        >>> t.set('hey', 123)
        Node {hey: 123}
        >>> t.get('hey')
        123

        Get:
        - Compute 'key' hash value
        - Map hash value to index in array
        - Traverse linked-list at index until 'key' node
        - Return value of node

        Set:
        - Convert 'key' to hash value
        - Find array index associated with hash value
        - If no array index, map an index to hash value
        - Traverse linked list until 'key' node found
        - Set new value
        - If not found, append new node to end of linked list
    """
    def __init__(self):
        # array of linked-lists
        self._db = []
        # Map hash values to array indexes
        self._hash_map = {}

    def __repr__(self):
        return f'HashTable obj <{len(self._hash_map)} key/val pairs>'

    def _get_list(self, index):
        """Return :obj:`LinkedList` or None"""
        try:
            return self._db[index]
        except IndexError:
            return None

    def get(self, key):
        hash_key = to_hash(key)
        if hash_key not in self._hash_map:
            return None
        index = self._hash_map[hash_key]
        lst = self._get_list(index)
        if lst and lst.get(key):
            return lst.get(key).value

    def set(self, key=None, value=None):
        if key is None:
            return None
        hash_key = to_hash(key)
        if hash_key in self._hash_map:
            lst = self._get_list(index=self._hash_map[hash_key])
            node = lst.set(key, value)
        else:
            # Map hash to random index
            index = gen_index(len(self._db)+1)
            lst = self._get_list(index)
            if not lst:
                self._db.append(LinkedList())
                lst = self._db[-1]
            node = lst.set(key, value)
            self._hash_map[hash_key] = index
        return node
