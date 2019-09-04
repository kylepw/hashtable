from hash import HashTable, LinkedList, Node, to_hash
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
        self.ht = HashTable()

        lst1 = LinkedList(head=Node('key', 'value'))
        lst1.head.next = Node('geee', 'bahhh')
        lst1.head.next.next = Node('mah', 'yo')
        lst1.head.next.next.next = Node('veloce', 123)
        self.ht._db.append(lst1)
        self.ht._hash_map.update([(to_hash(key), 0) for key in ('key', 'geee', 'mah', 'veloce')])

        lst2 = LinkedList(head=Node('man', {1, 2, 3}))
        lst2.head.next = Node('abacus', 'YES')
        lst2.head.next.next = Node('iphone', 'I do not know.')
        lst2.head.next.next.next = Node('monkey', 565.98)
        self.ht._db.append(lst2)
        self.ht._hash_map.update([(to_hash(key), 1) for key in ('man', 'abacus', 'iphone', 'monkey')])

        print(ht._hash_map)

    def test_set(self):
        self.assertIsNone(self.ht.set())

        self.assertEqual(self.ht.get('geee'), 'bahhh')
        self.ht.set('geee', 'wiz!')
        self.assertEqual(self.ht.get('geee'), 'wiz!')

        self.assertEqual(self.ht.get('monkey'), 565.98)
        self.ht.set('monkey', 'mammal')
        self.assertEqual(self.ht.get('monkey'), 'mammal')

        t = HashTable()
        t.set('hey', 'you')

    def test_get(self):
        self.assertIsNone(self.ht.get('ninjaturtles343'))
        self.assertEqual(self.ht.get('geee'), 'bahhh')
        self.assertEqual(self.ht.get('monkey'), 565.98)
        self.assertEqual(self.ht.get('iphone'), 'I do not know.')

        t = HashTable()
        self.assertIsNone(t.get('hey'))