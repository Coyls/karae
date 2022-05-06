import subprocess

test = 21

# subprocess.run(['espeak','-g','3' ,'-v' ,'fr',f"la temperature est de {test} degré"])
cmd = subprocess.run(["sudo", "python3" ,"./switch.py"])
