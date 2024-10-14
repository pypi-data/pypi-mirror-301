import matrix_add

a = np.array([[1,2,3],[4,5,6],[7,8,9]])
b = np.array([[1,2,3],[4,5,6],[7,5,4]])

c = matrix_add.add(a,b)

print('a =\n', np.array_str(a))
print('b =\n', np.array_str(b))
print('c =\n', np.array_str(c))