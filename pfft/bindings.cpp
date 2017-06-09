#include <pybind11/pybind11.h>
#include <iostream>

namespace py = pybind11;

PYBIND11_MODULE(bindings, m) {

  m.doc() = "pfft build plugin";
  m.def("funcy", []() { return std::string("this is funcy"); }, "funcy function");

}
