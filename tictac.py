import pygame, sys, random, time
from pygame.locals import *

pygame.init()

FPSCLOCK = pygame.time.Clock()
FPS = 30
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.SCALED|pygame.RESIZABLE|pygame.SRCALPHA)
BLACK = (0,0,0)
GREEN = (48, 200,113)
PURPLE = (198,76,190)
GREY = (20,20,20)
WHITE = (255,255,255)
BORDER_RADIUS = 20
RANDOM_COLOR = (100,100,100)
DARKBLUE = (120,100,255)
TILE_SIZE = 150 
GAPSIZE = 5
XMARGIN = ((WINDOWWIDTH-(TILE_SIZE * 3))/2)
YMARGIN = ((WINDOWHEIGHT-(TILE_SIZE * 3))/2)
CRATIO = 50
CIRCLE = 'circle'
SQUARE = 'square'
WIDTH = 10
COMPUTER = 'computer'
PLAYER = 'player'



# those 3 variables are ONLY used in the DrawFirstToPlay() func
rectAnimation = Rect(0,0,0,0) 
animationRight = True
speedAnimation = 4

def drawMessage():
    Font1 = pygame.font.SysFont("arial",40,bold=True) # get Font and set it's size
    TitleText = Font1.render("Tic Tac Toe",1 ,DARKBLUE,) # Write the message

    BlackBg1 = TitleText.get_rect(width=(266*2),center=(WINDOWWIDTH/2,20),height=52)  # Creates a black rect background

    pygame.draw.rect(DISPLAYSURF, BLACK, (BlackBg1)) # draws the bigger black rect background


    Font2 = pygame.font.SysFont("arial",20) # get Font and set it's size
    UserText = Font2.render("By github.com/patrickReiis",1,DARKBLUE)  # Write the message

    BlackBg2 = UserText.get_rect(width=(266),height=35,center=(WINDOWWIDTH/2,13*5)) # Creates a black rect background

    pygame.draw.rect(DISPLAYSURF, BLACK, (BlackBg2)) # draws the smaller black rect background
    
             
    DISPLAYSURF.blits(blit_sequence=( # blits the messages onto the screen, the rect positions are specified inside get_rect() func
                                    (TitleText,(TitleText.get_rect(center=(WINDOWWIDTH/2,20+10))))
                                    ,
                                    (UserText,(UserText.get_rect(center=(WINDOWWIDTH/2,13*5)))) 
                                    ))


    
