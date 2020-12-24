import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import collections
import mindquantum as mq
from openfermion import QubitOperator
import numpy as np
from mindspore.nn.optim import Momentum
from mindspore import Tensor
from mindspore.ops import operations as P
import time
import mindspore.context as context
from dataset import CircuitDataset
context.set_context(mode=context.PYNATIVE_MODE, device_target="GPU")


def convert_to_circuit(image, n_qubits=None):
    values = np.ndarray.flatten(image)
    if n_qubits is None:
        n_qubits = len(values)

    c = mq.Circuit()
    for i, value in enumerate(values[:n_qubits]):
        if value:
            c += mq.X.on(i + 1)
    return c


class CircuitLayerBuilder():
    def __init__(self, data_qubits, readout):
        self.data_qubits = data_qubits
        self.readout = readout

    def add_layer(self, circuit, gate, prefix):
        for i, qubit in enumerate(self.data_qubits):
            symbol = prefix + '-' + str(i)
            circuit.append(gate({symbol: np.pi / 2}).on([qubit, self.readout]))


def create_quantum_model(n):
    data_qubits = range(1, n)
    readout = 0
    c = mq.Circuit()

    c = c + mq.X.on(readout) + mq.H.on(readout)
    builder = CircuitLayerBuilder(data_qubits=data_qubits, readout=readout)
    builder.add_layer(c, mq.XX, 'xx1')
    builder.add_layer(c, mq.ZZ, 'zz1')
    c += mq.H.on(readout)
    return c, mq.Z.on(readout)


datas = np.load('./mnist_resize.npz')

n = 16
num_sampling = 2000
x_train_bin, y_train_nocon, x_test_bin, y_test = datas['arr_0'], datas[
    'arr_1'], datas['arr_2'], datas['arr_3']
x_train_circ = [convert_to_circuit(x, n - 1) for x in x_train_bin]
x_test_circ = [convert_to_circuit(x, n - 1) for x in x_test_bin]
train_loader = CircuitDataset(
    {
        'x_train': x_train_circ[:num_sampling],
        'y_train': y_train_nocon[:num_sampling]
    },
    batch_size=20)
test_loader = CircuitDataset({'x_test': x_test_circ, 'y_test': y_test})

model_circuit, model_readout = create_quantum_model(n)
s = mq.Simulator(n)
s.set_ansatz(model_circuit)

pname = list(model_circuit.paras_set)
measurement = mq.Hamiltonian(QubitOperator('Z0'), n)
mql = mq.MindquantumLayer(s, measurement, pname,
                          np.random.random(len(pname)) * 2 * np.pi - np.pi)

epochs = 3
lr = 0.7
mom = 0.7
optimizer = Momentum(filter(lambda x: x.requires_grad, mql.get_parameters()),
                     learning_rate=lr,
                     momentum=mom)
t0 = time.time()
for epoch in range(epochs):
    for batch, (imgs, labels) in enumerate(train_loader):
        labels = Tensor(labels[None, :].T.astype('float32'))
        output, grad_mq = mql.calc(imgs)
        output = (output + 1) / 2
        losslayer = mq.nn.LossLayer(output)
        loss = losslayer(labels)
        grad_loss = losslayer.grad(labels)
        grad_back = P.MatMul(transpose_a=True)(grad_loss, grad_mq / 2)
        optimizer((grad_back, ))
        print("Epoch: {}/{}, Batch: {}/{}, loss: {}, acc: {}.".format(
            epoch, epochs, batch, train_loader.get_num_batches(),
            loss.asnumpy() * 1, np.mean(((output > 0.5) == labels).asnumpy())))
print('total time:{}'.format(time.time() - t0))
