from contextlib import contextmanager
import os

@contextmanager
def different_cwd(path: str):
    """
    :param path: Path that you want to change directory to
    """
    oldpwd=os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

path_to_data = r""
with different_cwd(path_to_data):
    # Everything inside this block will be in the new working directory
    # Once this block is exited, the working directory will be reset to the initial
    print(os.listdir())
