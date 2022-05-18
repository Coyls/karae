from datetime import datetime
import time
from utils.speak import Speak
from utils.utils import speakSentence
# Dev
# from plantState import AwakeState

class AwakenState:

    stateName = "awaken-state"

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

    stateName = "hello-state"

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
        Speak.speak("Contente de te voir j'èspere que tu vas bien !")
    
class AwakeSetupState(AwakenState):

    stateName = "setup-state"
    
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

    stateName = "need-state"

    needs : list[list[str,str]] = []
    
    def process(self):
        print("AwakeNeedState")
        self.checkNeeds()
        lengthNeeds = len(self.needs)
        if lengthNeeds > 0:
            time.sleep(3)
            self.awake.setState(AwakeInfoMirrorState(self.awake, self.needs))
        else: 
            self.awake.setState(AwakeInfoGeneralState(self.awake))
    
    def checkNeeds(self):
        percent = self.checkWater()
        self.speakWater(percent)


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

    def checkTemperature(self):
        # Reproduire checkWater pour la tmp
        pass

    def speakWater(self, percent : int):
        MIN = 20
        TARGET = 80
        sentences = self.awake.plant.sentence["needs"]["water"]

        if (percent <= MIN):
            self.needs.append(["water","min"])
            speakSentence(sentences["min"])
        if (percent > MIN  and percent < TARGET):
            pass
        if (percent >= TARGET):
            self.needs.append(["water","max"])
            speakSentence(sentences["max"])
  
class AwakeInfoGeneralState(AwakenState):

    stateName = "info-general-state"

    def process(self):
        print("AwakeInfoGeneralState")
        self.speakInfos()
        self.awake.setState(AwakeThanksState(self.awake))

    def speakInfos(self):
        now = datetime.now()
        h = now.hour
        m = now.minute
        tmp = self.awake.plant.storage.store["temperature"]
        str = f"Il est {h} heures {m}, la temperature est de {tmp} degré. J'èspere que tu pass une bonne journée, pense à aller prendre l'air !"
        Speak.speak(str)

class AwakeInfoMirrorState(AwakenState):

    stateName = "info-mirror-state"

    def __init__(self, awake, needs : list[list[str,str]]):
        self.needs = needs
        super().__init__(awake)

    def process(self):
        print("AwakeInfoMirorState")
        self.speakInfos()
        self.awake.setState(AwakeThanksState(self.awake))

    def speakInfos(self):
        for need in self.needs:
            [root, key] = need
            sentences = self.awake.plant.sentence["mirror"][root][key]
            speakSentence(sentences) 

class AwakeThanksState(AwakenState):

    stateName = "thanks-state"
    
    def process(self):
        print("AwakeGreetState")
        self.speakGreet()
        self.awake.setState(AwakeEndState(self.awake))

    def speakGreet(self):
        sentences = self.awake.plant.sentence["thanks"]
        speakSentence(sentences)

class AwakeEndState(AwakenState):

    stateName = "end-state"
    
    def process(self):
        print("AwakeEndState")
        
        


        