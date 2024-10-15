import os
import subprocess

from pydantic import BaseModel
from linux_tutorial_nabla.colors import Colors
import socket
import getpass
import copy

from linux_tutorial_nabla.common import NablaModel
from linux_tutorial_nabla.tutorial_handler import TutorialHandler

help_message = Colors.nabla_text(f"""
    Custom terminal commands for Nabla Linux tuorial:
        {Colors.command('exit')}: Exit the program.
        {Colors.command('nablahelp')}: View this help message.
        {Colors.command('home')}: Return to first screen.
        {Colors.command('start')}: See completed and available tutorials.
        {Colors.command('start <tutorial name>')}: Start a tutorial.
        {Colors.command('status')}: View the status of all tutorials and the current step.
        {Colors.command('reset')}: Reset current step.

    Useful commands for linux terminal:'
        {Colors.command('help <command>')}: View description and help info of a command.
        {Colors.command('man <command>')}: View manual of a command.
        {Colors.command('whatis <command>')}: View short description of a command.


    "NOTE: This is a python script, not a real terminal. Some commands may not work as expected. Auto-complete is not available."
""")

nabla_art = """
                    @                                                                       
   @@@@@@@@@@@@@@@@@    _   _       _     _                                                                            
  @@@@ @         @@    | \ | |     | |   | |                                          
     @@ @       @      |  \| | __ _| |__ | | __ _                                  
      @@ @     @       | . ` |/ _` | '_ \| |/ _` |                                  
       @@ @   @        | |\  | (_| | |_) | | (_| |                                  
        @@ @ @         |_| \_|\__,_|_.__/|_|\__,_|                                  
         @@ @                                                                               
          @@@                                                                               
        """

start_message = Colors.nabla_text(f"""
        Welcome to the {Colors.highlight('Nabla')} Linux Tutorial!
        {Colors.highlight(nabla_art)}
        This is a terminal tutorial by the {Colors.highlight('Nabla')} line union at NTNU (Norwegian University of Science and Technology).
        You can run any command you want, and we will try to help you understand it.

        To exit the tutorial, type {Colors.command('exit')} and press enter.
        To get help, type {Colors.command('nablahelp')} and press enter.
        To return here, type {Colors.command('home')} and press enter.

        Type {Colors.command('start')} and press enter to see completed and available tutorials.

        NOTE: This is a python script, not a real terminal. Some commands may not work as expected. Auto-complete is not available."
        """)


class Terminal(NablaModel):
    pwd: str = os.getcwd()
    username: str = getpass.getuser()
    hostname: str = "nabla"
    tutorial_handler: TutorialHandler = TutorialHandler()


    @property
    def terminal_pwd(self):
        if f"/home/{self.username}" in self.pwd:
            pwd = copy.deepcopy(self.pwd).replace(f"/home/{self.username}", "~")
        else:
            pwd = self.pwd
        return f"{Colors.G(self.username+'@'+self.hostname)}:{Colors.B(pwd)}"

    def terminal_print(self, string):
        print(f"{self.terminal_pwd}$ {string}")

    def terminal_input(self):
        return input(f"{self.terminal_pwd}$ ")
    
    def print_home_page(self):
        print(start_message)

    def run(self):
        self.print_home_page()
        self.tutorial_handler.read_user_data(self.username)

        while True:

            command = self.terminal_input()
            command = self.check_command(command)
            # print(command)
            process = subprocess.run(
                command, 
                cwd=self.pwd, 
                capture_output=True, 
                shell=True, 
            )
            if process.stderr:
                print(Colors.error("Error:"), end="")
                print(repr(process.stderr.decode()))
                print(Colors.nabla_text("Check spelling and syntax and try again!"))
            else:
                if process.stdout.decode() != "":
                    print(process.stdout.decode())
                
                if self.tutorial_handler.check_completion(command, self.pwd):
                    self.tutorial_handler.write_user_data(self.username)
    
    def check_command(self, command: str) -> str:
        command = command.strip()
        run_command = ""
        match command:
            case "exit":
                print("Goodbye!")
                exit()
            case "nablahelp":
                print(help_message)
            case "home":
                self.print_home_page()
                self.tutorial_handler.selected_tutorial_name = None
            case _:
                command = self.cd_command(command)
                command = self.tutorial_handler.check_command(command)
                run_command = command
        return run_command
    
    def cd_command(self, command: str) -> str:
        command = command.split()
        if len(command) == 0:
            return ""
        if command[0] == "cd":
            if len(command) == 1:
                self.pwd = os.path.expanduser("~")
            else:
                self.pwd = os.path.abspath(f"{self.pwd}/{command[1]}")
            command = []
        return " ".join(command)
    
