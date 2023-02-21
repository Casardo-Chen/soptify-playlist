#!/usr/bin/env python3

from operator import truediv
import pprint

class MaxHeap:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.Heap = [''] * (self.capacity + 1)
        self.dict = {}
        self.Heap[0] = 'init' # avoid the first element being swapped to position 0
        self.dict['init'] = 1000000
        self.dict[''] = -1 # set empty elements -1
        self.front = 1
        
    
    def getValue(self,pos):
        return self.dict[self.Heap[pos]]

    def getParent(self, pos):
        return pos // 2
    
    def getLeftChild(self, pos):
        return (pos * 2)

    def getRightChild(self, pos):
        return (pos * 2) + 1
    
    def swap(self, a, b):
        self.Heap[a], self.Heap[b] = self.Heap[b], self.Heap[a]
    
    def isEmpty(self):
        if self.size == 0:
            return True
        return False

    def isLeaf(self, pos):
        if self.Heap[self.getLeftChild(pos)] == '' and self.Heap[self.getLeftChild(pos)] == '':
            return True
        return False

    # insert a new element
    def insert(self, element, value):
        if self.size >= self.capacity:
            return
        self.dict[element] = self.dict.get(element,value)
        self.size += 1
        self.Heap[self.size] = element
        current = self.size

        while (self.getValue(current) > self.getValue(self.getParent(current))):
            self.swap(current, self.getParent(current))
            current = self.getParent(current)

        
    
    # after pop the max, re-organize the max heap
    def heapify(self, pos):
        # base
        if(self.isLeaf(pos)):
            return

        # recursion
        if (self.getValue(pos) < self.getValue(self.getLeftChild(pos)) or self.getValue(pos) < self.getValue(self.getRightChild(pos))):
            if (self.getValue(self.getLeftChild(pos)) > self.getValue(self.getRightChild(pos))):
                self.swap(pos, self.getLeftChild(pos))
                self.heapify(self.getLeftChild(pos))
            else:
                self.swap(pos, self.getRightChild(pos))
                self.heapify(self.getRightChild(pos))
        
        
    # pop the max
    def popMax(self):
        max = self.Heap[self.front]
        self.Heap[self.front] = self.Heap[self.size]
        self.Heap[self.size] = ''
        self.size -= 1
        self.heapify(self.front)
        return max

    # display
    def displayHeap(self):
        for i in range(1, ((self.size // 2)+1)):
            print(" PARENT : " + str(self.Heap[i]) + " value: " + str(self.getValue(i)) 
                    + " LEFT CHILD : " + str(self.Heap[2 * i ]) + " value: " + str(self.getValue(2*i)) 
                    + " RIGHT CHILD : " + str(self.Heap[2 * i + 1]) +" value: " + str(self.getValue(2*i+1)))