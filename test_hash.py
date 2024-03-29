from hash import Hashtable, LinkedList, Node, to_hash
import random
import unittest


class TestNode(unittest.TestCase):
    def setUp(self):
        self.node3 = Node('mah', 'yo')
        self.node2 = Node('geee', 'bahhh', self.node3)
        self.node1 = Node('key', 'value', self.node2)

    def test_node_connection(self):
        self.assertEqual(self.node1.next, self.node2)
        self.assertEqual(self.node2.next, self.node3)
        self.assertEqual(self.node1.next.next, self.node3)


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.lst = LinkedList(head=Node('all', 'day'))
        self.lst.head.next = Node('another', 'one')
        self.lst.head.next.next = Node('last', 'entry')

    def test_iter(self):
        for node in self.lst:
            self.assertEqual(type(node), Node)

    def test_len(self):
        self.assertEqual(len(self.lst), 3)

        self.assertEqual(len(LinkedList()), 0)

    def test_get(self):
        self.assertIsNone(self.lst.get('lkjdlfjl3'))
        self.assertIsNotNone(self.lst.get('all'))
        self.assertEqual(self.lst.get('last').value, 'entry')

    def test_append(self):
        self.assertIsNone(self.lst.get('uno'))
        node = self.lst._append('uno', 'more')
        self.assertIsNotNone(self.lst.get('uno'))
        self.assertEqual(node.key, 'uno')
        self.assertEqual(node.value, 'more')
        self.assertIsNone(node.next)

    def test_set(self):
        # Overwrite existing values
        node = self.lst.get('last')
        self.assertEqual(node.value, 'entry')
        self.lst.set('last', 678.88)
        self.assertEqual(node.value, 678.88)

        # Append
        self.assertIsNone(self.lst.get('nonexistent'))
        node = self.lst.set('nonexistent', 987)
        self.assertEqual(self.lst.get('nonexistent'), node)
        self.assertEqual(node.value, 987)


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = Hashtable()

        lst1 = LinkedList(head=Node('key', 'value'))
        lst1.head.next = Node('geee', 'bahhh')
        lst1.head.next.next = Node('mah', 'yo')
        lst1.head.next.next.next = Node('veloce', 123)
        self.ht._buckets[0] = lst1
        self.ht._hash_map.update(
            [(to_hash(key), 0) for key in ('key', 'geee', 'mah', 'veloce')]
        )

        lst2 = LinkedList(head=Node('man', {1, 2, 3}))
        lst2.head.next = Node('abacus', 'YES')
        lst2.head.next.next = Node('iphone', 'I do not know.')
        lst2.head.next.next.next = Node('monkey', 565.98)
        self.ht._buckets[1] = lst2
        self.ht._hash_map.update(
            [(to_hash(key), 1) for key in ('man', 'abacus', 'iphone', 'monkey')]
        )

    def test_set(self):
        self.assertIsNone(self.ht.set())

        self.assertEqual(self.ht.get('geee'), 'bahhh')
        self.ht.set('geee', 'wiz!')
        self.assertEqual(self.ht.get('geee'), 'wiz!')

        self.assertEqual(self.ht.get('monkey'), 565.98)
        self.ht.set('monkey', 'mammal')
        self.assertEqual(self.ht.get('monkey'), 'mammal')

        t = Hashtable()
        self.assertIsNone(t.get('hey'))
        t.set('hey', 'you')
        self.assertIsNotNone(t.get('hey'))

    def test_get(self):
        self.assertIsNone(self.ht.get('ninjaturtles343'))
        self.assertEqual(self.ht.get('geee'), 'bahhh')
        self.assertEqual(self.ht.get('monkey'), 565.98)
        self.assertEqual(self.ht.get('iphone'), 'I do not know.')

        values = self.ht.get('geee', 'monkey', 'iphone')
        self.assertEqual(len(values), 3)
        self.assertEqual(values, ('bahhh', 565.98, 'I do not know.'))

        a_wrong_value = self.ht.get('geee', 'shit3433', 'iphone')
        self.assertEqual(len(a_wrong_value), 2)
        self.assertEqual(a_wrong_value, ('bahhh', 'I do not know.'))

        t = Hashtable()
        self.assertIsNone(t.get('hey'))

    def test_keys(self):
        keys = self.ht.keys()
        self.assertEqual(
            keys, ('key', 'geee', 'mah', 'veloce', 'man', 'abacus', 'iphone', 'monkey')
        )
        self.assertEqual(len(keys), 8)

        self.assertEqual(Hashtable().keys(), ())


class TestHashTableWithBigData(unittest.TestCase):
    def setUp(self):
        self.ht = Hashtable()
        self.keys = tuple(k for k in range(1000))
        self.values = tuple(v for v in range(1000, 0, -1))
        data = list(zip(self.keys, self.values))
        for k, v in data:
            self.ht.set(k, v)

    def test_key_values(self):
        self.assertEqual(len(self.ht.keys()), len(self.keys))
        self.assertEqual(sorted(self.ht.keys()), sorted(self.keys))

    def test_get(self):
        for key in self.ht.keys():
            self.assertIsNotNone(self.ht.get(key))

    def test_set(self):
        keys = random.sample(self.ht.keys(), 10)
        new_values = tuple(random.sample(range(500, 1000), 10))
        pairs = list(zip(keys, new_values))

        self.assertNotEqual(self.ht.get(*keys), new_values)
        for k, v in pairs:
            self.ht.set(k, v)
        self.assertEqual(self.ht.get(*keys), new_values)


class TestUtilities(unittest.TestCase):
    def setUp(self):
        self.objs = (123, 'str', 123.5, {'a': 1}, (x for x in range(5)))

    def test_to_hash(self):
        for obj in self.objs:
            to_hash(obj)
