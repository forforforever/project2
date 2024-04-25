import hashlib


def hash_code64(pid: str, object_name: str, file_path: str):
    """
    Generate 64-strings(in hashlib.sha256()) hash code.
    :return: 64-strings long hash code.
    """
    text = pid+object_name+file_path
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == '__main__':
    print(hash_code64('whosbug_0001', 'main', 'src/package1/main.py'))
