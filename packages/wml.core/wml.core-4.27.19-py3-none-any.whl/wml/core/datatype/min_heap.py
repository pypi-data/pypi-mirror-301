# Python3 implementation of Min Heap

import sys

from mt import tp, logg


class MinHeap:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.size = 0
        self.Heap = [0] * (self.maxsize + 1)
        self.Heap[0] = -1 * sys.maxsize
        self.FRONT = 1

    def parent(self, pos):
        """Returns the position of parent for the node currently at pos"""
        return pos // 2

    def leftChild(self, pos):
        """Returns the position of the left child for the node currently at pos"""
        return 2 * pos

    def rightChild(self, pos):
        """Returns the position of the right child for the node currently at pos"""
        return (2 * pos) + 1

    def isLeaf(self, pos):
        """Returns whether the passed node is a leaf node"""
        return pos * 2 > self.size

    def swap(self, fpos, spos):
        """Swaps two nodes of the heap"""
        self.Heap[fpos], self.Heap[spos] = self.Heap[spos], self.Heap[fpos]

    def heapify(self, pos):
        """Heapifies the node at pos"""
        # If the node is a non-leaf node and greater
        # than any of its child
        if not self.isLeaf(pos):
            if (
                self.Heap[pos] > self.Heap[self.leftChild(pos)]
                or self.Heap[pos] > self.Heap[self.rightChild(pos)]
            ):
                # Swap with the left child and heapify
                # the left child
                if self.Heap[self.leftChild(pos)] < self.Heap[self.rightChild(pos)]:
                    self.swap(pos, self.leftChild(pos))
                    self.heapify(self.leftChild(pos))

                # Swap with the right child and heapify
                # the right child
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.heapify(self.rightChild(pos))

    def insert(self, element):
        """Inserts a node into the heap"""
        if self.size >= self.maxsize:
            return
        self.size += 1
        self.Heap[self.size] = element

        current = self.size

        while self.Heap[current] < self.Heap[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def print(self, logger: tp.Optional[logg.IndentedLoggerAdapter] = None):
        """Prints the contents of the heap"""
        for i in range(1, (self.size // 2) + 1):
            msg = (
                " PARENT : "
                + str(self.Heap[i])
                + " LEFT CHILD : "
                + str(self.Heap[2 * i])
                + " RIGHT CHILD : "
                + str(self.Heap[2 * i + 1])
            )
            logg.info(msg, logger=logger)

    def build(self):
        """Builds the min heap using the heapify function"""
        for pos in range(self.size // 2, 0, -1):
            self.heapify(pos)

    def pop(self):
        """Pops the minimum element from the heap"""
        popped = self.Heap[self.FRONT]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size -= 1
        self.heapify(self.FRONT)
        return popped


# Driver Code
if __name__ == "__main__":
    logg.info("The minHeap is ")
    minHeap = MinHeap(15)
    minHeap.insert(5)
    minHeap.insert(3)
    minHeap.insert(17)
    minHeap.insert(10)
    minHeap.insert(84)
    minHeap.insert(19)
    minHeap.insert(6)
    minHeap.insert(22)
    minHeap.insert(9)
    minHeap.build()

    minHeap.print(logger=logg.logger)
    logg.info("The Min val is " + str(minHeap.remove()))
