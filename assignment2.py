def mystery(n):
    list =[]
    for i in range(1,n+1):
        list.append(int(str(i)*i))
    v= sum(list)
    return v

print(mystery(4))