

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

