=========
Hashtable
=========
Basic hash table implementation based on Cracking the Coding Interview, p. 88.

Usage
-----
Like this: ::

    $ git clone https://github.com/kylepw/hashtable.git && cd hashtable
    $ python
    >>> from hash import Hashtable
    >>> h = Hashtable()
    >>> h.set('jimmy', 54)
    Node {jimmy: 54}
    >>> h.set('jasmine', 32.5)
    Node {jasmine: 32.5}
    >>> h.get('jasmine', 'jimmy')
    (32.5, 54)
    >>> h.keys()
    ('jimmy', 'jasmine')


