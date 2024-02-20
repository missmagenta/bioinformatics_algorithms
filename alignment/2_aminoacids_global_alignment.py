from Bio.Align import substitution_matrices

def load_blosum62():
    return substitution_matrices.load("BLOSUM62")


def global_alignment(s, t, gap_penalty=-5):
    blosum62 = load_blosum62()
    n = len(s)
    m = len(t)

    score_matrix = [[0] * (m + 1) for _ in range(n + 1)]
    traceback = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        score_matrix[i][0] = gap_penalty * i
        traceback[i][0] = 'up'

    for j in range(1, m + 1):
        score_matrix[0][j] = gap_penalty * j
        traceback[0][j] = 'left'

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = blosum62.get((s[i - 1], t[j - 1]), blosum62.get((t[j - 1], s[i - 1])))
            diagonal_score = score_matrix[i - 1][j - 1] + match_score
            up_score = score_matrix[i - 1][j] + gap_penalty
            left_score = score_matrix[i][j - 1] + gap_penalty

            max_score = max(diagonal_score, up_score, left_score)
            score_matrix[i][j] = max_score

            if max_score == diagonal_score:
                traceback[i][j] = 'diagonal'
            elif max_score == up_score:
                traceback[i][j] = 'up'
            else:
                traceback[i][j] = 'left'

    align_s = ''
    align_t = ''
    i, j = n, m

    while i > 0 or j > 0:
        if i > 0 and j > 0 and traceback[i][j] == 'diagonal':
            align_s = s[i - 1] + align_s
            align_t = t[j - 1] + align_t
            i -= 1
            j -= 1
        elif i > 0 and traceback[i][j] == 'up':
            align_s = s[i - 1] + align_s
            align_t = '-' + align_t
            i -= 1
        else:
            align_s = '-' + align_s
            align_t = t[j - 1] + align_t
            j -= 1

    return align_s, align_t


if __name__ == '__main__':
    seq1 = input()
    seq2 = input()

    aligned_1, aligned_2 = global_alignment(seq1, seq2)

    print(aligned_1)
    print(aligned_2)
