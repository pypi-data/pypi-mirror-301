import random
import secrets
import string as _string
from datetime import datetime
from typing import Optional
from warnings import warn
from .include import length_check

warn("DEPRICATED: As of version 2.0.0 SimpleUID has been renamed to Strig. It's advised to use the new package instead of this one. pip install strig")

digits = _string.digits ## 0123456789


def integer(length: int = 6, prefix: Optional[int] = None, ignore_max_length: bool = False):
    """
    Generate a random integer value
    
    * length: Length in characters to return
    * prefix: Integer value to prefix the return value with
    """

    length_check(length, ignore_max_length)

    if not isinstance(prefix, int):
        if not prefix == None:
            raise TypeError("Prefix should be of type int")

    generated = ""

    #### Create random integer
    c = length
    while not c == 0:
        cur_random_int = random.choice(digits)
        if (
            not int(cur_random_int) == 0
        ):  ## If an integer starts with 0 the 0 will be ignored
            generated += "".join(cur_random_int)
            c -= 1

    generated = int(generated)

    #### Add prefix
    if not prefix == None:
        generated = int(
            str(prefix) + str(generated)
        )  ## Workaround with int and str functions TODO clean up

    return generated


#### Return random string value
def string(
    length: int = 6,
    prefix: Optional[str] = None,
    ignore_max_length: bool = False,
    type: str = "all",
    uppercase_only=False,
    lowercase_only=False,
):
    """
    Generate a random string
    
    * length: Length in characters to return
    * prefix: String value to prefix the return value with
    """

    length_check(length, ignore_max_length)

    if not isinstance(prefix, str):
        if not prefix == None:
            raise TypeError("Prefix should be of type str")

    if uppercase_only and lowercase_only:
        raise ValueError(
            "A string can not be uppercase only and lowercase only at the same time"
        )

    if type == "number":
        generated = str(integer(length=length))
    else:
        alphabet = (
            _string.ascii_uppercase
            if uppercase_only
            else _string.ascii_lowercase if lowercase_only else _string.ascii_letters
        )

        choices = (
            alphabet + _string.digits
            if type == "all"
            else alphabet if type == "letter" else _string.digits
        )
        generated = "".join(secrets.choice(choices) for i in range(length))

    if not prefix == None:
        generated = prefix + generated

    return str(generated)


def password(length: int = 10, ignore_max_length: bool = False, symbols=True):
    """
    Generate a password
    By default includes letters, numbers and symbols
    
    * length: Length in characters to return
    * symbols: If symbols should be included
    """

    length_check(length, ignore_max_length)

    alphabet = _string.ascii_letters + digits
    if symbols:
        alphabet += "!!!@@@###...---___^^^&&&***"

    while True:
        password = "".join(secrets.choice(alphabet) for i in range(length))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break

    return password


def bytes(length: int = 32, ignore_max_length: bool = False):
    """
    Generate a random byte string
    
    * length: Length in bytes to return
    """
    length_check(length, ignore_max_length)

    return secrets.token_bytes(length)


#### Generate a random text string in hexadecimal (Basicly a wrapper for secrets.token_hex)
def hex(length: int = 32, ignore_max_length: bool = False):
    """
    Generate a random hexadecimal string
    
    * length: Length in bytes to return
    """
    length_check(length, ignore_max_length)

    return secrets.token_hex(length)


def urlsafe(*args, length: int = 32, ignore_max_length: bool = False):
    length_check(length, ignore_max_length)

    generated = secrets.token_urlsafe(length)

    if "padding" in args:
        generated += "="  ## Padding is useful when using for encryption

    if "encoded" in args:
        generated = generated.encode()

    return generated


def var(varstring: str, prefix: Optional[str] = None):
    """
    Generate a string based on variables
    """
    today = datetime.today()

    vars = {
        "yyyy": today.year,
        "yy": str(today.year)[-2:],
        "mm": today.month if len(str(today.month)) == 2 else "0" + str(today.month),
        "m": today.month,
        "dd": today.day if len(str(today.day)) == 2 else "0" + str(today.day),
        "d": today.day,
    }

    if varstring[0] == "%":
        varstring = varstring[1:]  ## Can't start with %
    generated = ""  ## Empty string to append data to

    for var in varstring.split("%"):
        generated += str(vars[var])

    if not prefix == None:
        generated = prefix + generated

    return generated


def database(cursor, *args, **kwargs):
    """
    Generate a random string and check a database if it already exists.
    If a match is found, it will retry until it's unique.
    """

    #### Default method is string
    if not "method" in kwargs:
        method = "string"
    else:
        method = kwargs["method"]
        del kwargs[
            "method"
        ]  ## Kwargs needs to be passed to generation functions, method is useless here

    #### Default type is sql
    if not "type" in cursor:
        cursor_type = "sql"
    else:
        cursor_type = cursor["type"]
        del cursor[
            "type"
        ]  ## Kwargs needs to be passed to generation functions, type is useless here

    if cursor_type == "sql":
        id_exists = True

        if method == "var":
            generated_id = var(*args, **kwargs)
            suffix = 1  ## Not ending in 0

            while id_exists:
                cursor["cursor"].execute(
                    f'SELECT "{ cursor["column"] }" FROM { cursor["table"] } WHERE { cursor["column"] } = "{ generated_id + str(suffix) }"'
                )
                if len(cursor["cursor"].fetchall()):
                    suffix += 1  ## If ID already exists add 1 to suffix
                else:
                    id_exists = False

            return generated_id + str(suffix)

        else:
            while id_exists:

                if method == "string":
                    generated_id = string(*args, **kwargs)
                if method == "integer":
                    generated_id = integer(*args, **kwargs)

                cursor["cursor"].execute(
                    f'SELECT "{ cursor["column"] }" FROM { cursor["table"] } WHERE { cursor["column"] } = "{ generated_id }"'
                )
                if not len(cursor["cursor"].fetchall()):
                    id_exists = False

            return generated_id

    elif cursor_type == "mongo":
        id_exists = True

        if method == "var":

            #### Generate the variable ID
            generated_id = var(*args, **kwargs)
            suffix = 1  ## Not ending in 0

            while id_exists:

                if cursor["cursor"].find_one({cursor["column"]: generated_id}):
                    suffix += 1  ## If ID already exists add 1 to suffix
                else:
                    id_exists = False

            return generated_id + str(suffix)

        else:
            while id_exists:
                if method == "string":
                    generated_id = string(*args, **kwargs)
                if method == "integer":
                    generated_id = integer(*args, **kwargs)

                if not cursor["cursor"].find_one({cursor["column"]: generated_id}):
                    id_exists = False

            return generated_id

    else:
        raise NameError(f"{ cursor_type.capitalize() } cursor is not supported!")
