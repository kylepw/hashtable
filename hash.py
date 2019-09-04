"""
    hash.py
    ~~~~~~~

    Simple hash table implementation.
    Based on: Cracking the Coding Interview, p.88

    >>> from hash import HashTable
    >>> t = HashTable()
    >>> t.get('hey')
    >>> t.set('hey', 123)
    Node {hey: 123}
    >>> t.get('hey')
    123
"""
from random import randrange


def to_hash(key, length=10):
    """Convert key to hash value.

    Args:
        key (:obj:): key value.
        length (int): length of hash value.

    Returns:
        str: hash value of key.
    """
    try:
        return abs(hash(key)) % (10 ** length)
    except TypeError:
        return abs(hash(str(key))) % (10 ** length)


class Node:
    """Linked list node"""

    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node

    def __repr__(self):
        return f'Node {{{self.key}: {self.value}}}'


class LinkedList:
    """Linked list of nodes"""

    def __init__(self, head=None):
        # First node
        self.head = head
        # Used for iteration
        self.current = self.head

    def __repr__(self):
        return f'LinkedList <{self.head}> -> ...'

    def __next__(self):
        if self.current is not None:
            node, self.current = self.current, self.current.next
            return node
        raise StopIteration

    def __iter__(self):
        return self

    def _append(self, key, value):
        """Append node to end of linked list"""
        node = self.head
        if node is None:
            self.head = self.current = Node(key, value)
            return self.head
        else:
            while node.next:
                node = node.next
            node.next = Node(key, value)
            return node.next

    def get(self, key):
        """Return :obj:`Node` with `key` key value"""
        node = self.head
        if node is None:
            return None
        if node.key == key:
            return node
        while node:
            if node.key == key:
                return node
            node = node.next
        return node

    def set(self, key, value):
        """Overwrite or append node value"""
        node = self.get(key)
        if node:
            node.value = value
        else:
            node = self._append(key, value)
        return node


class HashTable:
    """Represents simple hash table

        `get` flow:
        - Compute 'key' hash value
        - Map hash value to index in array
        - Traverse linked list at index
        - Return value of 'key' node or None

        `set` flow:
        - Convert 'key' to hash value
        - Map hash value to index in array (create index if necessary)
        - Traverse linked list at index
        - Set new value at 'key' node
        - If no 'key' node, append new 'key' node to end list
    """

    def __init__(self):
        # array of linked-lists
        self._lists = []
        # Map hash values to array indexes
        self._hash_map = {}

    def __repr__(self):
        return f'HashTable <{len(self._hash_map)} key/val pairs>'

    def _get_list(self, index):
        """Return `LinkedList` obj at `index` or None"""
        try:
            return self._lists[index]
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
            index = randrange(len(self._lists) + 1)
            lst = self._get_list(index)
            if not lst:
                self._lists.append(LinkedList())
                lst = self._lists[-1]
            node = lst.set(key, value)
            self._hash_map[hash_key] = index
        return node

    def keys(self):
        """Return all key values"""
        lists = [self._get_list(lst) for lst in self._list]
        return [to_key(k) for k in self._hash_map.keys()]
