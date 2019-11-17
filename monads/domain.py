class Book:
    BOOK = {
        "JOSSELIN": "0612345678"
    }

    @staticmethod
    def find(name: str) -> str:
        return Book.BOOK[name]


class Dialer:
    class Response:
        pass

    @staticmethod
    def dial(contact: str):
        if contact.startswith("06"):
            return Dialer.Response()
