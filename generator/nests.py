from abc import ABC, abstractmethod


class BaseNest(ABC):
    @abstractmethod
    def connect(self, src):
        pass

    @abstractmethod
    def disconnect(self, src=None):
        pass

    def __hash__(self):
        return hash(id(self))

    @abstractmethod
    def is_connected(self, src):
        pass


class OutputNest(BaseNest):
    def __init__(self, nod):
        self.node = nod
        self.outs = set()
        self.value = None

    def connect(self, src):
        if not self.is_connected(src):
            if not isinstance(src, InputNest):
                raise TypeError("Output Nest can only be connected with Input Nests")
            self.outs.add(src)
            src.connect(self)

    def disconnect(self, src=None):
        if not isinstance(src, InputNest):
            raise TypeError(f"Cannot disconnect nest with {type(src)}")
        self.outs.remove(src)
        src.disconnect(self)

    def is_connected(self, src):
        return src in self.outs

    def get_value(self):
        self.node.calculate()
        return self.value


class InputNest(BaseNest):
    def __init__(self):
        self.__input = None

    def connect(self, src):
        if not self.is_connected(src):
            if isinstance(src, OutputNest):
                src.connect(self)
            self.__input = src

    def disconnect(self, src=None):
        try:
            self.__input.disconnect(self)
        except AttributeError:
            pass
        self.__input = None

    def calculate(self):
        if isinstance(self.__input, OutputNest):
            return self.__input.get_value()
        else:
            return self.__input

    def is_connected(self, src):
        return self.__input == src


class OrderOutputNest(BaseNest):
    def __init__(self, nod):
        self.node = nod
        self.out = None

    def connect(self, src):
        if not self.is_connected(src):
            if not isinstance(src, OrderInputNest):
                raise TypeError("Order input nest can only be connected with Output order nest")
            self.out = src
            src.connect(self)

    def disconnect(self, src=None):
        if not isinstance(src, OrderInputNest):
            raise TypeError(f"Cannot disconnect nest with {type(src)}")
        src.disconnect(self)
        self.out = None

    def is_connected(self, src):
        return self.out == src


class OrderInputNest(BaseNest):
    def __init__(self, nod):
        self.node = nod
        self.__input = None

    def connect(self, src):
        if not self.is_connected(src):
            if not isinstance(src, OrderOutputNest):
                raise TypeError("Order input nest can only be connected with Output order nest")

            self.__input = self
            src.connect(self)

    def disconnect(self, src=None):
        self.__input.disconnect(self)
        self.__input = None

    def is_connected(self, src):
        return self.__input == src

