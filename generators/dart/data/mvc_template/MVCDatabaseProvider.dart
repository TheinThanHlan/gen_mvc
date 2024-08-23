import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite/sqlite_api.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

class MVCDatabaseProvider {
  final int _version = 3;
  late final String _dbName;
  late final String _sql_create_schema;
  late final Database _db;
  static MVCDatabaseProvider? _instance = null;

  static Future<Database> getDatabase() async {
    if (_instance == null) {
      _instance = await MVCDatabaseProvider();

      _instance!._dbName =
          jsonDecode(await File("assets/global.json").readAsString())["name"];

      _instance!._sql_create_schema =
          await File("assets/databases/database.sql").readAsString();

      if (Platform.isWindows || Platform.isLinux) {
        sqfliteFfiInit();
      }
      databaseFactory = databaseFactoryFfi;

      String db_path = join(await getDatabasesPath(), _instance!._dbName);
      print(db_path);
      _instance!._db = await openDatabase(db_path, version: _instance!._version,
          onCreate: (db, version) {
        db.execute(_instance!._sql_create_schema);
      });
    }
    return _instance!._db;
  }
}

