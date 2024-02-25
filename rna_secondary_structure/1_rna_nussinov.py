import numpy as np

def couple(pair):
    pairs = [('U', 'A'), ('A', 'U'), ('G', 'C'), ('C', 'G')]

    if pair in pairs:
        return True
    return False


def build_dp(matrix, rna):
	rna_len = len(rna)
	minimal_loop_length = 2

	for k in range(1, rna_len):
		for j in range(k, rna_len):
			i = j - k

			if j - i >= minimal_loop_length:
				down = matrix[i + 1][j]
				left = matrix[i][j - 1] 
				diag = matrix[i + 1][j - 1] + couple((rna[i], rna[j])) 

				rc = 0
				for t in range(i, j):
					rc = max(rc, matrix[i][t] + matrix[t + 1][j]) 

				matrix[i][j] = max(down, left, diag, rc)
			
			else:
				matrix[i][j] = 0

	return matrix	

def traceback(matrix, rna, fold, i, L):
	j = L

	if i < j:
		if matrix[i][j] == matrix[i + 1][j]:
			traceback(matrix, rna, fold, i + 1, j)
		elif matrix[i][j] == matrix[i][j - 1]: 
			traceback(matrix, rna, fold, i, j - 1)
		elif matrix[i][j] == matrix[i + 1][j - 1] + couple((rna[i], rna[j])):
			fold.append((i, j))
			traceback(matrix, rna, fold, i + 1, j - 1)
		else:
			for k in range(i + 1, j - 1):
				if matrix[i][j] == matrix[i, k] + matrix[k + 1][j]: 
					traceback(matrix, rna, fold, i, k)
					traceback(matrix, rna, fold, k + 1, j)
					break

	return fold


def init_matrix(rna):
	M = len(rna)
	
	matrix = np.empty([M, M])

	matrix[range(M), range(M)] = 0
	matrix[range(1, M), range(M - 1)] = 0

	return matrix


if __name__ == "__main__":
	rna = input()

	nm = init_matrix(rna)
	nm = build_dp(nm, rna)

	fold = []

	fold = traceback(nm, rna, fold, 0, len(rna) - 1)
	
	print(len(fold))