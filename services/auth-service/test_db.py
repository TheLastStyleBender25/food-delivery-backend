ratings = [1,3,4,5,2]
cndy = [1] * len(ratings)
for i in range(1, len(ratings)):
    if ratings[i] > ratings[i-1]:
        cndy[i] = cndy[i-1]+1
print(cndy)
for i in range(len(ratings)-2, -1, -1):
    if ratings[i] > ratings[i+1]:
        new = cndy[i+1]+1
        old = cndy[i]
        cndy[i] = max(old, new)

print(cndy)
print(sum(cndy))
