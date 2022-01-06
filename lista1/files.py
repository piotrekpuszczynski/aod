#   file for creating random graphs
import random


x = 0.6


def createDGraph(vertices):
    data = []
    r = random.randint(0, int(vertices * x))

    for i in range(vertices):
        for j in range(vertices):
            if i == j:
                continue
            if r == 0:
                data.append([0] * 2)
                data[len(data) - 1][0] = i + 1
                data[len(data) - 1][1] = j + 1
                r = random.randint(0, int(vertices * x))
            else:
                r = r - 1

    print(data)

    file = open("D" + str(vertices) + ".txt", "w")
    file.write("D\n" + str(vertices) + "\n" + str(len(data)) + "\n")

    for i in range(len(data)):
        file.write(str(data[i][0]) + " " + str(data[i][1]) + "\n")

    file.close()


def createUGraph(vertices):
    data = []
    r = random.randint(0, int(vertices * x))

    for i in range(vertices):
        for j in range(i + 1, vertices):
            if r == 0:
                data.append([0] * 2)
                data[len(data) - 1][0] = i + 1
                data[len(data) - 1][1] = j + 1
                r = random.randint(0, int(vertices * x))
            else:
                r = r - 1

    print(data)

    file = open("U" + str(vertices) + ".txt", "w")
    file.write("U\n" + str(vertices) + "\n" + str(len(data)) + "\n")

    for i in range(len(data)):
        file.write(str(data[i][0]) + " " + str(data[i][1]) + "\n")

    file.close()


createUGraph(10)
createUGraph(100)
createUGraph(1000)
createUGraph(10000)
createDGraph(10)
createDGraph(100)
createDGraph(1000)
createDGraph(10000)
