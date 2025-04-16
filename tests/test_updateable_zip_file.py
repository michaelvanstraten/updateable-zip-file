import os
import tempfile
from zipfile import ZipFile

from updateable_zip_file import UpdateableZipFile


def test_overwriting_deleted_file():
    tmp = tempfile.mktemp(suffix=".zip")

    with ZipFile(tmp, "w") as zip:
        with zip.open("text.txt", "w") as f:
            f.write(b"original content")

    with UpdateableZipFile(tmp, "a") as zip:
        zip.remove_file("text.txt")
        with zip.open("text.txt", "w") as f:
            f.write(b"updated content")

    with ZipFile(tmp, "r") as zip:
        with zip.open("text.txt") as f:
            assert f.read() == b"updated content"

    os.remove(tmp)


def test_add_new_file():
    tmp = tempfile.mktemp(suffix=".zip")

    with ZipFile(tmp, "w") as zip:
        pass

    with UpdateableZipFile(tmp, "a") as zip:
        with zip.open("new_file.txt", "w") as f:
            f.write(b"new file content")

    with ZipFile(tmp, "r") as zip:
        with zip.open("new_file.txt") as f:
            assert f.read() == b"new file content"

    os.remove(tmp)


def test_delete_existing_file():
    tmp = tempfile.mktemp(suffix=".zip")

    with ZipFile(tmp, "w") as zip:
        with zip.open("delete_me.txt", "w") as f:
            f.write(b"this will be deleted")

    with UpdateableZipFile(tmp, "a") as zip:
        zip.remove_file("delete_me.txt")

    with ZipFile(tmp, "r") as zip:
        assert "delete_me.txt" not in zip.namelist()

    os.remove(tmp)


def test_multiple_operations():
    tmp = tempfile.mktemp(suffix=".zip")

    with ZipFile(tmp, "w") as zip:
        zip.writestr("file1.txt", b"content1")
        zip.writestr("file2.txt", b"content2")

    with UpdateableZipFile(tmp, "a") as zip:
        zip.remove_file("file1.txt")
        with zip.open("file2.txt", "w") as f:
            f.write(b"updated content2")
        with zip.open("file3.txt", "w") as f:
            f.write(b"content3")

    with ZipFile(tmp, "r") as zip:
        assert "file1.txt" not in zip.namelist()
        assert zip.read("file2.txt") == b"updated content2"
        assert zip.read("file3.txt") == b"content3"

    os.remove(tmp)


def test_readding_deleted_file():
    tmp = tempfile.mktemp(suffix=".zip")

    with ZipFile(tmp, "w") as zip:
        zip.writestr("file.txt", b"initial content")

    with UpdateableZipFile(tmp, "a") as zip:
        zip.remove_file("file.txt")

    with UpdateableZipFile(tmp, "a") as zip:
        with zip.open("file.txt", "w") as f:
            f.write(b"new content after delete")

    with ZipFile(tmp, "r") as zip:
        assert zip.read("file.txt") == b"new content after delete"

    os.remove(tmp)


if __name__ == "__main__":
    test_overwriting_deleted_file()
    test_add_new_file()
    test_delete_existing_file()
    test_multiple_operations()
    test_readding_deleted_file()
    print("All tests passed!")
