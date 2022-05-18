from datetime import datetime
from utils.speak import Speak
from utils.utils import speakSentence
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

    hasNeed = []
    
    def process(self):
        print("AwakeNeedState")
        hasNeed = self.checkNeeds()
        if hasNeed:
            # Ennoncer les besoins
            self.speakNeeds()
            self.awake.setState(AwakeInfoMirorState(self.awake))
        else: 
            self.awake.setState(AwakeInfoGeneralState(self.awake))
    
    def checkNeeds(self) -> bool:
        percent = self.checkWater()
        self.speakWater(percent)
        return True

    def speakNeeds(self):
        str = "Je commence à avoir un peu soif"
        Speak.speak(str)

    def checkWater(self):
        hg = self.awake.plant.storage.store["humidityground"]
        waterDb = datetime.strptime(hg, '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.now()
        res = now - waterDb
        # !! Definir si second ou jours
        resRdy = int(res.total_seconds())
        delta = int(self.awake.plant.storage.plantCarac["deltaWater"])
        percent = int(100 * resRdy / delta) 
        return percent

    def speakWater(self, percent : int):
        MIN = 20
        TARGET = 80
        sentences = self.awake.plant.sentence["needs"]["water"]

        if (percent <= MIN):
            self.hasNeed.append("water")
            speakSentence(sentences["min"])
        if (percent > MIN  and percent < TARGET):
            pass
        if (percent >= TARGET):
            self.hasNeed.append("water")
            speakSentence(sentences["max"])

        
        
class AwakeInfoGeneralState(AwakenState):

    def process(self):
        print("AwakeInfoGeneralState")
        self.speakInfos()
        self.awake.setState(AwakeGreetState(self.awake))

    def speakInfos(self):
        now = datetime.now()
        h = now.hour
        m = now.minute
        str = f"Il est {h} heures {m}. J'èspere que tu pass une bonne journée, pense à aller prendre l'air !"
        Speak.speak(str)

class AwakeInfoMirorState(AwakenState):

    def process(self):
        print("AwakeInfoMirorState")
        hasInfo = self.checkInfos()
        if hasInfo:
            self.speakInfos()
        self.awake.setState(AwakeGreetState(self.awake))
        
    def checkInfos(self) -> bool:
        return True

    def speakInfos(self):
        Speak.speak("Stp bug pas")
        

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
        
        


        