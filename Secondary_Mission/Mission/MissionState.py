from Sensor import GetSensorData
from enum import IntEnum

class State(IntEnum):
    IDLE = 0
    DESCENT  = 1
    LOWALTITUDE = 2
    MISSIONEND = 3
 
CurrentState = State.IDLE
altitude, temperature, humidity, pressure = GetSensorData()

def GetState():
    global CurrentState
    if(altitude <= 200):
        CurrentState = State.DESCENT
    elif(altitude<=20): #or landing dected by imu
        CurrentState = State.MISSIONEND
    else:
        CurrentState = State.DESCENT
    return CurrentState