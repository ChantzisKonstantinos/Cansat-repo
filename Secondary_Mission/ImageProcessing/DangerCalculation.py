eurosatDangers = [
0.2,#AnnualCrop
0.6,#Forest
0.3,#HerbaceousVegatation
0.7,#Highway
0.6,#Industrial
0.5,#Pasture
0.3,#PermanentCrop
0.5,#Residential
0.8,#River
0.85,#SeaLake
]

directions = [
    (0,1),
    (0,-1),
    (1,0),
    (-1,0),
    (1,1),
    (-1,-1),
    (1,-1),
    (-1,1)
]

def CalculateDanger(classes):
    global directions
    rawHazards = [
        [eurosatDangers[classes[0]],eurosatDangers[classes[1]],eurosatDangers[classes[2]],eurosatDangers[classes[3]]],
        [eurosatDangers[classes[4]],eurosatDangers[classes[5]],eurosatDangers[classes[6]],eurosatDangers[classes[7]]],
        [eurosatDangers[classes[8]],eurosatDangers[classes[9]],eurosatDangers[classes[10]],eurosatDangers[classes[11]]],
        [eurosatDangers[classes[12]],eurosatDangers[classes[13]],eurosatDangers[classes[14]],eurosatDangers[classes[15]]],
    ]
    finalHazards = []
    columns = len(rawHazards[0])
    rows = len(rawHazards)
    print(columns,rows)
    for r in range(rows):
        for c in range(columns):
            neighbours = []
            sum = 0
            mean = 0
            for dColumn, dRow in directions:
                nRow, nColumn = dRow + r,dColumn + c
                if(nRow>=0 and nRow<rows) and (nColumn>=0 and nColumn<columns):
                    neighbours.append(rawHazards[nRow][nColumn])
            print(neighbours, r, c)
            for n in range(len(neighbours)):
                sum += neighbours[n]
            mean = sum/len(neighbours)
            finalHazard = rawHazards[r][c] * 0.5 + mean * 0.5 
            finalHazard = round(finalHazard,4)
            print(f"raw hazard {rawHazards[r][c]} final hazard {finalHazard}")
            finalHazards.append(finalHazard)
            neighbours.clear()
    print(rawHazards)
    return(finalHazards)

test1 = [
    1,2,2,3,
    4,3,2,3,
    5,0,2,1,
    7,8,9,3,
    ]
print(CalculateDanger(test1))