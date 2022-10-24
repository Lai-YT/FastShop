import re
from datetime import datetime
from hashlib import sha512

from database.util import execute_command


def validate_by_regex(data: str, regex: str) -> bool:
    return bool(re.fullmatch(regex, data))


def validate_email(email: str) -> bool:
    return validate_by_regex(
        email,
        r"^[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*@[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*(\.[A-Za-z0-9_]{2,3})+$",
    )


def validate_birthday_format(birthday: str) -> bool:
    try:
        format_string = "%Y-%m-%d"
        datetime.strptime(birthday, format_string)
    except Exception:
        return False
    return True


def login(email: str, password: str) -> bool:

    m = sha512()
    m.update(password.encode("utf-8"))
    hash = m.hexdigest()
    user_count = execute_command(
        "SELECT COUNT(*) FROM `user` WHERE email=? and password=?", (email, hash)
    )[0]["COUNT(*)"]

    return user_count > 0


def register(email: str, password: str, profile: dict) -> bool:

    m = sha512()
    m.update(password.encode("utf-8"))
    hash = m.hexdigest()
    user_count = execute_command(
        "SELECT COUNT(*) FROM `user` WHERE email=? and password=?", (email, hash)
    )[0]["COUNT(*)"]

    if user_count > 0:
        return False

    execute_command(
        "INSERT INTO `user`(email, password, firstname, lastname, sex, birthday) VALUES(?, ?, ?, ?, ?, ?)",
        (
            email,
            hash,
            profile["firstname"],
            profile["lastname"],
            profile["sex"],
            profile["birthday"],
        ),
    )

    return True
