"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int or None
	@param key: key of your node
	@type value: any
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.parent = None
		# set up virtual node
		if self.is_real_node():
			r = AVLNode(None,None)
			l = AVLNode(None,None)
			self.set_left(r)
			self.set_right(l)
			r.set_parent(self)
			l.set_parent(self)
			self.height = 0
			self.size = 1
		# set up real node
		else:
			self.left = None
			self.right = None
			self.height = -1
			self.size = 0
		

	"""returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""
	def get_key(self):
		return self.key


	"""returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""
	def get_value(self):
		return self.value


	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	"""
	def get_left(self):
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""
	def get_right(self):
		return self.right


	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def get_parent(self):
		return self.parent


	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def get_height(self):
		return self.height


	"""returns the size of the subtree

	@rtype: int
	@returns: the size of the subtree of self, 0 if the node is virtual
	"""
	def get_size(self):
		return self.size


	"""sets key

	@type key: int or None
	@param key: key
	"""
	def set_key(self, key):
		self.key = key


	"""sets value

	@type value: any
	@param value: data
	"""
	def set_value(self, value):
		self.value = value


	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def set_left(self, node):
		self.left = node


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def set_right(self, node):
		self.right = node


	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def set_parent(self, node):
		self.parent = node


	"""sets the height of the node

	@type h: int
	@param h: the height
	"""
	def set_height(self, h):
		self.height = h


	"""sets the size of node

	@type s: int
	@param s: the size
	"""
	def set_size(self, s):
		self.size = s


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return (self.key != None)
	
	
	"""calculate Balance Factor"""
	def get_BF(self):
		if self.is_real_node():
			return ((self.get_left()).get_height() - (self.get_right()).get_height())
		return 0



"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	def __init__(self):
		self.root = None



	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key.

	@Time-Complexity: O(log(n = size of tree)) - goes all the way down the AVLTree while
	performing constant number of operations each step, each operation is of consant complexity.
	"""
	def search(self, key):
		p = self.root # start the search from the root
		while(p.is_real_node() and p.get_key() != key): # dont stop looking until found a virtual node or the key
			p = p.get_left() if (p.get_key() > key) else p.get_right() # go left if current value < key, else go right
		
		return (p if p.is_real_node() else None)


	"""inserts val at position i in the dictionary

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing

	@Time-Complexity: O(log(n = size of tree)) - goes all the way down and up the AVLTree while
	performing constant number of operations each step, each operation is of consant complexity.
	"""
	def insert(self, key, val):
		# handle first insertion (root)
		if self.root == None:
			self.root = AVLNode(key,val)
			return 0
		# find the virtual node that needs to be replaced with the new one
		p = self.root
		while(p.is_real_node()): 
			p = p.get_left() if (p.get_key() > key) else p.get_right()
		p = p.get_parent()
		# insert new node regularly (without AVL-rebalancing)
		newNode = AVLNode(key,val)
		if p.get_key() > key:
			p.set_left(newNode)
		else:
			p.set_right(newNode)
		newNode.set_parent(p)
		# rebalance
		rebalanceCounter = self.__rebalance(p) # look in "private methods" down below for implementation
		return rebalanceCounter # return num of rebalancing operations
	
	
	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		if (node.get_right()).is_real_node() and (node.get_left()).is_real_node():
			suc = self.__successor(node)
			tempKey = suc.get_key()
			tempVal = suc.get_value()
			node.set_key(tempKey)
			node.set_value(tempVal)
			return self.delete_hlp(suc)
		return self.delete_hlp(node)

	def delete_hlp(self, node):
		# handle case of 1-node-tree
		if (self.get_root()).get_size() == 1:
			self.root = None
			return 0
		# physically delete node from parent
		parent = node.get_parent()
		# case 1: node is a leaf
		if (not (node.get_right()).is_real_node()) and (not (node.get_left()).is_real_node()):
			child = AVLNode(None,None)
		# case 2: node has one child
		else:
			if node.get_right().is_real_node():
				child = node.get_right()
			else: child = node.get_left()
		if parent.get_key() > node.get_key():
			parent.set_left(child)
		else: parent.set_right(child)
		child.set_parent(parent)
		node.set_parent(None)			
		# rebalance upwards
		return self.__rebalance(parent)


	"""returns an array representing dictionary 
    
    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    
    @Time-Complexity: O(n = size of tree) - inorder scan
    """
	def avl_to_array(self):
		res = [] 
		# in case of empty tree
		if self.root is None:
			return res 
		s = []
		p = self.root
		# perform inorder scan of the tree using stack-like functionality
		while len(s) != 0 or p.is_real_node():
			if p.is_real_node():
				s.append(p)
				p = p.get_left()
			else:
				p = s.pop()
				res.append((p.get_key(),p.get_value()))
				p = p.get_right()
		return res	

	
	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 

	@Time-Complexity: O(1) - constant number of operations of constant complexity.
	"""
	def size(self):
		return (self.root).get_size()	

	
	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
	# Creating new AVLTrees for smaller and bigger than the given node's key
		smaller = AVLTree()
		bigger = AVLTree()
		if node.get_left().is_real_node():
			smaller.root = node.get_left()
			node.set_left(None)
			(smaller.root).set_parent(None)
		if node.get_right().is_real_node():
			bigger.root = node.get_right()
			node.set_right(None)
			(bigger.root).set_parent(None)
		
		# Recursive helper function to traverse the AVLTree and split nodes
		def split_helper(current_node, smaller, bigger, key):
			if current_node == None:
				return [smaller,bigger]
				
			toJoin = AVLTree()
			# Splitting the AVLTree based on the given node's key
			if current_node.key < key:
				toJoin.root = current_node.get_left()
				(toJoin.root).set_parent(None)
				smaller.join(toJoin, current_node.get_key(), current_node.get_value())
			elif current_node.key > key:
				toJoin.root = current_node.get_right()
				(toJoin.root).set_parent(None)
				bigger.join(toJoin, current_node.get_key(), current_node.get_value())
				
			return split_helper(current_node.get_parent(), smaller, bigger, key)

		# Calling and returning the split_helper function starting from the given node
		return split_helper(node, smaller, bigger, node.get_key())


	"""joins self with key and another AVLTree

	@type tree: AVLTree 
	@param tree: a dictionary to be joined with self
	@type key: int 
	@param key: The key separting self with tree
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree are larger than key,
	or the other way around.
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined

	@Time-Complexity: O(log(n = size of joined trees)) - - goes all the way down and up the AVLTree while
	performing constant number of operations each step, each operation is of consant complexity.
	"""
	def join(self, tree, key, val):
		joint = AVLNode(key,val) # main joint
		if (tree.root != None) and (not tree.get_root().is_real_node()): tree.root = None
		if (self.root != None) and (not self.get_root().is_real_node()): self.root = None

		# first handle the case in which one of the trees is empty
		if self.get_root() == None and tree.get_root() != None:
			if key > (tree.get_root()).get_key(): joint.set_left(tree.get_root())
			else: joint.set_right(tree.get_root())
			tree.get_root().set_parent(joint)
			self.root = joint
			self.__rebalance(joint)
			return tree.get_root().get_height()
		elif self.get_root() != None and tree.get_root() == None:
			if key > (self.get_root()).get_key(): joint.set_left(self.get_root())
			else: joint.set_right(self.get_root())
			self.get_root().set_parent(joint)
			self.root = joint
			self.__rebalance(joint)
			return self.get_root().get_height()
		elif self.get_root() == None and tree.get_root() == None:
			self.root = joint
			return 0

		ret = abs(self.get_root().get_height() - tree.get_root().get_height()) + 1 # to return
		# figure out which tree is taller
		if (self.get_root()).get_height() > (tree.get_root()).get_height():
			Ltree = self
			Stree = tree
		else:
			Ltree = tree
			Stree = self
		# case 1: Larger tree has larger values
		if (Ltree.get_root()).get_key() > (Stree.get_root()).get_key():
			# find left joint and right joint
			right_joint = Ltree.get_root()
			left_joint = Stree.get_root()
			while(right_joint.get_height() > left_joint.get_height()):
				right_joint = right_joint.get_left()
			parent = right_joint.get_parent()
			# connect trees through the joints
			joint.set_left(left_joint)
			joint.set_right(right_joint)
			joint.set_parent(parent)
			right_joint.set_parent(joint)
			left_joint.set_parent(joint)
			if parent != None: parent.set_left(joint)
			else: Ltree.root = joint
		# case 2: Larger tree has smaller values
		else:
			# find left joint and right joint
			right_joint = Stree.get_root()
			left_joint = Ltree.get_root()
			while(left_joint.get_height() > right_joint.get_height()):
				left_joint = left_joint.get_right()
			parent = left_joint.get_parent()
			# connect trees through the joints
			joint.set_left(left_joint)
			joint.set_right(right_joint)
			joint.set_parent(parent)
			right_joint.set_parent(joint)
			left_joint.set_parent(joint)
			if parent != None: parent.set_right(joint)
			else: Ltree.root = joint
		# all that remains is to rebalance the tree
		self.root = Ltree.get_root()
		self.__rebalance(joint) # look in "private methods" down below for implementation
		return ret


	"""compute the rank of node in the self

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary which we want to compute its rank
	@rtype: int
	@returns: the rank of node in self

	@Time-Complexity: O(log(n = size of tree)) - goes at most all the way up the AVLTree while
	performing constant number of operations each step, each operation is of constant complexity. 
	"""
	def rank(self, node):
		if not node.is_real_node():
			return 0
		rank = 1 + (node.get_left()).get_size() # start the count from the node itself
		# count every node with key <= node.key
		parent = node.get_parent()
		while(parent != None):
			if parent.get_key() < node.get_key():
				rank += 1 + (parent.get_left()).get_size()
			parent = parent.get_parent()
			node = node.get_parent()
		return rank


	"""finds the i'th smallest item (according to keys) in self

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: int
	@returns: the item of rank i in self

	@Time-Complexity: O(log(n = size of tree)) we go down the AVL tree once
	and perform a constant amount of O(1) operations at each level.
	"""
	def select(self, i):
		return self.select_hlp(self.get_root(),i)

	def select_hlp(self,x,i):
		r = (x.get_left()).get_size() + 1
		if i == r: # we found the required element
			return x.get_key()
		elif i < r: # required element is on the left
			return self.select_hlp(x.left,i)
		# required element is on the right
		else: return self.select_hlp(x.right,i-r)


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty

	@Time-Complexity: O(1) - constant number of operations and each are of O(1) time.
	"""
	def get_root(self):
		return self.root
	

	"""private methods: """

	"""Successor method:
	@Time-Complexity: O(log(n = size of tree)) 
	"""
	def __successor(self, p):
		# Case 1: p has a right son
		if (p.get_right()).is_real_node():
			p = p.get_right()
			while((p.get_left()).is_real_node()):
				p = p.get_left()
			return p
		# Case 2: p does not have a right son
		else:
			parent = p.get_parent()
			while(parent != None and parent.get_key() < p.get_key()):
				parent = parent.get_parent()
				p = p.get_parent()
			return parent # may return None in case of maximal node

	"""Rebalancing method
	rebalances tree from the node given and upwards

	@returns: number of rebalancing operations
	@time complexity: O(log(n = size of tree)) - goes at most all the way up the AVLTree while
	performing constant number of operations each step, each operation is of constant complexity.
	"""
	def __rebalance(self, p):
		rebalanceCounter = 0
		while(p != None): # go up the tree until past root
			# check BF score and act accordingly
			if p.get_BF() >= 2:
				if (p.get_left()).get_BF() == 1 or (p.get_left()).get_BF() == 0:
					rebalanceCounter += self.__RR(p) # right rotation case
				else:
					rebalanceCounter += self.__LRR(p) # left-then-right rotation case
			elif p.get_BF() <= -2:
				if (p.get_right()).get_BF() == -1 or (p.get_right()).get_BF() == 0:
					rebalanceCounter += self.__LR(p) # left rotation case
				else:
					rebalanceCounter += self.__RLR(p) # right-then-left rotation case
			else:
				#maintain size and height
				p.set_height(1 + max((p.get_left()).get_height(), (p.get_right()).get_height()))
				rebalanceCounter += 1
				p.set_size(1 + (p.get_left()).get_size() + (p.get_right()).get_size())
			p = p.get_parent()
		return rebalanceCounter
	
	"""Rotation methods:"""
	"""Performs Left-Rotation
	
	@type node: AVLNode
	@pre node: node.get_BF() = -2 and (node.get_right()).get_BF() = -1 or 0

	@Time-Complexity: O(1) - constant number of operations and each are of O(1) time
	"""
	def __LR(self, node): # recives the node with BF = -2
		son = node.get_right() # node with BF = -1 or 0
		parent = node.get_parent() # get previous parent
		leftGrandSon = son.get_left() # get left subtree of the son
		if leftGrandSon != None:
			# move left subtree of son to right subtree of node and maintain virtual nodes
			node.set_right(leftGrandSon)
			leftGrandSon.set_parent(node)
			virtualNode = AVLNode(None,None)
			son.set_left(virtualNode)
			virtualNode.set_parent(son)
		# reset the node's parent child
		if parent == None:
			self.root = son
			son.set_parent(None)
		elif (parent.get_right()).get_key() == node.get_key():
			parent.set_right(son)
			son.set_parent(parent)
		else:
			parent.set_left(son)
			son.set_parent(parent)
		# hook original node into place
		son.set_left(node)
		node.set_parent(son)
		# update heights and sizes that were changed during rotation
		node.set_height(1 + max((node.get_left()).get_height(), (node.get_right()).get_height()))
		son.set_height(1 + max((son.get_left()).get_height(), (son.get_right()).get_height()))
		node.set_size(1 + (node.get_left()).get_size() + (node.get_right()).get_size())
		son.set_size(1 + (son.get_left()).get_size() + (son.get_right()).get_size())
		return 1

	"""Performs Right-Rotation
	
	@type node: AVLNode
	@pre node: node.get_BF() = 2 and (node.get_right()).get_BF() = 1 or 0

	@Time-Complexity: O(1) - constant number of operations and each are of O(1) time
	"""
	def __RR(self, node): # recives the node with BF = +2
		son = node.get_left() # node with BF = +1 or 0
		parent = node.get_parent() # get previous parent
		rightGrandSon = son.get_right() # get right subtree of son
		if rightGrandSon != None:
			# move left subtree of son to right subtree of node and maintain virtual nodes
			node.set_left(rightGrandSon)
			rightGrandSon.set_parent(node)
			virtualNode = AVLNode(None,None)
			son.set_right(virtualNode)
			virtualNode.set_parent(son)
		# reset the node's parent children		
		if parent == None:
			self.root = son
			son.set_parent(None)
		elif (parent.get_right()).get_key() == node.get_key():
			parent.set_right(son)
			son.set_parent(parent)
		else:
			parent.set_left(son)
			son.set_parent(parent)
		# hook original node into place
		son.set_right(node)
		node.set_parent(son)
		# update heights that were changed during rotation
		node.set_height(1 + max((node.get_left()).get_height(), (node.get_right()).get_height()))
		son.set_height(1 + max((son.get_left()).get_height(), (son.get_right()).get_height()))
		node.set_size(1 + (node.get_left()).get_size() + (node.get_right()).get_size())
		son.set_size(1 + (son.get_left()).get_size() + (son.get_right()).get_size())
		return 1

	"""Performs Left-Right-Rotation
	
	@type node: AVLNode
	@pre node: node.get_BF() = 2 and (node.get_right()).get_BF() = -1

	@Time-Complexity: O(1) - constant number of operations and each are of O(1) time
	"""
	def __LRR(self, node): # recives the node with BF = +2
		son = node.get_left() # node with BF = -1
		self.__LR(son)
		self.__RR(node)
		return 2

	"""Performs Right-Left-Rotation
	
	@type node: AVLNode
	@pre node: node.get_BF() = -2 and (node.get_right()).get_BF() = 1

	@Time-Complexity: O(1) - constant number of operations and each are of O(1) time
	"""
	def __RLR(self, node): # recives the node with BF = -2
		son = node.get_right() # node with BF = +1
		self.__RR(son)
		self.__LR(node)
		return 2
