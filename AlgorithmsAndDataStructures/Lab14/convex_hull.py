# SKOŃCZONE

def orientation(p1, p2, p3):
    result = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p3[1] - p2[1]) * (p2[0] - p1[0])

    return result


def convexHull(points, version2=False):
    size = len(points)
    if size < 3:
        return points

    # wybieranie punktu początkowego
    p = 0
    for idx in range(size):
        if points[idx][0] < points[p][0]:
            p = idx
        elif points[idx][0] == points[p][0]:
            if points[idx][1] < points[p][1]:
                p = idx

    hull = []

    last_p_idx = p
    while True:
        hull.append(points[p])

        q = p + 1 if p + 1 < size else 0  # zawijanie indeksu

        for r in range(size):
            alpha = orientation(points[p], points[q], points[r])
            if alpha > 0:
                q = r
            if version2 and alpha == 0:  # dodatkowy warunek dla drugiej wersji
                if points[p] <= points[q] <= points[r] or points[r] <= points[q] <= points[p]:
                    q = r

        p = q

        if p == last_p_idx:
            return hull


if __name__ == '__main__':
    points0 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
    points1 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
    points2 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]

    # print(convexHull(points0, version2=True))
    # print(convexHull(points1, version2=True))
    print(convexHull(points2))
    print(convexHull(points2, version2=True))
