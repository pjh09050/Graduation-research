import numpy as np

class TrafficGenerator:
    def __init__(self, max_steps):
        self.max_steps = max_steps

    def generate_routefile(self, seed):
        np.random.seed(seed)

        N = self.max_steps # 3600초 동안 시뮬레이션을 돌린다.

        with open("cross.rou.xml", 'w') as routes:
            print(""" <routes>
            <vType id="typeCAR" length="5" minGap="1" sigma='0' maxSpeed="10" guiShape="passenger"/>

            <!-- W1 출발-->
            <route id='routeW1_N1' edges='02to05 05to02_left 02_leftto3'/>
            <route id='routeW1_S1' edges=''/>
            <route id='routeW1_B1' edges=''/>
            <route id='routeW1_N2' edges=''/>
            <route id='routeW1_S2' edges=''/>
            <route id='routeW1_B2' edges=''/>
            <route id='routeW1_S3' edges=''/>
            <route id='routeW1_E3' edges='03to06 06to012 012to017 017to023'/>

            <!-- N1 출발-->
            <route id='routeN1_W1' edges=''/>
            <route id='routeN1_S1' edges='1to4 4to10'/>
            <route id='routeN1_B1' edges=''/>
            <route id='routeN1_N2' edges=''/>
            <route id='routeN1_S2' edges=''/>
            <route id='routeN1_B2' edges=''/>
            <route id='routeN1_S3' edges=''/>
            <route id='routeN1_E3' edges='2to5 5to2_left 2_leftto012 012to017 017to023'/>

            <!-- S1 출발-->
            <route id='routeS1_W1' edges='11to8 8to3_left 3_leftto01'/>
            <route id='routeS1_N1' edges='12to9 9to3'/>
            <route id='routeS1_B1' edges=''/>
            <route id='routeS1_N2' edges=''/>
            <route id='routeS1_S2' edges=''/>
            <route id='routeS1_B2' edges=''/>
            <route id='routeS1_S3' edges=''/>
            <route id='routeS1_E3' edges=''/>

            <!-- N2 출발-->
            <route id='routeN2_S2' edges='13to15 15to19'/>
            <route id='routeN2_N1' edges=''/>
            <route id='routeN2_S1' edges=''/>
            <route id='routeN2_W1' edges=''/>
            <route id='routeN2_B2' edges=''/>
            <route id='routeN2_S3' edges=''/>
            <route id='routeN2_E3' edges='13to15 15to6_left 6_leftto017 017to023'/>

            <!-- S2 출발-->
            <route id='routeS2_N2' edges='20to18 18to14'/>
            <route id='routeS2_W1' edges='20to18 18to7_left 7_leftto07 07to01'/>
            <route id='routeS2_N1' edges=''/>
            <route id='routeS2_S1' edges=''/>
            <route id='routeS2_B2' edges=''/>
            <route id='routeS2_S3' edges=''/>
            <route id='routeS2_E3' edges=''/>

            <!-- N3 출발-->
            <route id='routeN3_S3' edges='21to24 24to30'/>
            <route id='routeN3_E3' edges='22to25 25to10_left 10_leftto023'/>
            <route id='routeN3_N2' edges=''/>
            <route id='routeN3_S2' edges=''/>
            <route id='routeN3_N1' edges=''/>
            <route id='routeN3_S1' edges=''/>
            <route id='routeN3_W1' edges=''/>

            <!-- S3 출발-->
            <route id='routeS3_N3' edges='32to29 29to23'/>
            <route id='routeS3_E3' edges=''/>
            <route id='routeS3_N2' edges=''/>
            <route id='routeS3_S2' edges=''/>
            <route id='routeS3_N1' edges=''/>
            <route id='routeS3_S3' edges=''/>
            <route id='routeS3_W1' edges='31to28 28to11_left 11_leftto013 013to07 07to01'/>

            <!-- E3 출발-->
            <route id='routeE3_S3' edges='022to019 019to07_left 07_leftto30'/>
            <route id='routeE3_N3' edges=''/>
            <route id='routeE3_S2' edges=''/>
            <route id='routeE3_N2' edges=''/>
            <route id='routeE3_S1' edges=''/>
            <route id='routeE3_N1' edges=''/>
            <route id='routeE3_W1' edges='021to018 018to013 013to07 07to01'/>

            <!-- B1 출발-->
            <route id='routeB1_N2' edges=''/>
            <route id='routeB1_S2' edges=''/>
            <route id='routeB1_B2' edges=''/>
            <route id='routeB1_S3' edges=''/>
            <route id='routeB1_E3' edges=''/>

            <!-- B2 출발-->
            <route id='routeB2_S3' edges=''/>
            <route id='routeB2_E3' edges=''/>
            
            <!--차량-->
            <route id="route1" edges="13to15 15to19"/>
            <route id="route2" edges="13to15 15to6_left 6_leftto017"/>
            <route id="route3" edges="20to18 18to7_left 7_leftto07"/>
            <route id="route4" edges="20to18 18to14"/>
            <route id="route5" edges="011to04_left 04_leftto14"/>
            <route id="route6" edges="03to06 06to012 012to017"/>
            <route id="route7" edges="018to013 013to07"/>
            <route id="route8" edges="014to05_left 05_leftto19"/>""", file=routes)

            # for 반복문 써서 차량 생성
            # 반복문과 조건문을 알맞게 작성해야함. 좌우방향은 빽빽하게, 상하방향은 조금 빽빽하게
            # 적당한 우회전 차량과 적당한 좌회전 차량
            # 가끔 나타나는 spillback 차량
            # 모든 경로를 다 설정해놓고 빽빽한 차량은 계속 for문 돌리고 적당한 경로과 약간의 경로는 조건문으로 설정???
            for i in range(N):
                if i % 2 == 0: # 좌회전 차량 추가
                    print('    <vehicle id="LeftW%i_N%i" type="typeCAR" route="routeW%i_N%i" depart="%i" />' % (i, i, i, i, i), file=routes)
                    print('    <vehicle id="StraightW%i_E%i" type="typeCAR" route="routeW%i_E%i" depart="%i" />' % (i, i, i, i, i), file=routes)
                elif i % 3 == 0: # 우회전 차량 추가
                    print('    <vehicle id="RightW%i_S%i" type="typeCAR" route="routeW%i_S%i" depart="%i" />' % (i, i, i, i, i), file=routes)
                    print('    <vehicle id="StraightW%i_E%i" type="typeCAR" route="routeW%i_E%i" depart="%i" />' % (i, i, i, i, i), file=routes)
                elif i % 4 == 0: # Spillback 차량 추가
                    print('    <vehicle id="SpillW%i_B%i" type="typeCAR" route="routeW%i_B%i" depart="%i" />' % (i, i, i, i, i), file=routes)
                    print('    <vehicle id="StraightW%i_E%i" type="typeCAR" route="routeW%i_E%i" depart="%i" />' % (i, i, i, i, i), file=routes)
                      
            print("</routes>", file=routes)