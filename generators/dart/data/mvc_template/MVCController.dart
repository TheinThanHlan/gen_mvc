import './interface/IMVCModel.dart';
import './MVCView.dart';

abstract class MVCController<M extends IMVCModel> {
  MVCView view;
  M model;
  MVCController({required this.view, required this.model}) {
    view.controller = this;
  }
}
