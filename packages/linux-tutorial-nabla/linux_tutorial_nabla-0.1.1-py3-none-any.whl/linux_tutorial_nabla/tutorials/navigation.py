import os
from linux_tutorial_nabla.colors import Colors
from linux_tutorial_nabla.tutorial import Step, Tutorial
from linux_tutorial_nabla.common import empty, make_nabla_dir, nabla_tutorial_path

def pwd_check_completion(command, pwd):
    if command == "pwd":
        return True
    return False

step = Step(
    num=0,
    description=
    Colors.nabla_text(f"""
    In this tutorial, we will learn how to navigate the terminal.
    Your current position is always shown in the terminal.
    This is called the {Colors.highlight("present working directory")} or {Colors.command("pwd")}
    You can also see where you are by typing {Colors.command("pwd")} and pressing enter.
    Sometimes pwd is be shortened with a tilde {Colors.highlight("~")} which means your home directory, or /home/username.
    
    Your first task is to type {Colors.command("pwd")} and press enter.
    """),
    check_completion=pwd_check_completion,
    initialize=empty,
)

def cd_check_completion(command, pwd):
    return pwd == str(nabla_tutorial_path)

step2 = Step(
    num=1,
    description=
    Colors.nabla_text(f"""
    Next we will learn how to navigate to different directories.

    The main command we will use is {Colors.command("cd")} which stands for {Colors.highlight("change directory.")}
    To move to a different directory, type {Colors.command("cd <directory>")} and press enter.

    You can specify the directory with an absolute path, like {Colors.highlight("cd /home/username/path_to_some_directory")}
    Or with a Relative path which is based on your current directory. Example {Colors.highlight("cd path_to_some_directory")}
    You can think of it as using {Colors.highlight("cd (pwd/)path_to_some_directory")}

    It can get pretty tiring navigating with absolute and relative paths all the time, luckily there are some shortcuts to help you out.

    {Colors.command("cd .")} (current directory). This is the directory you are currently in."
    {Colors.command("cd ..")} (parent directory). Takes you to the directory above your current."
    {Colors.command("cd ~")} (home directory). This directory defaults to your “home directory”. Such as /home/username.
    {Colors.command("cd -")} (previous directory). This will take you to the previous directory you were just at.

    Your second task is to move to the {Colors.highlight("/home/username/nabla_tutorial")} directory.
    """),
    check_completion=cd_check_completion,
    initialize=make_nabla_dir,
)

def ls_init():
    open(nabla_tutorial_path / "are_you_seeing_this.txt", 'a').close()

def ls_check_completion(command, pwd):
    if command == "ls":
        return True
    return False


step3 = Step(
    num=2,
    description=
    Colors.nabla_text(f"""
    Next we will learn how see the contents of the current directory.

    To see what is in the current directory, type {Colors.command("ls")} and press enter.
    """),
    check_completion=ls_check_completion,
    initialize=ls_init,

)

navigation_tutorial = Tutorial(
    name="Navigation",
    description="Learn how to navigate the terminal",
    steps=[step, step2, step3]
)