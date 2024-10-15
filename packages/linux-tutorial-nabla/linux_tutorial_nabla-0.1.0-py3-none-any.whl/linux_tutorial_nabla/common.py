import os
import pathlib
from pydantic import BaseModel, ConfigDict

model_config = ConfigDict(validate_assignment=True,
                          arbitrary_types_allowed=True,
                          use_enum_values=True)


user_data_path = pathlib.Path(__file__).parent.resolve() / "user_data.json"

nabla_tutorial_path = pathlib.Path(os.path.expanduser("~/nabla_tutorial"))

def empty():
    pass

def make_nabla_dir():
    try:
        os.mkdir(nabla_tutorial_path)
    except FileExistsError:
        pass

def get_full_dir(arg, pwd):
    if arg.startswith("/"):
        d = arg
    else:
        d = pwd + "/" + arg
    return d

class NablaModel(BaseModel):
    model_config = model_config