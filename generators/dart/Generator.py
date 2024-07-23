from .mvc import *
from .mvc import local_config
from pathlib import Path
def generate(class_name,data,program_config,program_root):
    #create model dir
    Path(
            local_config.model_dir.format(
                program_root=program_root,
                program_name=program_config.get("name"),
                )
            ).mkdir(parents=True, exist_ok=True)

    with open(local_config.model_dir.format(program_root=program_root,
                                            program_name=program_config.get("name"),
                                           )+ class_name +".dart","w") as f:

        f.write(model.generate(class_name,data,program_config))
