import numpy as np

class TrafficGenerator:
    def __init__(self, max_steps):
        self._max_steps = max_steps

    #def generate_routefile(self):
        np.random.seed(1234)

        N = self._max_steps # 3600초 동안 시뮬레이션을 돌린다.

        with open("a.rou.xml", 'w') as routes:
            print("""
            """, file=routes)
        

            # for 반복문 써서 차량 생성
            # 반복문과 조건문을 알맞게 작성해야함. 좌우방향은 빽빽하게, 상하방향은 조금 빽빽하게
            # 차선 갯수에 따른 분류?
            # 적당한 우회전 차량과 적당한 좌회전 차량
            # 가끔 나타나는 spillback 차량
            # 모든 경로를 다 설정해놓고 빽빽한 차량은 계속 for문 돌리고 적당한 경로과 약간의 경로는 조건문으로 설정???
            # 설정해야할 것 : id, departLane, depart
            for i in range(N):
                a = np.random.randint(2)
                b = np.random.randint(3)
                c = np.random.randint(4)
                
                print('    <vehicle id="StraightW1_E3_%i" type="typeCAR" route="routeW1_E3" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                print('    <vehicle id="StraightS1_N1_%i" type="typeCAR" route="routeS1_N1" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                print('    <vehicle id="StraightN1_S1_%i" type="typeCAR" route="routeN1_S1" departLane="%i" depart="%i" />' % (i, b, i), file=routes)
                print('    <vehicle id="StraightS2_N2_%i" type="typeCAR" route="routeS2_N2" departLane="%i" depart="%i" />' % (i, a, i), file=routes)
                print('    <vehicle id="StraightN2_S2_%i" type="typeCAR" route="routeN2_S2" departLane="%i" depart="%i" />' % (i, a, i), file=routes)
                print('    <vehicle id="StraightS3_N3_%i" type="typeCAR" route="routeS3_N3" departLane="%i" depart="%i" />' % (i, c, i), file=routes)
                print('    <vehicle id="StraightN3_S3_%i" type="typeCAR" route="routeN3_S3" departLane="%i" depart="%i" />' % (i, c, i), file=routes)
                print('    <vehicle id="StraightE3_W1_%i" type="typeCAR" route="routeE3_W1" departLane="%i" depart="%i" />' % (i, b, i), file=routes)

            print("</routes>", file=routes)