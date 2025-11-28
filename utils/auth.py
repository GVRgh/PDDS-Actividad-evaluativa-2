VALID_TOKEN = "abcd12345"

def validate_token(token: str) -> bool:
    if token is None:
        return False
    token = token.strip()
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    return token == VALID_TOKEN

