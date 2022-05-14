# from plantState import AwakeState

class AwakenState:

    # ! awake : AwakeState --> pas possible d'importer ou de setup
    # ! l'IDE dectect un import circulair + class declarer avant son initialisation 
    # !!!!!!!!!!!!!!!!!!!!!!!!! vvvvvvvv Suprimer pour eviter les inport circulaire
    def __init__(self, awake):
        self.awake = awake
        self.process()

    def process(self):
        pass

    def start(self):
        pass

class AwakeHelloState(AwakenState):

    def start(self):
        self.speak()
        self.setState()

    def process(self):
        print("Ready to start !")
        print("AwakeHelloState")
        

    def setState(self):
        self.awake.setState(AwakeSetupState(self.awake))

    def speak(self):
        pass
    
class AwakeSetupState(AwakenState):
    
    def process(self):
        print("AwakeSetupState")
        lost = self.getConnectionLost()
        isBroken = self.checkConnectionLost(lost)
        if isBroken:
            # Message d'erreur enonssant les capteur deco
            # et demande a l'utilisateur de redemarer Karae
            self.speakError()
            self.awake.setState(AwakeEndState(self.awake))
        else :
            # AwakeNeed
            self.awake.setState(AwakeNeedState(self.awake))

    def getConnectionLost(self) -> list[str]:
        return self.awake.plant.connectionManager.discClients

    def checkConnectionLost(self, cl : list[str]) -> bool:
        if len(cl > 0):
            return True
        else:
            return False

    def speakError(self):
        pass

class AwakeNeedState(AwakenState):
    
    def process(self):
        print("AwakeNeedState")
        hasNeed = self.checkNeeds()
        if hasNeed:
            # Ennoncer les besoins
            self.speakNeeds()
        self.awake.setState(AwakeInfoState(self.awake))
    
    def checkNeeds(self) -> bool:
        return True

    def speakNeeds(self):
        pass
        
class AwakeInfoState(AwakenState):

    def process(self):
        print("AwakeInfoState")
        hasInfo = self.checkInfos()
        if hasInfo:
            # Ennoncer les Infos
            self.speakInfos()
        self.awake.setState(AwakeGreetState(self.awake))
        
    def checkInfos(self) -> bool:
        return True

    def speakInfos(self):
        pass

class AwakeGreetState(AwakenState):
    
    def process(self):
        print("AwakeInfoState")
        hasGreet = self.checkGreets()
        if hasGreet:
            # Ennoncer les remerciment
            self.speakGreet()
        self.awake.setState(AwakeEndState(self.awake))
    
    def checkGreets(self) -> bool:
        return True

    def speakGreet(self):
        pass

class AwakeEndState(AwakenState):
    
    def process():
        print("AwakeEndState")
        # Do nothing
        pass


        