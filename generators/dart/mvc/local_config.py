types={
    "string": {
        "name": "String",
        "builtin_default": "\"\"",
        "sqlite": "TEXT"
    },
    "int": {
        "name": "int",
        "builtin_default": "0",
        "sqlite": "INTEGER"
    },
    "long": {
        "name": "int",
        "builtin_default": "0",
        "sqlite": "INTEGER"
    },
    "double": {
        "name": "double",
        "builtin_default": "0.0",
        "sqlite": "REAL"
    },
    "float": {
        "name": "double",
        "builtin_default": "0.0",
        "sqlite": "REAL"
    },
    "bool": {
        "name": "bool",
        "builtin_default": "false",
        "sqlite": "INTEGER"  # SQLite does not have a separate Boolean storage class. Instead, boolean values are stored as integers 0 (false) and 1 (true).
    },
    "list": {
        "name": "List",
        "builtin_default": "[]",
        "sqlite": "TEXT"  # In SQLite, complex types like lists are often stored as TEXT (e.g., JSON strings).
    },
    "map": {
        "name": "Map",
        "builtin_default": "{}",
        "sqlite": "TEXT"  # As above, stored as JSON strings.
    },
    "datetime": {
        "name": "DateTime",
        "builtin_default": "DateTime.now()",
        "sqlite": "TEXT"  # SQLite stores dates and times as TEXT, REAL, or INTEGER.
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





