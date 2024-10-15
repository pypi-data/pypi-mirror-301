from linux_tutorial_nabla.common import NablaModel
from linux_tutorial_nabla.colors import Colors
from typing import Callable

class Step(NablaModel):
    num: int
    description: str
    check_completion: Callable[[str, str], bool]
    initialize: Callable[[], None]

class Tutorial(NablaModel):
    name: str
    description: str
    completed: bool = False
    available: bool = True
    dependencies: list[str] = []
    steps: list[Step] = []
    current_step: int = 0

    def __str__(self):
        if self.completed:
            return (f" * {Colors.success(self.name)}: {Colors.nabla_text(self.description+' - Completed')}")
        else:
            return (f" * {Colors.highlight(self.name)}: {Colors.other_text(self.description)}{self.progress_bar}")

    @property
    def progress_bar(self):
        if self.steps:
            return f"{Colors.nabla_text(', Progress:')} {Colors.C('*')*self.current_step}{Colors.C('-')*(len(self.steps)-self.current_step)} {Colors.nabla_text(str(self.current_step*100/len(self.steps)))+Colors.nabla_text('%')}"
        else:
            return ""

    def update_available(self, completed_tutorials):
        if all([dependency in completed_tutorials for dependency in self.dependencies]):
            self.available = True
        else:
            self.available = False
    
    def get_step(self, num = None):
        num = self.current_step if num is None else num
        for step in self.steps:
            if step.num == num:
                return step
        return None

    def step_status(self):
        print(f"\n{Colors.nabla_text('Current step:')} {Colors.highlight(str(self.current_step+1))+ Colors.nabla_text(' out of ')+Colors.highlight(str(len(self.steps)))}")
        print(f"\n{Colors.nabla_text('Description:')} \n {self.get_step().description}")

    def check_completion(self, command, pwd):
        complete = self.get_step().check_completion(command, pwd)
        if complete:
            self.current_step += 1
            print(f"\n{Colors.success('Step completed!')}")

            if self.current_step == len(self.steps):
                self.completed = True
                self.current_step = 0
            else:
                print(f"{Colors.nabla_text('Moving to next step...')}\n")
                self.step_status()
                self.get_step().initialize()
        return self.completed
    
