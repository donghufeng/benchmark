from mindquantum import Simulator, Circuit, X, RY, Hamiltonian
from openfermion import QubitOperator
c = Circuit([X.on(0)])
ansatz = Circuit([RY('a').on(0)])
i=1
print(i)
s = Simulator(i)
s.set_ansatz(ansatz)
print(s.gradient([1.2], ['a'], '0'))
# s.evolution(ansatz, {'a': 1})
print(s.cheat())
