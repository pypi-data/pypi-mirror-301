import os
from linux_tutorial_nabla.colors import Colors
from linux_tutorial_nabla.tutorial import Step, Tutorial
from linux_tutorial_nabla.common import make_nabla_dir, nabla_tutorial_path, empty, get_full_dir

def file_1_init():
    make_nabla_dir()
    os.remove(nabla_tutorial_path / "first_file.txt")

def file_1_check_completion(command, pwd):
    return os.path.exists(nabla_tutorial_path / "first_file.txt")

step = Step(
    num=0,
    description=
    f"""
    {Colors.g("In this tutorial, we will learn some simple file operations.")}
    {Colors.g("The first command to learn is")} {Colors.M("touch <filename>")}{Colors.g(", which creates a new file.")}
    {Colors.g("Try to create the file")} {Colors.B("first_file.txt")} {Colors.g("in the ")} {Colors.B("/home/username/nabla_tutorial")} {Colors.g("directory.")}
    """,
    check_completion=file_1_check_completion,
    initialize=file_1_init,
)

def file_check_completion(command, pwd):
    command = command.split()
    if len(command) != 2:
        return False
    print(command)
    if command[0] == "file" and command[1] == "first_file.txt":
        d = get_full_dir(command[1], pwd)
        if d == str(nabla_tutorial_path / "first_file.txt"):
            return True
    return False


step2 = Step(
    num=1,
    description=
    f"""
    {Colors.g("Next we will learn how see a description of the contents of a file.")}

    {Colors.g("To see a description, type")} {Colors.M("file <filename>")} {Colors.g("and press enter.")}
    {Colors.g("Try to see the description of the file you just created.")}
""",
    check_completion=file_check_completion,
    initialize=empty,

)

def cat_init():
    with open(nabla_tutorial_path / "first_file.txt", 'w') as f:
        f.write("This is a tutorial on the cat command.")

def cat_check_completion(command, pwd):
    command = command.split()
    if len(command) != 2:
        return False
    if command[0] == "cat" and command[1].endswith("first_file.txt"):
        d = get_full_dir(command[1], pwd)
        if d == str(nabla_tutorial_path / "first_file.txt"):
            return True
    return False


step3 = Step(
    num=2,
    description=
    f"""
    {Colors.g("After seeing a description of the contents of a file, it would be nice to see the contents.")}

    {Colors.g("To see the contents of a file, type")} {Colors.M("cat <filename>")} {Colors.g("and press enter.")}
    {Colors.g("Try to see the contents of the file you just created. I added some text to it to help you out.")}
""",
    check_completion=cat_check_completion,
    initialize=cat_init,

)

file_1 = Tutorial(
    name="File_Basics",
    description="Learn how to navigate the terminal",
    steps=[step, step2, step3],
    dependencies=["Navigation"]
)