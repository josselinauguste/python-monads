"""
future monad adapted from https://www.toptal.com/javascript/option-maybe-either-future-monads-js
"""
import threading
from functools import reduce

from monads.maybe import Just, Nothing
from monads.either import Either, Right, Left


class Future:
    # __init__ :: ((Either err a -> void) -> void) -> Future (Either err a)
    def __init__(self, f):
        self.subscribers = []
        self.cache = Nothing()
        self.semaphore = threading.BoundedSemaphore(1)
        f(self.__callback)

    # pure :: a -> Future a
    @staticmethod
    def pure(value):
        return Future(lambda cb: cb(Either.pure(value)))

    @staticmethod
    def __exec(f, cb):
        try:
            data = f()
            cb(Right(data))
        except Exception as err:
            cb(Left(err))

    @staticmethod
    def __exec_on_thread(f, cb):
        t = threading.Thread(target=Future.__exec, args=[f, cb])
        t.start()

    @staticmethod
    def do_async(f):
        return Future(lambda cb: Future.__exec_on_thread(f, cb))

    # map :: (a -> b) -> Future b
    def map(self, f):
        return self.bind(lambda x: self.pure(f(x)))

    # bind :: (a -> Future b) -> Future b
    def bind(self, f):
        return Future(
            lambda cb: self.__subscribe(
                lambda value: cb(value)
                if (value is Left)
                else f(value.value).__subscribe(cb)
            )
        )

    # traverse :: [a] -> (a -> Future b) -> Future [b]
    @staticmethod
    def traverse(arr):
        return lambda f: reduce(
            lambda acc, elem: acc.bind(
                lambda values: f(elem).map(lambda value: values + [value])
            ),
            arr,
            Future.pure([]),
        )

    # callback :: Either err a -> void
    def __callback(self, value):
        self.semaphore.acquire()
        self.cache = Just(value)
        while len(self.subscribers) > 0:
            sub = self.subscribers.pop(0)
            t = threading.Thread(target=sub, args=[value])
            t.start()
        self.semaphore.release()

    # subscribe :: (Either err a -> void) -> void
    def __subscribe(self, subscriber):
        self.semaphore.acquire()
        if isinstance(self.cache, Just):
            self.semaphore.release()
            subscriber(self.cache.value)
        else:
            self.subscribers.append(subscriber)
            self.semaphore.release()
