

############################################################
# Imports
############################################################

from copy import deepcopy

############################################################
#  Sudoku
############################################################

def sudoku_cells():
    cells=[]
    for i in range(0,9):
        for j in range(0,9):
            cells.append((i,j))
    return cells

def row_arcs(point):
    res=[]
    for i in range(0,9):
        if i==point[1]:
            pass
        else:
            res.append((point[0],i))
    return res

def col_arcs(point):
    res=[]
    for i in range(0,9):
        if i==point[0]:
            pass
        else:
            res.append((i,point[1]))
    return res

def block_arcs(point):
    res = []
    pos = (point[0]/3, point[1]/3)
    for row in range(pos[0] * 3, pos[0] * 3 + 3):
        for col in range(pos[1] * 3, pos[1] * 3 + 3):
            if row != point[0] or col != point[1]:
                res.append((row, col))
    return res


def sudoku_arcs():
    res=[]
    for i in range(0,9):
        for j in range(0,9):
            point=(i,j)
            for ele in row_arcs(point):
                res.append((point,ele))
            for ele in col_arcs(point):
                res.append((point,ele))
            for ele in block_arcs(point):
                res.append((point,ele))
    res=list(set(res))
    return res


def read_board(path):
    puzzle={}
    i=0;j=0
    l=set([1,2,3,4,5,6,7,8,9])
    f_read=open(path,'r')
    lines=f_read.read().split()
    for line in lines:
        for char in line:
            if char=='*':
                puzzle[(i,j)]=l
            else:
                puzzle[(i,j)]=set([int(char)])
            j=(j+1)%9
        i=(i+1)%9
    return puzzle
   
class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    

    def __init__(self, board):
        self.board=board

    def get_values(self, cell):
        return self.board[(cell)]

    def remove_inconsistent_values(self, cell1, cell2):
        ele=list(self.board[cell2])
        if len(list(self.board[cell1]))>1 or len(list(self.board[cell2]))>1:     
            if len(ele)>1:
                return False
            else:
                ele=ele[0]
            temp=list(self.board[cell1])
            if ele in temp:
                temp.remove(ele)
                self.board[cell1]=set(temp)
                return True
        return False


    def infer_ac3(self):
        q=deepcopy(self.ARCS)
        while q!=[]:
            top=q.pop(0)
            if self.remove_inconsistent_values(top[0],top[1]):
                for tup in self.ARCS:
                    if (tup[1]==top[0] and tup[0]!=top[1]): #or (tup[0]==top[0] and tup[1]!=top[1]):
                        q.append(tup)


    def check(self,checkpoint,val):
        count1=0
        count2=0
        count3=0
        for points in row_arcs(checkpoint):
            if val in self.board[points]:
                count1+=1
        for points in col_arcs(checkpoint):
            if val in self.board[points]:
                count2+=1
        for points in block_arcs(checkpoint):
            if val in self.board[points]:
                count3+=1
        if count1>0 and count2>0 and count3>0:
            return False
        else:
            return True

                
    def infer_improved(self):
        copy=deepcopy(self.board)
        self.infer_ac3()
        for point in self.CELLS:
          if (len(list(self.board[point]))>1):
            for vals in (list(self.board[point])):
                if self.check(point,vals):
                    self.board[point]=set([vals])
                    break
        self.infer_ac3()
        if copy==self.board:
            return
        else:
            self.infer_improved()

    def is_complete(self):
        for points in self.CELLS:
            if len(list(self.board[points]))>1 or len(list(self.board[points]))<1:
                return False
        return True

    def is_valid(self):
        for point1,point2 in self.ARCS:
            val=self.board[point1]
            for arc_points in self.ARCS:
                if point1==arc_points[0]:
                    if self.board[arc_points[1]]==val:
                        return False
        return True

    def infer_helper(self, new_b):
        if new_b.is_complete() and new_b.is_valid():
            return True
        for points in new_b.CELLS:
            if len(list(new_b.board[points]))>1:
                for vals in list(new_b.board[points]):
                    newbie2=deepcopy(new_b)
                    newbie2.board[points]=set([vals])
                    newbie2.infer_improved()
                    if not newbie2.is_complete() or not newbie2.is_valid():
                        continue
                    if self.infer_helper(newbie2):
                        self.board = newbie2.board
                        return True
        return False

    def infer_with_guessing(self):
        self.infer_improved()
        self.infer_helper(self)

    def print_board(self):
        for i in range(0,9):
            for j in range(0,9):
                print str((i,j))+str(self.get_values((i,j)))




    


    


