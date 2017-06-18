import tkinter as tk
from tkinter import *
from datetime import timedelta
from datetime import datetime

class appWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.entry = tk.Entry(self)
        self.button = tk.Button(self, text="Calculate", command=self.processData)
        self.button.pack()
        self.entry.pack()

    def processData(self):
        processData(self.entry.get())

def getCleanList(tList):
    for i in range (0, len(tList)):
        tempStr = tList[i]
        if tempStr.__contains__("Notify"):
            print(tempStr)
            break
        else:
            if tempStr.__contains__("    Combat  "):
                tempStr = re.sub("^[0-9][0-9]:[0-5][0-9]:[0-5][0-9](    Combat  )", "", tempStr)  # Removes timestamp and combat
                tempStr = re.sub("(- .*)", "", tempStr)  # Removes ammunition used and type of hit
                if tempStr.__contains__("]") or tempStr.__contains__("("):
                    print("I'm here!")
                    tempStr = re.sub("\]\(", "] (", tempStr)
                tList[i] = tempStr
            else:
                tempStr = re.sub("^[0-9][0-9]:[0-5][0-9]:[0-5][0-9](	Combat	)", "", tempStr) # Removes timestamp and combat
                tempStr = re.sub("(- .*)", "", tempStr) # Removes ammunition used and type of hit
                if tempStr.__contains__("]") or tempStr.__contains__("("):
                    print("I'm here!")
                    tempStr = re.sub("\]\(","] (", tempStr)
                tList[i] = tempStr
    return tList

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
    startTime = re.findall("^[0-9][0-9]:[0-5][0-9]:[0-5][0-9]?", tList[0])[0]
    endTime = re.findall("^[0-9][0-9]:[0-5][0-9]:[0-5][0-9]", tempStr)[0]
    return getSingleTime(startTime, endTime)

def processData(String):
    try:
        tList = String.split('\n')
        try:
            totalTime = getTotalTime(tList)
        except:
            print("Bad Time")
        try:
            tList = getCleanList(tList)
        except:
            print("Cannot Clean List")
        totalDamage = []
        userNames = []
        ships = []
        for i in range(0, len(tList)):
            tempStr = tList[i]
            try:
                if tempStr.__contains__("["):   # If someone in a corp did damage
                    currentName = re.findall("from .*]", tempStr)[-1]
                elif re.search("\\bto", tempStr):   # elif you did damage
                    currentName = "From You"
                else:   # else if an npc or someone not in a corp did damage
                    tempStr = re.sub(" - .*", "", tempStr)
                    currentName = re.findall("from .*", tempStr)[-1]
            except:
                print("Bad Name")
            try:
                currentDamage = re.search("\d+", tempStr).group() #Magic to make things string not lists
            except:
                print("Bad Damage")
            try:
                if tempStr.__contains__("["):
                    currentShip = re.findall("\((.*?)\)", tempStr)[-1]
            except:
                print("Bad Ship")
            if currentName in userNames:
                temp = int(totalDamage[userNames.index(currentName)])  # The reason I hate python.
                temp2 = int(currentDamage) + int(temp)  # This is awful >:(
                totalDamage[userNames.index(currentName)] = temp2
            elif currentName not in userNames:  # If there is no index including the current name, append name, dmg, and ship
                userNames.append(currentName)
                totalDamage.append(currentDamage)
                if tempStr.__contains__("["):
                    ships.append(currentShip)

        if totalTime > 0:
            for i in range(0, totalDamage.__len__()):
                totalDamage[i] /= totalTime
        else:
            print("Negative time or no time elapsed")
        for i in range(0, userNames.__len__()):
            if ships.__len__() > 0:
                print("Avg Damage:", "%.2f" % totalDamage[i], userNames[i], "Flying:", ships[i])
            else:
                print("Avg Damage:", "%.2f" % totalDamage[i], userNames[i])
    except:
        print("Bad Input, try again.")

def main():
    app = appWindow()
    app.mainloop()
    return
main()