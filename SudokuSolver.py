# change lists to arrays for performance                                     --> Missing
from sudokuField import field as baseField
import numpy as np
import colored
import math
import time
import os

update = True
field = baseField.copy()
length = len(field)
size = int(math.sqrt(length))
index = 0

cF_field = []
for j in [0, 3, 6, 27, 30, 33, 54, 57, 60]: # hard coded :(                  --> Missing
    temp = []
    temp.append(j)

    for i, x in enumerate(range(1, 9)):
        if x % 3 == 0:
            n = temp[i] + 7
        else:
            n = temp[i] + 1
        temp.append(n)

    cF_field.append(temp)

cF_field = np.array(cF_field)
cF_field = np.resize(cF_field, (9, 9))

def isPossible(index, nr):
    # checks if n can be put into field[index] using sudoku rules
    ud_index = 0
    for i, x in enumerate(range(9, length+1, size)):
        # (x-size < index < x)
        # output x: 9, 18, 27, 36, 45, 54,, 63, 72, 81
        if index > x-size and index < x:
            ud_index = i
            break

    if index < 9:
        lr_index = index
    else:
        lr_index = int(index/9) if ud_index==0 else index - 9 * ud_index

    if index%9==0:
        # why do I have to do this???
        lr_index, ud_index = ud_index, lr_index

    cF_index = 0
    for i, x in enumerate(cF_field):
        if index in x:
            cF_index = i

    temp_field = np.array(field, dtype=np.int32)

    temp_lr = np.resize([temp_field[x::9] for x in range(9)], (size, size))
    lr = temp_lr[lr_index]

    temp_ud = np.resize(temp_field, (size, size))
    ud = temp_ud[ud_index]

    cF = np.array([], dtype=np.int32)
    for x in cF_field[cF_index]:
        cF = np.append(cF, field[x])

    # print("Testing:", nr, "index:", index, lr_index, lr, ud_index, ud, cF_index, cF)

    temp = np.concatenate((lr, ud, cF)) # a list containing all numbers intresting to sudoku rules
    temp = temp[temp!=0] # delete all zeros

    return False if nr in temp else True

def last_number(index):
    # returns last index that is 0 in baseField
    while True:
        index -= 1
        # print(index, baseField[index])
        if baseField[index] == 0:
            if field[index] != 9:
                return index
            else:
                field[index] = 0

def change_number(n):
    global index
    breaking = False
    color_temp = "green"

    for x in range(n+1, 10):
        output = "Increase the number by 1"
        if isPossible(index, x):
            # x is working
            color_temp = "green"
            output = "Changing index {}: {} -> {}".format(index, field[index], x)
            field[index] = x                                               # --> colored output
            index += 1
            n = 0
            breaking = True
        elif x == 9:
            # no hits for x: backtracking
            color_temp = "red"
            output = "Backtracking at:", index
            field[index] = 0
            index = last_number(index)
            change_number(field[index])
            breaking = True
        else:
            field[index] = x

        temp_field = np.resize(field, (9, 9))
        # print(output)
        # print(temp_field) # better looking output                            --> Missing
        for col_index, x in enumerate(temp_field):
            for row_index, i in enumerate(x):
                current_index = col_index*9+row_index
                if current_index != index:
                    color = "white"
                else:
                    color = color_temp
                print(colored.stylize(i, colored.fg(color)), end=" ")
            print()
        if update: time.sleep(.0075) # timedelta?
        if update: os.system("cls")
        if breaking: break

while True:
    if index > 80:
        break
    if baseField[index] == 0:
        n = 0
        change_number(n)
    else:
        index += 1 # index=index+1 if BaseField[index]!=0 else index

baseField = np.resize(baseField, (9,9))
field = np.resize(field, (9,9))

print("Base field:")
print(baseField)

print("Solved field:")
print(field)
