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
    f"""
    {Colors.g("In this tutorial, we will learn how to navigate the terminal.")}
    {Colors.g("Your current position is always shown in the terminal.")}
    {Colors.g("This is called the")} {Colors.B("present working directory")} {Colors.g("or")} {Colors.M("pwd")}
    {Colors.g("You can also see where you are by typing")} {Colors.M("pwd")} {Colors.g("and pressing enter.")}
    {Colors.g("Sometimes pwd is be shortened with a tilde")} {Colors.B("~")} {Colors.g("which means your home directory, or /home/username.")}
    
    {Colors.g("Your first task is to type")} {Colors.M("pwd")} {Colors.g("and press enter.")}
    """,
    check_completion=pwd_check_completion,
    initialize=empty,
)

def cd_check_completion(command, pwd):
    return pwd == str(nabla_tutorial_path)

step2 = Step(
    num=1,
    description=
    f"""
    {Colors.g("Next we will learn how to navigate to different directories.")}

    {Colors.g("The main command we will use is")} {Colors.M("cd")} {Colors.g("which stands for")} {Colors.B("change directory.")}
    {Colors.g("To move to a different directory, type")} {Colors.M("cd <directory>")} {Colors.g("and press enter.")}

    {Colors.g("You can specify the directory with an absolute path, like")} {Colors.B("cd /home/username/path_to_some_directory")}
    {Colors.g("Or with a Relative path which is based on your current directory. Example ")}{Colors.B("cd path_to_some_directory")}
    {Colors.B("You can think of it as using ")}{Colors.B("cd (pwd/)path_to_some_directory")}

    {Colors.g("It can get pretty tiring navigating with absolute and relative paths all the time, luckily there are some shortcuts to help you out.")}

    {Colors.M("cd .")}{Colors.g(" (current directory). This is the directory you are currently in.")}
    {Colors.M("cd ..")}{Colors.g(" (parent directory). Takes you to the directory above your current.")}
    {Colors.M("cd ~")}{Colors.g(" (home directory). This directory defaults to your “home directory”. Such as /home/username.")}
    {Colors.M("cd -")}{Colors.g(" (previous directory). This will take you to the previous directory you were just at.")}

    {Colors.g("Your second task is to move to the")} {Colors.B("/home/username/nabla_tutorial")} {Colors.g("directory.")}
    """,
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
    f"""
    {Colors.g("Next we will learn how see the contents of the current directory.")}

    {Colors.g("To see what is in the current directory, type")} {Colors.M("ls")} {Colors.g("and press enter.")}
""",
    check_completion=ls_check_completion,
    initialize=ls_init,

)

navigation_tutorial = Tutorial(
    name="Navigation",
    description="Learn how to navigate the terminal",
    steps=[step, step2, step3]
)