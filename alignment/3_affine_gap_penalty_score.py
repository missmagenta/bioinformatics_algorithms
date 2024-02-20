import math

MATCH = 1
MISMATCH = -1

def align_with_affine_gap_penalty(seqA, seqB, GAPOPEN, GAP):
    matD = [[-math.inf for _ in range(len(seqB)+1)] for _ in range(len(seqA)+1)]
    matI = [[-math.inf for _ in range(len(seqB)+1)] for _ in range(len(seqA)+1)]
    matS = [[-math.inf for _ in range(len(seqB)+1)] for _ in range(len(seqA)+1)]

    matS[0][0] = 0
    matD[0][0] = matI[0][0] = GAPOPEN

    for i in range(1, len(seqA)+1):
        matD[i][0] = matD[i-1][0] + GAP
        matS[i][0] = matD[i][0]
    for j in range(1, len(seqB)+1):
        matI[0][j] = matI[0][j-1] + GAP
        matS[0][j] = matI[0][j]

    for i in range(1, len(seqA)+1):
        for j in range(1, len(seqB)+1):
            matD[i][j] = max(matD[i-1][j] + GAP, matS[i-1][j] + GAPOPEN + GAP)
            matI[i][j] = max(matI[i][j-1] + GAP, matS[i][j-1] + GAPOPEN + GAP)
            matS[i][j] = max(matS[i-1][j-1] + (MATCH if seqA[i-1] == seqB[j-1] else MISMATCH), max(matD[i][j], matI[i][j]))

    aligned_seqA = ""
    aligned_seqB = ""
    i = len(seqA)
    j = len(seqB)
    score = matS[i][j]

    while i > 0 or j > 0:
        if i > 0 and j > 0 and matS[i][j] == matS[i-1][j-1] + (MATCH if seqA[i-1] == seqB[j-1] else MISMATCH):
            aligned_seqA = seqA[i-1] + aligned_seqA
            aligned_seqB = seqB[j-1] + aligned_seqB
            i -= 1
            j -= 1
        elif i > 0 and matS[i][j] == matD[i][j]:
            aligned_seqA = seqA[i-1] + aligned_seqA
            aligned_seqB = '-' + aligned_seqB
            i -= 1
        else:
            aligned_seqA = '-' + aligned_seqA
            aligned_seqB = seqB[j-1] + aligned_seqB
            j -= 1

    return score


def print_matrix(seqA, seqB, matD, matI, matS):
    seqB = "-" + seqB
    seqA = "-" + seqA
    for (mat_name, mat) in zip(['D', 'I', 'S'], [matD, matI, matS]):
        print(" {} =".format(mat_name))
        print("  A\B", end="")
        print(''.join(['{:>5}'.format(b) for b in seqB]))

        for i, row in enumerate(mat):
            row = ['{:5d}'.format(x) if x > -math.inf else "   -∞" for x in row]
            row = ['{:>5}'.format(seqA[i])] + row
            print(''.join(row))


if __name__ == '__main__':
    seq1 = input()
    seq2 = input()
    gap_open, gap_extend = map(int, input().split())

    score = align_with_affine_gap_penalty(seq1, seq2, gap_open, gap_extend)

    print(score)
