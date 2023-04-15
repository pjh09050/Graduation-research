import random 

def generate_routefile():
    random.seed(10)
    N = 3600
    
    with open("cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="15" guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="15" guiShape="passenger"/>
        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />
        <route id="up" edges="53o 3i 4o 54i" />""", file=routes)
        vehNr = 0
        for i in range(N):
            print('    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />' % (vehNr, i), file=routes)
            print('    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (vehNr, i), file=routes)
            print('    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>' % (vehNr, i), file=routes)
            print('    <vehicle id="up_%i" type="typeNS" route="up" depart="%i" color="1,0,0"/>' % (vehNr, i), file=routes)
            vehNr += 1
        print("</routes>", file=routes)