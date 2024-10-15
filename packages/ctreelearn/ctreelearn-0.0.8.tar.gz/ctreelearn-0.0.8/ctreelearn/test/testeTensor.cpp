#include <torch/torch.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>


int main() {
  // Create a tensor.
  torch::Tensor tensor = torch::rand({2, 3});

  py::array_t<float> gradWeight_np = py::array(py::buffer_info(
                    tensor.data_ptr<float>(),            
                    sizeof(float),     
                    py::format_descriptor<float>::value, 
                    1,         
                    {  3 }, 
                    { sizeof(float) }
            ));
  

  std::cout << tensor << std::endl;
}