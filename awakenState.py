from plantState import AwakeState

class AwakenState:

    # ! awake : AwakeState --> pas possible d'importer ou de setup
    # ! l'IDE dectect un import circulair + class declarer avant son initialisation 
    # !!!!!!!!!!!!!!!!!!!!!!!!! vvvvvvvv Suprimer pour eviter les inport circulaire
    def __init__(self, awake : AwakeState):
        self.awake = awake
        self.process()

    def process():
        pass

class AwakeHelloState(AwakenState):

    def process(self):
        # Playsound
        self.setState()

    def setState(self):
        self.awake.setState(AwakeSetupState(self.awake))
    
class AwakeSetupState(AwakenState):
    
    def process(self):
        lost = self.getConnectionLost()
        isBroken = self.checkConnectionLost(lost)
        if isBroken:
            # Message d'erreur enonssant les capteur deco
            # et demande a l'utilisateur de redemarer Karae
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

class AwakeNeedState(AwakenState):
    
    def process(self):
        if True:
            # Ennocer les besoin
            pass
        self.awake.setState(AwakeInfoState(self.awake))
        
class AwakeInfoState(AwakenState):
    
    def process(self):
        if True:
            # Ennocer les Info
            pass
        self.awake.setState(AwakeGreetState(self.awake))

class AwakeGreetState(AwakenState):
    
    def process(self):
        if True:
            # Ennocer les Info
            pass
        self.awake.setState(AwakeEndState(self.awake))

class AwakeEndState(AwakenState):
    
    def process():
        # Do nothing
        pass


        