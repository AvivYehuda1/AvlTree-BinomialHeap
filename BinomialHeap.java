package src;

/**
 * 
 * BinomialHeap
 *
 * An implementation of binomial heap over non-negative integers.
 * Based on exercise from previous semester.
 * 
 */
public class BinomialHeap
{
	public int size = 0;
	public int numTrees = 0;
	public HeapNode last = null;
	public HeapNode min = null;

	/**
	 * 
	 * @pre: key > 0
	 * Insert (key,info) into the heap and return the newly generated HeapItem.
	 *
	 */
	
	public HeapItem insert(int key, String info) 
	{    
		HeapItem newItem = new HeapItem(key, info);
		HeapNode newNode = new HeapNode();
		newNode.item = newItem;
		newNode.next = newNode;
		newItem.node = newNode;
		
		BinomialHeap singleNodeHeap = new BinomialHeap();
		singleNodeHeap.last = newNode;
		singleNodeHeap.min = newNode;
		singleNodeHeap.size = 1;
		singleNodeHeap.numTrees = 1;
		
		this.meld(singleNodeHeap);
		
		return newItem; // should be replaced by student code
	}

	/**
	 * 
	 * Delete the minimal item.
	 * @complexity O(log(heap.size))
	 * 
	 */
	public void deleteMin()
	{
		HeapNode nodeToDelete = this.min;
		int treeSize = (int) (Math.pow(2, nodeToDelete.rank));
		
		// Delete the minimum's tree
		if (this.numTrees == 1) {
			this.last = null;
		}
		
		HeapNode currNode = this.min.next;
		HeapNode prevNode = this.min;
		
		while (currNode != this.min) {
			prevNode = currNode;
			currNode = currNode.next;
		}
		
		if (this.last == this.min) {
			this.last = prevNode;
		}
		
		prevNode.next = this.min.next;
		this.size -= treeSize;
		this.numTrees--;
		
		//Meld descendants of minimum
		BinomialHeap childrenHeap = new BinomialHeap();
		childrenHeap.last = nodeToDelete.child;
		childrenHeap.numTrees = nodeToDelete.rank;
		childrenHeap.size = treeSize - 1;
		childrenHeap.min = nodeToDelete; //Arbitrary value, has no effect
		
		currNode = childrenHeap.last;
		for (int i = 0; i < childrenHeap.numTrees(); i++, currNode=currNode.next) {
			currNode.parent = null;
		}
		
		this.meld(childrenHeap);
		
		
		//Find new minimum.
		currNode = this.last;
		this.min = currNode;
		for (int i = 0; i < this.numTrees(); i++, currNode=currNode.next)
			if (currNode.item.key < this.min.item.key) {
				this.min = currNode;
			}
	}

	/**
	 * 
	 * Return the minimal HeapItem.
	 *
	 */
	public HeapItem findMin()
	{
		return this.min.item;
	} 

	/**
	 * 
	 * @pre: 0 < diff < item.key
	 * Decrease item's key by diff and fix the heap.
	 * @complexity O(log(heap.size)) 
	 * 
	 */
	public void decreaseKey(HeapItem item, int diff) 
	{
		HeapNode node = item.node;
		if (node==null || diff < 0 || diff > item.key)
			return;  
		
		node.item.key -= diff;
		HeapNode parent = node.parent;
		while (parent != null && node.item.key < parent.item.key) {
				// Swap the items of node and parent directly
				HeapItem temp = node.item;
				node.item = parent.item;
				parent.item = temp;
				node = parent;
				parent = parent.parent;
		}
		if (node.item.key < min.item.key) {
		    this.min = node;
		}
	}

	/**
	 * 
	 * Delete the item from the heap.
	 * @complexity O(log(heap.size))
	 * 
	 */
	public void delete(HeapItem item) 
	{    
		int diff = item.key - this.findMin().key + 1;
		this.decreaseKey(item, diff);
		this.deleteMin();
		return;
	}

