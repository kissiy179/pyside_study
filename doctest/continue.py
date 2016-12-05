'''
>>> s = 'this is doctest test.'
'''


def Test():
	'''
	>>> s = 'test'
	'''
	pass



def Test2():
	'''
	>>> s
	'this is doctest test.'
	'''
	pass



if __name__ == '__main__':
	import doctest
	doctest.testmod(verbose=True)