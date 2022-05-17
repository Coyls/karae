from datetime import datetime
from utils.speak import Speak
# Dev
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
        Speak.speak("Salut humain !")
    
class AwakeSetupState(AwakenState):
    
    def process(self):
        print("AwakeSetupState")
        losts = self.getConnectionLost()
        isBroken = self.checkConnectionLost(losts)
        if isBroken:
            # Message d'erreur enonssant les capteur deco
            # et demande a l'utilisateur de redemarer Karae
            print("Lost : ", losts)
            self.speakError(losts)
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

    def speakError(self, losts : list[str]):
        str = ""
        for lost in losts:
            str = str + f"{lost}, "
        str = f"Oups j’ai un petit soucis technique {str}sont déconnectés. Je te conseille de débrancher et rebrancher le pot."
        Speak.speak(str)
        
        

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
        str = "Je commence à avoir un peu soif"
        Speak.speak(str)

    def checkWater(self):
        # Verifier le delta entre maintenant et la date stocker
        # Si 80% du temps du delta ajouter
        hg = self.awake.plant.storage.store["humidityground"]
        
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
        now = datetime.now()
        h = now.hour
        m = now.minute
        str = f"Il est {h} heures {m}. J'èspere que tu pass une bonne journée, pense à aller prendre l'air !"
        Speak.speak(str)
        

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
        str = "A bientôt ! Merci d’avoir pris de mes nouvelles !"
        Speak.speak(str)

class AwakeEndState(AwakenState):
    
    def process(self):
        print("AwakeEndState")
        
        


        