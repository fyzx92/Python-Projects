"""
Authored by Bryce Burgess

6/4/2019

"""

import math
import skimage
import random
import numpy as np

class Image():
    def __init__(self, size):
        self.size = size
        self.__init_pixels()

    def __init_pixels(self):
        return None


class ImageMask():
    def __init__(self, height=1000, width = 1000):
        self.dims = (height, width)
        self.height = height
        self.width = width
        self.mask = np.zeros(self.dims)

    def ordered_lines(self, slope = 1/3, intercept_step = 50):
        
        for i in range(-self.height*slope, self.height, intercept_step):
            rr1, cc1 = skimage.draw.line(i, i, self.height*slope + i, self.width)
            rr2, cc2 = skimage.draw.line(i, self.width, self.height*slope + i, i)
        
        for i in range(intercept_step):
            rr3, cc3 = skimage.draw.line(0, i, self.height, i)

        self.mask[rr1, cc1] = 1
        self.mask[rr2, cc2] = 1
        self.mask[rr3, cc3] = 1

    def random_lines(self, n_lines):

        # choose random points on each edge
        grouped_intercepts   = {"left":  [[random.choice(range(self.height)), 0         ] for i in range(n_lines)],
                                "right": [[random.choice(range(self.height)), self.width] for i in range(n_lines)],
                                "top":   [[0,           random.choice(range(self.width))] for i in range(n_lines)],
                                "bottom":[[self.height, random.choice(range(self.width))] for i in range(n_lines)]
        }

        # get pairs of intercepts to create lines
        intercepts = [pt for key in grouped_intercepts.keys() for pt in grouped_intercepts[key]]
        for i in range(n_lines):
            pt1 = random.choice(intercepts)
            pt2 = random.choice(intercepts)

            # check that intercept pair are not on the same edge
            for key in grouped_intercepts:
                while pt1 in grouped_intercepts[key] and pt2 in grouped_intercepts[key]:
                    pt2 = random.choice(intercepts)
            
            # create line
            rr, cc = skimage.draw.line(pt1[0], pt1[1], pt2[0], pt2[1])
            self.mask[rr, cc] = 1

    def polygon_segments(self, _n_vertices):
        self.n_vertices = _n_vertices
        self.vertices = []
        for i in range(self.n_vertices):
            self.vertices.append([random.choice(range(self.height)), random.choice(range(self.width))])

        # how to create polygons?
    

    def find_region_indices(self):
        self.regions = {1:[]}
        for i,j in self.mask:
            for r in self.regions.keys():
                pix_in_regions = True
                
                # assign border pixels to region (bottom left for reference)
                if self.mask[i,j] == 1:
                    if any([self.mask[i+1,j] in self.regions[r], self.mask[i,j+1] in self.regions[r]]):
                        self.regions[r] += [[i,j]]

                # assign empty pixels to region based on neighbors
                if self.mask[i,j] == 0:
                    if any([self.mask[i+1,j] in self.regions[r], self.mask[i,j+1] in self.regions[r], self.mask[i-1,j] in self.regions[r], self.mask[i,j-1] in self.regions[r],]):
                        self.regions[r] += [[i,j]]
            else:
                pix_in_regions = False

            # if pixel not in existing regions, create a new one and add it
            if not pix_in_regions:
                self.regions[r+1] = [[i,j]]

        return self.regions



class PolygonPainting(Image):
    def __init__(self, size, n_colors, n_polygons):
        self.size = size
        self.__init_pixels()

        self.n_colors = n_colors

        self.n_polygons = n_polygons
        self.partition()

    def __init_pixels(self):
        pass

    def partition(self):
        # get random number
        polygon_max = 100 
        polygon_min = 30

        poly_dist = lambda polygon_min, polygon_max: random.random()*(polygon_max-polygon_min) + polygon_min

        # use number to get points around border
        border_len = 2*self.size[0] + 2*self.size[1]
        intervals = []
        while max(intervals) < border_len:
            intervals.append(poly_dist(polygon_max, polygon_min))

        for i in range(len(intervals)):
            if i != 0:
                intervals[i] += intervals[i-1]
            
        # turn interval into coordinates by travelling along edge
        outer_vertices = []
        for i in intervals:
            if i < self.size[0]:
                x = i
                y = 0

            elif i < self.size[0] + self.size[1]:
                x = self.size[0]
                y = i-self.size[0]

            elif i < 2*self.size[0] + self.size[1]:
                x = -i+self.size[0]+self.size[1]
                y = self.size[1]

            elif i < 2*self.size[0] + 2*self.size[1]:
                x = 0
                y = i-2*self.size[0] - self.size[1]
            
            outer_vertices.append((x, y))
        
        # get set of points randomly within some distance of border
        # connect nearish points to make polygons

        used_vertices = []
        dist = lambda x,y: (x[0] - y[0])**2 + (x[1] - y[1])**2
        for i in outer_vertices:
            # make polygon from 2-3 border vertices + nearby internal vertex
            pass


def choose_color():
    pass

