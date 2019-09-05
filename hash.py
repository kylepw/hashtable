"""
    hash.py
    ~~~~~~~

    Simple hash table implementation.

    >>> from hash import Hashtable
    >>> t = Hashtable()
    >>> t.set('hey', 123)
    Node {hey: 123}
    >>> t.set(678, 456.5)
    Node {678, 456.5}
    >>> t.get('hey', 678)
    (123, 456.5)
"""


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
        # Iteration placeholder
        self.current = self.head

    def __repr__(self):
        return f'LinkedList <{self.head}> -> ...'

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is not None:
            node, self.current = self.current, self.current.next
            return node
        # Reset
        self.current = self.head
        raise StopIteration

    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count

    def _append(self, key, value):
        """Append node to end of linked list"""
        node = self.head
        if node is None:
            self.head = Node(key, value)
            self.current = self.head
            return self.head
        else:
            while node.next:
                node = node.next
            node.next = Node(key, value)
            return node.next

    def get(self, key):
        """Return :obj:`Node` with `key`"""
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


class Hashtable:
    """Simple hash table.

        `get` flow:
        - Compute 'key' hash value
        - Map hash value to index in bucket
        - Traverse linked list at index
        - Return value of 'key' node or None

        `set` flow:
        - Convert 'key' to hash value
        - Map hash value to index in bucket (add linked list if necessary)
        - Traverse linked list at index
        - Set new value at 'key' node
        - If no 'key' node, append new 'key' node to end list
    """

    def __init__(self, size=100):
        # Number of buckets (linked lists)
        self.size = size
        # Bucket of linked lists
        self._buckets = [None for i in range(size)]
        # Map of hash values to bucket indices
        self._hash_map = {}

    def __repr__(self):
        return f'Hashtable <{len(self._hash_map)} key/val pairs>'

    def _get_list(self, index):
        """Return `LinkedList` at `index` or None"""
        try:
            return self._buckets[index]
        except IndexError:
            return None

    def get(self, *keys):
        """Get value(s) of key(s)"""
        values = []
        for key in keys:
            hash_key = to_hash(key)
            if hash_key not in self._hash_map:
                continue
            index = self._hash_map[hash_key]
            lst = self._get_list(index)
            if lst and lst.get(key):
                values.append(lst.get(key).value)
        return values[0] if len(values) == 1 else tuple(values) or None

    def set(self, key=None, value=None):
        if key is None:
            return None
        hash_key = to_hash(key)
        if hash_key in self._hash_map:
            lst = self._get_list(index=self._hash_map[hash_key])
            node = lst.set(key, value)
        else:
            # Map hash to index
            index = hash_key % self.size
            if self._get_list(index) is None:
                self._buckets[index] = LinkedList()
            node = self._buckets[index].set(key, value)
            self._hash_map[hash_key] = index
        return node

    def keys(self):
        """Return all key values in hash table"""
        keys = []
        indices = set(self._hash_map.values())
        for i in indices:
            keys.extend([node.key for node in self._buckets[i] if node])
        return tuple(keys)
