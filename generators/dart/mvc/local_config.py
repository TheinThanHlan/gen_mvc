model_dir="{program_root}/{program_name}/lib/data/model/"
dao_dir="{program_root}/{program_name}/lib/data/dao/"
types={
    "string":{
        "name":"String",
        "builtin_default":'""'
    },
    "int": {
        "name": "int",
        "builtin_default":"0"
    },
    "long": {
        "name": "int",
        "builtin_default":"0"
    },
    "double": {
          "name": "double",
          "builtin_default":"0.0"
    },
    "float": {
          "name": "double",
          "builtin_default":"0.0"
    },
    "bool": {
        "name": "bool",
        "builtin_default":"false"
    },
    "list": {
        "name": "List",
        "builtin_default":"[]"
    },
    "map": {
        "name": "Map",
        "builtin_default":"{}"
    },
    "datetime":{
        "name":"DateTime",
        "builtin_default":"DateTime.now()"
    }

}

def variableTypeParser(var):
    output = ""
    if ("<" not in var) and (">" not in var):
        output = types.get(var,{}).get("name",var)
    else:
        b = ""
        for a in var:
            if a == "<":
                output += types.get(b,{}).get("name",b) + "<"
                b = ""
            elif a == ">":
                output += types.get(b,{}).get("name",b) + ">"
                b = ""

            elif a == ",":
                output += types.get(b,{}).get("name",b) + ","
                b = ""

            else:
                b += a
    return output

def getBuiltinVariableDefault(var,isOptional):
    output = ""
    if ("<" not in var) and (">" not in var) :
        output = var;
    else:
        b = ""
        for a in var:
            if a == "<":
                output += b
                break
            else:
                b += a
    if(not output in types.keys() and  isOptional==False):
        raise Exception("in variable type '"+var+"' the default value must be specify" )
    else:
        return types.get(output,{}).get("builtin_default","")





