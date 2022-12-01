#include "QuEST.h"

#include <cstdlib>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <vector>

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
class BasicTestEnv {
 public:
    explicit BasicTestEnv(int n_qubits) : n_qubits(n_qubits) {
        env = createQuESTEnv();
        qubits = createQureg(n_qubits, env);
    }

    void ReportQuESTEnv() {
        reportQuESTEnv(env);
    }
    void ReportStateToScreen() {
        reportStateToScreen(qubits, env, (1UL << n_qubits));
    }
    void GetAmp(long long index) {
        auto res = getAmp(qubits, index);
        std::cout << res.real << ", " << res.imag << std::endl;
    }
    ~BasicTestEnv() {
        destroyQureg(qubits, env);
        destroyQuESTEnv(env);
    }

 public:
    int n_qubits;
    QuESTEnv env;
    Qureg qubits;
};

class RandomCircuit : public BasicTestEnv {
 public:
    explicit RandomCircuit(int n_qubits) : BasicTestEnv(n_qubits) {
    }

    int get_np() {
        return (n_qubits - 3) * 11;
    }
    void apply_gate(std::string name, int q1, int q2, double coeff) {
        if (name == "x") {
            pauliX(qubits, q1);
        } else if (name == "y") {
            pauliY(qubits, q1);
        } else if (name == "z") {
            pauliZ(qubits, q1);
        } else if (name == "h") {
            hadamard(qubits, q1);
        } else if (name == "s") {
            sGate(qubits, q1);
        } else if (name == "t") {
            tGate(qubits, q1);
        } else if (name == "cx") {
            controlledNot(qubits, q1, q2);
        } else if (name == "cy") {
            controlledPauliY(qubits, q1, q2);
        } else if (name == "cz") {
            controlledPhaseFlip(qubits, q1, q2);
        } else if (name == "rx") {
            rotateX(qubits, q1, coeff);
        } else if (name == "ry") {
            rotateY(qubits, q1, coeff);
        } else if (name == "rz") {
            rotateZ(qubits, q1, coeff);
        } else if (name == "xx") {
            int targetQubits[2] = {q1, q2};
            pauliOpType targetPaulis[2] = {PAULI_X, PAULI_X};
            multiRotatePauli(qubits, targetQubits, targetPaulis, 2, coeff);
        } else if (name == "yy") {
            int targetQubits[2] = {q1, q2};
            pauliOpType targetPaulis[2] = {PAULI_Y, PAULI_Y};
            multiRotatePauli(qubits, targetQubits, targetPaulis, 2, coeff);
        } else if (name == "zz") {
            int targetQubits[2] = {q1, q2};
            pauliOpType targetPaulis[2] = {PAULI_Z, PAULI_Z};
            multiRotatePauli(qubits, targetQubits, targetPaulis, 2, coeff);
        } else {
            throw std::runtime_error("gate no implement for quest");
        }
    }
    void apply_gate(std::string name, int q1) {
        apply_gate(name, q1, 0, 0.0);
    }
    void apply_gate(std::string name, int q1, int q2) {
        apply_gate(name, q1, q2, 0.0);
    }
    void apply_gate(std::string name, int q1, double coeff) {
        apply_gate(name, q1, 0, coeff);
    }
};

class RandomHam : public BasicTestEnv {
 public:
    explicit RandomHam(int n_qubits, const std::vector<std::vector<std::pair<std::string, int>>>& py_hams)
        : BasicTestEnv(n_qubits) {
        terms = py_hams.size();
        pauliCodes = reinterpret_cast<pauliOpType*>(malloc(sizeof(pauliOpType) * n_qubits * terms));
        termCoeffs = reinterpret_cast<qreal*>(malloc(sizeof(qreal) * terms));
        for (size_t i = 0; i < py_hams.size(); ++i) {
            termCoeffs[i] = 1;
        }
        int poi = 0;
        for (auto& term : py_hams) {
            std::vector<pauliOpType> current(n_qubits, PAULI_I);
            for (auto& [p, idx] : term) {
                if (p == "X") {
                    current[idx] = PAULI_X;
                } else if (p == "Y") {
                    current[idx] = PAULI_Y;
                } else if (p == "Z") {
                    current[idx] = PAULI_Z;
                } else {
                    throw std::runtime_error("");
                }
            }
            for (auto a : current) {
                pauliCodes[poi++] = a;
            }
        }
        for (int i = 0; i < n_qubits; i++) {
            hadamard(qubits, i);
        }
    }
    auto run() {
        auto workspace = createQureg(n_qubits, env);

        auto res = calcExpecPauliSum(qubits, pauliCodes, termCoeffs, get_nterms(), workspace);
        destroyQureg(workspace, env);
        return res;
    }

    int get_nterms() {
        return terms;
    }
    ~RandomHam() {
        free(pauliCodes);
        free(termCoeffs);
    }

 public:
    pauliOpType* pauliCodes;
    qreal* termCoeffs;
    int terms;
};
namespace py = pybind11;
#ifdef ENABLE_GPU
#    define quest_test quest_test_gpu
#endif
using namespace pybind11::literals;
PYBIND11_MODULE(quest_test, m) {
    py::class_<BasicTestEnv, std::shared_ptr<BasicTestEnv>>(m, "basic_test_env")
        .def(py::init<int>())
        .def("reportQuESTEnv", &BasicTestEnv::ReportQuESTEnv)
        .def("reportStateToScreen", &BasicTestEnv::ReportStateToScreen);
    py::class_<RandomCircuit, BasicTestEnv, std::shared_ptr<RandomCircuit>>(m, "random_circuit_test")
        .def(py::init<int>())
        .def("apply_gate", py::overload_cast<std::string, int>(&RandomCircuit::apply_gate))
        .def("apply_gate", py::overload_cast<std::string, int, int>(&RandomCircuit::apply_gate))
        .def("apply_gate", py::overload_cast<std::string, int, int, double>(&RandomCircuit::apply_gate))
        .def("apply_gate", py::overload_cast<std::string, int, double>(&RandomCircuit::apply_gate))
        .def("get_np", &RandomCircuit::get_np);
    py::class_<RandomHam, BasicTestEnv, std::shared_ptr<RandomHam>>(m, "random_ham_test")
        .def(py::init<int, std::vector<std::vector<std::pair<std::string, int>>>>())
        .def("run", &RandomHam::run)
        .def("get_nterms", &RandomHam::get_nterms);
}
