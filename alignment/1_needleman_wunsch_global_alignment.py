match_award = 1
mismatch_penalty = -1
gap_penalty = -2


def zeros(rows, cols):
    retval = []
    for x in range(rows):
        retval.append([])
        for y in range(cols):
            retval[-1].append(0)
    
    return retval


def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty


def needleman_wunsch(seq1, seq2):
    n = len(seq1)  
    m = len(seq2)
    
    score = zeros(m + 1, n + 1)
   
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            
            match = score[i - 1][j - 1] + match_score(seq1[j - 1], seq2[i - 1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            
            score[i][j] = max(match, delete, insert)
    
    align1 = ""
    align2 = ""
    
    i = m
    j = n
    
    while i > 0 and j > 0:
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1]):
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += seq1[j-1]
            align2 += '-'
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += '-'
            align2 += seq2[i-1]
            i -= 1

    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        j -= 1

    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        i -= 1
    
    align1 = align1[::-1]
    align2 = align2[::-1]
    
    return(align1, align2)


if __name__ == '__main__':
    seq1 = input()
    seq2 = input()

    alligned1, alligned2 = needleman_wunsch(seq1, seq2)

    print(alligned1)
    print(alligned2)