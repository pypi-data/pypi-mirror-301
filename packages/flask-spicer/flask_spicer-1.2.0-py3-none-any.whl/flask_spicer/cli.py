from os import mkdir
from colorama import just_fix_windows_console, Fore
from sys import argv
argc:int = len(argv)

def comment(content:str) -> str:
	return f"{Fore.LIGHTBLACK_EX}# {content}{Fore.RESET}"
minus:str = f"{Fore.LIGHTYELLOW_EX}-{Fore.RESET}"

def run_help(command_name:str) -> None:
	if command_name == "all":
		print()
		print(f"Spicer commands list")
		print()
		print(f"{minus} spicer help <command name> {comment('Provides information on a command')}")
		print(f"{minus} spicer new <project name> {comment('Creates a new project')}")
		print()

		return
	if command_name == "help":
		print()
		print(f"{Fore.LIGHTYELLOW_EX}help <command name> {Fore.RESET}| Command Information")
		print()
		print(f"Gets information on a command (the <command name> argument). By passing \"all\" as the <command name> a list of every command will be generated.")
		print()
		return
	if command_name == "new":
		print()
		print(f"{Fore.LIGHTYELLOW_EX}new <project name> {Fore.RESET}| Command Information")
		print()
		print(f"Creates a new project. The <project name> argument is the name of the project.")
		print()
		return

def run_new(project_name:str) -> None:
	return

def run() -> None:
	just_fix_windows_console()
	if argc < 2:
		print()
		print("Welcome to the Spicer command-line utility!")
		print("If you need more information on a command or on")
		print(f"the tool itself, run {Fore.LIGHTYELLOW_EX}spicer help <command name>{Fore.RESET}.")
		print()
		print(f"If you want a list of commands, try {Fore.LIGHTYELLOW_EX}spicer help all{Fore.RESET}!")
		print()
		return
	if argv[1] == "help":
		if argc < 3:
			print()
			print(f"Nuh uh. You {Fore.LIGHTRED_EX}must{Fore.RESET} provide a {Fore.LIGHTYELLOW_EX}command name{Fore.RESET}!")
			print()
			return
		run_help(argv[2])
		return
	if argv[1] == "new":
		if argc < 3:
			print()
			print(f"Nuh uh. You {Fore.LIGHTRED_EX}must{Fore.RESET} provide a {Fore.LIGHTYELLOW_EX}project name{Fore.RESET}!")
			print()
			return
		run_new(argv[2])
		return
	return None