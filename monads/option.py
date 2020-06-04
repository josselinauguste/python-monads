from typing import Callable, TypeVar, Generic

T, TR = TypeVar("T"), TypeVar("TR")


class Option(Generic[T]):
    def map(self, f: Callable[[T], TR]) -> "Option[TR]":
        raise Exception("Not implemented")

    def bind(self, f):
        raise Exception("Not implemented")

    @staticmethod
    def pure(value):
        return Some(value)


class Some(Option):
    def __init__(self, value):
        self.value = value

    def map(self, f: Callable[[T], TR]) -> "Option[TR]":
        return Some(f(self.value))

    def bind(self, f):
        return f(self.value)


class Nothing(Option):
    def map(self, f: Callable[[T], TR]) -> "Option[TR]":
        return self

    def bind(self, f):
        return self