	/**
	 * 
	 * Meld the heap with heap2
	 * @complexity O(log(heap.size) + log(heap2.size))
	 * 
	 */
	public void meld(BinomialHeap heap2)
	{
		if (heap2.empty()) {
			return;
		}
		
		if (this.empty()) {
			this.size = heap2.size;
			this.numTrees = heap2.numTrees;
			this.min = heap2.min;
			this.last = heap2.last;
			return;
		}
		
		if (heap2.findMin().key < this.findMin().key) {
			this.min = heap2.min;
		}
		
		HeapNode treeToLink = heap2.last.next;
		HeapNode nextTreeToLink = treeToLink.next;
		int numOfTrees = heap2.numTrees();
		
		for (int i = 0; i < numOfTrees; i++, treeToLink = nextTreeToLink, nextTreeToLink = nextTreeToLink.next) {
			HeapNode prevNode = this.last;
			HeapNode currNode = this.last.next;
			treeToLink.next = treeToLink;
			while(true) {
				if (currNode.rank == treeToLink.rank) {
					if (prevNode == currNode) { //Only one tree
						this.last = link(treeToLink, currNode);
						break;
					}
					else if (this.last == currNode) { //Linking with last tree
						HeapNode first = this.last.next;
						treeToLink = link(treeToLink, this.last);
						this.last = treeToLink;
						treeToLink.next = first;
						prevNode.next = treeToLink;
						break;
					}
					prevNode.next = currNode.next;
					currNode.next = currNode;
					treeToLink = link(treeToLink, currNode);
					currNode = prevNode.next;
					this.numTrees--;
				}
	
				else if (currNode.rank < treeToLink.rank) { 
					if (currNode == this.last) { // treeToLink is greater than all other trees
						treeToLink.next = this.last.next;
						this.last.next = treeToLink;
						this.last = treeToLink;
						this.numTrees++;
						break;
					}
					prevNode = currNode; // Keep searching
					currNode = currNode.next;
				}
	
				else if (currNode.rank > treeToLink.rank) { //treeToLink has no tree of matching rank
					treeToLink.next = currNode;
					prevNode.next = treeToLink;
					this.numTrees++;
					break;
				}
			}
		}
		this.size += heap2.size;
	}

	/**
	 * 
	 * Return the number of elements in the heap
	 *   
	 */
	public int size()
	{
		return this.size;
	}

	/**
	 * 
	 * The method returns true if and only if the heap
	 * is empty.
	 *   
	 */
	public boolean empty()
	{
		return this.size == 0;
	}

	/**
	 * 
	 * Return the number of trees in the heap.
	 * 
	 */
	public int numTrees()
	{
		return this.numTrees;
	}
	
	/**
	 * 
	 * @pre node1,2.parent==null
	 * @pre node1.rank = node2.rank
	 * @post node1 and node2 are not usable
	 * Joins two binomial trees of the rank into one.
	 * Return the root node of the joint tree.
	 * @complexity O(1)
	 * 
	 */
	public HeapNode link(HeapNode node1, HeapNode node2)
	{
		HeapNode smallNode = node1; 
		HeapNode bigNode = node2;
		
		if (node1.item.key > node2.item.key) {
			smallNode = node2; 
			bigNode = node1;
		}
		if (smallNode.child != null) {
            bigNode.next = smallNode.child.next;
            smallNode.child.next = bigNode;
	        }
		bigNode.parent = smallNode;
		smallNode.child = bigNode;
		smallNode.rank++;
		
		return smallNode;
	}

	/**
	 * 
	 * Class implementing a node in a Binomial Heap.
	 *  
	 */
	public class HeapNode{
		public HeapItem item = null;
		public HeapNode child = null;
		public HeapNode next = null;
		public HeapNode parent = null;
		public int rank = 0;
	}

	/**
	 * 
	 * Class implementing an item in a Binomial Heap.
	 *  
	 */
	public class HeapItem{
		public HeapNode node = null;
		public int key;
		public String info;
		
		public HeapItem(int key, String info) 
		{
			this.key = key;
			this.info = info;
		}
	} 

}
