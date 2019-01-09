from pathlib import Path


def exist_warrior(warrior):
    for p in Path("/tmp/").glob("ibs-*"):
        if str(p)[9:] == warrior:
            return True
    return False