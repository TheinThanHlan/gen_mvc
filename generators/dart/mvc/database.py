from . import local_config


def generate(data,program_config):
    return generate_class(data,program_config)







def generate_class(data,program_config):
    DATABASE_CLASS_TEMPLATE="""

import 'dart:async';
import 'dart:io';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

class DatabaseService {{
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


            ")

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





def generate_tables(data):
    CREATE_TABLE_TEMPLATE="""
CREATE TABLE [IF NOT EXISTS] {class_name} (
    {columns}
    {constraints}
) [WITHOUT ROWID];
    """
    columns=generate_columns()
    for a in data.keys():
        for data.get(a).get("variables"):









