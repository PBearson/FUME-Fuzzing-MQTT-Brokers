import globals as g
import os

def create_crash_directory():
    dir_exists = os.path.exists(g.CRASH_DIRECTORY)

    if not dir_exists:
        os.makedirs(g.CRASH_DIRECTORY)