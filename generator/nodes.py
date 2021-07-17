import random
from abc import ABC, abstractmethod
import logging

from generator import nests
from generator.globals import GlobalVars, Result


def cls_stable_wrapper(cls):
    def stable_calculator(func):
        def new_calculate(self):
            try:
                return self.saved
            except AttributeError:
                self.saved = func(self)
            return self.saved

        return new_calculate

    cls.calculate = stable_calculator(cls.calculate)
    return cls


class BaseNode(ABC):
    @abstractmethod
    def calculate(self):
        pass


class BaseFunc(BaseNode):
    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def next_node(self):
        pass


class StopRuntime:
    pass


class BaseMacros(BaseNode):
    @abstractmethod
    def calculate(self):
        pass


class Sum(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = 0
        for i in self.inputs.values():
            res += i.calculate()
        self.outputs["result"].value = res
        return res

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 2:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class Subtract(BaseMacros):  # TODO: изменить название
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() - self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Multiply(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = 1
        for i in self.inputs.values():
            res *= i.calculate()
        self.outputs["result"].value = res
        return res

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 2:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class Divide(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() / self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Div(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() // self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Mod(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() % self.inputs["input2"].calculate()
        return self.outputs["result"].value


class BitAnd(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() & self.inputs["input2"].calculate()
        return self.outputs["result"].value


class BitOr(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() | self.inputs["input2"].calculate()
        return self.outputs["result"].value


class BitXor(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() ^ self.inputs["input2"].calculate()
        return self.outputs["result"].value


class ShiftLeft(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() << self.inputs["input2"].calculate()
        return self.outputs["result"].value


class ShiftRight(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() >> self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Negative(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = -self.inputs["input1"].calculate()
        return self.outputs["result"].value


class BitInversion(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = ~self.inputs["input1"].calculate()
        return self.outputs["result"].value


class Pow(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() ** self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Equal(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() == self.inputs["input2"].calculate()
        return self.outputs["result"].value


class NotEqual(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() != self.inputs["input2"].calculate()
        return self.outputs["result"].value


class LessOrEqual(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() <= self.inputs["input2"].calculate()
        return self.outputs["result"].value


class GreaterOrEqual(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() >= self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Less(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() < self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Greater(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() > self.inputs["input2"].calculate()
        return self.outputs["result"].value


class And(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() and self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Or(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() or self.inputs["input2"].calculate()
        return self.outputs["result"].value


class MatrixMultiply(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["input1"].calculate() @ self.inputs["input2"].calculate()
        return self.outputs["result"].value


class Str(BaseMacros):
    def __init__(self):
        self.inputs = {
            "object": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = str(self.inputs["object"].calculate())
        return self.outputs["result"].value


class Int(BaseMacros):
    def __init__(self):
        self.inputs = {
            "x": nests.InputNest(),
            "base": nests.InputNest()
        }

        self.inputs["base"].connect(10)

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        x = self.inputs["x"].calculate()
        if isinstance(x, str):
            self.outputs["result"].value = int(x, self.inputs["base"].calculate())
        else:
            self.outputs["result"].value = int(x)
        return self.outputs["result"].value


class Float(BaseMacros):
    def __init__(self):
        self.inputs = {
            "x": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = float(self.inputs["x"].calculate())
        return self.outputs["result"].value


class List(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 2

    def calculate(self):
        res = []
        for i in self.inputs.values():
            res.append(i.calculate())
        self.outputs["result"].value = list(*res)
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 0:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class Tuple(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = []
        for i in self.inputs.values():
            res.append(i.calculate())
        self.outputs["result"].value = tuple(res)
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 0:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class Set(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = set()
        for i in self.inputs.values():
            res.add(i.calculate())
        self.outputs["result"].value = res
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 0:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class FrozenSet(BaseMacros):
    def __init__(self):
        self.inputs = {
            "input1": nests.InputNest(),
            "input2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = set()
        for i in self.inputs.values():
            res.add(i.calculate())
        self.outputs["result"].value = frozenset(res)
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 0:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class Dict(BaseMacros):
    def __init__(self):
        self.inputs = {
            "key1": nests.InputNest(),
            "value1": nests.InputNest(),
            "key2": nests.InputNest(),
            "value2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = {}
        for i in self.inputs:
            if 'value' in i:
                res[self.inputs[f"key{i[5:]}"].calculate()] = self.inputs[i].calculate()
        self.outputs["result"].value = res
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'key{self.c}'] = nests.InputNest()
        self.inputs[f'value{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 0:
            del self.inputs[f"key{self.c - 1}"]
            del self.inputs[f"value{self.c - 1}"]
            self.c -= 1


class StrSplit(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "sep": nests.InputNest()
        }
        self.inputs['sep'].connect(None)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().split(self.inputs["sep"].calculate())
        return self.outputs["result"].value


class StrRSplit(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "sep": nests.InputNest()
        }
        self.inputs['sep'].connect(None)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().rsplit(self.inputs["sep"].calculate())
        return self.outputs["result"].value


class Join(BaseMacros):
    def __init__(self):
        self.inputs = {
            "iter": nests.InputNest(),
            "sep": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["sep"].calculate().join(self.inputs["iter"].calculate())
        return self.outputs["result"].value


class StrLower(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().lower()
        return self.outputs["result"].value


class StrUpper(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().upper()
        return self.outputs["result"].value


class StrCapitalize(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().capitalize()
        return self.outputs["result"].value


class StrTitle(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().title()
        return self.outputs["result"].value


class StrCaseFold(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().casefold()
        return self.outputs["result"].value


class StrCenter(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "width": nests.InputNest(),
            "fillchar": nests.InputNest()
        }
        self.inputs['fillchar'].connect(' ')
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().center(self.inputs['width'].calculate(),
                                                                                self.inputs['fillchar'].calculate())
        return self.outputs["result"].value


class Count(BaseMacros):
    def __init__(self):
        self.inputs = {
            "container": nests.InputNest(),
            "object": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().count(self.inputs["object"].calculate())
        return self.outputs["result"].value


class StrEndswith(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "suffix": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().endswith(self.inputs["suffix"].calculate())
        return self.outputs["result"].value


class StrStartswith(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "prefix": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().startswith(self.inputs["prefix"].calculate())
        return self.outputs["result"].value


class StrExpandTabs(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "tabsize": nests.InputNest()
        }
        self.inputs["tabsize"].connect(8)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().expandtabs(self.inputs["tabsize"].calculate())
        return self.outputs["result"].value


class StrFind(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "sub": nests.InputNest(),
            "start": nests.InputNest(),
            "end": nests.InputNest()
        }
        self.inputs["start"].connect(None)
        self.outputs["end"].connect(None)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().find(self.inputs["sub"].calculate(),
                                                                              self.inputs["start"].calculate(),
                                                                              self.inputs["end"].calculate())
        return self.outputs["result"].value


class StrRFind(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "sub": nests.InputNest(),
            "start": nests.InputNest(),
            "end": nests.InputNest()
        }
        self.inputs["start"].connect(None)
        self.outputs["end"].connect(None)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().rfind(self.inputs["sub"].calculate(),
                                                                               self.inputs["start"].calculate(),
                                                                               self.inputs["end"].calculate())
        return self.outputs["result"].value


class StrIsalnum(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isalnum()
        return self.outputs["result"].value


class StrIsalpha(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isalpha()
        return self.outputs["result"].value


class StrIsascii(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isascii()
        return self.outputs["result"].value


class StrIsdecimal(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isdecimal()
        return self.outputs["result"].value


class StrIsdigit(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isdigit()
        return self.outputs["result"].value


class StrIsIdentifier(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isidentifier()
        return self.outputs["result"].value


class StrIslower(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().islower()
        return self.outputs["result"].value


class StrIsnumeric(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isdigit()
        return self.outputs["result"].value


class StrIsPrintable(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isdigit()
        return self.outputs["result"].value


class StrIsSpace(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isspace()
        return self.outputs["result"].value


class StrIsTitle(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().istitle()
        return self.outputs["result"].value


class StrIsupper(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().isupper()
        return self.outputs["result"].value


class StrLJust(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "width": nests.InputNest(),
            "fillchar": nests.InputNest()
        }
        self.inputs['fillchar'].connect(' ')
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().ljust(self.inputs['width'].calculate(),
                                                                               self.inputs['fillchar'].calculate())
        return self.outputs["result"].value


class StrZFill(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "width": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().zfill(self.inputs['width'].calculate())
        return self.outputs["result"].value


class StrRJust(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "width": nests.InputNest(),
            "fillchar": nests.InputNest()
        }
        self.inputs['fillchar'].connect(' ')
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().rjust(self.inputs['width'].calculate(),
                                                                               self.inputs['fillchar'].calculate())
        return self.outputs["result"].value


class StrLStrip(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "chars": nests.InputNest()
        }
        self.inputs["chars"].connect(None)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().lstrip(self.inputs["chars"].calculate())
        return self.outputs["result"].value


class StrRStrip(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "chars": nests.InputNest()
        }
        self.inputs["chars"].connect(None)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().rstrip(self.inputs["chars"].calculate())
        return self.outputs["result"].value


class StrStrip(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "chars": nests.InputNest()
        }
        self.inputs["chars"].connect(None)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().strip(self.inputs["chars"].calculate())
        return self.outputs["result"].value


class StrPartition(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "sep": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().partition(self.inputs["sep"].calculate())
        return self.outputs["result"].value


class StrRPartition(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "sep": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().rpartition(self.inputs["sep"].calculate())
        return self.outputs["result"].value


class StrSplitLines(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
            "keepends": nests.InputNest()
        }
        self.inputs['keepends'].connect(False)
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().splitlines(self.inputs["keepends"].calculate())
        return self.outputs["result"].value


class StrSwapCase(BaseMacros):
    def __init__(self):
        self.inputs = {
            "string": nests.InputNest(),
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["string"].calculate().swapcase()
        return self.outputs["result"].value


class ListAppend(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
            "new_el": nests.InputNest()
        }

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        res.append(self.inputs["new_el"].calculate())
        self.outputs["result_list"].value = res
        return self.outputs["result_list"].value


class ListInsert(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
            "index": nests.InputNest(),
            "new_el": nests.InputNest()
        }

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        res.insert(self.inputs["index"].calculate(), self.inputs["new_el"].calculate())
        self.outputs["result_list"].value = res
        return self.outputs["result_list"].value


class Clear(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
        }

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        res.clear()
        self.outputs["result"].value = res
        return self.outputs["result"].value


class ListExtend(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
            "other": nests.InputNest()
        }

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        res.extend(self.inputs["other"].calculate())
        self.outputs["result"].value = res
        return self.outputs["result_list"].value


class Index(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
            "el": nests.InputNest(),
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        try:
            self.outputs["result"].value = self.inputs["list"].calculate().index(self.inputs['el'].calculate())
        except ValueError:
            self.outputs["result"].value = -1
        return self.outputs["result"].value


class ListRemove(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
            "new_el": nests.InputNest()
        }

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        try:
            res.remove(self.inputs["new_el"].calculate())
        except ValueError as ex:
            # logging.warning(f"{ex.args[0]}")
            pass
        self.outputs["result_list"].value = res
        return self.outputs["result_list"].value


class ListPop(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
            "index": nests.InputNest()
        }

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        try:
            res.pop(self.inputs["index"].calculate())
        except ValueError as ex:
            # logging.warning(f"{ex.args[0]}")
            pass
        self.outputs["result"].value = res
        return self.outputs["result_list"].value


class ListReverse(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
        }

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        res.reverse()
        self.outputs["result_list"].value = res
        return self.outputs["result_list"].value


class ListSort(BaseMacros):
    def __init__(self):
        self.inputs = {
            "list": nests.InputNest(),
            "reverse": nests.InputNest()
        }
        self.inputs["reverse"].connect(False)

        self.outputs = {
            "result_list": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["list"].calculate()
        res.sort()
        if self.inputs["reverse"].calculate():
            res.reverse()
        self.outputs["result_list"].value = res
        return self.outputs["result_list"].value


class SetAdd(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set": nests.InputNest(),
            "new_el": nests.InputNest()
        }

        self.outputs = {
            "result_set": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["set"].calculate()
        res.add(self.inputs["new_el"].calculate())
        self.outputs["result_set"].value = res
        return self.outputs["result_set"].value


class SetDifferenceMacro(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set1": nests.InputNest(),
            "set2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = []
        for i in list(self.inputs.values())[1:]:
            res.append(i.calculate())
        self.outputs["result"].value = self.inputs['set1'].calculate().difference(*res)
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 2:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class SetSymmetricDifferenceMacro(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set1": nests.InputNest(),
            "set2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = []
        for i in list(self.inputs.values())[1:]:
            res.append(i.calculate())
        self.outputs["result"].value = self.inputs['set1'].calculate().symmetric_difference(*res)
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 2:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class SetUnionMacro(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set1": nests.InputNest(),
            "set2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = []
        for i in list(self.inputs.values())[1:]:
            res.append(i.calculate())
        self.outputs["result"].value = self.inputs['set1'].calculate().union(*res)
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 2:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class SetDiscard(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set": nests.InputNest(),
            "el": nests.InputNest()
        }

        self.outputs = {
            "result_set": nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs["set"].calculate()
        res.discard(self.inputs["el"].calculate())
        self.outputs["result_set"].value = res
        return self.outputs["result_set"].value


class SetIntersectionMacro(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set1": nests.InputNest(),
            "set2": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }
        self.c = 3

    def calculate(self):
        res = []
        for i in list(self.inputs.values())[1:]:
            res.append(i.calculate())
        self.outputs["result"].value = self.inputs['set1'].calculate().intersection(*res)
        return self.outputs["result"].value

    def add_input(self):
        self.inputs[f'input{self.c}'] = nests.InputNest()
        self.c += 1

    def remove_input(self):
        if self.c > 2:
            del self.inputs[f"input{self.c - 1}"]
            self.c -= 1


class SetIsDisjoint(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set1": nests.InputNest(),
            "set2": nests.InputNest()
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["set1"].calculate().isdisjoint(self.inputs["set2"].calculate())
        return self.outputs["result"].value


class SeIsSubset(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set1": nests.InputNest(),
            "set2": nests.InputNest()
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["set1"].calculate().issubset(self.inputs["set2"].calculate())
        return self.outputs["result"].value


class SetIsSuperset(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set1": nests.InputNest(),
            "set2": nests.InputNest()
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["set1"].calculate().issuperset(self.inputs["set2"].calculate())
        return self.outputs["result"].value


class SetPop(BaseMacros):
    def __init__(self):
        self.inputs = {
            "set": nests.InputNest(),
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["set"].calculate().pop()
        return self.outputs["result"].value


class GetItem(BaseMacros):
    def __init__(self):
        self.inputs = {
            "sequence": nests.InputNest(),
            "index": nests.InputNest()
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = self.inputs["sequence"].calculate()[self.inputs["index"].calculate()]
        return self.outputs["result"].value


class GetVar(BaseMacros):
    def __init__(self):
        self.inputs = {
            "var_name": nests.InputNest(),
        }

        self.outputs = {
            "value": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["value"].value = GlobalVars()[self.inputs["var_name"].calculate()]
        return self.outputs["result"].value


class GenerateInt(BaseMacros):
    def __init__(self):
        self.inputs = {
            "start": nests.InputNest(),
            "end": nests.InputNest()
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = random.randint(self.inputs["start"].calculate(), self.inputs["end"].calculate())
        return self.outputs["result"].value


@cls_stable_wrapper
class GenerateStableInt(GenerateInt):
    pass


class GenerateString(BaseMacros):
    def __init__(self):
        self.inputs = {
            "allowed": nests.InputNest(),
            "length": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        res = ''
        allowed = self.inputs["allowed"].calculate()
        for i in range(self.inputs["length"].calculate()):
            res += random.choice(allowed)
        self.outputs["result"].value = res
        return self.outputs["result"].value


@cls_stable_wrapper
class GenerateStableString(GenerateString):
    pass


class GenerateFloat(BaseMacros):
    def __init__(self):
        self.inputs = {
            "min": nests.InputNest(),
            "max": nests.InputNest()
        }

        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        min_ = self.inputs["min"].calculate()
        max_ = self.inputs["max"].calculate()
        self.outputs["result"].value = random.random() * (max_ - min_) + min_
        return self.outputs["result"].value


@cls_stable_wrapper
class GenerateStableFloat(GenerateFloat):
    pass


class GenerateList(BaseMacros):
    def __init__(self):
        self.inputs = {
            "allowed": nests.InputNest(),
            "length": nests.InputNest()
        }
        self.outputs = {
            "result": nests.OutputNest(self)
        }

    def calculate(self):
        res = []
        allowed = self.inputs["allowed"].calculate()
        for i in range(self.inputs["length"].calculate()):
            res.append(random.choice(allowed))
        self.outputs["result"].value = res
        return self.outputs["result"].value


@cls_stable_wrapper
class GenerateStableList(GenerateList):
    pass


class Range(BaseMacros):
    def __init__(self):
        self.inputs = {
            "start": nests.InputNest(),
            "end": nests.InputNest(),
            "step": nests.InputNest()
        }
        self.inputs["start"].connect(0)
        self.inputs["end"].connect(0)
        self.inputs["step"].connect(1)

        self.outputs = {
            "range": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["range"].value = range(
            self.inputs["start"].calculate(),
            self.inputs["end"].calculate(),
            self.inputs["step"].calculate()
        )
        return self.outputs["range"].value


class Len(BaseMacros):
    def __init__(self):
        self.inputs = {
            'obj': nests.InputNest()
        }
        self.outputs = {
            'result': nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["result"].value = len(self.inputs['obj'].calculate())
        return self.outputs["result"].value


class Shuffle(BaseMacros):
    def __init__(self):
        self.inputs = {
            'obj': nests.InputNest()
        }
        self.outputs = {
            'result': nests.OutputNest(self)
        }

    def calculate(self):
        res = self.inputs['obj'].calculate()
        random.shuffle(res)
        self.outputs["result"].value = res
        return res
# ############################################################################################################# fggdgdf

class Start(BaseFunc):
    def __init__(self):
        self.outputs = {
            "order_output": nests.OrderOutputNest(self)
        }

    def calculate(self):
        pass

    def next_node(self):
        return self.outputs["order_output"].out.node


class End(BaseFunc):
    def __init__(self):
        self.inputs = {
            "order_input": nests.OrderInputNest(self)
        }

    def calculate(self):
        pass

    def next_node(self):
        return StopRuntime()


class SetVar(BaseFunc):
    def __init__(self):
        self.inputs = {
            "order_input": nests.OrderInputNest(self),
            "var_name": nests.InputNest(),
            "new_val": nests.InputNest()
        }
        self.outputs = {
            "order_output": nests.OrderOutputNest(self),
            "new_val": nests.OutputNest(self)
        }

    def calculate(self):
        self.outputs["new_val"].value = (x := self.inputs["new_val"].calculate())
        GlobalVars()["var_name"] = x

    def next_node(self):
        return self.outputs["order_output"].out.node


class For(BaseFunc):
    def __init__(self):
        self.inputs = {
            "order_input": nests.OrderInputNest(self),
            "iterable": nests.InputNest()
        }
        self.outputs = {
            "loop": nests.OrderOutputNest(self),
            "ended": nests.OrderOutputNest(self),
            "index": nests.OutputNest(self),
            "value": nests.OutputNest(self)
        }
        self.iterator = enumerate(self.inputs["iterable"].calculate())
        self.is_loop = False

    def calculate(self):
        try:
            i, val = next(self.iterator)
            self.outputs["index"].value = i
            self.outputs["value"].value = val
            self.is_loop = True
        except StopIteration:
            self.outputs["index"].value = None
            self.outputs["value"].value = None
            self.is_loop = False

    def next_node(self):
        if self.is_loop:
            return self.outputs["loop"].out.node
        return self.outputs["ended"].out.node


class If(BaseFunc):
    def __init__(self):
        self.inputs = {
                          "order_input": nests.OrderInputNest(self),
                          "condition": nests.InputNest()
                      },
        self.outputs = {
            "true": nests.OrderOutputNest(self),
            "false": nests.OrderOutputNest(self)
        }

    def calculate(self):
        pass

    def next_node(self):
        if self.inputs["condition"].calculate():
            return self.outputs["true"].out.node
        return self.outputs["false"].out.node


class Add(BaseFunc):
    def __init__(self):
        self.inputs = {
            "order_input": nests.OrderInputNest(self),
            "val": nests.InputNest()
        }
        self.outputs = {
            "order_output": nests.OrderOutputNest(self),
        }

    def calculate(self):
        res = self.inputs["val"].calculate()
        Result().add(res)
        return res

    def next_node(self):
        return self.outputs["order_output"].out.node


class AddEnter(Add):
    def __init__(self):
        self.inputs = {
            "order_input": nests.OrderInputNest(self),
        }
        self.outputs = {
            "order_output": nests.OrderOutputNest(self),
        }

    def calculate(self):
        res = '\n'
        Result().add(res)
        return res

    def next_node(self):
        return self.outputs["order_output"].out.node

