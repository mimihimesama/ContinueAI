from abc import ABC, abstractmethod


class Manager(ABC):
    def __init__(self):
        if type(self) is Manager:
            raise TypeError('Cannot instantiate abstract class')

    @abstractmethod
    def add(self, id, *args):
        raise NotImplementedError('Method not implemented.')

    @abstractmethod
    def remove(self, id, *args):
        raise NotImplementedError('Method not implemented.')

    @abstractmethod
    def clear_all(self):
        raise NotImplementedError('Method not implemented.')
