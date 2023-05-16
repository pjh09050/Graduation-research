import numpy as np
import random

class TrafficGenerator:
    def __init__(self, max_steps):
        self._max_steps = max_steps

    #def generate_routefile(self):
        np.random.seed(1234)

        N = self._max_steps # 3600초 동안 시뮬레이션을 돌린다.

        with open("b.rou.xml", 'w') as routes:
            print("""<routes>
            <vType id="typeCAR" length="5" minGap="3" maxSpeed="10" allowLaneChange="False" guiShape="passenger"/>

            <route id='routeW1_N1' edges='02to00 00to2'/>
            <route id='routeW1_S1' edges='02to00 00to3'/>
            <route id='routeW1_E3' edges='02to00 00to000 000to0000 0000to04'/>
            <route id='routeW1_N2' edges='02to00 00to009 009to010 010to000 000to6'/>
            <route id='routeW1_S2' edges='02to00 00to000 000to7'/>
            <route id='routeW1_S3' edges='02to00 00to000 000to0000 0000to11'/>

            <route id='routeN1_W1' edges='1to00 00to01'/>
            <route id='routeN1_S1' edges='1to00 00to3'/>
            <route id='routeN1_E3' edges='1to00 00to000 000to0000 0000to04'/>
            <route id='routeN1_S2' edges='1to00 00to000 000to7'/>
            <route id='routeN1_S3' edges='1to00 00to000 000to0000 0000to11'/>

            <route id='routeS1_W1' edges='4to00 00to01'/>
            <route id='routeS1_N1' edges='4to00 00to2'/>
            <route id='routeS1_E3' edges='4to00 00to000 000to0000 0000to04'/>
            <route id='routeS1_S3' edges='4to00 00to000 000to0000 0000to11'/>

            <route id='routeN2_S2' edges='5to000 000to7'/>
            <route id='routeN2_S1' edges='5to000 000to011 011to012 012to00 00to3 '/>
            <route id='routeN2_W1' edges='5to000 000to00 00to01'/>
            <route id='routeN2_S3' edges='5to000 000to0000 0000to11'/>
            <route id='routeN2_E3' edges='5to000 000to0000 0000to04'/>

            <route id='routeS2_N2' edges='8to000 000to6'/>
            <route id='routeS2_W1' edges='8to000 000to00 00to01'/>
            <route id='routeS2_N1' edges='8to000 000to00 00to2'/>
            <route id='routeS2_S3' edges='8to000 000to0000 0000to11'/>
            <route id='routeS2_E3' edges='8to000 000to0000 0000to04'/>

            <route id='routeN3_S2' edges='9to0000 0000to013 013to014 014to000 000to7'/>
            <route id='routeN3_S1' edges='9to0000 0000to000 000to011 011to012 012to00 00to3'/>
            <route id='routeN3_S3' edges='9to0000 0000to11'/>
            <route id='routeN3_E3' edges='9to0000 0000to04'/>
            <route id='routeN3_N2' edges='9to0000 0000to000 000to6'/>
            <route id='routeN3_N1' edges='9to0000 0000to000 000to00 00to2'/>
            <route id='routeN3_W1' edges='9to0000 0000to000 000to00 00to01'/>

            <route id='routeS3_S1' edges='12to0000 0000to000 000to011 011to012 012to00 00to3'/>
            <route id='routeS3_N3' edges='12to0000 0000to10'/>
            <route id='routeS3_E3' edges='12to0000 0000to04'/>
            <route id='routeS3_N2' edges='12to0000 0000to000 000to6'/>
            <route id='routeS3_N1' edges='12to0000 0000to000 000to00 00to2'/>
            <route id='routeS3_W1' edges='12to0000 0000to000 000to00 00to01'/>

            <route id='routeE3_S2' edges='03to0000 0000to013 013to014 014to000 000to7'/>
            <route id='routeE3_S1' edges='03to0000 0000to000 000to011 011to012 012to00 00to3'/>
            <route id='routeE3_S3' edges='03to0000 0000to11'/>
            <route id='routeE3_N3' edges='03to0000 0000to10'/>
            <route id='routeE3_N2' edges='03to0000 0000to000 000to6'/>
            <route id='routeE3_N1' edges='03to0000 0000to000 000to00 00to2'/>
            <route id='routeE3_W1' edges='03to0000 0000to000 000to00 00to01'/>""", file=routes)
        

            # for 반복문 써서 차량 생성
            # 반복문과 조건문을 알맞게 작성해야함. 좌우방향은 빽빽하게, 상하방향은 조금 빽빽하게
            # 적당한 우회전 차량과 적당한 좌회전 차량
            # 가끔 나타나는 spillback 차량
            # 모든 경로를 다 설정해놓고 빽빽한 차량은 계속 for문 돌리고 적당한 경로과 약간의 경로는 조건문으로 설정???
            # 설정해야할 것 : id, departLane, depart
            # 좌회전, 우회전 차량은 departLane 설정해주기 (차선 갯수에 따른 분류?)
            # id는 등장 기준 방향
            for i in range(N):
                a = random.randint(1,2)
                b = random.randint(0,2)
                c = random.randint(0,1)
                d = random.randint(0,3)
                if i % 6 == 0:
                    print('    <vehicle id="RightW1_N1_%i" type="typeCAR" route="routeW1_N1" departLane="3" depart="%i" />' % (i, i), file=routes)
                    print('    <vehicle id="LeftW1_S1_%i" type="typeCAR" route="routeW1_S1" departLane="0" depart="%i" />' % (i, i), file=routes)
                    print('    <vehicle id="StraightW1_E3_%i" type="typeCAR" route="routeW1_E3" departLane="%i" depart="%i" />' % (i, a, i), file=routes)
                    print('    <vehicle id="StraightW1_S2_%i" type="typeCAR" route="routeW1_S2" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    print('    <vehicle id="StraightW1_S3_%i" type="typeCAR" route="routeW1_S3" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    print('    <vehicle id="StraightW1_N2_%i" type="typeCAR" route="routeW1_N2" departLane="%i" depart="%i" />' % (i, a, i), file=routes)

                    # print('    <vehicle id="RightN1_W1_%i" type="typeCAR" route="routeN1_W1" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="StraightN1_S1_%i" type="typeCAR" route="routeN1_S1" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    # print('    <vehicle id="LeftN1_E3_%i" type="typeCAR" route="routeN1_E3" departLane="3" arrivalLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    # print('    <vehicle id="LeftN1_S2_%i" type="typeCAR" route="routeN1_S2" departLane="3" arrivalLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftN1_S3_%i" type="typeCAR" route="routeN1_S3" departLane="3" arrivalLane="0" depart="%i" />' % (i, i), file=routes)

                    # print('    <vehicle id="LeftS1_W1_%i" type="typeCAR" route="routeS1_W1" departLane="3" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="StraightS1_N1_%i" type="typeCAR" route="routeS1_N1" departLane="%i" depart="%i" />' % (i, a, i), file=routes)
                    # print('    <vehicle id="RightS1_E3_%i" type="typeCAR" route="routeS1_E3" deparLane="0" arrivalLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    # print('    <vehicle id="RightS1_S3_%i" type="typeCAR" route="routeS1_S3" deparLane="0" depart="%i" />' % (i, i), file=routes)

                    # print('    <vehicle id="StraightN2_S2_%i" type="typeCAR" route="routeN2_S2" departLane="%i" depart="%i" />' % (i, c, i), file=routes)
                    # print('    <vehicle id="RightN2_S1_%i" type="typeCAR" route="routeN2_S1" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightN2_W1_%i" type="typeCAR" route="routeN2_W1" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftN2_S3_%i" type="typeCAR" route="routeN2_S3" departLane="1" arrivalLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftN2_E3_%i" type="typeCAR" route="routeN2_E3" departLane="1" arrivalLane="0" depart="%i" />' % (i, i), file=routes)
                    
                    # print('    <vehicle id="StraightS2_N2_%i" type="typeCAR" route="routeS2_N2" departLane="%i" depart="%i" />' % (i, c, i), file=routes)
                    # print('    <vehicle id="LeftS2_W1_%i" type="typeCAR" route="routeS2_W1" departLane="1" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftS2_N1_%i" type="typeCAR" route="routeS2_N1" departLane="1" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightS2_S3_%i" type="typeCAR" route="routeS2_S3" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightS2_E3_%i" type="typeCAR" route="routeS2_E3" departLane="0" depart="%i" />' % (i, i), file=routes)

                    # print('    <vehicle id="StraightN3_S3_%i" type="typeCAR" route="routeN3_S3" departLane="%i" depart="%i" />' % (i, d, i), file=routes)
                    # print('    <vehicle id="LeftN3_E3_%i" type="typeCAR" route="routeN3_E3" departLane="4" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightN3_N2_%i" type="typeCAR" route="routeN3_N2" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightN3_N1_%i" type="typeCAR" route="routeN3_N1" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightN3_W1_%i" type="typeCAR" route="routeN3_W1" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightN3_S1_%i" type="typeCAR" route="routeN3_S1" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightN3_S2_%i" type="typeCAR" route="routeN3_S2" departLane="0" depart="%i" />' % (i, i), file=routes)

                    # print('    <vehicle id="StraightS3_N3_%i" type="typeCAR" route="routeS3_N3" departLane="%i" depart="%i" />' % (i, d, i), file=routes)
                    # print('    <vehicle id="RightS3_E3_%i" type="typeCAR" route="routeS3_E3" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftS3_N2_%i" type="typeCAR" route="routeS3_N2" departLane="4" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftS3_N1_%i" type="typeCAR" route="routeS3_N1" departLane="4" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftS3_W1_%i" type="typeCAR" route="routeS3_W1" departLane="4" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="LeftS3_S1_%i" type="typeCAR" route="routeS3_S1" departLane="4" depart="%i" />' % (i, i), file=routes)

                    # print('    <vehicle id="LeftE3_S3_%i" type="typeCAR" route="routeE3_S3" departLane="3" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="RightE3_N3_%i" type="typeCAR" route="routeE3_N3" departLane="0" depart="%i" />' % (i, i), file=routes)
                    # print('    <vehicle id="StraightE3_N2_%i" type="typeCAR" route="routeE3_N2" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    # print('    <vehicle id="StraightE3_N1_%i" type="typeCAR" route="routeE3_N1" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    # print('    <vehicle id="StraightE3_W1_%i" type="typeCAR" route="routeE3_W1" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                    # print('    <vehicle id="StraightE3_S2_%i" type="typeCAR" route="routeE3_S2" departLane="%i" depart="%i" />' % (i, a, i), file=routes)
                    # print('    <vehicle id="StraightE3_S1_%i" type="typeCAR" route="routeE3_S1" departLane="%i" depart="%i" />' % (i, a, i), file=routes)

            print("</routes>", file=routes)