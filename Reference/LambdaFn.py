#
# Authored by Bryce Burgess
# basics of lambda functions
#
#

# valid but not super useful
lambda x: x**2 # does not return anything, can't be reused

(lambda x: x**2)(4) # return 2**4, can't be reused

# usually assign to a variable
a = lambda x: x**3
a(7) # returns 7**3 == 347

