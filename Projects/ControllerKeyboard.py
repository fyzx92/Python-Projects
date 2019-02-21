# shift pressed for both, first only, second only, neither


# continuously check for button press
# if button is pressed, is shift also pressed?
# map button sequence to command
# if command is to exit, stop checking for button presses


# minimal key breakdown options (n_button 1, n button 2)
# (5,11), (11,5)
# (6,9), (9,6)
# (7,8), (8,7)
# remaining keys will be programmable for common combinations?


# PURE
key_map =       (("a","e","i","o","u","y"),
				("1","2","3","4","5","6","7","8","9","0"),
				("`","-","=","\t","[","]","delete"),
				("\\",";","'",",",".","/"," "),

				("j","m","n","s","t","z"),
				("b","d","f","p","v"),
				("c","g","k","q","x"),
				("h","r","l","w"))


shift_key_map = (("A","E","I","O","U","Y"),
				("!","@","#","$","%","^","&","*"),
				("~","_","+","{","}","(",")", "exit"),
				("|",":","\"","<",">","?","\n"),

				("J","M","N","S","T","Z"),
				("B","D","F","G","P","V"),
				("C","K","Q","X"),
				("H","L","R","W"))


# ALT TRUNCATED
key_map_alt =   (("a","e","i","o","u","y"),
				("j","m","n","s","t","z"),
				("b","d","f","p","v"),
				("c","g","k","q","x"),
				("h","r","l","w"),

				("1","2","3","4","5"),
				("6","7","8","9","0"),
				("`","'",",",".","/"," ","delete"),

				("@","^","*","|","\\","\"","`",""))

				
shift_key_map_alt = (("A","E","I","O","U","Y"),
					("J","M","N","S","T","Z"),
					("B","D","F","G","P","V"),
					("C","K","Q","X"),
					("H","L","R","W"),

					("!","#","$","%","&","\n","<",">"),
					("~","_","-","=","+","?",";",":",),
					("\t","{","}","(",")","[","]","exit"))
	



def get_key_input(button_1, shift=False):
	button_2 = input()
	if shift:
		return shift_key_map[button_1][button_2]
	else:
		return key_map[button_1][button_2]

def controller_keyboard():
	exit_command = "exit"
	running = True
	while(running):
			show_options()
		if button_pressed() and shift_pressed():
			show_options()
			command = get_key_input(button, shift=True)

		elif button_pressed():
			show_options()
			command = get_key_input(button)

		if command == exit_command:
			running = False
			break

def show_options():
	pass

def button_pressed():
	pass

def shift_pressed():
	pass
