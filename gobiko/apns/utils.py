
from textwrap import wrap

def validate_private_key(private_key):
    mode = "start"
    for line in private_key.split("\n"):
        if mode == "start":
            if "BEGIN PRIVATE KEY" in line:
                mode = "key"
        elif mode == "key":
            if "END PRIVATE KEY" in line:
                mode = "end"
                break
    if mode != "end":
        raise Exception("The auth key provided is not valid")


def wrap_private_key(private_key):
    # Wrap key to 64 lines
    comps = private_key.split("\n")
    wrapped_key = "\n".join(wrap(comps[1], 64))
    return "\n".join([comps[0], wrapped_key, comps[2]])


