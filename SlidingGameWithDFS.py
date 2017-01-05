import pygame
import time
from pygame.locals import *
import sys
import os
import KaistCamp.SlidingPuzzleSolverDFS
TARGET_FPS = 30
clock = pygame.time.Clock()

#색 지정
Background_Color = (235,222,240)
Rectangle_Color = (17,120,100)
Rectangle_Shadow = (23,165,137)
Number_Color = (39,55,70)
Button_Color_NotPressed = (217,136,128)
Button_Color_shadow_Pressed = (158,158,88)
Button_Color_shadow_NotPressed = (148,49,38)
Button_Color_Pressed = (244,208,63)

#파이게임 실행 및 스크린 범위 지정하고 노드들을 받아오는 단계
pygame.init()
screen = pygame.display.set_mode((500, 550), DOUBLEBUF)
puzzle = [1,2,4,16,5,6,3,7,9,10,15,8,13,14,12,11]
AllNodes = KaistCamp.SlidingPuzzleSolverDFS.returnresult([[1,2,0,4],[5,6,3,7],[9,10,15,8],[13,14,12,11]])
Pos = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]] #왼쪽 위 좌표를 의미한다

#기본 변수 지정
RUNNING, PAUSE = 0, 1
rectcolor = Button_Color_NotPressed
rectshadow_1= Button_Color_shadow_Pressed
rectshadow_2=Button_Color_shadow_NotPressed
_iter = 0

#텍스트의 폰트를 받아옵니다
fontObj = pygame.font.Font('BAUHS93.TTF', 24)
fontObj2 = pygame.font.Font('ITCKRIST.ttf', 40)
fontStopPause = pygame.font.Font('calibri.ttf', 26)

#이곳부터는 Pygame Animation 에 관한 함수 작성
def draw():
    global fontObj, rectshadow_2
    #폰트 및 사각형 만들기
    puzzlenum=1
    screen.fill(Background_Color)
    textSurfaceObj = fontObj.render('Current Move = %d' % (_iter+1), True, Number_Color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (350,475)
    pauserect = pygame.draw.rect(screen, rectshadow_2, (55, 455, 100, 50), 0)
    pygame.draw.rect(screen, rectcolor, (50, 450, 100, 50), 0)
    pauserect.center = (119, 485)
    pausetext = fontStopPause.render('pause', True, Number_Color)
    pygame.draw.rect(screen, rectcolor, (50, 450, 100, 50), 0)  # button
    screen.blit(textSurfaceObj, textRectObj)
    screen.blit(pausetext, pauserect)
    for x in Pos[:15] :
        #슬라이딩 퍼즐을 만든다
        a = pygame.draw.rect(screen, Rectangle_Color, (x[0], x[1], 90, 90), 0)
        b = pygame.draw.rect(screen, Rectangle_Shadow, (x[0]-5, x[1]-5, 90, 90), 0)
        textNum = fontObj2.render('%d' % (puzzlenum), True, Number_Color)
        textNumObj = textNum.get_rect()
        textNumObj.center = (x[0] + 40, x[1] + 40)
        screen.blit(textNum,textNumObj)
        puzzlenum+=1
    #새로고침
    pygame.display.flip()

#초기화
def initialize(Node):
    i = 0
    for j in range(4):
        for k in range(4):
            Pos[Node[i]-1][1] = 50+j*100
            Pos[Node[i]-1][0] = 50+k*100
            i+=1
    draw()

#주어진 경우 (어디로 가야하는가)와 옮겨야 하는 퍼즐의 번호를 받아 움직임
def move(Case, number):
    if Case == 'LEFT' :
        for i in range(100) :
            Pos[number-1][0] -= 1
            Pos[15][0] += 1
            draw()
    if Case == 'RIGHT' :
        for i in range(100) :
            Pos[number-1][0] += 1
            Pos[15][0] -= 1
            draw()
    if Case == 'UP' :
        for i in range(100):
            Pos[number-1][1] -= 1
            Pos[15][1] += 1
            draw()
    if Case == 'DOWN' :
        for i in range(100) :
            Pos[number-1][1] += 1
            Pos[15][1] -= 1
            draw()

#이곳부터는 Sliding Game 에 관한 함수 작성
def caldiff(NodePrior, NodeAfter):
    diff = [0,0,0]
    diff[0] = NodePrior.index(16) #빈 칸의 처음 위치 파악
    diff[1] = NodeAfter.index(16) #빈 칸의 나중 위치 파악
    for i in range(0,16): #어떤 숫자가 움직여야 하는지 파악
        if NodePrior[i] != NodeAfter[i] and NodePrior[i] == 16:
            diff[2] = NodeAfter[i]
    """주어진 위치를 기반으로, 빈 칸의 배열상 위치 차이를 통해 어디로 움직여야 하는지 파악합니다."""
    if diff[1]-diff[0] == 4 :
        move('UP',diff[2])
    if diff[1]-diff[0] == -4 :
        move('DOWN',diff[2])
    if diff[1]-diff[0] == 1 :
        move('LEFT',diff[2])
    if diff[1]-diff[0] == -1 :
        move('RIGHT',diff[2])

#메인함수
def main():
    pygame.display.set_caption("Sliding with SWAG~~")
    state = RUNNING
    print(AllNodes)
    global _iter, rectcolor, rectshadow_1, rectshadow_2
    initialize(AllNodes[_iter])
    time.sleep(1)
    while (_iter<len(AllNodes)-1):
        mouse= pygame.mouse.get_pos()
        for event in pygame.event.get():
             if event.type == QUIT:
                    pygame.QUIT
                    sys.exit()
             #pause 기능
             if event.type==pygame.MOUSEBUTTONDOWN:
                if 50<mouse[0]<150 and 450<mouse[1]<500: #마우스의 위치가 pause 버튼 위인지 확인
                    if state == RUNNING : #RUNNING 상태에서 클릭시 PAUSE 상태로
                        state = PAUSE
                        rectcolor = Button_Color_Pressed
                        pygame.draw.rect(screen, rectshadow_1, (55, 455, 100, 50), 0)
                        stoprect=pygame.draw.rect(screen, rectcolor, (50, 450, 100, 50), 0)
                        stoprect.center=(114,485)
                        stoptext = fontStopPause.render('paused', True, Number_Color)
                        screen.blit(stoptext,stoprect)
                        pygame.display.flip()
                    elif state == PAUSE : #그 반대
                        state = RUNNING
                        rectcolor = Button_Color_NotPressed
                        pygame.display.flip()
        else:
            if state == RUNNING: #RUNNING 상태일때만 작동하도록 설계
                screen.fill(Background_Color)
                initialize(AllNodes[_iter])
                caldiff(AllNodes[_iter],AllNodes[_iter+1])
                _iter+=1 #다양한 곳에 사용되는 움직인 횟수
                time.sleep(1)

            clock.tick(TARGET_FPS)
    time.sleep(5)
if __name__ == '__main__':
    main()