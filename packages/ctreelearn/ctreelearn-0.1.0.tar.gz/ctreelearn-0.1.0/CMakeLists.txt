# Instruções de compilação
#
# Compilar somente os arquivos de teste: 
#    cmake -DBUILD_PYBIND=OFF -DBUILD_DEBUG=ON -DBUILD_TESTS=ON ../
#    cmake -DBUILD_PYBIND=OFF -DBUILD_DEBUG=OFF -DBUILD_TESTS=ON ../
#
# Compilar arquivos de testes e bindings Python: 
#    cmake -DBUILD_DEBUG=ON -DBUILD_TESTS=ON -DPYTHON_LIBRARY_DIR=$(python -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))") -DPYTHON_EXECUTABLE=$(python -c "import sys; print(sys.executable)") ../
#    cmake -DBUILD_TESTS=ON -DPYTHON_LIBRARY_DIR=$(python -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))") -DPYTHON_EXECUTABLE=$(python -c "import sys; print(sys.executable)") ../
#
# Compilar somente os bindings Python:
#    cmake -DPYTHON_LIBRARY_DIR=$(python3 -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))") -DPYTHON_EXECUTABLE=$(python3 -c "import sys; print(sys.executable)") ../
#
# Depois:
#   make
#   make install
cmake_minimum_required(VERSION 3.14)
project(ctreelearn)

# Opções configuráveis
option(BUILD_PYBIND "Enable building Python bindings with pybind11" ON)
option(BUILD_DEBUG "Enable Debug mode" OFF)
option(BUILD_TESTS "Enable building of tests" OFF)

# Configurações de compilação (Release por padrão)
if(BUILD_DEBUG)
    set(CMAKE_BUILD_TYPE Debug)
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
else()
    set(CMAKE_BUILD_TYPE Release)
    set(CMAKE_CXX_FLAGS "-O3")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif()

# Padrões de C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Incluir o diretório do subprojeto ctreelearn
add_subdirectory(ctreelearn)

# Incluir pybind11 se BUILD_PYBIND estiver ativado
if(BUILD_PYBIND)

    # Incluir pybind11 via FetchContent ou localmente
    include(FetchContent)
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.10.4
    )
    FetchContent_MakeAvailable(pybind11)
    
    # Arquivo fonte principal do módulo pybind
    set(PYBIND_CPP_FILE "ctreelearn/ctreelearn.cpp")

    # Módulo Python usando pybind11
    pybind11_add_module(ctreelearn ${PYBIND_CPP_FILE})

    # Encontrar o PyTorch
    if(NOT Torch_DIR)
        set(Torch_DIR "/opt/anaconda3/lib/python3.9/site-packages/torch/share/cmake/Torch")
    endif()

    # Configurar explicitamente o RPATH no CMakeLists.txt
    set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
    set(CMAKE_INSTALL_RPATH "/opt/anaconda3/lib/python3.9/site-packages/torch/lib")
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

    find_package(Torch REQUIRED)

    # Definir o RPATH para encontrar as bibliotecas do PyTorch corretamente
    #set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
    #set(CMAKE_INSTALL_RPATH "${TORCH_INSTALL_PREFIX}/lib")

    # Linkar o módulo Python com a biblioteca ctreelearn_lib e o PyTorch
    target_link_libraries(ctreelearn PRIVATE ctreelearn_lib "${TORCH_LIBRARIES}")

    # Propriedades de RPATH para o target
    set_target_properties(ctreelearn PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "${CMAKE_INSTALL_RPATH}"
        SKIP_BUILD_RPATH FALSE
    )

    message(STATUS "Torch libraries: ${TORCH_LIBRARIES}")
    message(STATUS "Torch include dirs: ${TORCH_INCLUDE_DIRS}")

    # Definir PYTHON_LIBRARY_DIR corretamente ou usar padrão
    if(NOT DEFINED PYTHON_LIBRARY_DIR)
        set(PYTHON_LIBRARY_DIR "${CMAKE_INSTALL_PREFIX}/lib/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages")
    endif()

    # Instalar o módulo Python
    install(TARGETS ctreelearn
            COMPONENT python
            LIBRARY DESTINATION "${PYTHON_LIBRARY_DIR}"
    )
endif()

# Condicionalmente adicionar a compilação de testes
if(BUILD_TESTS)

    # Adicionar o executável de testes
    add_executable(testeResidualTree 
        ctreelearn/test/testeResidualTree.cpp
    )
    target_link_libraries(testeResidualTree PRIVATE ctreelearn_lib)

    # Encontrar o PyTorch
    if(NOT Torch_DIR)
        set(Torch_DIR "/opt/anaconda3/lib/python3.9/site-packages/torch/share/cmake/Torch")
    endif()

    find_package(Torch REQUIRED)

    # Adicionar teste com PyTorch
    add_executable(testeTensor
        ctreelearn/test/testeTensor.cpp
    )
    target_link_libraries(testeTensor PRIVATE ctreelearn_lib "${TORCH_LIBRARIES}")

endif()
