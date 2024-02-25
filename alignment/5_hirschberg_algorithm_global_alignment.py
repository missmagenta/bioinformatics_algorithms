match_award = 2
mismatch_penalty = -1
gap_penalty = -2


def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty


def nw(A, B):
    n, m = len(A), len(B)
    mat = []

    for i in range(n+1):
        mat.append([0]*(m+1))

    for j in range(m+1):
        mat[0][j] = gap_penalty*j

    for i in range(n+1):
        mat[i][0] = gap_penalty*i

    for i in range(1, n+1):
        for j in range(1, m+1):
            mat[i][j] = max(mat[i-1][j-1] + match_score(A[i-1], B[j-1]), mat[i][j-1] + gap_penalty, mat[i-1][j] + gap_penalty)

    alignment_A = ""
    alignment_B = ""
    i, j = n, m

    while i and j:
        score, score_diag, score_up, score_left = mat[i][j], mat[i-1][j-1], mat[i-1][j], mat[i][j-1]
        if score == score_diag + match_score(A[i-1], B[j-1]):
            alignment_A = A[i-1] + alignment_A
            alignment_B = B[j-1] + alignment_B
            i -= 1
            j -= 1
        elif score == score_up + gap_penalty:
            alignment_A = A[i-1] + alignment_A
            alignment_B = '-' + alignment_B
            i -= 1
        elif score == score_left + gap_penalty:
            alignment_A = '-' + alignment_A
            alignment_B = B[j-1] + alignment_B
            j -= 1
    while i:
        alignment_A = A[i-1] + alignment_A
        alignment_B = '-' + alignment_B
        i -= 1
    while j:
        alignment_A = '-' + alignment_A
        alignment_B = B[j-1] + alignment_B
        j -= 1
    
    return [alignment_A, alignment_B, mat[n][m]]


def forwards(x, y):

    n, m = len(x), len(y)
    mat = []
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j] = gap_penalty*j
    for i in range(1, n+1):
        mat[i][0] = mat[i-1][0] + gap_penalty
        for j in range(1, m+1):
            mat[i][j] = max(mat[i-1][j-1] + match_score(x[i-1], y[j-1]),
                            mat[i-1][j] + gap_penalty,
                            mat[i][j-1] + gap_penalty)
        
        mat[i-1] = []
    return mat[n]    


def backwards(x, y):
    
    n, m = len(x), len(y)
    mat = []
    for i in range(n+1):
        mat.append([0]*(m+1))
    for j in range(m+1):
        mat[0][j] = gap_penalty*j
    for i in range(1, n+1):
        mat[i][0] = mat[i-1][0] + gap_penalty
        for j in range(1, m+1):
            mat[i][j] = max(mat[i-1][j-1] + match_score(x[n-i], y[m-j]),
                            mat[i-1][j] + gap_penalty,
                            mat[i][j-1] + gap_penalty)
        
        mat[i-1] = []
    return mat[n]


def hirschberg(x, y):
    n, m = len(x), len(y)
    if n<2 or m<2:

        return nw(x, y)
    else:

        F, B = forwards(x[:n//2], y), backwards(x[n//2:], y)
        partition = [F[j] + B[m-j] for j in range(m+1)]
        cut = partition.index(max(partition))
       
        F, B, partition = [], [], []

        call_left = hirschberg(x[:n//2], y[:cut])
        call_right = hirschberg(x[n//2:], y[cut:])
       
        return [call_left[r] + call_right[r] for r in range(3)]
    

if __name__ == '__main__':
    A = input()
    B = input()
        
    z = hirschberg(A, B)

    print(z[0])
    print(z[1])
