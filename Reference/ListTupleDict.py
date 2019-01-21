#
# Authored by Bryce Burgess
# basics of included data structures
#
#

# LISTS
list1 = []
list1.append('a')				# puts 'a' into list
list1.extend("", 34, 6, list1)	# adds sequence to list
list1.count('a')				# how many instances of 'a'
list1.index(6)					# lowest index w/ value 6
list1.insert(4,'hello')			# insert 'hello' at index 4
list1.remove('a')				# remove entry from list
list1.pop()						# remove and return last entry
list1.pop(6)					# remove and return designated object
list1.reverse()					# reverse order of list
list1.sort()					# sort list, use comparison fn if provided

list1[0]
len(list1)
list1 = list1 + list2
list1 = list1*2
del list[3]
6 in list

# TUPLES
# Declaring, can include different data types
tuple1 = ('physics', 'chemistry', 1997, 2000)
tuple2 = (1, 2, 3, 4, 5 )
tuple3 = "a", "b", "c", "d"

tuple1[0]			# get value at index
tuple1 + tuple2		# concatenated tuple
tuple1*2			# tuple concatenated with itself
6 in tuple1			# is 6 in tuple
len(tuple1)			# give tuple length
cmp(tuple1, tuple2)	# compare the similarity of tuples
max(tuple1)			# get max value of tuple
min(tuple1)			# get min value of tuple
tuple1(list1)		# turn list into tuple

# DICTIONARIES
# Declare dictionary
key = 'blah'
value = 7
dict1 = {key:value}
dict1['blah']				# return value of key 'blah'
dict1['new key'] = 32964	# create new key:value pair

cmp(dict1, dict2)
len(dict1)			# length of dict1
str(dict1)			# printable string from dict1

dict1.keys()		# return all keys in dict1
dict1.values()		# return all values in dict1
dict1.items()		# return all (key, value) in dict1
dict1.clear()		# remove all elements from dict1
dict1.copy()		# copy dict1
dict1.fromkeys(seq)	# create new dict with keys in seq
dict1.get(key)		# return value of key 
dict1.setdefault()	# 
dict1.has_key(key)	# check if key in dict1
dict1.update(dict2)
