import datetime
from awakenState import AwakeHelloState, AwakenState
from utils.protocol import ProtocolDecodeur, ProtocolGenerator
from utils.types import BtnType

class PlantState:
    stateName : str

    # ! plant : Plant --> pas possible d'importer ou de setup
    # ! l'IDE dectect un import circulair + class declarer avant son initialisation 
    def __init__(self, plant):
        self.plant = plant

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        pass

    def afterProcess(self):
        pass

class SetupState(PlantState):
    # Wait for all connections

    stateName = "setup-state"

    twofa = 1

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        pass

    def afterProcess(self):
        print("Wait for all connection")
        isOk = self.waitForAllConnection()
        print("isOk", isOk)
        if isOk:
            self.plant.storage.initStorage()
            print("Go to StandbyAfterSetup after init storage !")
            self.plant.setState(StandbyAfterSetup(self.plant,10))
    
    # ----------------------------------------

    def waitForAllConnection(self) -> bool:
        nb = len(self.plant.connectionManager.clients)
        
        if (nb >= 5 and self.twofa >= 5):# ! 5 pour l'instant
            return True
        else:
            self.twofa += 1
            return False
        
class StandbyAfterSetup(PlantState):
    # Wait for user action or pass
    stateName = "standby-after-setup"

    def __init__(self, plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go to TutorielState")
        self.plant.setState(TutorielState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            # !!!!!!!!!!!!!!!!!! SleepState
            self.plant.setState(TutorielState(self.plant))

    def handleButtons(self, type : BtnType):
        pass

    def afterProcess(self):
        pass

class TutorielState(PlantState):

    stateName = "tutoriel-state"

    def __init__(self, plant):
        super().__init__(plant)
        self.afterProcess()

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        pass

    def afterProcess(self):
        self.playTutorial()
        print("Go to SleepState")
        self.plant.setState(SleepState(self.plant))
        print("N'ARRIVE PAS A CHANGER L'ETAT")
        print("State : ", self.plant.state)
        print(" SELF ON STATE : " , self.plant)
        

    # ----------------------------------------

    def playTutorial(self):
        print("Play tutorial")

class SleepState(PlantState):
    
    stateName = "sleep-state"

    def handleSwitch(self):
        pass

    def handleProximity(self):
        print("Go to WakeUpState")
        date = datetime.datetime.now()
        self.plant.storage.saveOnStore("proximity", str(date))
        self.plant.storage.saveOnFile("proximity", str(date))
        self.plant.setState(WakeUpState(self.plant, 10))

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        print("Go to SelectPlantState")
        self.plant.setState(SelectPlantState(self.plant))

    def afterProcess(self):
        pass

class WakeUpState(PlantState):

    stateName = "wake-up-state"

    def __init__(self, plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go To AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            # !!!!!!!!!!!!!!!!! SleepState
            self.plant.setState(AwakeState(self.plant))

    def handleButtons(self, type : BtnType):
        print("Go to SelectPlantState")
        self.plant.setState(SelectPlantState(self.plant))

    def afterProcess(self):
        pass

class AwakeState(PlantState):

    stateName = "awake-state"
    awakeState : AwakenState

    def __init__(self, plant):
        super().__init__(plant)
        self.awakeState = AwakeHelloState(self)
        self.afterProcess()

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        pass

    def afterProcess(self):
        print("Go To StandbyAfterAwake")
        print("Systeme/Miror/jsp")
        self.awakeState.start()
        self.plant.setState(StandbyAfterAwake(self.plant, 10))

    # ----------------------------------------

    def setState(self, state : AwakenState):
        self.state = state
    

class StandbyAfterAwake(PlantState):

    stateName = "standby-after-awake"
    
    def __init__(self, plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go to AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            self.plant.setState(SleepState(self.plant))

    def handleButtons(self, type : BtnType):
        pass

    def afterProcess(self):
        pass

class SelectPlantState(PlantState):
    
    stateName = "select-plant-state"

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        if type == BtnType.OK.value:
            self.okButton()
        if type == BtnType.RIGHT.value:
            self.rightButton()
        if type == BtnType.LEFT.value:
            self.leftButton()

    def afterProcess(self):
        pass

    # ----------------------------------------

    def rightButton(self):
        self.plant.storage.changePlantRight()

    def leftButton(self):
        self.plant.storage.changePlantLeft()

    def okButton(self):
        print("Go to SleepState")
        self.plant.setState(SleepState(self.plant))
