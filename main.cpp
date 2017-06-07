#include <iostream>
#include "ce.h"
#include <boost/optional.hpp>

void hello();


int main(int, char**) {
  boost::optional<double> bo;
  bo = S::d;   // link error
  // xbo = (double)S::d;

  std::cout << "bo is " << *bo << "\n";
  hello();
}
