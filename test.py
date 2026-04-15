def faire(a,b, c, d):
    res = []
    for i in range(a, c+1):
        for j in range(b, d+1):
            res.append((i, j))
    return res
print(faire(16, 4, 19, 9 ))