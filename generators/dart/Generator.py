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
    #create dao dir
    Path(
            local_config.dao_dir.format(
                program_root=program_root,
                program_name=program_config.get("name"),
                )
            ).mkdir(parents=True, exist_ok=True)

    imports=generate_import(data,program_config,program_root)
    #model
    with open(local_config.model_dir.format(program_root=program_root,
                                            program_name=program_config.get("name"),
                                           )+ class_name +".dart","w") as f:

        f.write(imports+model.generate(class_name,data,program_config))

    #dao
    with open(local_config.dao_dir.format(program_root=program_root,
                                            program_name=program_config.get("name"),
                                           )+ class_name +"Dao.dart","w") as f:

        f.write(imports+dao.generate(class_name,data,program_config))



#tempoary
def generate_import(data,program_config,program_root):
    IMPORT_TEMPLATE="""
import 'package:{dir_name}/{class_name}.dart';
    """
    imports="""
    """
    _model_dir=local_config.model_dir.format(program_root=program_root,program_name=program_config.get("name"))
    _dao_dir=local_config.dao_dir.format(program_root=program_root,program_name=program_config.get("name"))
    for a in data.keys():
        imports+=IMPORT_TEMPLATE.format(dir_name=_model_dir,class_name=a);
        imports+= IMPORT_TEMPLATE.format(dir_name=_dao_dir,class_name=a+"Dao");


    return imports;



