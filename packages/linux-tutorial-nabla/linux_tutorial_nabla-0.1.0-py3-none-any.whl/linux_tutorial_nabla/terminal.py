import os
import subprocess

from pydantic import BaseModel
from linux_tutorial_nabla.colors import Colors
import socket
import getpass
import copy

from linux_tutorial_nabla.common import NablaModel
from linux_tutorial_nabla.tutorial_handler import TutorialHandler

help_message = f"""
    {Colors.g('Custom terminal commands for Nabla Linux tuorial:')}
        {Colors.M('exit')}{Colors.g(': Exit the program')} 
        {Colors.M('nablahelp')}{Colors.g(': View this help message')}  
        {Colors.M('home')}{Colors.g(': Return to first screen')}
        {Colors.M('start')}{Colors.g(': See completed and available tutorials.')}
        {Colors.M('start <tutorial name>')}{Colors.g(': Start a tutorial.')}
        {Colors.M('status')}{Colors.g(': View the status of all tutorials and the current step.')}
        {Colors.M('reset')}{Colors.g(': Reset current step.')}

    {Colors.g('Useful commands for linux terminal:')}
        {Colors.M('help <command>')}{Colors.g(': View description and help info of a command.')}
        {Colors.M('man <command>')}{Colors.g(': View manual of a command.')}
        {Colors.M('whatis <command>')}{Colors.g(': View short description of a command.')}


    {Colors.g("NOTE: This is a python script, not a real terminal. Some commands may not work as expected. Auto-complete is not available.")}
"""

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

start_message = f"""
        {Colors.g('Welcome to the')} {Colors.B('Nabla')} {Colors.g('Linux Tutorial!')}
        {Colors.B(nabla_art)}
        {Colors.g('This is a terminal tutorial by/for')} {Colors.B('Nabla')} {Colors.g('components.')}
        {Colors.g('You can run any command you want, and we will try to help you understand it.')}

        {Colors.g('To exit the tutorial, type')} {Colors.M('exit')} {Colors.g('and press enter.')}
        {Colors.g('To get help, type')} {Colors.M('nablahelp')} {Colors.g('and press enter.')}
        {Colors.g('To return here, type')} {Colors.M('home')} {Colors.g('and press enter.')}

        {Colors.g('Type')} {Colors.M('start')} {Colors.g('and press enter to see completed and available tutorials.')}

        {Colors.g("NOTE: This is a python script, not a real terminal. Some commands may not work as expected. Auto-complete is not available.")}
        """


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
                print(Colors.R("Error:"), end="")
                print(repr(process.stderr.decode()))
                print(Colors.g("Check spelling and syntax and try again!"))
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
    
