import 'package:flutter/material.dart';
import './MVCController.dart';

abstract class MVCView<T extends MVCController> extends StatefulWidget {
  late final T controller;
}