def chooseSymbol():
    circleColor = PURPLE
    alphaC = 0 # 'C' stands for Circle

    squareColor = GREEN #GREEN
    alphaS = 0 # 'S' stands for Square

    halfScreen1 = pygame.Surface((WINDOWWIDTH//2,WINDOWHEIGHT),pygame.SRCALPHA) # Right side of screen
    halfScreen2 = pygame.Surface((WINDOWWIDTH//2,WINDOWHEIGHT)) # Left side of screen

    while True:
        checkForQuit()
        mouse = pygame.mouse.get_pos()
        if mouse:

            DISPLAYSURF.fill((WHITE))

            DISPLAYSURF.blit(halfScreen1,(0,0)) # Right side of screen
            halfScreen1.fill(circleColor)
            halfScreen1.set_alpha(alphaC)

            DISPLAYSURF.blit(halfScreen2,(WINDOWWIDTH-WINDOWWIDTH//2,0)) # Left side of screen
            halfScreen2.fill(squareColor)
            halfScreen2.set_alpha(alphaS)

            if halfScreen1.get_rect().collidepoint((mouse)):
                if alphaC < 255:
                    alphaC += 5
                if alphaS != 0:
                    alphaS -= 5

            else:
                if alphaS < 250:
                    alphaS += 5
                if alphaC != 0:    
                    alphaC -= 5

            pygame.draw.rect(DISPLAYSURF,BLACK,(WINDOWWIDTH/2-((TILE_SIZE/2)/2)+WINDOWWIDTH/4, # x coord
                                                -((TILE_SIZE/2)/2)+WINDOWHEIGHT/2, # y coord
                                                TILE_SIZE/2 # width 
                                                ,TILE_SIZE/2) # height
                                                ,width=WIDTH # line thickness, do not confuse with the width of Rect()
                                                ,border_radius=1)
            pygame.draw.circle(DISPLAYSURF,BLACK,(WINDOWWIDTH/4,WINDOWHEIGHT/2),(CRATIO),width=WIDTH)
            
        click = mouseCoords()
        if click:
            if halfScreen1.get_rect().collidepoint((click)):
                return [CIRCLE,SQUARE]
            else:
                return [SQUARE,CIRCLE]

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def mouseCoords():
        for event in pygame.event.get(MOUSEBUTTONDOWN):
            return event.pos

def chooseFirst():
    if random.randint(0,1):
        return PLAYER

    return COMPUTER

def DrawFirstToPlay(turn):
    global rectAnimation,animationRight


    message = 'The {turn} will start'.format(turn=turn)
    FONT = pygame.font.Font(None,50) # pygame default font
    text = FONT.render(message,True,(32,190,200),(67,123,129)) # the message to render

    rectAnimation.width = text.get_rect().width
    
    if animationRight:
        rectAnimation.x += speedAnimation # move the message to the right

        if rectAnimation.right >= WINDOWWIDTH: # if right of rect collide with right of the screen change the variable to False
            animationRight= False
    else:
        rectAnimation.x -= speedAnimation # move the message to the left

        if rectAnimation.x == 0: # if left of rect collide with the left of screen change the variable to True
            animationRight = True

    DISPLAYSURF.blit(text,(rectAnimation.x,WINDOWHEIGHT-60))

def renderRects(board):

    board3D = []
    for i in range(3):
        board3D.append(board[i:i+3])

    rects = []

    for y in range(len(board3D)):
        for x in range(len(board3D[y])):
            rects.append(Rect(
                              120+(GAPSIZE+TILE_SIZE)*x, # x coord
                              WINDOWHEIGHT/5+(GAPSIZE+TILE_SIZE)*y, # y coord
                              TILE_SIZE, # width
                              TILE_SIZE)) # height
    return rects

def drawGame(board):

    rects = renderRects(board)

    for i in rects:
        pygame.draw.rect(DISPLAYSURF,BLACK,i,width=WIDTH,border_radius=BORDER_RADIUS)

    return rects

def getPlayerMove(board,turn):
    while True:
###
        DISPLAYSURF.fill(WHITE)
        
        checkForQuit() # Check if the player wants to quit
        drawMessage() # Draw the game title and the name of the creator (me)
        DrawFirstToPlay(turn) # Animated message showing the first one to play
        drawGame(board) # Draw only the entire board
        drawBoardUpdated(board) # Draw SQUARE or CIRCLE into the board
        
        rects = renderRects(board) # For each number between 1-9 creates Rect() objects. 
        moves = dictBoard(rects)
        mouse = mouseCoords()

        for number in range(len(rects)):
            moves[number+1] = rects[number] # the first is 0, so I add 1 at the beginning

        if mouse:
            for key in moves:
                if isSpaceFree(board,key):
                    if moves[key].collidepoint((mouse)):
                        return key

        FPSCLOCK.tick(FPS)
        pygame.display.update()

def makeMove(board,symbol,move):
    board[move] = symbol

def dictBoard(rects):
    moves = {}

    for number in range(len(rects)):
        moves[number+1] = rects[number] # the first is 0, so I add 1 at the beginning

    return moves

def drawSquare(rect):
    pygame.draw.rect(DISPLAYSURF,GREEN,(
                                        rect.x+(TILE_SIZE/2)/2, # X coordW
                                        rect.y+(TILE_SIZE/2)/2, # Y coord
                                        rect.width/2, # Width
                                        rect.height/2), # Height
                                        width=WIDTH)#

def drawCircle(rect):
    pygame.draw.circle(DISPLAYSURF,PURPLE,(rect.x+TILE_SIZE/2, # Center of circle X
                                           rect.y+TILE_SIZE/2), # Center of cirlce Y
                                           CRATIO, # Radius
                                           WIDTH) # Line thickness

def drawBoardUpdated(board):
    rects = renderRects(board)
    moves = dictBoard(rects)
    
    for i in range(1,len(board)):
        if board[i] == CIRCLE:
            drawCircle(moves[i])

        elif board[i] == SQUARE:
            drawSquare(moves[i])

def isWinner(bo,sy): # bo stands for 'Board', sy stands for 'Symbol'
    return ((bo[1] == sy and bo[2] == sy and bo[3] == sy) or # horizontal, first row
            (bo[4] == sy and bo[5] == sy and bo[6] == sy) or # horizontal, second row
            (bo[7] == sy and bo[8] == sy and bo[9] == sy) or # horizontal, third row
            (bo[1] == sy and bo[4] == sy and bo[7] == sy) or # vertical, first row
            (bo[2] == sy and bo[5] == sy and bo[8] == sy) or # vertical, second row
            (bo[3] == sy and bo[6] == sy and bo[9] == sy) or # vertical, third row
            (bo[1] == sy and bo[5] == sy and bo[9] == sy) or # diagonal, right to left
            (bo[3] == sy and bo[5] == sy and bo[7] == sy))   # diagonal, left to right

def isSpaceFree(board,index):
    '''
    Returns True if the space is free
    '''
    if board[index] == 'e':
        return True

    return False

def boardFull(board): 
    '''
     returns True if the board is full
    '''
    for index in range(1,len(board)):
        if isSpaceFree(board,index):
            return False

    return True

def chooseRandomMove(board,movesList):
    moves = []
    for i in movesList:
        if isSpaceFree(board,i):
            moves.append(i)
    if moves:
        return random.choice(moves)

    return None

def getComputerMove(board,computerSymbol):
    if computerSymbol == SQUARE:
        player = CIRCLE
    else:
        player = SQUARE

    # Now the AI algorithm starts

    # Check if the computer can win with one move
    for i in range(1,len(board)):
        replicate = board.copy()
        if isSpaceFree(replicate,i):
            makeMove(replicate,computerSymbol,i)
            if isWinner(replicate,computerSymbol):
                return i

    # Check if the player will win on the next move
    for i in range(1,len(board)):
        replicate = board.copy()
        if isSpaceFree(replicate,i):
            makeMove(replicate,player,i)
            if isWinner(replicate,player):
                return i

    # Check if any corner is available
    move = chooseRandomMove(board,[1,3,7,9])

    if move:
        return move

    # Check if the center is available
    if isSpaceFree(board,5):
        return 5
    
    # Check if the mid parts are avaibale
    return chooseRandomMove(board,[2,4,6,8])
    
def returnColor(symbol):
    if symbol == SQUARE:
        return GREEN
    else:
        return PURPLE

def drawLine(moves,coords,symbol,winner):
    # draw a line that cross the path of the winner
    start,end = coords
    finishAnimation = False
    add = 0
    while not finishAnimation:
        checkForQuit()
        add += 5
        if start == 1 and end == 3:
            startX,startY = (moves[1].x-moves[1].width/2, moves[1].y+moves[1].height/2) # starting point
            copyStartX = startX
            copyStartX += add
            endX,endY = (moves[3].x+moves[3].width*1.5,moves[3].y+moves[1].height/2) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(copyStartX,endY),width=20)
            if copyStartX >= endX:
                finishAnimation = True
        elif start == 4 and end == 6:
            startX,startY = (moves[start].x-moves[start].width/2, moves[start].y+moves[start].height/2) # starting point
            copyStartX = startX
            copyStartX += add
            endX,endY = (moves[end].x+moves[end].width*1.5,moves[end].y+moves[end].height/2) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(copyStartX,endY),width=20)
            if copyStartX >= endX:
                finishAnimation = True
        elif start == 7 and end == 9:
            startX,startY = (moves[start].x-moves[start].width/2, moves[start].y+moves[start].height/2) # starting point
            copyStartX = startX
            copyStartX += add
            endX,endY = (moves[end].x+moves[end].width*1.5,moves[end].y+moves[end].height/2) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(copyStartX,endY),width=20)
            if copyStartX >= endX:
                finishAnimation = True
        elif start == 1 and end == 7:
            startX,startY = (moves[start].x+moves[start].width/2, moves[start].y-moves[start].height/2) # starting point
            copyStartY = startY
            copyStartY += add
            endX,endY = (moves[end].x+moves[end].width*0.5,moves[end].y+moves[end].height*1.5) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(startX,copyStartY),width=20)
            if copyStartY >= endY:
                finishAnimation = True
        elif start == 2 and end == 8:
            startX,startY = (moves[start].x+moves[start].width*0.5, moves[start].y-moves[start].height/2) # starting point
            copyStartY = startY
            copyStartY += add
            endX,endY = (moves[end].x+moves[end].width*0.5,moves[end].y+moves[end].height*1.5) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(startX,copyStartY),width=20)
            if copyStartY >= endY:
                finishAnimation = True
        elif start == 3 and end == 9:
            startX,startY = (moves[start].x+moves[start].width*0.5, moves[start].y-moves[start].height/2) # starting point
            copyStartY = startY
            copyStartY += add
            endX,endY = (moves[end].x+moves[end].width*0.5,moves[end].y+moves[end].height*1.5) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(startX,copyStartY),width=20)
            if copyStartY >= endY:
                finishAnimation = True
        elif start == 1 and end == 9:
            startX,startY = (moves[start].x-moves[start].width*0.5, moves[start].y-moves[start].height/2) # starting point
            copyStartY = startY
            copyStartY += add

            copyStartX = startX
            copyStartX += add

            endX,endY = (moves[end].x+moves[end].width*0.5,moves[end].y+moves[end].height*1.5) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(copyStartX,copyStartY),width=20)
            if copyStartY >= endY:
                finishAnimation = True

        elif start == 3 and end == 7:
            startX,startY = (moves[start].x+moves[start].width*1.5, moves[start].y-moves[start].height/2) # starting point
            copyStartY = startY
            copyStartY += add

            copyStartX = startX
            copyStartX -= add

            endX,endY = (moves[end].x-moves[end].width*0.5,moves[end].y+moves[end].height*1.5) # ending point

            pygame.draw.line(DISPLAYSURF,returnColor(symbol),(startX,startY),(copyStartX,copyStartY),width=20)
            if copyStartY >= endY:
                finishAnimation = True

        drawMessage() # call this because the lines override the intro message

        pygame.draw.rect(DISPLAYSURF,(50,50,255),(0,WINDOWHEIGHT-95,WINDOWWIDTH,100)) # Background to erased previous information
        font = pygame.font.SysFont('Noto Sans CJK JP',50,bold=True)
        message = font.render('{winner} won!'.format(winner=winner),True,(255,50,50))
        if winner == COMPUTER:
            DISPLAYSURF.blit(message,(161.5,600+13.5))
        else:
            DISPLAYSURF.blit(message,(203,600+13.5))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def winAnimation(board,winner,symbol):
    # line that cross the path of the winner,also draw a white rect at the bottom
    rects = renderRects(board)
    moves = dictBoard(rects)

    if board[1] == board[2] == board[3]:
        drawLine(moves,(1,3),symbol,winner)
    elif board[4] == board[5] == board[6]:
        drawLine(moves,(4,6),symbol,winner)
    elif board[7] == board[8] == board[9]:
        drawLine(moves,(7,9),symbol,winner)
    elif board[1] == board[4] == board[7]:
        drawLine(moves,(1,7),symbol,winner)
    elif board[2] == board[5] == board[8]:
        drawLine(moves,(2,8),symbol,winner)
    elif board[3] == board[6] == board[9]:
        drawLine(moves,(3,9),symbol,winner)
    elif board[1] == board[5] == board[9]:
        drawLine(moves,(1,9),symbol,winner)
    elif board[3] == board[5] == board[7]:
        drawLine(moves,(3,7),symbol,winner)



