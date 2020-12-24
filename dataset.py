import numpy as np


class CircuitDataset:
    def __init__(self, source, batch_size=None, shuffle=False):
        self.shuffle = shuffle
        self.column_names = list(source.keys())
        self.source = np.array([i for i in source.values()]).T
        if batch_size is None:
            self.batch_size = len(self.source)
        else:
            self.batch_size = batch_size
        self.shuffle_index = self.generate_shuffle_index()
        self.current_batch = -1

    def get_dataset_size(self):
        return len(self.source)

    def get_batch_size(self):
        return len(self.batch_size)

    def get_num_batches(self):
        return len(self.shuffle_index)

    def generate_shuffle_index(self):
        index = np.arange(len(self.source))
        if self.shuffle:
            index = np.random.permutation(index)
        indexs = []
        for i in range(len(self.source) // self.batch_size):
            indexs.append(index[i * self.batch_size:(i + 1) * self.batch_size])
        if len(self.source) % self.batch_size:
            indexs.append(index[(i + 1) * self.batch_size:])
        return indexs

    def __next__(self):
        if self.current_batch == len(self.shuffle_index) - 1:
            self.current_batch = -1
            raise StopIteration
        else:
            self.current_batch += 1
            return [
                self.source[self.shuffle_index[self.current_batch]][:, i]
                for i in range(len(self.column_names))
            ]

    def __iter__(self):
        return self