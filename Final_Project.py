import tkinter as tk

from tkinter import Frame, Label, CENTER

import numpy as np

import keyboard
import time





class Node:
    '''
    class that defines a binary tree node
    each node has a pointer for the node to its left and its right
    the values stored in the node is the x and y position of the node within
    the greater graph
    '''
    def __init__(self, x, y):
        self.left = None
        self.right = None
        self.x = x
        self.y = y




class Tree:
    '''
    class that represents a binary tree. This class is used to represent
    the nodes that make up the root system. It is called tree to avoid confusion
    as it follows a generic binary tree method
    '''
    def __init__(self):
        '''
        in this case self.root represents the top of the tree
        rather than the actual roots that they represent
        '''
        self.root = None

   
    def add_node(self, parent, x, y):
        '''
        this method adds a new node to the tree 
        parent represents the parent node to which the 
        new node will be added, None if the tree is empty.
        x and y represent the coordinates of the new node
        and dir whether it will be to the left or the right
        of the parent node
        '''
        if self.root is None and parent is None:
            self.root = Node(x, y)
        
    def getRoot(self):
        return self.root
    def printTree(self):
        if self.root is not None:
            self._printTree(self.root)
    def _printTree(self, node):
        if node is not None:
            self._printTree(node.left)
            print(str([node.x, node.y]) + ' ')
            self._printTree(node.right)



