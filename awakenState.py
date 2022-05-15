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
        print("self.awake.state : ",self.awake.awakeState)
        self.awake.setState(AwakeSetupState(self.awake))
        # print("self.awake.state : ",self.awake.awakeState)

    def speak(self):
        print("Speak")
    
class AwakeSetupState(AwakenState):
    
    def process(self):
        print("AwakeSetupState")
        lost = self.getConnectionLost()
        isBroken = self.checkConnectionLost(lost)
        if isBroken:
            # Message d'erreur enonssant les capteur deco
            # et demande a l'utilisateur de redemarer Karae
            print("Lost : ", lost)
            self.speakError()
            self.awake.setState(AwakeEndState(self.awake))
        else :
            # AwakeNeed
            print("Go to AwakeNeed")
            self.awake.setState(AwakeNeedState(self.awake))

    def getConnectionLost(self) -> list[str]:
        return self.awake.plant.connectionManager.discClients

    def checkConnectionLost(self, cl : list[str]) -> bool:
        if len(cl) > 0:
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
        print("AwakeGreetState")
        hasGreet = self.checkGreets()
        if hasGreet:
            # Ennoncer les remerciment
            self.speakGreet()
        self.awake.setState(AwakeEndState(self.awake))
    
    def checkGreets(self) -> bool:
        return True

    def speakGreet(self):
        print("speakGreet")

class AwakeEndState(AwakenState):

    def __init__(self, awake):
        super().__init__(awake)
        print("awake : " , awake.awakeState)
    
    def process(self):
        print("AwakeEndState")
        
        


        