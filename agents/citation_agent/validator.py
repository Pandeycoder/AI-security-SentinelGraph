def validate_input(data: dict) -> bool:
    return bool(data)

def validate_output(response: str) -> bool:
    return bool(response and len(response) > 0)
