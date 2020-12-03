from enum import Enum

class SourceManager:
    def __init__(self, manager):
        self.ActualSensor = dict()
        self.VirtualSensor = dict()
        self.AllSensors = dict()
        self.manager = manager

    def init(self):
        pass

    def addActualSensor(self, sens):
        self.__addSensor(self.ActualSensor, sens)

    def addVirtualSensor(self, sens):
        self.__addSensor(self.VirtualSensor, sens)

    def __addSensor(self, sendict, sensor):
        if (sensor.sensorName in sendict) is False:
            sensor.addManager(self.manager)
            sendict[sensor.sensorName] = sensor
            self.AllSensors[sensor.sensorName] = sensor
        else:
            print("error SensorName: %s already in SensorList" % sensor.sensorName)

    def printSensorList(self):
        print("-"*30)
        print("Adapted Sensor List")
        for sen in self.AllSensors.values():
            print("stype: %s, scate : %s, sname : %s" % (str(sen.sensorType), str(sen.sensorCategory), sen.sensorName))
        print("-" * 30)