def tieAnimation():
    # draw white rect at the bottom with a message and that's it
    pygame.draw.rect(DISPLAYSURF,(50,50,255),(0,WINDOWHEIGHT-95,WINDOWWIDTH,100)) # Background to erased previous information
    font = pygame.font.SysFont('Noto Sans CJK JP',50,bold=True)
    message = font.render('Tie  ;-;',True,(255,50,50))
    DISPLAYSURF.blit(message,(276,600+13.5))

def playAgain():
    '''
        Draws a screen telling if the player wants to play again, return True if so.
        Creates a small good to watch game while the player decides
    '''
    while True:
        DISPLAYSURF.fill(GREY)
        checkForQuit()
        click = pygame.event.get(MOUSEBUTTONDOWN)

        mouse = pygame.mouse.get_pos()

        # Play Again message and Rect
        askPlayRect = Rect(236.5-15,WINDOWHEIGHT/2-180-15,227+15*2,40+15*2)
        askPlay = pygame.font.SysFont('Nimbus Sans',40,bold=True)
        askPlay = askPlay.render('Play Again?',True,BLACK)
        
        pygame.draw.rect(DISPLAYSURF,WHITE,askPlayRect)

        # Yes message and Rect
        yesRect = Rect(236.5-15,WINDOWHEIGHT/2-180-15+(40+15*2),129,70)
        yes = pygame.font.SysFont('Nimbus Sans',40)
        if yesRect.collidepoint((mouse)):
            yes = yes.render('Yes',True,WHITE)
            pygame.draw.rect(DISPLAYSURF,BLACK,yesRect)
            if click:
                return True
        else:
            yes = yes.render('Yes',True,BLACK)
            pygame.draw.rect(DISPLAYSURF,WHITE,yesRect)

        # No message and Rect 
        # check if the mouse is hover the No Rect
        noRect = Rect(350,225,128.5,70) 
        no = pygame.font.SysFont('Nimbus Sans',40)
        if noRect.collidepoint((mouse)):
            no = no.render('No',True,WHITE)
            pygame.draw.rect(DISPLAYSURF,BLACK,noRect)
            if click:
                return False
        else:
            no = no.render('No',True,BLACK)
            pygame.draw.rect(DISPLAYSURF,WHITE,noRect)
    
        # Blits all the messages onto the screen
        DISPLAYSURF.blits(blit_sequence=(
            (askPlay,(236.5,WINDOWHEIGHT/2-180)),
            (yes,(221+30,225+15)),
            (no,(38.75+350,225+15))
            ))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    return False


