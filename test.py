#! /usr/bin/env python3
# coding:utf-8

a1 = [12, 1, 32, 12, 43, 32, 1]
m = 0
for i in a1:
    if a1.index(i) != m:
        a1.remove()
    m += 1
print(a1)
# print(a1.index(a1[2]))
# temp = []
# for x in range(0, len(a1)):
#     temp.append(a1.index(a1[x]))
#
# print(temp)
# index = list(set(temp))
# target = []
# for i in range(0, len(index)):
#     target.append(a1[index[i]])
# print(target)
