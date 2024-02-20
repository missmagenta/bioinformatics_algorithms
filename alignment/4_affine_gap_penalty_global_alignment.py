import math

def align_with_affine_gap_penalty(s, t, gap_open, gap):
    mismatch = -1
    match = 1

    main = [[-math.inf for _ in range(len(t) + 1)] for _ in range(len(s) + 1)]
    upper = [[-math.inf for _ in range(len(t) + 1)] for _ in range(len(s) + 1)]
    lower = [[-math.inf for _ in range(len(t) + 1)] for _ in range(len(s) + 1)]

    main[0][0] = 0
    for i in range(1, len(s) + 1):
        lower[i][0] = gap * i
        main[i][0] = lower[i][0] + gap_open
        
    for j in range(1, len(t) + 1):
        upper[0][j] = gap * j
        main[0][j] = upper[0][j] + gap_open
        
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            coef = match
            if s[i - 1] != t[j - 1]: 
                coef = mismatch
            upper[i][j] = max(upper[i][j - 1] + gap, main[i][j - 1] + gap_open + gap)
            lower[i][j] = max(lower[i - 1][j] + gap, main[i - 1][j] + gap_open + gap)
            main[i][j] = max(main[i - 1][j - 1] + coef, max(lower[i][j], upper[i][j]))

    i = len(s)
    j = len(t)
    wayS = ""
    wayT = ""
    flag = 0
    
    while i > 0 or j > 0:
        if i == 0:
            wayS = wayS + "-"
            wayT = wayT + t[j - 1]
            j -= 1
        elif j == 0: 
            wayS = wayS + s[i - 1]
            wayT = wayT + "-"
            i -= 1
        else: 
            coef = match
            if t[j - 1] != s[i - 1]:
                coef = mismatch
            if flag == 0:
                if main[i][j] == main[i - 1][j - 1] + coef:
                    wayS = wayS + s[i - 1]
                    wayT = wayT + t[j - 1]
                    i = i - 1
                    j = j - 1
                elif main[i][j] == lower[i][j]:
                    flag = 1
                else: 
                    flag = 2
            elif flag == 1:
                if lower[i][j] != lower[i - 1][j] + gap:
                    flag = 0
                wayS = wayS + s[i - 1]
                wayT = wayT + "-"
                i -= 1
            elif flag == 2:
                if upper[i][j] != upper[i][j - 1] + gap:
                    flag = 0
                wayS = wayS + "-"
                wayT = wayT + t[j - 1]
                j -= 1
    
    return wayS, wayT


if __name__ == '__main__':
    s = input()
    t = input()
    gap_open, gap = map(int, input().split())

    wayS, wayT = align_with_affine_gap_penalty(s, t, gap_open, gap)

    print(wayS[::-1])
    print(wayT[::-1])
