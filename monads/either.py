from typing import TypeVar, Callable, Generic

TOK, TError, TR = TypeVar("TOK"), TypeVar("TError"), TypeVar("TR")

class Result(Generic[TOK, TError]):
    def __init__(self, value):
        self.value = value

    def map(self, f: Callable[[TOK], TR]) -> "Result[TR]":
        raise Exception("Not implemented")

    def map_error(self, f: Callable[[TError], TR]) -> "Result[TR]":
        raise Exception("Not implemented")

    def bind(self, f):
        raise Exception("Not implemented")

    @staticmethod
    def pure(value):
        return Ok(value)


class Ok(Result):
    def map(self, f: Callable[[TOK], TR]) -> "Result[TR]":
        return Ok(f(self.value))

    def map_error(self, f: Callable[[TError], TR]) -> "Result[TR]":
        return self

    def bind(self, f):
        return f(self.value)


class Error(Result):
    def map(self, f: Callable[[TOK], TR]) -> "Result[TR]":
        return self

    def map_error(self, f: Callable[[TError], TR]) -> "Result[TR]":
        return Error(f(self.value))

    def bind(self, f):
        return self