class Display(Frame):
    EDGE_LENGTH = 100
    CELL_COUNT = 20
    CELL_PAD = 0.5

    iterations = 0

    GAME_COLOR = "black"

    COLOR_MAP = {-1 :"white", 0: "gray", 1: "#836539", 2: "#654321", 3: "#2b1d0e"}

    cells = 10
    nutrient_map = []
    rootSystem = Tree()
    rootMap = []
    def __init__(self):
        
        cell_count = input("How big of a grid would you like?: ")
        #self.iterations = input("How many iterations would you like the simulation to run? (0 to iterate manually): ")

        print("Click on the window that opened and use the Spacebar to iterate one step")
        

        self.cells =int(cell_count)

        for row in range(self.cells):
            cur_row = []
            for cols in range(self.cells):
                cur_row.append(0)
            self.rootMap.append(cur_row)
        

        self.init_grid()

        self.init_tree()

        Frame.__init__(self)

        self.grid()
        self.master.title('Root Simulation')
        self.master.bind("<Key>", self.key_press)

        self.CELL_COUNT = int(cell_count)
        
        self.grid_cells = []
        self.build_grid(self.nutrient_map)
        self.update_grid()

        
        self.mainloop()
        
    
    def key_press(self, event):
    
        R = self.rootSystem.getRoot()
        self.visitLeaves(R)
        self.update_grid()

    
    # creates the initial grid of nutrient values
    def init_grid(self):
        '''
        # generates a randomized nutrient map where 0 is no nutrients, 1 is low
        # 2 is medium, and 3 is high
        '''
        for rows in range (self.cells):
            cur_row = []
            for cols in range (self.cells):

                cur_row.append(np.random.randint(0,4))

            self.nutrient_map.append(cur_row)

        #self.nutrient_map = [[0, 2, 1, 3, 1], [1, 3, 2, 1, 0], [3, 1, 2, 0, 0], [3, 0, 1, 2, 1], [1, 2, 1, 3, 1]]
        #print(self.nutrient_map)

     

    def init_tree(self):
        '''
        This method sets up the binary tree by placing the first node in it
        and respecitvely updating that in the rootMap
        '''
        self.rootSystem.add_node(None, int(self.cells/2), 0)
        self.rootMap[0][int(self.cells/2)] = -1

        
    def notTouching(self, parentX, parentY, childX, childY):
        '''
        checks to see surrounding squares of a potential child node
        this is done to create more separation between root nodes
        '''
        #print([parentX, parentY, childX, childY])
        if(childY == 0 or self.rootMap[childY - 1][childX] != -1 or (childY - 1 == parentY and childX == parentX)):
            if(childX + 1 == self.cells or self.cells or self.rootMap[childY][childX + 1] != -1 or (childY== parentY and childX + 1 == parentX)):
                if(childX == 0 or self.rootMap[childY][childX - 1] != -1 or (childY == parentY and childX - 1 == parentX)):
                    if(childY + 1 == self.cells or self.cells and self.rootMap[childY + 1][childX] != -1 or (childY + 1 == parentY and childX == parentX)):
                        return True

        #print('cant go on')
        return False


    def visitLeaves(self, root):
        '''
        This code is what drives leaf growth. It recursively visits all of the
        leaves of the binary tree  and then performs the main operations below
        '''

        # the recursive algorithm works by checking to see if a node has a child
        # to the left or to the right. If it does, then that one is visited, 
        # otherwise it knows a leaf has been found
        if(root.left is not None):
            self.visitLeaves(root.left)

        if(root.right is not None):
            self.visitLeaves(root.right)

        if(root.left is None and root.right is None):
            x = root.x
            y = root.y


            valLeft = [0, 0]
            valRight = [0, 0]
            valMiddle = -1

            if(x-1 >= 0 and x + 1 < self.cells):
                if(y + 1 < self.cells):
                    # the node has space left, right, horizontally, and downwards
                    valLeft[0] = self.nutrient_map[y][x-1]
                    valLeft[1] = self.nutrient_map[y+1][x-1]

                    valMiddle = self.nutrient_map[y + 1][x]
                  
                    valRight[0] = self.nutrient_map[y][x + 1]
                    valRight[1] = self.nutrient_map[y+1][x+1]

                    # is the value in the middle greater than all the values to the left
                    # and is it valid to grow into
                    if(valMiddle >= max(valLeft) and self.rootMap[y + 1][x] != -1 and valMiddle != 0 and self.notTouching(x, y, x, y + 1)):
                        #print("going down full space ", [root.x, root.y])
                        root.left = Node(x,y+1)
                        self.rootMap[y + 1][x] = -1
                        
                    else:
                        # searches through other possible options until the best one is found
                        if(valLeft[0] >= valLeft[1] and self.rootMap[y][x - 1] != -1 and valLeft[0] != 0 and self.notTouching(x, y, x - 1, y)):
                            #print("going left full space ", [root.x, root.y])
                            
                            root.left = Node(x-1, y)
                            self.rootMap[y][x - 1] = -1
                         
                        elif(valLeft[1] != 0 and self.rootMap[y + 1][x - 1] != -1 and self.notTouching(x, y, x - 1, y + 1)):
                            #print("trying to go diagonal")
                            if(valMiddle != 0 and self.rootMap[y + 1][x] != -1):
                                root.left = Node(x, y+1)
                                root.left.left = Node(x-1,y+1)
                                #print("going down left full space ", [root.x, root.y])
                                #print(valLeft[1], self.nutrient_map[y + 1][x - 1])
                                self.rootMap[y + 1][x - 1] = -1
                                self.rootMap[y + 1][x] = -1
                            elif(valLeft[0] != 0 and self.rootMap[y][x - 1] != -1):
                                root.left = Node(x - 1, y)
                                root.left.left = Node(x-1,y+1)
                                #print("going down left full space ", [root.x, root.y])
                                #print(valLeft[1], self.nutrient_map[y + 1][x - 1])
                                self.rootMap[y][x - 1] = -1
                                self.rootMap[y + 1][x] = -1

                        # worst case scenario, a child cannot be made
                        else:
                            root.left = None

                    #print("checking right side")

                    # the exact process is repeated with the right side of the node
                    if(valMiddle >= max(valRight) and self.rootMap[y + 1][x] != -1 and valMiddle != 0 and self.notTouching(x, y, x, y + 1)):
                        #print("going down full space ", [root.x, root.y])
                        root.right = Node(x,y+1)
                        self.rootMap[y + 1][x] = -1
                    
                    elif(valRight[0] >= valRight[1] and self.rootMap[y][x + 1] != -1 and valRight[0] != 0 and self.notTouching(x, y, x + 1, y)):
                        root.right = Node(x+1, y)
                        #print("going right full space ", [root.x, root.y])
                        #print(valRight[0], self.nutrient_map[y][x + 1])
                        self.rootMap[y][x + 1] = -1
                           
                    elif(valRight[1] != 0 and self.rootMap[y + 1][x + 1] != -1 and self.notTouching(x, y, x + 1, y + 1)):
                        if(valMiddle != 0 and self.rootMap[y + 1][x] != -1):
                            root.right = Node(x,y + 1)
                            root.right.right = Node(x+1,y+1)
                            #print("going down right full space ", [root.x, root.y])
                            #print(valRight[1], self.nutrient_map[y + 1][x + 1])     
                            self.rootMap[y + 1][x + 1] = -1
                            self.rootMap[y + 1][x] = -1
                        elif(valRight[0] != 0 and self.rootMap[y][x + 1] != -1):
                                root.right = Node(x + 1, y)
                                root.right.right = Node(x+1,y+1)
                                #print("going down left full space ", [root.x, root.y])
                                #print(valLeft[1], self.nutrient_map[y + 1][x - 1])
                                self.rootMap[y][x + 1] = -1
                                self.rootMap[y + 1][x + 1] = -1
    
                    else:
                        root.right = None

                    # if(root.left is None and root.right is None):
                    #     return -1
                    # else:
                    #     return 1

                else:
                    # if it enters here then the node has room left and right, but not down
                    if(self.nutrient_map[y][x - 1] != 0 and self.rootMap[y][x - 1] != -1 and self.notTouching(x, y, x - 1, y)):
                        root.left = Node(x-1, y)
                        self.rootMap[y][x - 1] = -1
                    else:
                        root.left = None
                    if(self.nutrient_map[y][x + 1] != 0 and self.rootMap[y][x + 1] != -1 and self.notTouching(x, y, x + 1, y)):
                        root.right = Node(x+1, y)
                        self.rootMap[y][x + 1] = -1
                    else:
                        root.right = None
                # return 0

            # the rest of the method is functionally identical, only
            # with some parts cut out due to restrictions in the general area


            elif(x-1 >= 0 and x + 1 >= self.cells):
                root.right = None
                if(y + 1 < self.cells):
                    # the node has space to the left and down, but not to the right
                    valLeft[0] = self.nutrient_map[y][x - 1]
                    valLeft[1] = self.nutrient_map[y+1][x-1]
                    valMiddle = self.nutrient_map[y + 1][x] 

                    if(valMiddle >= max(valLeft) and self.rootMap[y + 1][x] != -1 and valMiddle != 0 and self.notTouching(x, y, x, y + 1)):
                        root.left = Node(x,y+1)
                        self.rootMap[y + 1][x] = -1
                        # return 1

                    else:
                        if(valLeft[0] >= valLeft[1] and self.rootMap[y][x - 1] != -1 and valLeft[0] != 0 and self.notTouching(x, y, x - 1, y)):
                            root.left = Node(x-1, y)
                            self.rootMap[y][x - 1] = -1
                            # return 1
                        elif(valLeft[1] != 0 and self.rootMap[y + 1][x - 1] != -1 and self.notTouching(x, y, x - 1, y + 1)):
                            #print("going down left less space ", [root.x, root.y])
                            print(valLeft[1], self.nutrient_map[y + 1][x - 1])
                            if(valMiddle != 0 and self.rootMap[y + 1][x] != -1):
                                root.left = Node(x, y+1)
                                root.left.left= Node(x-1,y+1)
                                self.rootMap[y + 1][x - 1] = -1
                                self.rootMap[y + 1][x] = -1
                                # return 1
                        else:
                            root.left = None
                            # return -1

                else:
                    # the node only has space to the left
                    if(self.nutrient_map[y-1][x-1] != 0 and self.rootMap[y][x - 1] != -1 and self.notTouching(x, y, x - 1, y)):
                        root.left = Node(x-1,y)
                        self.rootMap[y][x - 1] = -1
                        # return 1
                    else:
                        root.left = None
                        # return -1
                # return 0
            elif(x - 1 < 0 and x + 1 < self.cells):
                root.left = None
                if(y + 1 < self.cells):
                    # node has space to the right and down but not to the left
                    valRight[0] = self.nutrient_map[y][x+1]
                    #valRight[1] = self.nutrient_map[y+1][x + 1]
                    valMiddle = self.nutrient_map[y + 1][x] 

                    if(valMiddle >= max(valRight) and self.rootMap[y + 1][x] != -1 and valMiddle != 0 and self.notTouching(x, y, x, y + 1)):
                        root.right = Node(x,y+1)
                        self.rootMap[y + 1][x] = -1
                        # return 1
                    else:
                        if(valRight[0] >= valRight[1] and self.rootMap[y][x + 1] != -1 and valRight[0] != 0 and self.notTouching(x, y, x + 1, y)):
                            root.right = Node(x+1, y)
                            self.rootMap[y][x + 1] = -1
                            # return 1
                        elif(valLeft[1] != 0 and self.rootMap[y + 1][x + 1] != -1 and self.notTouching(x, y, x + 1, y + 1)):
                            if(valMiddle != 0 and self.rootMap[y + 1][x] != -1):
                                root.right = Node(x, y+1)
                                root.right= Node(x+1,y+1)
                                self.rootMap[y + 1][x] = -1
                                self.rootMap[y + 1][x + 1] = -1
                                # return 1
                        else:
                            root.right = None
                            # return -1
                else:
                    # the node only has space to the right
                    if(self.nutrient_map[y][x+1] != 0 and self.rootMap[y][x + 1] != -1 and self.notTouching(x, y, x + 1, y)):
                        root.right = Node(x+1,y)
                        self.rootMap[y][x+1] = -1
                        # return 1
                    else:
                        root.right = None
                        # return -1
                # return 0

            return -1
        

    def build_grid(self, map):
        '''
        This method initializes the grid based on the generated rootmap
        '''
        background = Frame(self, bg=self.GAME_COLOR, width=self.EDGE_LENGTH, height=self.EDGE_LENGTH)
        background.grid()

        for row in range(self.CELL_COUNT):
            grid_row = []
            for col in range(self.CELL_COUNT):
                cell = Frame(background, bg=self.COLOR_MAP[map[row][col]],width=2,height=1)

                cell.grid(row=row, column=col, padx=self.CELL_PAD,pady=self.CELL_PAD)

                t = Label(master=cell,bg=self.COLOR_MAP[map[row][col]],justify=CENTER, width=2, height=1)

                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)
        
    
    def update_grid(self):
        '''
        this method is called on keypresses and updates the colors on the map to show
        root growth
        '''
        for row in range(self.CELL_COUNT):

            for col in range(self.CELL_COUNT):
                if(self.rootMap[row][col] == -1):
                    self.grid_cells[row][col].configure(bg = self.COLOR_MAP[-1])
                    
        self.update_idletasks() 

   
        
grid = Display()

    


    

