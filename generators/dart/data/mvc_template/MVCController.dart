import './interface/IMVCModel.dart';
import './interface/IMVCDao.dart';
import './MVCView.dart';

abstract class MVCController<M extends IMVCModel, D extends IMVCDao> {
  MVCView view;
  M model;
  D dao;

  MVCController({required this.view, required this.model, required this.dao}) {
    view.controller = this;
  }
}