def main():

    while True:    
        DISPLAYSURF.fill(WHITE)
        
        theBoard = ['e'] * 10 # 'e' stands for empty
        
        checkForQuit()

        player, computer = chooseSymbol()

        turn = chooseFirst()
        initialTurn = turn



        gameIsPlaying = True

        while gameIsPlaying:

            if turn == PLAYER:
                drawGame(theBoard) # Draws only the map without Circle or Square

                move = getPlayerMove(theBoard,initialTurn) # Get the player move and also draw it
                makeMove(theBoard,player,move) # Update the player move to theBoard list
                
                if isWinner(theBoard,player):

                    drawBoardUpdated(theBoard)
                    winAnimation(theBoard,turn,player)
                    gameIsPlaying = False

                elif boardFull(theBoard):
                    drawBoardUpdated(theBoard)
                    tieAnimation()

                    gameIsPlaying = False

                else:
                    turn = COMPUTER

            else:
                move = getComputerMove(theBoard,computer)
                makeMove(theBoard,computer,move)

                if isWinner(theBoard,computer):

                    drawBoardUpdated(theBoard)
                    winAnimation(theBoard,turn,computer)
                    gameIsPlaying = False

                elif boardFull(theBoard):

                    drawBoardUpdated(theBoard)
                    tieAnimation()

                    gameIsPlaying = False

                else:
                    turn = PLAYER
            
            checkForQuit()

            pygame.display.update()
            FPSCLOCK.tick(FPS)

        time.sleep(3) 
        if not playAgain():
            break

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
        
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
        
if __name__ == '__main__':
    main()
