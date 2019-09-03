from hash import HashTable, Node
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


class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.ht = HashTable()

        self.node4 = Node('veloce', 123)
        self.node3 = Node('mah', 'yo', self.node4)
        self.node2 = Node('geee', 'bahhh', self.node3)
        self.node1 = Node('key', 'value', self.node2)
        head0 = self.node1
        self.ht.db.append(head0)

        self.node8 = Node('monkey', 565.98)
        self.node7 = Node('iphone', 'I do not know.', self.node8)
        self.node6 = Node('abacus', 'YES', self.node7)
        self.node5 = Node('man', {1, 2, 3}, self.node6)
        head1 = self.node5
        self.ht.db.append(head1)

    def test_write(self):
        pass

    def test_get_node(self):
        self.assertEqual(self.ht._get_node(0, 'key'), self.node1)
        self.assertEqual(self.ht._get_node(0, 'geee'), self.node2)
        self.assertEqual(self.ht._get_node(0, 'mah'), self.node3)
        self.assertEqual(self.ht._get_node(0, 'veloce'), self.node4)
        self.assertIsNone(self.ht._get_node(0, 'moot343'))
        with self.assertRaises(IndexError):
            self.ht._get_node(100, 'jesus')

    def test_append_node(self):
        node = self.ht._append_node(0, 'another', 'value')
        self.assertEqual(node.key, 'another')
        self.assertEqual(node.value, 'value')
        self.assertIsNone(node.next)

        with self.assertRaises(IndexError):
            self.ht._append_node(100, 'jesus', 'xmas')

    def test_write_node(self):
        # Overwrite
        node = self.ht._get_node(0, 'geee')
        self.assertEqual(node.value, 'bahhh')
        self.ht._write_node(0, 'geee', 678.88)
        self.assertEqual(node.value, 678.88)

        # Append
        self.assertIsNone(self.ht._get_node(1, 'nonexistent'))
        node = self.ht._write_node(1, 'nonexistent', 987)
        self.assertEqual(self.ht._get_node(1, 'nonexistent'), node)
        self.assertEqual(node.value, 987)
