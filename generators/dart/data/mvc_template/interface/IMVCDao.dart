import "./IMVCModel.dart";

abstract class IMVCDao<T extends IMVCModel> {
  void create(T data);
  T read(int id);
  void update(T data);
  void delete(T data);
}
