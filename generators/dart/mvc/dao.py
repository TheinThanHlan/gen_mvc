from . import local_config




def generate(class_name,data,program_config):
    return generate_class(class_name,data,program_config)







def generate_class(class_name,data,program_config):
    MODEL_CLASS_TEMPLATE="""
import 'package:{program_name}/mvc_template/interface/IMVCDao.dart';
import 'package:{program_name}/mvc_template/MVCDatabaseProvider.dart';
import 'package:{program_name}/data/model/{class_name}.dart';
import 'package:{program_name}/mvc_template/MVCDao.dart';

class {class_name}Dao extends MVCDao implements IMVCDao<{class_name}>{{
    {methods}
}}
"""
    methods=""
    methods+=generateInsert(class_name,data,program_config)
    methods+=generateDelete(class_name,data,program_config)
    return MODEL_CLASS_TEMPLATE.format(class_name=class_name,
                                       program_name=program_config.get("name"),
                                       methods= methods
                                       )




def generateInsert(class_name,data,program_config):
    INSERT_METHOD_TEMPLATE="""
Future<{class_name}> insert({class_name} tmp) async {{
    var database = await MVCDatabaseProvider.getDatabase();
    
    tmp.{primary_key}=await database.rawInsert(
        "insert into {class_name}({vars}) values({var_assigns});"
    );
    {mtm_inserts}
    return tmp;
}}   
    """
    MTM_INSERTS_TEMPLATE="""
tmp.{mtm_var}.forEach((b){{
     database.rawInsert(
        "INSERT INTO {junction_table_name}({junction_columns}) values({junction_value},${{b.{primary_key_of_join_column}}})"
    );
}});
    """
    insert_statements=[]
    vars=[]
    var_assigns=[]
    primary_key=""
    mtm_inserts=[]
    for a in data.get(class_name).get("variables"): 
        if "primary key" in a.get("constraints").lower():
            primary_key=a.get("name")
            
        elif a.get("map") !="":
            if a.get("map")=="OneToOne" or a.get("map")=="ManyToOne":
                vars.append(a.get("name")+"_id"); # add vars 
                for b in data.get(a.get("type")).get("variables"):
                    if "primary key" in b.get("constraints").lower():
                        var_assigns.append("'${tmp."+a.get("name")+"."+b.get("name")+"}'") #assign vars
                        break
                
            elif a.get("map") == "ManyToMany" and a.get("mappedBy")!="":
                join_column_name=[]
                if a.get("mappedBy")!="":
                    join_column_name=[a.get("mappedBy"),a.get("name")]
                else:
                    for b in data.get(local_config.variableTypeParser(a.get("type"))[1]).get("variables"):
                        if b.get("mappedBy")==a.get("name"):
                            join_column_name=[b.get("name"),a.get("name")]
                            
                #join column set
                junction_table_name="_".join(join_column_name)
                junction_columns=[s + "_id" for s in join_column_name]
                primary_key_of_join_column=local_config.getPrimaryKeyOfColumn(local_config.variableTypeParser(a.get("type"))[1],data).get("name")
                mtm_inserts.append(
                    MTM_INSERTS_TEMPLATE.format(junction_table_name=junction_table_name,junction_columns=",".join(junction_columns),junction_value="${tmp."+primary_key+"}",mtm_var=a.get("name"),primary_key_of_join_column=primary_key_of_join_column)
                )
                print(junction_table_name)

            
        else:
            vars.append(a.get("name"))
            var_assigns.append("'${tmp."+a.get("name")+"}'")
            
    
    insert_statements.append(
        INSERT_METHOD_TEMPLATE.format(
            class_name=class_name,
            vars=",".join(vars),
            var_assigns=",".join(var_assigns),
            primary_key=primary_key,
            mtm_inserts=" ".join(mtm_inserts)
        )
    )
    insert_statements.reverse()

    return ";".join(insert_statements)

    
    
    



def generateDelete(class_name,data,program_config):
    DELETE_CLASS_TEMPLATE="""
void delete({class_name} tmp) async {{
    var database = await MVCDatabaseProvider.getDatabase();
    await database.delete("{class_name}", where: "{id}=${{tmp.{id}}}");
}}
    """
    DELETE_TEMPLATE="""
    """
    
    id=local_config.getPrimaryKeyOfColumn(class_name,data).get('name')
    
    return DELETE_CLASS_TEMPLATE.format(
        class_name=class_name,
        id=id,
        recursive_delete=""
    )









