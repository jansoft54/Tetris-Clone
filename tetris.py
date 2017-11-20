import pygame
import random
width = 400;
height = 800;
#Color
fieldColors = [[0]*8 for x in range(0,18)]
pygame.font.init()
font = pygame.font.SysFont("Arial",30)
		  #W 				#Black	#Cy		      #Blue		  #Green	#Red 	    #Purple		  #Orange		#Yellow
colors = [(0xFF,0xFF,0xFF),(0,0,0),(0,0xFF,0xFF),(0,0,0xFF),(0,0xFF,0),(0xFF,0,0),(0x94,0,0xD3),(0xFF,0x8C,0),(0xFF,0xFF,0)]
end = False;
clock = pygame.time.Clock()
#Hex values: Grid of 4 x 4 can be represented by a 16 bit unsigned integer
#color is the index into the colors list
I = {"blocks": [0x0F00, 0x2222, 0x00F0, 0x4444], "color":2}
J = {"blocks": [0x44C0, 0x8E00, 0x6440, 0x0E20], "color":3}
L = {"blocks": [0x4460, 0x0E80, 0xC440, 0x2E00], "color":7}
O = {"blocks": [0xCC00, 0xCC00, 0xCC00, 0xCC00], "color":8}
S = {"blocks": [0x06C0, 0x8C40, 0x6C00, 0x4620], "color":4}
T = {"blocks": [0x0E40, 0x4C40, 0x4E00, 0x4640], "color":6}
Z = {"blocks": [0x0C60, 0x4C80, 0xC600, 0x2640], "color":5}

pieces = [I,J,L,O,S,T,Z]
curPiece = 0
curRotation = 0
score = 0
Xpos = 240
Ypos = 120

def init(width,height):
	global display
	pygame.init()
	pygame.mixer.music.load('Tetris.ogg')
	pygame.mixer.music.play(-1)
	display = pygame.display.set_mode((width,height))
#Init the game
init(width,height)
def writeToBlocks():
	for y in range(0,4):
		for x in range(0,4):
			A = pieces[curPiece]["blocks"][curRotation]
			A = A >> (y * 4 + x)
			A &= 0x1
			if A > 0:				
				posx = Xpos - (x * 40)
				posy = Ypos - (y * 40)
				fieldColors[int((posy / 40)) -1][int((posx / 40)) -1] = pieces[curPiece]["color"]
def generatenewBlock():
	global Ypos
	global Xpos
	global curPiece
	global curRotation
	curRotation = 0
	curPiece = random.randint(0,6)
	Xpos = 240
	Ypos = 120
def destroyBlocks():
	global score
	for y in range(0,18):
		blockOcc = 0
		for x in range(0,8):
			blockOcc+= 1 if fieldColors[y][x] > 0 else 0
		if blockOcc == 8:
			score += 10*y
			for j in range(0,8):
				fieldColors[y][j] = 0
			moveBlocksDown(y)
def moveBlocksDown(delimiter):
	for y in range(delimiter-1,-1,-1):
		fieldColors[y+1] = fieldColors[y]
		if y == 0:
			fieldColors[y] = [0]*8
def checkUnOccupied(posy,posx,curR,XInput = 0,YInput = 0):
	global end
	global curRotation
	interA = posx
	interB = posy
	for y in range(0,4):
		for x in range(0,4):
			A = pieces[curPiece]["blocks"][curR]
			A = A >> (y * 4 + x)
			A &= 0x1
			if A > 0:							
				posx = interA - (x * 40)
				posy = interB - (y * 40)
				posx /= 40
				posy /= 40
				#Check if surounding quads are Occupied
				# If so that indicates that there is an other block that lives there
				posx = int(posx) 
				posy = int(posy)
				if posx > 8 or posx <=0:
					return False
				posx -= int(XInput/40)
				if (posx < 8 and YInput == 0 and XInput == 40) and fieldColors[posy-1][posx] > 0:
					return False
				if (posx < 8 and YInput == 0 and XInput == -40) and fieldColors[posy-1][posx-2] > 0:
					return False
				if (posx < 8 and YInput == 0 and XInput == 0) and fieldColors[posy-1][posx-1] > 0:
					return False
				if posy != 19:
					if fieldColors[posy-1][posx - 1] > 0 and XInput == 0 and curRotation == curR:
						if posy > 5:
							writeToBlocks()
							generatenewBlock()
						else:
							end = True
						return
				else:
					writeToBlocks()
					generatenewBlock()
					return False
				posx  += int(XInput/40)
	return True
def render():
	text = font.render("Score " + str(score),True,colors[1])
	# draw field
	for y in range(0,18):
			for x in range(0,8):
				pygame.draw.rect(display,colors[fieldColors[y][x]],[(x+1)*40, (y+1)*40,40,40])
	#draw tetromino
	for y in range(0,4):
		for x in range(0,4):
			A = pieces[curPiece]["blocks"][curRotation]
			A = A >> (y * 4 + x)
			A &= 0x1
			if A > 0:				
				posx = Xpos - (x * 40)
				posy = Ypos - (y * 40)	
				pygame.draw.rect(display,colors[pieces[curPiece]["color"]],[posx,posy,40,40])
	display.blit(text,(50,0))

ticksA = pygame.time.get_ticks();
ticksB = ticksA;
while not end:
	tickTime = 500
	ticksA = pygame.time.get_ticks()
	holdKeys = pygame.key.get_pressed()
	if holdKeys[pygame.K_DOWN]:
		tickTime = 100
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			end = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				tickTime = 500
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				i = curRotation - 1 if curRotation - 1 >= -4 else 3
				curRotation = i if checkUnOccupied(Ypos,Xpos, i) else curRotation
			elif event.key == pygame.K_a:
				i = curRotation + 1 if curRotation + 1 < 4 else 0
				curRotation = i if checkUnOccupied(Ypos,Xpos,i) else curRotation
			elif event.key == pygame.K_RIGHT:
				if checkUnOccupied(Ypos,Xpos + 40,curRotation,40):					
					Xpos = Xpos + 40 
			elif event.key == pygame.K_LEFT:
				if checkUnOccupied(Ypos,Xpos - 40,curRotation,-40):					
					Xpos = Xpos - 40 
	if ticksA - ticksB >= tickTime:
		UnOccupied = checkUnOccupied(Ypos+40,Xpos,curRotation,YInput = 40)
		Ypos += 40 if UnOccupied else 0
		ticksB = ticksA
	display.fill(colors[0])
	destroyBlocks()
	render()
	pygame.draw.rect(display,colors[1],[0, 0, 40, height])
	pygame.draw.rect(display,colors[1],[width-40, 0, 40, height])
	pygame.draw.rect(display,colors[1],[0, height-40, width, 40])
	pygame.display.flip()
	clock.tick(20)
