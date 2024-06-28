"""Module providing function to hash and salt password"""

import bcrypt


def hash_password(password: str):
    """Function that hashes and salt the given password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(query_pw, ground_truth_pw):
    """Function that checks the query password with the ground truth password"""
    return bcrypt.checkpw(query_pw, ground_truth_pw)
