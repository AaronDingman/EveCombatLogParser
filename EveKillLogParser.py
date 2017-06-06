import os
import re
# import numpy as np
from datetime import timedelta
from datetime import datetime
def getFile():
    inputFile = 'C:\\Users\\Patchouli\\Documents\\EveCombatLogParser\\input.txt'
    tList = []
    with open(inputFile) as f:
        for line in f:
            tList.append(line)
            if 'str' in line:
                print("I'm here")
                return tList
    return tList

def getCleanList(tList):
    #tList = getFile()
    for i in range (0, len(tList)):
        tempStr = tList[i]
        tempStr = re.sub("^[0-2][0-3]:[0-5][0-9]:[0-5][0-9](	Combat	)", "", tempStr) # Removes timestamp and combat
        tempStr = re.sub("(- .*)", "", tempStr) # Removes ammunition used and type of hit
        tempStr = re.sub("\]\(","] (", tempStr)
        tList[i] = tempStr
    return tList

def getCurrentShip(String):
    return re.findall("\((.*?)\)", String)[-1]

def getCurrentDamage(String):
    currentDamage = re.search("\d+", String).group() #Magic to make things string not lists
    return currentDamage

def getCurrentName(String):
    return re.findall("from .*]", String)[-1]

def getSingleTime(startTime, endTime):
    s1 = startTime
    s2 = endTime
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    if tdelta.days < 0:
        tdelta = timedelta(days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)
    return tdelta.seconds

def getTotalTime(tList):
    for i in range(0, len(tList)):
        tempStr = tList[i]
        tList[i] = tempStr
    startTime = re.findall("^[0-2][0-3]:[0-5][0-9]:[0-5][0-9]?", tList[0])[0]
    endTime = re.findall("^[0-2][0-3]:[0-5][0-9]:[0-5][0-9]", tempStr)[0]
    return getSingleTime(startTime, endTime)

def main():
    tList = getFile()
    totalTime = getTotalTime(tList)
    tList = getCleanList(tList)
    totalDamage = []
    userNames = []
    ships = []
    for i in range(0, len(tList)):
        tempStr = tList[i]
        currentName = getCurrentName(tempStr)
        currentDamage = getCurrentDamage(tempStr)
        currentShip = getCurrentShip(tempStr)

        if currentName not in userNames: #If there is no index including the current name, append name, dmg, and ship
            userNames.append(currentName)
            totalDamage.append(currentDamage)
            ships.append(currentShip)

        if currentName in userNames:
            temp = int(totalDamage[userNames.index(currentName)]) # The reason I hate python.
            temp2 = int(currentDamage) + int(temp) # This is awful >:(
            totalDamage[userNames.index(currentName)] = temp2

    for i in range (0, totalDamage.__len__()):
        totalDamage[i] /= totalTime

    for i in range(0, userNames.__len__()):
        print("Avg Damage:", "%.2f" % totalDamage[i], userNames[i], "Flying:", ships[i])

    return

main()


