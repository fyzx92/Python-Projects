# Authored by Bryce Burgess
# Dragon curve fractal
# note: it can always be translated into a line
# never doubles back on itself
# need to establish origin(s)

class Line():
    def ___init1___(self, angle):
        self.length = 1
        self.angle = angle

    def ___init2___(self, end1, end2):
        self.length = 1
        if len(end1) == 2 and len(end2) == 2:
            self.end1 = end1
            self.end2 = end2
        else:
            print("error, bad endpoints for line declaration")

class Fractal():
    def ___init___(self, start_seg_list = "0"):
        self.seg_list_old = start_seg_list
        self.seg_list_new = ""
        #  3  2  1
        #   \ | /
        #  4- . -0 number corresponds to direction
        #   / | \
        #  5  6  7
        self.dictionary = ["0","1","2","3","4","5","6","7"]

    # Method 1 iterates by copying the previous fractal, rotating the copy, and concatenating it
    def iterate_copy(self, fold = "left", iter = 1):
        # how to fold
        if fold == "left" or fold == "alternate":
            left = True
        elif fold == "right":
            left = False
        # 
        for j in list(range(iter)):
            self.seg_list_old = self.seg_list_new
            if left:
                self.seg_list_new = rotate_fractal_90(fold_left = True) + self.seg_list_old
            elif ~left:
                self.seg_list_new = rotate_fractal_90(fold_left = False) + self.seg_list_old
            
            if fold == "alternate":
                left = ~left

        def rotate_fractal_90 (self, fold_left = True):
            self.seg_list_copy = ""
            if fold_left:
                for i in self.seg_list_old:
                    for j in self.dictionary:
                        if i == self.dictionary[j]:
                            self.seg_list_copy += self.dictionary[(j+2)%8]
                        else:
                            print("error, bad character in string")
                            self.seg_list_copy = ""
                            return
                return self.seg_list_copy

            if ~fold_left:
                for i in self.seg_list_old:
                    for j in self.dictionary:
                        if i == self.dictionary[j]:
                            self.seg_list_copy += self.dictionary[(j-2)%8]
                        else:
                            print("error, bad character in string")
                            self.seg_list_copy = ""
                            return
                return self.seg_list_copy

        return self.seg_list_new

    # Method 2 iterates by going line by line through a set of rules to choose the new direction based on the previous
    def iterate_sequence(self, iter = 1, fold = "left"):
        # choose how to start first fold
        if fold == "left" or "alternate":
            left = True
        else:
            left = False

        for i in list(range(iter)):
            if fold == "alternate":
                left = ~left

            # 
            for j in self.dictionary:
                if self.seg_list_old[0] == self.dictionary[j]:

                    if left:
                        self.seg_list_new[0] = self.dictionary[(j+1)%8]
                    elif ~left:
                        self.seg_list_new[0] = self.dictionary[(j-1)%8]

                # 
                while self.seg_list_new < 2*self.seg_list_old:
                    if self.seg_list_new[-1] == self.dictionary[j]:
                        # joints must be 90*
                        # line connecting endpoints must match original line
                        if self.seg_list_old[ (int)(len(self.seg_list_new)/2) ] == self.dictionary[(j+1)%8]:
                            next_char = (j+2)%8
                        if self.seg_list_old[ (int)(len(self.seg_list_new)/2) ] == self.dictionary[(j-1)%8]:
                            next_char = (j-2)%8

                        self.seg_list_new.append(next_char)


#    for i in self.seg_list_old:
#        if i == "0":
#            newchar = [[1,7],[7,1]]
