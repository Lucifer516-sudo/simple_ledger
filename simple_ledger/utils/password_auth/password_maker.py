from hashlib import sha256
import random


def encrypt(string: str | bytes) -> str:
    return sha256(bytes(string, "utf-8")).hexdigest()


def authenticate(password: str, password_hash: str) -> bool:
    if encrypt(password) == password_hash:
        return True
    else:
        return False


def generate_random_password(
    length: int = 16,
    symbols: list[str] = list("~`!@#$%^&*()_-+=\{\}:;'\"<>,.?/"),
    numbers: list[str] = list("1234567890"),
    lowercase_letters: list[str] = list("abcdefghijklmnopqrstuvwxyz"),
    uppercase_letters: list[str] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
) -> str:
    # shuffling the chars
    random.shuffle(symbols)
    random.shuffle(numbers)
    random.shuffle(lowercase_letters)
    random.shuffle(uppercase_letters)

    chars: list[str] = symbols + numbers + lowercase_letters + uppercase_letters
    return "".join(random.choices(chars, k=length))
