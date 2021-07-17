class GlobalVars(dict):
    def __new__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.need_init = True
            return cls.__instance

    def __init__(self, *args, **kwargs):
        if self.need_init:
            super(GlobalVars, self).__init__(*args, **kwargs)
            self.need_init = False


class Result:
    def __new__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super().__new__(cls, *args, **kwargs)
            cls.__instance.need_init = True
            return cls.__instance

    def __init__(self):
        if self.need_init:
            self.need_init = False
            self.res = ''

    def add(self, val):
        sep = " " if self.res and self.res[-1] != "\n" else ""
        if isinstance(val, (list, tuple, set)):
            self.res += sep + ' '.join((str(x) for x in val))
        else:
            self.res += sep + str(val)

    def flush(self):
        self.res = ''
