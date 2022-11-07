#include "QuEST.h"

#include <iostream>
#include <memory>
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

    void run(std::vector<double> p0) {
        for (int i = 0; i < n_qubits - 3; i++) {
            hadamard(qubits, i);
            hadamard(qubits, i + 1);
            hadamard(qubits, i + 2);
            hadamard(qubits, i + 3);
            rotateX(qubits, i, p0[i * 11]);
            rotateX(qubits, i + 1, p0[i * 11 + 1]);
            rotateX(qubits, i + 2, p0[i * 11 + 2]);
            rotateX(qubits, i + 3, p0[i * 11 + 3]);
            controlledNot(qubits, i, i + 1);
            controlledNot(qubits, i + 1, i + 2);
            controlledNot(qubits, i + 2, i + 3);
            controlledNot(qubits, i + 3, i);
            int idx1[2] = {i, i + 1};
            int idx2[2] = {i + 1, i + 2};
            int idx3[2] = {i + 2, i + 3};
            pauliOpType pdx1[2] = {PAULI_X, PAULI_X};
            pauliOpType pdx2[2] = {PAULI_Y, PAULI_Y};
            pauliOpType pdx3[2] = {PAULI_Z, PAULI_Z};
            multiRotatePauli(qubits, idx1, pdx1, 2, p0[i * 11 + 4]);
            multiRotatePauli(qubits, idx2, pdx2, 2, p0[i * 11 + 5]);
            multiRotatePauli(qubits, idx3, pdx3, 2, p0[i * 11 + 6]);
            sGate(qubits, i);
            sGate(qubits, i + 1);
            tGate(qubits, i + 2);
            tGate(qubits, i + 3);
            rotateY(qubits, i + 1, p0[i * 11 + 7]);
            rotateY(qubits, i + 2, p0[i * 11 + 8]);
            swapGate(qubits, i, i + 3);
            rotateX(qubits, i, p0[i * 11 + 9]);
            rotateX(qubits, i + 3, p0[i * 11 + 10]);
        }
    }
};

class RandomHam : public BasicTestEnv {
 public:
    explicit RandomHam(int n_qubits) : BasicTestEnv(n_qubits) {
        std::vector<qreal> coeffs(get_nterms(), 1.0);
        enum pauliOpType* paulis = new enum pauliOpType[n_qubits * 4 * (n_qubits - 3)];
        int idx = 0;
        for (int i = 0; i < n_qubits - 3; i++) {
            {
                std::vector<pauliOpType> current(n_qubits, PAULI_I);
                current[i] = PAULI_Y;
                current[i + 1] = PAULI_Y;
                current[i + 2] = PAULI_Y;
                current[i + 3] = PAULI_Y;
                for (auto p : current) {
                    paulis[idx++] = p;
                }
            }
            {
                std::vector<pauliOpType> current(n_qubits, PAULI_I);
                current[i] = PAULI_X;
                current[i + 2] = PAULI_X;
                for (auto p : current) {
                    paulis[idx++] = p;
                }
            }
            {
                std::vector<pauliOpType> current(n_qubits, PAULI_I);
                current[i + 1] = PAULI_Z;
                current[i + 3] = PAULI_Z;
                for (auto p : current) {
                    paulis[idx++] = p;
                }
            }
            {
                std::vector<pauliOpType> current(n_qubits, PAULI_I);
                current[i] = PAULI_Z;
                current[i + 1] = PAULI_Y;
                current[i + 2] = PAULI_X;
                current[i + 3] = PAULI_Z;
                for (auto p : current) {
                    paulis[idx++] = p;
                }
            }
        }
        ham = {paulis, coeffs.data(), get_nterms(), n_qubits};
        for (int i = 0; i < n_qubits; i++) {
            hadamard(qubits, i);
        }
    }

    auto run() {
        auto workspace = createQureg(n_qubits, env);

        auto res = calcExpecPauliSum(qubits, ham.pauliCodes, ham.termCoeffs, get_nterms(), workspace);
        destroyQureg(workspace, env);
        return res;
    }

    int get_nterms() {
        return 4 * (n_qubits - 3);
    }

 public:
    PauliHamil ham;
};
namespace py = pybind11;

PYBIND11_MODULE(quest_test, m) {
    py::class_<BasicTestEnv, std::shared_ptr<BasicTestEnv>>(m, "basic_test_env")
        .def(py::init<int>())
        .def("reportQuESTEnv", &BasicTestEnv::ReportQuESTEnv)
        .def("reportStateToScreen", &BasicTestEnv::ReportStateToScreen);
    py::class_<RandomCircuit, BasicTestEnv, std::shared_ptr<RandomCircuit>>(m, "random_circuit_test")
        .def(py::init<int>())
        .def("run", &RandomCircuit::run)
        .def("get_np", &RandomCircuit::get_np);
    py::class_<RandomHam, BasicTestEnv, std::shared_ptr<RandomHam>>(m, "random_ham_test")
        .def(py::init<int>())
        .def("run", &RandomHam::run);
}
