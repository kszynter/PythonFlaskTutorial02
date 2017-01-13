from passlib.hash import sha256_crypt


def check_password_match(input_password, db_hash):
    return sha256_crypt.verify(input_password, db_hash)
