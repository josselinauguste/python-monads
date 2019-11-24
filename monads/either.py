class Either:
    def __init__(self, value):
        self.value = value

    def map(self, f):
        raise Exception("Not implemented")

    def bind(self, f):
        raise Exception("Not implemented")

    @staticmethod
    def pure(value):
        return Right(value)


class Right(Either):
    def map(self, f):
        return Right(f(self.value))

    def bind(self, f):
        return f(self.value)


class Left(Either):
    def map(self, f):
        return self

    def bind(self, f):
        return self
