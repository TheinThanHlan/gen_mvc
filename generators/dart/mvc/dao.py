from . import local_config




def generate(class_name,data,program_config):
    return generate_class(class_name,data,program_config)







def generate_class(class_name,data,program_config):
    MODEL_CLASS_TEMPLATE="""
import 'package:{program_name}/mvc_template/interface/IMVCDao.dart';
import 'package:{program_name}/data/model/{class_name}.dart';

class {class_name}Dao implements IMVCDao<{class_name}>{{
    void create({class_name} data){{

    }}
    {class_name} read(){{}}

    void update({class_name} data){{

    }}

    void delete({class_name} data){{
    }}

}}
"""
    return MODEL_CLASS_TEMPLATE.format(class_name=class_name,
                                       program_name=program_config.get("name"))











