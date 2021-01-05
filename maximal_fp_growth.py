import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re
import itertools
import sys

class Node:
    
    freq = dict()
    def __init__(self, value):
        
        Node.freq = dict()
        self.__value = value
        self.__count = 1
        self.__children = []
        self.__parent = 'NULL'
        self.__link = 'NULL'
        
    def update(self):
        self.__count += 1
        
    def reinit_dict(self):
        Node.freq = dict()
        
    def add_children(self,n):
        
        self.__children.append(n)
        n.add_parent(self)
        
    def add_parent(self,n):
        self.__parent = n
        
    def add_link(self, n):
        self.__link = n
        
    def __get_count(self):
        return self.__count
    
    def get_value(self):
        return self.__value
        
    def get_parent_count(self):
        print(self.__parent.__get_count())
        
    def get_children(self):
        return self.__children
            
    def check_children(self,data,d):
        
        m = -1
        j = -1
        
        for k in data:
            
            if d[k][0] > m or (d[k][0] == m and k < j):
                m = d[k][0]
                j = k
                
        for i in range(len(self.__children)):
            
            if self.__children[i].get_value() == j:
                return (self.__children[i], j)
            
        return (False, j)
    
    def preorder(self):
        
        print(self.__value+':'+str(self.__count))
        
        for i in range(len(self.__children)):
            self.__children[i].preorder()
            
    def backtrack(self, s):
        
        if self.__value == 'NULL':
            return frozenset(s)
        
        s.append(self.__value)
        
        return self.__parent.backtrack(s)
        
    def link_traverse(self, l, d):
        
        #print(self.__value+': '+str(self.__count))
        s = self.__parent.backtrack([])
        
        if s != frozenset():
            l[s] = self.__count
            d = d.union(s)
        
        #print(str(s)+': '+str(self.__count))
        
        if self.__link == 'NULL':
            return (l,d)
        
        return self.__link.link_traverse(l,d)
    
    def node_mine(self, s, v, c):
        
        new_l = []
        
        if len(self.__children) == 0 or (self.__count < c and self.__value != 'NULL'):
            
            if len(self.__children) == 0 and self.__count >= c:
                
                for i in range(len(s)):

                    a = set(s[i][0])
                    a.add(self.__value)
                    new_l.append((a, self.__count))

                a = set()
                a.add(self.__value)
                new_l.append((a, self.__count))
                s.extend(new_l)
                #print(s)
                
            if s == []:
                return Node.freq
                
                
            for i in range(len(s)):
                
                s[i][0].add(v)
                Node.freq[frozenset(s[i][0])] = s[i][1]
                
            return Node.freq
        
        elif self.__value != 'NULL':
            
            for i in range(len(s)):

                a = set(s[i][0])
                a.add(self.__value)
                new_l.append((a, self.__count))
            
            a = set()
            a.add(self.__value)
            new_l.append((a, self.__count))
            s.extend(new_l)
            #print(s)
            
        se = list(s)
        
        for i in range(len(self.__children)):
            self.__children[i].node_mine(s, v, c)
            s = se
            
        return Node.freq

    def node_mine_maximal(self, s, v, c, r):
        
        if len(self.__children) == 0 or (self.__count < c and self.__value != 'NULL'):
            
            if len(self.__children) == 0 and self.__count >= c:

                a = s[0]
                a.add(self.__value)
                s = (a, self.__count)
                #print(s)
                
            if s == ():
                return Node.freq, r
                
            s[0].add(v)
            k = 0
            if frozenset(s[0]) not in Node.freq.keys():
                for i in Node.freq.keys():
                    if frozenset(s[0]) < i:
                        k = 1
                if k == 0:
                    Node.freq[frozenset(s[0])] = s[1]

            if frozenset(s[0]) not in r.keys():
                r[frozenset(s[0])] = s[1]
            else:
                r[frozenset(s[0])] = s[1]

            #print(Node.freq)
                
            return Node.freq, r
        
        elif self.__value != 'NULL':
            
            a = s[0]
            a.add(self.__value)
            s = (a, self.__count)
            
        se = (s[0],s[1])
        
        for i in range(len(self.__children)):
            self.__children[i].node_mine_maximal(s, v, c, r)
            s = se
            
        return Node.freq, r

