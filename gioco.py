import pip
try:
	__import__("pygame")
except ImportError:
	pip.main(['install', "pygame"]) 
import pygame
import sys
import textbox
import textarea
import button
import background
import os
import hashlib

pygame.init()

clock = pygame.time.Clock()

livelli = [None]
ind = 1
curr_path = os.path.abspath(os.path.dirname(__file__))
while os.path.exists(curr_path+"/livelli/livello_"+str(ind)+".txt"):
	f = open(curr_path+"/livelli/livello_"+str(ind)+".txt", "r", encoding="utf-8")
	data = f.read().split('§')
	f.close()
	livelli.append({"hint": data[0]+" ", "password": data[1], "hash": data[-1] == "cifrato=true", "error":data[2:-1], "errorLevel":0, "tentativi": 0})
	ind += 1
livello = 1
if os.path.exists(curr_path+"/livelli/salvataggio.txt"):
	f = open(curr_path+"/livelli/salvataggio.txt", "r", encoding="utf-8")
	try:
		livello = int(f.read())
	except:
		pass
	f.close()
if livello == len(livelli):
	livello = 1

screen = pygame.display.set_mode([1920, 1080], pygame.FULLSCREEN)


inputField = textbox.TextBox(50, 50, 300, 50, True, pygame.Color('#5588bb'), pygame.Color('#004477'), pygame.Color('#dd5522'), screen)
hintArea = textarea.TextArea(50, 40, screen.get_width()/10*9, screen.get_height()/10*6, True, pygame.Color('#5588bb'), pygame.Color('#004477'), screen, livelli[livello]["hint"], 50)
errorArea = textarea.TextArea(50, 65, screen.get_width()/10*9, 100, True, pygame.Color('#dd5522'), pygame.Color('#004477'), screen, "ERRORE!!", 50)

errorArea.setVisibility(False)

def calc_text_width(s):
	return pygame.font.Font(None, 50).render(s, True, (255, 255, 255)).get_width()+textarea.TextArea.margin*2
levelArea = textarea.TextArea(50, 20, calc_text_width("livello "+str(livello)), 35, True, pygame.Color('#5588bb'), pygame.Color('#004477'), screen, "livello "+str(livello), 50)

def loadLevel():
	hintArea.updateText(livelli[livello]["hint"])
	inputField.reset()
	levelArea.updateWidth(calc_text_width("livello "+str(livello)))
	levelArea.updateText("livello "+str(livello))
	errorArea.setVisibility(False)

def checkPassword():
	global livello
	global state
	input_text = inputField.getValue().lower()
	if livelli[livello]["hash"]:
		input_text = hashlib.sha256(input_text.encode('ascii')).hexdigest()
	if input_text == livelli[livello]["password"]:
		livello += 1
		f = open(curr_path+"/livelli/salvataggio.txt", "w", encoding="utf-8")
		f.write(str(livello))
		f.close()
		if livello < len(livelli):
			loadLevel()
		else:
			state = "end"
	else:
		inputField.setError(True)
		livelli[livello]["tentativi"] += 1
		if livelli[livello]["tentativi"] == 3:
			livelli[livello]["tentativi"] = 0

			if len(livelli[livello]["error"]) > 0 and livelli[livello]["errorLevel"] < len(livelli[livello]["error"]):
				errorArea.setVisibility(True)
				errorArea.updateText(livelli[livello]["error"][livelli[livello]["errorLevel"]])
				livelli[livello]["errorLevel"] += 1

validateButton = button.Button(50, 55, 30, 30, True, screen, "INVIO", True,  checkPassword)


hintArea.setVisibility(False)

def toggle_hint():
	global livello
	hintArea.setVisibility(not hintArea.isVisible())
	validateButton.set_active(not hintArea.isVisible())
	if errorArea.isVisible():
		errorArea.setVisibility(False)
		textPlusHints = livelli[livello]["hint"]
		for s in livelli[livello]["error"][:livelli[livello]["errorLevel"]]:
			textPlusHints += "\n\n" + s
		hintArea.updateText(textPlusHints)
infoButton = button.Button(50, 85, 10, 30, True, screen, "INFO", False,  toggle_hint)

def exit_game():
	pygame.quit()
	sys.exit()
	
exitButton = button.Button(97.6, screen.get_width()/40/screen.get_height()*100, screen.get_width()/20, screen.get_width()/20, True, screen, "X", False,  exit_game)

title = "Password Game: non essere come Gianfranco"
titleArea = textarea.TextArea(50, 20, calc_text_width(title), 38, True, pygame.Color('#5588bb'), pygame.Color('#004477'), screen, title, 50)

def start_game():
	global livello
	livello = 1
	continue_game()
def continue_game():
	global state
	state = "main"
	loadLevel()

playBtn_x_pos = 50
if livello != 1:
	playBtn_x_pos = 30
playButton = button.Button(playBtn_x_pos, 70, screen.get_width()/5, 30, True, screen, "NUOVA PARTITA", False,  start_game)
continueButton = button.Button(70, 70, screen.get_width()/5, 30, True, screen, "CONTINUA", False,  continue_game)


creditsArea = textarea.TextArea(50, 40, screen.get_width()/10*9, screen.get_height()/10*6, True, pygame.Color('#5588bb'), pygame.Color('#004477'), screen, "Hai raggiunto la vera fine!!\n\nGrazie per aver giocato al nostro gioco, speriamo sia stato divertente e ti abbia insegnato qualcosa sulla sicurezza informatica, ricorda che questa è solo la superficie, è un mondo vasto e complesso.", 50)


background = background.BackGround(screen)



state = "menu"

def appendStageElement(stage, type, el):
	if type not in stage:
		stage[type] = []
	stage[type].append(el)
	if "ordList" not in stage:
		stage["ordList"] = []
	stage["ordList"].append(el)

menu = {}
appendStageElement(menu, "textareas", titleArea)
appendStageElement(menu, "buttons", playButton)
if livello != 1:
	appendStageElement(menu, "buttons", continueButton)
appendStageElement(menu, "buttons", exitButton)

main = {}
appendStageElement(main, "textboxes", inputField)
appendStageElement(main, "textareas", errorArea)
appendStageElement(main, "textareas", levelArea)
appendStageElement(main, "buttons", validateButton)
appendStageElement(main, "buttons", infoButton)
appendStageElement(main, "buttons", exitButton)
appendStageElement(main, "textareas", hintArea)

end = {}
appendStageElement(end, "textareas", creditsArea)
appendStageElement(end, "buttons", exitButton)

while True:
	
	if state == "menu":
		elements = menu
	elif state == "main":
		elements = main
	elif state == "end":
		elements = end

	over_button = False
	over_text = False
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			exit_game()
		if "textboxes" in elements:
			for tb in elements["textboxes"]:
				tb.update(event)
		if "buttons" in elements:
			for bt in elements["buttons"]:
				bt.update(event)

	
	if "buttons" in elements:
		for bt in elements["buttons"]:
			over_button = bt.mouse_is_over() or over_button
	if "textboxes" in elements:
		for tb in elements["textboxes"]:
			over_text = tb.mouse_is_over() or over_text
	if over_button:
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
	elif over_text:
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
	else:
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
	
	screen.fill((255, 255, 255))

	background.draw(clock.tick(60))

	for el in elements["ordList"]:
		el.draw()
		
	
	pygame.display.flip()