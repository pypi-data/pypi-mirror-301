import os
from linux_tutorial_nabla.colors import Colors
from linux_tutorial_nabla.tutorial import Step, Tutorial
from linux_tutorial_nabla.common import make_nabla_dir, nabla_tutorial_path, empty, get_full_dir

first_file = "first_file.txt"
first_file_path = nabla_tutorial_path / first_file

def file_1_init():
    make_nabla_dir()
    if os.path.exists(first_file_path):
        os.remove(first_file_path)

def file_1_check_completion(command, pwd):
    return os.path.exists(first_file_path)

step = Step(
    num=0,
    description=
    Colors.nabla_text(f"""
    In this tutorial, we will learn some simple file operations.
    The first command to learn is {Colors.command("touch <filename>")}, which creates a new file.
    Try to create the file {Colors.highlight(first_file)} in the {Colors.highlight("/home/username/nabla_tutorial")} directory.
    """),
    check_completion=file_1_check_completion,
    initialize=file_1_init,
)

def file_check_completion(command, pwd):
    command = command.split()
    if len(command) != 2:
        return False

    if command[0] == "file" and command[1] == first_file:
        d = get_full_dir(command[1], pwd)
        if d == str(first_file_path):
            return True
    return False


step2 = Step(
    num=1,
    description=
    Colors.nabla_text(f"""
    Next we will learn how see a description of the contents of a file.

    To see a description, type {Colors.command("file <filename>")} and press enter.
    Try to see the description of the file you just created.
    """),
    check_completion=file_check_completion,
    initialize=empty,

)

def cat_init():
    with open(first_file_path, 'w') as f:
        f.write("This is a tutorial on the cat command.")

def cat_check_completion(command, pwd):
    command = command.split()
    if len(command) != 2:
        return False
    if command[0] == "cat" and command[1].endswith(first_file):
        d = get_full_dir(command[1], pwd)
        if d == str(first_file_path):
            return True
    return False


step3 = Step(
    num=2,
    description=
    Colors.nabla_text(f"""
    After seeing a description of the contents of a file, it would be nice to see the contents.

    To see the contents of a file, type {Colors.command("cat <filename>")} and press enter.
    Try to see the contents of the file you just created. I added some text to it to help you out.
    """),
    check_completion=cat_check_completion,
    initialize=cat_init,

)

file_1 = Tutorial(
    name="File_Basics",
    description="Learn how to navigate the terminal",
    steps=[step, step2, step3],
    dependencies=["Navigation"]
)