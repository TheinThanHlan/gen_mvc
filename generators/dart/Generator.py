from .mvc import *
from .mvc import local_config
from pathlib import Path

dao_dir="data/dao/"
model_dir="data/model/"
database_dir="data/databases/"
def generate(data,program_config,program_root):

    #generate MVC classes
    generate_mvc(data,program_config,program_root);


    #generate database
    _database_dir=program_root+"/"+program_config.get("name")+"/lib/"+database_dir
    #database dir
    Path(_database_dir).mkdir(parents=True, exist_ok=True)
    database.generate(data,program_config)




def generate_mvc(data,program_config,program_root):
    imports=generate_import(data,program_config,program_root)
    for class_name in data.keys():
        _dao_dir=program_root+"/"+program_config.get("name")+"/lib/"+dao_dir
        _model_dir=program_root+"/"+program_config.get("name")+"/lib/"+model_dir
        #create model dir
        Path(_dao_dir).mkdir(parents=True, exist_ok=True)
        #create dao dir
        Path(_model_dir).mkdir(parents=True, exist_ok=True)


        #model
        with open(_model_dir + class_name +".dart","w") as f:
            f.write(imports+model.generate(class_name,data,program_config))
        #dao
        with open(_dao_dir+ class_name +"Dao.dart","w") as f:
            f.write(imports+dao.generate(class_name,data,program_config))




#tempoary
def generate_import(data,program_config,program_root):
    IMPORT_TEMPLATE="""
import 'package:{dir_name}{class_name}.dart';"""
    imports=""""""


    _model_dir=program_config.get("name")+"/"+model_dir
    _dao_dir=program_config.get("name")+"/"+dao_dir
    for a in data.keys():
        imports+=IMPORT_TEMPLATE.format(dir_name=_model_dir,class_name=a);
        imports+= IMPORT_TEMPLATE.format(dir_name=_dao_dir,class_name=a+"Dao");

    return imports;



