from . import local_config




def generate(class_name,data,program_config):
    return generate_class(class_name,data,program_config)







def generate_class(class_name,data,program_config):
    MODEL_CLASS_TEMPLATE="""
import 'package:{program_name}/mvc_template/interface/IMVCModel.dart';
class {class_name} implements IMVCModel{{
    {variables}
    {constructor}
    {methods}
}}
"""
    constructor=generate_constructor(class_name,data,program_config)
    variables=generate_variables(class_name,data,program_config)
    methods = ""
    methods += generate_toJson(class_name,data,program_config)
    methods += generate_fromJson(class_name,data,program_config)
    return MODEL_CLASS_TEMPLATE.format(class_name=class_name,
                                       variables=variables,constructor=constructor
                                       ,program_name=program_config.get("name"),
                                        methods=methods
                                       )










def generate_variables(class_name,data,program_config):
    MODEL_VARIABLE_TEMPLATE="""
\t{variable_type} {required} {variable_name};
    """
    variables=""
    for a in data.get(class_name).get("variables"):
        #required        = "?" if not  ("not null" in a.get("constraints").lower() or "primary key" in a.get("constraints").lower()) else ""
        required = ""
        variable_name   =a.get("name")
        variable_type   =local_config.dartVariableTypeParser(a.get("type"))
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
        variable_type   =local_config.dartVariableTypeParser(a.get("type"))
        required=""
        #if ("not null" in a.get("constraints").lower() or "primary key" in a.get("constraints").lower()):
        if a.get("isOptional")==False:
            variable_type   = "required "+variable_type
        else:
            required="?"

        #check if the user gave the default
        default         =a.get("default")
        default         =default if (default!=None and default!="") else local_config.getBuiltinVariableDefault(a.get("type"),a.get("constraints").lower())
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
            class_name=class_name,
            variables=variables,
            assign_variables=assign_variables,
            );




def generate_toJson(class_name,data,program_config):
    TO_JSON_TEMPLATE="""
Map<String, dynamic> toJson() {{
    return {{
        {json_assigns}
    }};
}}
    """
    JSON_ASSIGN_TEMPLATE="""
"{var_name}":{var_assign}
    """
    types_keys=list(local_config.types.keys())
    json_assigns=[]
    for a in data.get(class_name).get("variables"):
        varType_tmp=local_config.variableTypeParser(a.get("type"))
        if varType_tmp[0] == types_keys[7]:
            if varType_tmp[1] in data.keys():
               json_assigns.append(
                JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign=a.get("name")+".map((x)=>x.toJson()).toList()"
                )
               )
            else:
               json_assigns.append(
                JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign=a.get("name")
                )
               )
        

        elif varType_tmp[0] in data.keys():
            json_assigns.append(
                JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign=a.get("name")+".toJson()"
                )
            )

        else:
            json_assigns.append(
                JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign=a.get("name")
                )
            )



    return TO_JSON_TEMPLATE.format(
        json_assigns=",".join(json_assigns)

    )


def generate_fromJson(class_name,data,program_config):
    FROM_JSON_TEMPLATE="""
factory {class_name}.fromJson(Map<String,dynamic> json) {{
    return {class_name}(
        {json_assigns}
    );
}}
    """
    FROM_JSON_ASSIGN_TEMPLATE="""
{var_name}:{var_assign}
    """
    types_keys=list(local_config.types.keys())
    json_assigns=[]
    for a in data.get(class_name).get("variables"):
        varType_tmp=local_config.variableTypeParser(a.get("type"))
        if varType_tmp[0] == types_keys[7]:
            if varType_tmp[1] in data.keys():
               json_assigns.append(
                FROM_JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign="json[\""+a.get("name")+"\"]"+".map((x)=>{"+varType_tmp[1]+".fromJson(x)}).toList()"
                )
               )
            else:
               json_assigns.append(
                FROM_JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign=a.get("name")
                )
               )
        

        elif varType_tmp[0] in data.keys():
            json_assigns.append(
                FROM_JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign=varType_tmp[0]+".fromJson(json[\""+a.get("name")+"\"])"
                )
            )

        else:
            json_assigns.append(
                FROM_JSON_ASSIGN_TEMPLATE.format(
                    var_name=a.get("name"),
                    var_assign="json[\""+a.get("name")+"\"]"
                )
            )



    return FROM_JSON_TEMPLATE.format(
        class_name=class_name,
        json_assigns=",".join(json_assigns)

    )






