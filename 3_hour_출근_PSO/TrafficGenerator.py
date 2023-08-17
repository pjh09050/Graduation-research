import numpy as np
import random
from Traffic_data import total_traffic


def generate_routefile():
    np.random.seed(1234)

    sorted_list = total_traffic()

    with open("new.rou.xml", 'w') as routes:
        print("""<routes>
        <vType id="typeCAR" length="5" minGap="2.5" maxSpeed="10" allowLaneChange="False" guiShape="passenger"/>
        <vType id="typeCAR1" length="4" minGap="2.5" maxSpeed="10" allowLaneChange="False" guiShape="passenger/sedan"/>
        <vType id="typeBUS" length="11" minGap="2" maxSpeed="7" allowLaneChange="False" guiShape="bus/coach"/>

        <route id='routeW1_S2' edges='02to00 00toc1 c1to000 000to7'/>
        <route id='routeW1_N1' edges='02to00 00to2'/>
        <route id='routeW1_S1' edges='02to00 00to3'/>
        <route id='routeW1_N2' edges='02to00 00toc1 c1to000 000to6'/>
        
        <route id='routeW1_S3' edges='02to00 00toc1 c1to000 000toc4 c4to0000 0000to11'/>
        <route id='routeW1_E3' edges='02to00 00toc1 c1to000 000toc4 c4to0000 0000to04'/>

        <route id='routeN1_W1' edges='1to00 00to01'/>
        <route id='routeN1_S1' edges='1to00 00to3'/>
        <route id='routeN1_S2' edges='1to00 00toc1 c1to000 000to7'/>
        <route id='routeN1_S3' edges='1to00 00toc1 c1to000 000toc4 c4to0000 0000to11'/>
        <route id='routeN1_E3' edges='1to00 00toc1 c1to000 000toc4 c4to0000 0000to04'/>

        <route id='routeS1_W1' edges='4to00 00to01'/>
        <route id='routeS1_N1' edges='4to00 00to2'/>
        <route id='routeS1_S3' edges='4to00 00toc1 c1to000 000toc4 c4to0000 0000to11'/>
        <route id='routeS1_E3' edges='4to00 00toc1 c1to000 000toc4 c4to0000 0000to04'/>
        
        <route id='routeN2_W1' edges='5to000 000toc2 c2to00 00to01'/>
        <route id='routeN2_S1' edges='5to000 000toc2 c2to00 00to3'/>
        <route id='routeN2_S2' edges='5to000 000to7'/>
        <route id='routeN2_S3' edges='5to000 000toc4 c4to0000 0000to11'/>
        <route id='routeN2_E3' edges='5to000 000toc4 c4to0000 0000to04'/>

        <route id='routeS2_W1' edges='8to000 000toc2 c2to00 00to01'/>
        <route id='routeS2_N1' edges='8to000 000toc2 c2to00 00to2'/>
        <route id='routeS2_N2' edges='8to000 000to6'/>
        <route id='routeS2_S3' edges='8to000 000toc4 c4to0000 0000to11'/>
        <route id='routeS2_E3' edges='8to000 000toc4 c4to0000 0000to04'/>

        <route id='routeN3_W1' edges='9to0000 0000toc3 c3to000 000toc2 c2to00 00to01'/>
        <route id='routeN3_N1' edges='9to0000 0000toc3 c3to000 000toc2 c2to00 00to2'/>
        <route id='routeN3_S1' edges='9to0000 0000toc3 c3to000 000toc2 c2to00 00to3'/>
        <route id='routeN3_S2' edges='9to0000 0000toc3 c3to000 000to7'/>
        <route id='routeN3_S3' edges='9to0000 0000to11'/>
        
        <route id='routeS3_W1' edges='12to0000 0000toc3 c3to000 000toc2 c2to00 00to01'/>
        <route id='routeS3_N1' edges='12to0000 0000toc3 c3to000 000toc2 c2to00 00to2'/>
        <route id='routeS3_S1' edges='12to0000 0000toc3 c3to000 000toc2 c2to00 00to3'/>
        <route id='routeS3_N2' edges='12to0000 0000toc3 c3to000 000to6'/>
        <route id='routeS3_N3' edges='12to0000 0000to10'/>
        <route id='routeS3_E3' edges='12to0000 0000to04'/>

        <route id='routeE3_W1' edges='03to0000 0000toc3 c3to000 000toc2 c2to00 00to01'/>
        <route id='routeE3_N1' edges='03to0000 0000toc3 c3to000 000toc2 c2to00 00to2'/>
        <route id='routeE3_S1' edges='03to0000 0000toc3 c3to000 000toc2 c2to00 00to3'/>
        <route id='routeE3_N2' edges='03to0000 0000toc3 c3to000 000to6'/>
        <route id='routeE3_S2' edges='03to0000 0000toc3 c3to000 000to7'/>
        <route id='routeE3_N3' edges='03to0000 0000to10'/>
        <route id='routeE3_S3' edges='03to0000 0000to11'/> """, file=routes)

        color = {'red':(255,0,0), 'green':(96,150,96), 'white':(255,255,255), 'yellow':(255,255,0)}
        for i in range(len(sorted_list)):
            car_type = random.choices(population=["typeCAR", "typeCAR1", "typeBUS"], weights=[0.6, 0.399, 0.001], k=1)[0]
            if car_type == "typeBUS":
                a = (0,255,0)
            else:
                a = random.choice(list(color.values()))
            print('    <vehicle id="route_%i" type="%s" route="%s" depart="%.1f" departLane="%i" arrivalLane="%i" color="%i,%i,%i" />' % (i, car_type ,sorted_list[i][0], sorted_list[i][1], sorted_list[i][2], sorted_list[i][3], a[0], a[1], a[2]), file=routes)
            
        print("</routes>", file=routes)