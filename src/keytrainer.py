# Keytrainer by
# Samuel Burch
# 25.08.2018
# v1.0.3
import sys
import subprocess as sp
import platform
import time
import random
import termios
import tty
import threading
import os
import signal

try:
	from msvcrt import getch  # try to import Windows version
except ImportError:
	def getch():   # define non-Windows version
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch
		
# roughly killing the program, else it falls into an infinite loop
def timeout():
		print("\n\n===> You ran out of time with a score of {}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n".format(str(highscore)))
		time.sleep(5)
		os.kill(os.getpid(), signal.SIGINT)
		sp.run([clear_command])
		
# askig the user whether to play again or not
def play_again(lvl, qtyt):
	time.sleep(4)
	sp.run([clear_command])
	if input("\n\n\n\nPlay again with the same settings? [y/n]\n\n\t") in "Yesyes":
		sp.run([clear_command])
		run_game(lvl, qtyt)
	else:
		print("\n\nWell then see you soon!")
		time.sleep(3)
		sp.run([clear_command])
		sys.exit(3)

# the main game logic
def run_game(level, qty):
	
	global tim
	global clear_command
	clear_command = ""
	global highscore
	highscore = 0
	prev_char = ''
	all_chars_default = "abcdefghijklmnopqrstuvwxyzöüä" # more characters to be used can be added here
	# ... or may be added to the custom config file
	if len(sys.argv) == 4:
		if sys.argv[3] == "-f":
			with open("CONFIG.txt", 'r') as configuration:
				all_chars = configuration.read()
				configuration.close()
		else:
			print("Usage: python3 keytrainer.py [level 1-5] [number of iterations] -f (optional)")
	elif len(sys.argv) == 3:
		all_chars = all_chars_default
	# determine how to clear the terminal screen
	if platform.system() == "Windows":
		clear_command = "cls"
	elif platform.system() == "Darwin" or platform.system() == "Linux":
		clear_command = "clear"
	else:
		print("Your OS is not supportet at the moment.  :-(")
		time.sleep(4)
		sys.exit(4)
			
	print("Look at the screen, not at the keyboard. Don't try to cheat.")
	time.sleep(3)
			
	sp.run([clear_command])
	
	for _ in range(qty):
		# waiting time equals 6 - level
		tim = threading.Timer(float(6 - level), timeout)
		character = random.choice(all_chars)
		# prevent repeating characters
		while character == prev_char:
			character = random.choice(all_chars)
		prev_char = character
		print("\n\n\n\t\t\tPress the following key:")
		print("\t\t\t-------------------")
		print("\t\t\t|\t\t  |")
		print("\t\t\t|  \t  {} \t  |".format(character))
		print("\t\t\t|\t\t  |")
		print("\t\t\t-------------------")
		print("\n\t\t\t Current score: {}".format(str(highscore)))
		print("\n\t\t\t {} iterations left".format(str(qty - highscore)))
		print("\n\n\n")
		tim.start()
				
		entered = getch()
		
		if entered == character:
			tim.cancel()
			highscore += 1
			sp.run([clear_command])
		else:
			# wrong key pressed
			tim.cancel()
			print("\n\n===> Looks like that was wrong  :-(")
			print("\n===> You pressed {} instead of {}".format(entered, character))
			print("\n===> Your score: " + str(highscore))
			play_again(level, qty)			
		del(tim)

	# if the game ends successfully
	print("\n\n===> Congratulations, you made it through!  :-)")
	print("\n===> Your score: {}".format(str(highscore)))
	play_again(level, qty)
		
def main():
	level = 0
	quantity = 0
	
	# checking if game was started correctly
	if len(sys.argv) != 4 and len(sys.argv) != 3:
		print("Usage: python3 keytrainer.py [level 1-5] [number of iterations] -f (optional)")
		sys.exit(2)
	else:
		if int(sys.argv[1]) >= 1 and int(sys.argv[1]) <= 5:
			level = int(sys.argv[1])
		else:
			print("Usage: python3 keytrainer.py [level 1-5] [number of iterations] -f (optional)")
			sys.exit(2)
		
		arg = int(sys.argv[2])
		if arg >= 1 and arg <= 1000:
			quantity = arg
		else:
			quantity = 15
		
	print("\n\nStarting a game on level {} and with {} iterations.\n\n".format(level, quantity))
	
	run_game(level, quantity)
	
# you know this part
if __name__ == "__main__":
	main()
