from random import randint, sample
from math import floor, ceil

class Sudoku():
    '''contains the game board representation and the AI that makes moves
    based on existing knowledge of the domains and the cells'''
    def __init__(self, file):
        self.testing = True#False#
        self.fixed = set()
        self.domain = {
            (x, y): {z for z in range(9)} 
            for x in range(9) for y in range(9)
        }
        data = open(file).read().split('\n')
        self.board = {(x, y):None for x in range(9) for y in range(9)}
        for x in range(9):
            for y in range(9):
                if data[y][x] != ' ':
                    self.fix(x, y, int(data[y][x])-1)
        print('Initialization complete')
        if self.testing: self.print(True)
    
    def fix(self, x, y, value):
        '''Sets a value (makes a move) and makes necassary changes'''
        if self.safe(x, y, value):
            self.board[x, y] = value
            self.domain[x, y] = {}
            self.fixed.add((x, y))
            for i in range(9):
                if value in self.domain[x, i]:
                    self.domain[x, i].discard(value)
                if value in self.domain[i, y]:
                    self.domain[i, y].discard(value)
            for j in range(3*floor(y/3), 3*ceil((y+1)/3)):
                for i in range(3*floor(x/3), 3*ceil((x+1)/3)):
                    if value in self.domain[i, j]:
                        self.domain[i, j].discard(value)
            if self.testing: print('Fixed %d at %d,%d'%(value+1, x, y))
            return True
        else:
            return False
    
    def safe(self, x, y, value):
        '''Returns True or False depending on whether or not the value can be
        safely placed in the cell (x, y)'''
        if self.testing: print('\n%d safe for %d,%d ? '%(value+1, x, y), end='')
        if value in [
                self.board[x, i] 
                for i in range(9)
                if i!=y and self.board[x, i]!=None
            ] or value in [
                self.board[i, y]
                for i in range(9)
                if i!=x and self.board[i, y]!=None
            ] or value in [
                self.board[i, j]
                for i in range(3*floor(x/3), 3*ceil((x+1)/3))
                for j in range(3*floor(y/3), 3*ceil((y+1)/3))
                if i!=x and j!=y and self.board[i, j]!=None
            ]:
            if self.testing: print('F')
            return False
        else:
            if self.testing:
                print('T')
#                self.print(True)
            return True
    
    def isset(self, x, y):
        '''Return True or False depending on whether or no the cell is fixed
        : only one value exists in its domain'''
        if self.board[x, y] != None:
            return True
        else:
            return False
    
    def print(self, domains=False):
        print('Current State : ')
        print('  0-1-2-3-4-5-6-7-8\n  _________________')
        for y in range(9):
            print(y, end='|')
            for x in range(9):
                if self.isset(x, y):
                    print(self.board[x, y]+1, end='-')
                else:
                    print(' -', end='')
            print()
        print()
        if domains:
            for x, y in self.domain:
                print("%d, %d : %s"%(x, y, str([z+1 for z in self.domain[x, y]])))
    
    def  makemove(self):
        for x,y in self.board:
            if not self.isset(x, y):
                if len(self.domain[x, y]) == 1:
                    if (self.fix(x, y, self.domain[x, y].pop())):
                        print()
                        return True
        print("UNABLE TO FIND SOLUTION")
        return False