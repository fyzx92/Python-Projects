#
# Authored by Bryce Burgess
#
# Genetic Algorithm
#

import random

class Creature(object):
    def __init__(self, _genes):
        self.genes = Genes(_genes)

    def reproduce(self, partner):
        genes_passed = self.genes.copy()
        genes_passed.crossover(partner)
        genes_passed.mutate(prob = 0.01)
        child = Creature(genes_passed)
        return child

    def getPhenotype(self):
        pass

    def calcFitness(self, target): # need better algorithm for this
        score = 0
        for i in target:
            if self.genes.genes[i] == target[i]:
                score += 1
        return score

class Genes(object):
    possible_genes = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    def __init__(self, _genes = None):
        self.genes =_genes 
    
    def copy(self):
        copy = Genes(self.genes)
        return copy
    
    def crossover(self, partner):
        midpoint = len(self.genes)//2 # calculate midpoint of genes
        child_dna = self.copy()

        for i in enumerate(self.genes):
            if i < midpoint:
                child_dna.genes[i] = partner.genes[i]

    def mutate(self, prob):
        mutated_genes = self.genes
        for i in enumerate(mutated_genes):
            if random.random() <= prob:
                mutated_genes[i] = random.choice(Genes.possible_genes)
        return mutated_genes

class Phenotype(Genes):
    def __init__(self, _genes):
        self.genes = _genes.genes

    def interpret(self):
        pass

    def fitness(self, env):
        pass