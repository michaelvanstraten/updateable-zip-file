import os
import tempfile
from zipfile import ZipFile

from updateable_zip_file import UpdateableZipFile


def test_overwriting_deleted_file():
    tmp = tempfile.mktemp(suffix=".zip")

    with ZipFile(tmp, "w") as zip:
        with zip.open("text.txt", "w") as f:
            f.write(b"something")

    with UpdateableZipFile(tmp, "a") as zip:
        zip.remove_file("text.txt")
        with zip.open("text.txt", "w") as f:
            f.write(b"something else")

    os.remove(tmp)


if __name__ == "__main__":
    test_overwriting_deleted_file()
