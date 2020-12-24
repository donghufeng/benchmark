import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import collections
import mindquantum as mq
from openfermion import QubitOperator
import numpy as np


def filter_36(x, y):
    keep = (y == 3) | (y == 6)
    x, y = x[keep], y[keep]
    y = y == 3
    return x, y


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


def binary_sum(y_true, y_pred):
    return torch.sum(((y_pred > 0.5) == y_true.reshape(-1, 1)).float())


def hing_sum(y_true, y_pred):
    return torch.sum(((y_pred > 0) == (y_true.reshape(-1, 1) > 0)).float())


class HingLoss(torch.nn.Module):
    def __init__(self):
        super(HingLoss, self).__init__()

    def forward(self, output, target):
        hing_loss = 1 - torch.mul(output, target)
        hing_loss[hing_loss < 0] = 0
        return hing_loss


def train(model, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        t0 = time.time()
        target = target.reshape(-1, 1)
        optimizer.zero_grad()
        output = model(data)
        loss = torch.nn.functional.mse_loss(output, target)
        # myloss = HingLoss()
        # loss = myloss(output, target)
        # loss = torch.nn.functional.hinge_embedding_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 10 == 0:
            t1 = time.time() - t0
            print(
                'Train Epoch:{} [{}/{} ({:.0f}%)]\tLoss:{:.6f}, \t{}ms for each sample'
                .format(epoch, batch_idx * len(data),
                        len(train_loader.dataset),
                        100 * batch_idx / len(train_loader), loss.item(),
                        round(t1 * 1000 / 32, 3)))


def test(model, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            target = target.reshape(-1, 1)
            output = model(data)
            test_loss += torch.nn.functional.hinge_embedding_loss(
                output, target).item()
            # pred = 1*(output > 0.5)
            correct += binary_sum(target, output).item()
    test_loss /= len(test_loader.dataset)
    print(
        '\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
            test_loss, correct, len(test_loader.dataset),
            100. * correct / len(test_loader.dataset)))


datas = np.load('./mnist_resize.npz')

n = 16
num_sampling = 2000
x_train_bin, y_train_nocon, x_test_bin, y_test = datas['arr_0'], datas[
    'arr_1'], datas['arr_2'], datas['arr_3']
x_train_circ = [convert_to_circuit(x, n - 1) for x in x_train_bin]
x_test_circ = [convert_to_circuit(x, n - 1) for x in x_test_bin]
train_loader, _ = train_test_dataset_loader(x_train_circ[:num_sampling],
                                            y_train_nocon[:num_sampling],
                                            batch_size=32)
test_loader, _ = train_test_dataset_loader(x_test_circ, y_test)

model_circuit, model_readout = create_quantum_model(n)
s = mq.Simulator(n)
s.set_ansatz(model_circuit)


class Shift(torch.nn.Module):
    def __init__(self, a, b):
        super(Shift, self).__init__()
        self.a = a
        self.b = b

    def forward(self, x):
        return torch.mul(torch.add(x, self.a), self.b)


class Net(torch.nn.Module):
    def __init__(self, hl):
        super(Net, self).__init__()
        self.hl = hl

    def forward(self, x):
        x = self.hl(x)
        x = torch.add(x, 1)
        x = torch.mul(x, 0.5)
        return x


pname = list(model_circuit.paras_set)
measurement = mq.Hamiltonian(QubitOperator('Z0'), n)
mql = mq.nn.mindquantumlayer(s, measurement, pname,
                             np.random.random(len(pname)) * 2 * np.pi - np.pi)


model = torch.nn.Sequential(hl, Shift(1, 0.5))
epochs = 1
optimizer = torch.optim.Adam(hl.parameters())
t_total = time.time()
for epoch in range(epochs):
    t0 = time.time()
    train(model, train_loader, optimizer, epoch)
    t1 = time.time() - t0
    print("time used: {}min, \t{}ms per sample".format(
        t1 / 60.0, t1 * 1000 / len(train_loader.dataset)))
    test(model, test_loader)
print('total time:{}'.format(time.time() - t_total))
