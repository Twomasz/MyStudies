# SKOŃCZONE

def innocent_search(S, W):
    compare_counter = 0
    how_many_matches = 0
    start = 0

    while start <= len(S) - len(W):
        same = True

        searching_fragment = S[start:start + len(W)]
        for idx, char in enumerate(searching_fragment):
            compare_counter += 1
            if W[idx] != char:
                same = False
                break

        start += 1

        if same:
            how_many_matches += 1

    return f'{how_many_matches};{compare_counter}'


def RabinKarp(S, W):
    compare_counter = 0
    how_many_matches = 0
    how_many_overlaps = 0
    d = 256
    q = 101  # liczba pierwsza

    def hash_(word):
        hw = 0
        N = len(word)  # długość wzorca
        for i in range(N):
            # dla d będącego potęgą 2 można mnożenie zastąpić shiftem uzyskując pewne przyspieszenie obliczeń
            hw = (hw * d + ord(word[i])) % q

        return hw

    hW = hash_(W)

    M, N = len(S), len(W)

    h = 1
    for _ in range(N - 1):  # N - jak wyżej - długość wzorca
        h = (h * d) % q

    # wyznaczam wartość funkcji hashującej dla pierwszej iteracji
    m = 0
    hS = hash_(S[m: m+N])
    while m < M - N + 1:
        if hS == hW:
            compare_counter += 1
            if S[m: m + N] == W:
                how_many_matches += 1
            else:
                how_many_overlaps += 1

        else:
            compare_counter += 1

        if m + N < M:
            hS = (d * (hS - ord(S[m]) * h) + ord(S[m + N])) % q
            if hS < 0:
                hS += q
        m += 1

    return f'{how_many_matches};{compare_counter}'


def kmp_table(W):
    pos = 1
    cnd = 0
    T = [None for _ in range(len(W)+1)]
    T[0] = -1

    while pos < len(W):
        if W[pos] == W[cnd]:
            T[pos] = T[cnd]

        else:
            T[pos] = cnd

            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]

        pos += 1
        cnd += 1

    T[pos] = cnd

    return T


def KMP(S, W):
    compare_counter = 0
    how_many_matches = 0
    m = 0
    i = 0
    T = kmp_table(W)

    while m < len(S):
        compare_counter += 1
        if W[i] == S[m]:
            m += 1
            i += 1

            if i == len(W):
                how_many_matches += 1
                i = T[i] if T[i] != -1 else print("can't be")

        else:
            i = T[i]

            if i < 0:
                m += 1
                i += 1

    return f'{how_many_matches};{compare_counter}'


if __name__ == "__main__":
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ' '.join(text).lower()
    W = 'time.'

    print(innocent_search(S, W))
    print(RabinKarp(S, W))
    print(KMP(S, W))
