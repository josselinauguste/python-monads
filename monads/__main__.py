from monads.domain import Book, Dialer


def read_name() -> str:
    return input("who you gonna call? ")


if __name__ == "__main__":
    print("We want monads")

    name = read_name()
    if name:
        first_name = name.split()[0]
        first_name = first_name.upper()
        print(f"Dialing {first_name}...")

        contact = Book.find(first_name)
        response = Dialer.dial(contact)
        if response:
            print("Call OK.")
