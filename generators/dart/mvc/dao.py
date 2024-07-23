
from . import local_config




def generate(class_name,data,program_config):
    return generate_class(class_name,data,program_config)







def generate_class(class_name,data,program_config):
    MODEL_CLASS_TEMPLATE="""
{imports}
class {class_name} implements IMVCModel{{
    {variables}
    {constructor}
}}
"""
    imports=generate_imports(class_name,data,program_config)
    constructor=generate_constructor(class_name,data,program_config)
    variables=generate_variables(class_name,data,program_config)
    return MODEL_CLASS_TEMPLATE.format(class_name=data.get(class_name).get("class"),variables=variables,constructor=constructor,imports=imports)






def generate_imports(class_name,data,program_config):
    IMPORT_TEMPLATE="""
import 'package:{program_name}/data/model/{class_name}.dart';
    """
    imports="""
import 'package:testproj/mvc_template/interface/IMVCModel.dart';
    """
    for a in data.get(class_name).get("variables"):
        class_name=a.get("type").split("<")[-1]
        if(not class_name in local_config.types.keys()):
            imports+=IMPORT_TEMPLATE.format(program_name=program_config.get("name"),class_name=class_name)

    return imports;





def generate_variables(class_name,data,program_config):
    MODEL_VARIABLE_TEMPLATE="""
\t{variable_type} {required} {variable_name};
    """
    variables=""
    for a in data.get(class_name).get("variables"):
        required        = "?" if a.get("isOptional")==True else ""
        variable_name   =a.get("name")
        variable_type   =local_config.variableTypeParser(a.get("type"))
        variables+=MODEL_VARIABLE_TEMPLATE.format(
                variable_type=variable_type,
                variable_name=variable_name,
                required=required
        )
    return variables;




def generate_constructor(class_name,data,program_config):
    MODEL_CONSTRUCTOR_TEMPLATE = """
\t{class_name}({{
{variables}
}}):{assign_variables}
    """
    #----------------------------------------
    MODEL_CONSTRUCTOR_VARIABLE_TEMPLATE="""
\t{variable_type} {required} {variable_name},
    """
    #----------------------------------------
    MODEL_CONSTRUCTOR_ASSIGN_VARIABLE_TEMPLATE="""
\tthis.{variable_name}={variable_name} {default} {postfix}
    """

    variables=""
    assign_variables=""
    no_of_vars=len(data.get(class_name).get("variables"))
    for index,a in enumerate(data.get(class_name).get("variables")):
        variable_name   =a.get("name")
        variable_type   =local_config.variableTypeParser(a.get("type"))
        required        = "?" if a.get("isOptional")==True else ""
        #check if the user gave the default
        default         =a.get("default")
        default         =default if (default!=None and default!="") else local_config.getBuiltinVariableDefault(a.get("type"),a.get("isOptional"))
        if(default!=""):
            default         = "??" + default
        #insert comma or semicolon for ending

        postfix         = ';' if index == no_of_vars-1 else ','

        #add format into variables and assign variables
        variables+=MODEL_CONSTRUCTOR_VARIABLE_TEMPLATE.format(
                variable_type=variable_type,
                variable_name=variable_name,
                required=required
        )
        assign_variables+=MODEL_CONSTRUCTOR_ASSIGN_VARIABLE_TEMPLATE.format(
                variable_name=variable_name,
                default=default,
                postfix=postfix,
        )
    return MODEL_CONSTRUCTOR_TEMPLATE.format(
            class_name=data.get(class_name).get("class"),
            variables=variables,
            assign_variables=assign_variables,
            );



