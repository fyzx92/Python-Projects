# Authored by Bryce Burgess
# Dragon curve fractal
# note: it can always be translated into a line
# never doubles back on itself
# need to establish origin(s)

import matplotlib.pyplot as plt
import math

class Fractal():
    def __init__(self, start_seg_list = "0", pattern = "left"):
        self.seg_list_old = start_seg_list
        self.seg_list_new = "0"
        #  3  2  1
        #   \ | /
        #  4- . -0 number corresponds to direction
        #   / | \
        #  5  6  7
        self.dictionary = ["0","1","2","3","4","5","6","7"]
        
        # how to fold TODO implement later
        self.pattern = pattern #"alternate", "right"
        if self.pattern == "left" or self.pattern =="alternate":
            self.fold_left = True
        elif self.pattern == "right":
            self.fold_left = False
            
    # Method 1 iterates by copying the previous fractal, rotating the copy, and concatenating it
    def iterate_by_copy(self, itr = 1):
            
        for j in list(range(itr)):
            self.rotate_copy_fractal_90(rotate_left = self.fold_left)
            # reverse and invert copy
            self.seg_list_old = self.seg_list_new
            if self.pattern == "alternate":
               self.fold_left = not self.fold_left

    def rotate_copy_fractal_90 (self, rotate_left = True):
        self.seg_list_copy = ""
        if rotate_left:
            rotation_direction = 2
        else:
            rotation_direction = -2
        
        try:
            # write the new list
            for c in self.seg_list_old:
                for j in range(len(self.dictionary)):
                    if c == self.dictionary[j]:
                        self.seg_list_copy += self.dictionary[(j-rotation_direction)%8]
            
            # reverse order of new list (prepare for prepending)
            self.seg_list_copy = self.seg_list_copy[::-1]
        
        except:
            print("error, bad character in string")
            self.seg_list_copy = ""
            
            
        self.seg_list_new = self.seg_list_copy + self.seg_list_old
        
    # Method 2 iterates by going line by line through a set of rules to choose the new direction based on the previous
    # TODO is only producing a sequence of ones
    def iterate_by_sequence(self, iter = 1, fold = "left"):
        # choose how to start first fold
#        if fold == "left" or "alternate":
#            left = True
#        else:
#            left = False

        for i in list(range(iter)):
#            if fold == "alternate":
#                left =  not left
            
            
            
            for j in range(len(self.dictionary)):
                
                if self.seg_list_old[0] == self.dictionary[j]:
                    
                    if left:
                        self.seg_list_new += self.dictionary[(j+1)%8]
                    elif not left:
                        self.seg_list_new += self.dictionary[(j-1)%8]
                        
                while len(self.seg_list_new) < 2*len(self.seg_list_old):
                    if self.seg_list_new[-1] == self.dictionary[j]:
                        # joints must be 90*
                        # line connecting endpoints must match original line
                        if self.seg_list_old[ (int)(len(self.seg_list_new)/2) ] == self.dictionary[(j+1)%8]:
                            next_char = (j+2)%8
                        if self.seg_list_old[ (int)(len(self.seg_list_new)/2) ] == self.dictionary[(j-1)%8]:
                            next_char = (j-2)%8
                            
                        self.seg_list_new += next_char
                        
    def display1(self):
        seg_length = 1
        x = [0]
        y = [0]
        for c in self.seg_list_new:
            if c == "0":
                x.append(x[-1] + seg_length*1)
                y.append(y[-1])
                
            if c == "1":
                x.append(x[-1] + seg_length*0.7)
                y.append(y[-1] + seg_length*0.7)
            
            if c == "2":
                x.append(x[-1])
                y.append(y[-1] + seg_length*1)
            
            if c == "3":
                x.append(x[-1] - seg_length*0.7)
                y.append(y[-1] + seg_length*0.7)
            
            if c == "4":
                x.append(x[-1] - seg_length*1)
                y.append(y[-1])

            if c == "5":
                x.append(x[-1] - seg_length*0.7)
                y.append(y[-1] - seg_length*0.7)
            
            if c == "6":
                x.append(x[-1])
                y.append(y[-1] - seg_length*1)
            
            if c == "7":
                x.append(x[-1] + seg_length*0.7)
                y.append(y[-1] - seg_length*0.7)
                
        # line from (x_old, y_old) to (x,y)
        plt.plot(x,y,"-")
            
    def display2(self):
        seg_length = 1
        x = []
        y = []
        for c in self.seg_list_new:
            for i in enumerate(self.dictionary):
                if c == self.dictionary[i]:
                    angle = i*math.pi/4
            x.append(seg_length*math.cos(angle))
            y.append(seg_length*math.sin(angle))
            # line from (x_old, y_old) to (x,y)
        
        plt.plot(x,y, "-")

