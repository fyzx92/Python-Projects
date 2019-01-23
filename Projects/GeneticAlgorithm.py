#
# Authored by Bryce Burgess
#
# Genetic Algorithm
#

import random

class Creature():
    def __init__(self, _dna):
        self.dna = _dna
        pass

    def reproduce(self):

        child = Creature()
        child.__init__()
        pass
class DNA(object):
    def __init__(self):
        self.genes = ""
        pass
    
    def copy(self):
        copy = self.genes
        return copy
    
    def mutate(self, prob):
        self.mutated_genes = self.genes
        for i in self.mutated_genes:
            pass