class FPGrowth:
    
    freq = []
    def __init__(self, sup_count = 10, conf = 0.5):
        
        if FPGrowth.freq == []:
            FPGrowth.freq = dict()
        self.__root = Node('NULL')
        self.__sup_count = sup_count
        self.__conf = conf
        self.__d = {}
        self.__l = []
        self.__freq = []
        self.__valid = {}
        
    def __preprocess(self, data):
        
        for i in data:
            for j in i:
                if j not in self.__d.keys():
                    self.__d[j] = [1, 'NULL', 'NULL']
                else:
                    self.__d[j][0] += 1
        
        self.__l = sorted(list(self.__d.items()),  key=lambda x: (x[1][0]), reverse=True)
        
    def fit(self, data):
        
        self.__preprocess(data)
        
        for i in data:
            self.__insert(self.__root, i)
        
    def __insert(self, node, data):
        
        if data == []:
            return True
        
        a = node.check_children(data,self.__d)
        data.remove(a[1])
        
        if a[0] != False:
            
            a[0].update()
            self.__valid[a[1]] += 1
            return self.__insert(a[0], data)
        
        else:
            
            c = Node(a[1])
            
            if a[1] not in self.__valid.keys():
                self.__valid[a[1]] = 1
            else:
                self.__valid[a[1]] += 1
            
            if self.__d[a[1]][2] == 'NULL':
                self.__d[a[1]][1] = c
            
            else:
                self.__d[a[1]][2].add_link(c)
                
            self.__d[a[1]][2] = c
            node.add_children(c)
            
            return self.__insert(c, data)
        
    def mine_tree(self, v):
        
        self.__root.reinit_dict()
        mined_items = self.__root.node_mine([], v, self.__sup_count)
        
        for i in mined_items.keys():
            
            if i not in FPGrowth.freq.keys():
                FPGrowth.freq[i] = mined_items[i]
            else:
                FPGrowth.freq[i] += mined_items[i]
    
    def mine_maximal(self, v):
        
        FPGrowth.freq = dict()
        
        self.__root.reinit_dict()
        mined_items = self.__root.node_mine_maximal((set(),0), v, self.__sup_count, dict())
        #print(mined_items[1])

        for i in mined_items[1]:
            print(str(set(i)))

    def traversal(self):
        self.__root.preorder()
        
    def check_valid(self):
        return self.__valid
        
    def lookup(self):
        
        for i in range(len(self.__l)-1,0,-1): 
            
            self.__valid = dict()
            
            if self.__l[i][1][0] >= self.__sup_count:
                
                #print(self.__l[i][0])
                c_rule = self.__d[self.__l[i][0]][1].link_traverse(dict(), set())
                #print(c_rule[0])
                freq = list()
                
                for j in c_rule[0].keys():
                    k = 1
                    while k <= c_rule[0][j]:
                        freq.append(list(j))
                        k += 1
                    
                #print(freq)
                
                sub_tree = FPGrowth(sup_count = self.__sup_count)
                sub_tree.fit(freq)
                #print(sub_tree.check_valid())
                #sub_tree.traversal()
                sub_tree.mine_tree(self.__l[i][0])
                s = set()
                s.add(self.__l[i][0])
                FPGrowth.freq[frozenset(s)] = self.__d[self.__l[i][0]][0]
                
        s = set()
        s.add(self.__l[0][0])
        FPGrowth.freq[frozenset(s)] = self.__d[self.__l[0][0]][0]

        return FPGrowth.freq
    
    def lookup_maximal(self):
        
        FPGrowth.freq = dict()
        
        for i in range(len(self.__l)-1,0,-1): 
            
            self.__valid = dict()
            
            if self.__l[i][1][0] >= self.__sup_count:
                
                #print(self.__l[i][0])
                c_rule = self.__d[self.__l[i][0]][1].link_traverse(dict(), set())
                #print(c_rule[0])
                freq = list()
                
                for j in c_rule[0].keys():
                    k = 1
                    while k <= c_rule[0][j]:
                        freq.append(list(j))
                        k += 1
                    
                #print(freq)
                
                sub_tree = FPGrowth(sup_count = self.__sup_count)
                sub_tree.fit(freq)
                #print(sub_tree.check_valid())
                #sub_tree.traversal()
                sub_tree.mine_maximal(self.__l[i][0])
         
        d = []   
        for i in FPGrowth.freq.keys():
            if i not in d:
                d.append(i)

        return d

    def frequent_itemsets(self):
        return FPGrowth.freq
    
    def get_rules(self):
        
        for i in FPGrowth.freq.keys():
            if len(i) > 1:
                list_A = []
                list_B = []
                
                for j in range(len(i)-1,0,-1):
                    A = list(itertools.combinations(list(i),j))
                    for a in A:
                        a = set(a)
                        b = set(i - a)

                        if FPGrowth.freq[i]/FPGrowth.freq[frozenset(a)] > self.__conf:
                            print(str(a)+' ==> '+str(b)+' confidence: '+str(FPGrowth.freq[i]/FPGrowth.freq[frozenset(a)]))

'''l = []
path = 'BMS1_itemset_mining.txt'

with open(path,'r') as o:
    l = o.readlines()
    
for i in range(len(l)):
    
    l[i] = l[i].rstrip()
    s = l[i].split(' ')
        
    l[i] = s
    #print(l[i])
c = int(0.008 * len(l))

f = FPGrowth(sup_count = c)
f.fit(l)
#f.traversal()
#f.lookup()
#print(f.check_valid())
#d1 = f.frequent_itemsets()
print('Maximal frequent itemsets')
f.lookup_maximal()
#print(d1)
#f.get_rules()'''
