import numpy as np
import random
from total_traffic import total_traffic


def generate_routefile():
    np.random.seed(1234)

    sorted_list = total_traffic()

    with open("b.rou.xml", 'w') as routes:
        print("""<routes>
        <vType id="typeCAR" length="5" minGap="2.5" maxSpeed="10" allowLaneChange="False" guiShape="passenger"/>

        <route id='routeW1_N1' edges='02to00 00to2'/>
        <route id='routeW1_S1' edges='02to00 00to3'/>
        <route id='routeW1_N2' edges='02to00 00to009 009to010 010to000 000to6'/>
        <route id='routeW1_S2' edges='02to00 00to000 000to7'/>
        <route id='routeW1_S3' edges='02to00 00to000 000to015 015to016 016to0000 0000to11'/>
        <route id='routeW1_E3' edges='02to00 00to000 000to0000 0000to04'/>

        <route id='routeN1_W1' edges='1to00 00to01'/>
        <route id='routeN1_S1' edges='1to00 00to3'/>
        <route id='routeN1_S2' edges='1to00 00to000 000to7'/>
        <route id='routeN1_S3' edges='1to00 00to000 000to015 015to016 016to0000 0000to11'/>
        <route id='routeN1_E3' edges='1to00 00to000 000to0000 0000to04'/>

        <route id='routeS1_W1' edges='4to00 00to01'/>
        <route id='routeS1_N1' edges='4to00 00to2'/>
        <route id='routeS1_S3' edges='4to00 00to000 000to015 015to016 016to0000 0000to11'/>
        <route id='routeS1_E3' edges='4to00 00to000 000to0000 0000to04'/>
        
        <route id='routeN2_W1' edges='5to000 000to00 00to01'/>
        <route id='routeN2_S1' edges='5to000 000to011 011to012 012to00 00to3 '/>
        <route id='routeN2_S2' edges='5to000 000to7'/>
        <route id='routeN2_S3' edges='5to000 000to015 015to016 016to0000 0000to11'/>
        <route id='routeN2_E3' edges='5to000 000to0000 0000to04'/>

        <route id='routeS2_W1' edges='8to000 000to00 00to01'/>
        <route id='routeS2_N1' edges='8to000 000to00 00to2'/>
        <route id='routeS2_N2' edges='8to000 000to6'/>
        <route id='routeS2_S3' edges='8to000 000to015 015to016 016to0000 0000to11'/>
        <route id='routeS2_E3' edges='8to000 000to0000 0000to04'/>

        <route id='routeN3_W1' edges='9to0000 0000to000 000to00 00to01'/>
        <route id='routeN3_N1' edges='9to0000 0000to000 000to00 00to2'/>
        <route id='routeN3_S1' edges='9to0000 0000to000 000to011 011to012 012to00 00to3'/>
        <route id='routeN3_N2' edges='9to0000 0000to000 000to6'/>
        <route id='routeN3_S2' edges='9to0000 0000to013 013to014 014to000 000to7'/>
        <route id='routeN3_S3' edges='9to0000 0000to11'/>
        <route id='routeN3_E3' edges='9to0000 0000to04'/>
        
        <route id='routeS3_W1' edges='12to0000 0000to000 000to00 00to01'/>
        <route id='routeS3_N1' edges='12to0000 0000to000 000to00 00to2'/>
        <route id='routeS3_S1' edges='12to0000 0000to000 000to011 011to012 012to00 00to3'/>
        <route id='routeS3_N2' edges='12to0000 0000to000 000to6'/>
        <route id='routeS3_N3' edges='12to0000 0000to10'/>
        <route id='routeS3_E3' edges='12to0000 0000to04'/>

        <route id='routeE3_W1' edges='03to0000 0000to000 000to00 00to01'/>
        <route id='routeE3_N1' edges='03to0000 0000to000 000to00 00to2'/>
        <route id='routeE3_S1' edges='03to0000 0000to000 000to011 011to012 012to00 00to3'/>
        <route id='routeE3_N2' edges='03to0000 0000to000 000to6'/>
        <route id='routeE3_S2' edges='03to0000 0000to013 013to014 014to000 000to7'/>
        <route id='routeE3_N3' edges='03to0000 0000to10'/>
        <route id='routeE3_S3' edges='03to0000 0000to11'/> """, file=routes)
    
        for i in range(len(sorted_list)):
            print('    <vehicle id="route_%i" type="typeCAR" route="%s" depart="%.1f" departLane="%i" arrivalLane="%i" />' % (i, sorted_list[i][0], sorted_list[i][1], sorted_list[i][2], sorted_list[i][3]), file=routes)

        
        print("</routes>", file=routes)