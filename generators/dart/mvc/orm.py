from . import local_config



def generate(data,program_config):
    database_class= generate_class(data,program_config)
    return database_class




def generate_class(data,program_config):
    DATABASE_CLASS_TEMPLATE="""

import 'dart:async';
import 'dart:io';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

class DatabaseProvider {{
  static final int _version = 3;
  static final String _dbName = "{program_name}.db";
  static Database? _db = null;

  static Future<Database> getDatabase() async {{
    if (_db == null) {{
      if (Platform.isWindows || Platform.isLinux) {{
        sqfliteFfiInit();
      }}
      databaseFactory = databaseFactoryFfi;

      String db_path = join(await getDatabasesPath(), _dbName);
      print(db_path);
      _db = await openDatabase(
        db_path,
        version: _version,
        onCreate: (db,version){{
            db.execute("
{tables}


            ");

        }}
      );
    }}
    return _db!;
  }}
}}




"""
    tables=generate_tables(data)
    return DATABASE_CLASS_TEMPLATE.format(program_name=program_config.get("name"),
                                            tables=tables)




sql_maps=["OneToOne","ManyToOne","OneToMany","ManyToMany"]
def generate_tables(data):
    CREATE_TABLE_TEMPLATE="""
CREATE TABLE IF NOT EXISTS {class_name}(
    {columns}
)"""
    COLUMN_TEMPLATE="""
{column_name} {column_type} {constraints}"""

    FOREIGN_KEY_TEMPLATE="""
foreign key ({column_name}) references {reference_class_name}({reference_column_name})"""

    KEY_TEMPLATE="""
{key} ({column_names})"""
    tables=[]
    junction_tables=[]
    for a in data.keys():
        columns=[]
        foreign_key=[]
        class_name=""
        constraints=""
        column_name=""
        column_type=[]
        for b in data.get(a).get("variables"):
            constraints=b.get("constraints")
            column_name=b.get("name")
            column_type=variableTypeParser(b.get("type"))
            map_type=b.get("map")
            if map_type in sql_maps:
                if map_type.lower() == sql_maps[0].lower(): #one to one
                    column_name=column_name+"_id"
                    constraints+=" unique " if "unique" not in constraints else ""
                    reference_class_name=column_type[0]                             #set reference class name
                    reference_class = getPrimaryKeyOfColumn(column_type[0],data)     #pre store the reference class

                    column_type=variableTypeParser(reference_class.get("type"))     #set the column type to type of reference class
                    column_type=getSqliteVarType(column_type[0])                     #get sql var type

                    reference_column_name=reference_class.get("name")

                    foreign_key.append(
                        FOREIGN_KEY_TEMPLATE.format(
                            column_name=column_name,
                            reference_class_name=reference_class_name,
                            reference_column_name=reference_column_name
                            ))




                elif map_type == sql_maps[1]: #One to Many
                    continue

                elif map_type == sql_maps[2]: #One to Many
                    column_name=column_name+"_id"

                    reference_class_name=column_type[1]                             #set reference class name
                    reference_class = getPrimaryKeyOfColumn(column_type[1],data)     #pre store the reference class

                    column_type=variableTypeParser(reference_class.get("type"))     #set the column type to type of reference class
                    column_type=getSqliteVarType(column_type[0])                     #get sql var type

                    reference_column_name=reference_class.get("name")

                    foreign_key.append(
                        FOREIGN_KEY_TEMPLATE.format(
                            column_name=column_name,
                            reference_class_name=reference_class_name,
                            reference_column_name=reference_column_name
                            ))


                elif map_type == sql_maps[3]: #Many to many
                    if(b.get("mappedBy") != ""):
                        references={}
                        reference_columns=[]
                        reference_foreign=[]
                        references[b.get("mappedBy")]               =getPrimaryKeyOfColumn(a,data)
                        references[b.get("name")]           =getPrimaryKeyOfColumn(variableTypeParser(b.get("type"))[1],data)

                        references[b.get("mappedBy")]["class"]      =  a
                        references[b.get("name")]["class"]  =  variableTypeParser(b.get("type"))[1]


                        for c in references.keys():
                            reference_columns.append(
                                COLUMN_TEMPLATE.format(
                                    column_name=c+"_id",
                                    column_type=getSqliteVarType(variableTypeParser(references.get(c).get("type"))[0]),
                                    constraints=" not null "
                                    )
                                )
                            reference_foreign.append(
                                FOREIGN_KEY_TEMPLATE.format(
                                    column_name=c+"_id",
                                    reference_class_name=references.get(c).get("class"),
                                    reference_column_name=references.get(c).get("name")
                                    )
                                )
                        reference_columns.extend(reference_foreign)
                        junction_tables.append(CREATE_TABLE_TEMPLATE.format(
                            class_name="_".join(references.keys()),
                            columns=",".join(reference_columns)
                        ))
                    continue

            else:
                column_type=getSqliteVarType(column_type[0])

            columns.append(COLUMN_TEMPLATE.format(
                column_name=column_name,
                column_type=column_type,
                constraints=constraints
                ))

        columns.extend(foreign_key)
        tables.append(
                CREATE_TABLE_TEMPLATE.format(
            class_name=a,
            columns=",".join(columns))
                )

    tables.extend(junction_tables)
    return ";".join(tables)


def getPrimaryKeyOfColumn(column_type,data):
    for a in data.get(column_type).get("variables"):
        if "primary key" in a.get("constraints").lower():
            return a



def variableTypeParser(variableType):
    return variableType.replace("<",",").replace(">",",").split(",")


def getSqliteVarType(column_type):
    column_type=local_config.types.get(column_type,{}).get("sqlite","TEXT")
    return column_type



