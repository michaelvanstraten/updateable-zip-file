# UpdateableZipFile

`UpdateableZipFile` is a simple python package base on a stack [overflow answer](https://stackoverflow.com/a/35435548).

It implements a single class, `UpdateableZipFile`, that builds on top of the standart library `ZipFile`,
which allows user to update files inside a zip archive with ease.

## Example

```python
from updateablezipfile import UpdateableZipFile

with UpdateableZipFile("C:\Temp\Test2.docx", "a") as o:
    # Overwrite a file with a string
    o.writestr("word/document.xml", "Some data")
    # exclude an exiting file from the zip
    o.remove_file("word/fontTable.xml")
    # Write a new file (with no conflict) to the zp
    o.writestr("new_file", "more data")
    # Overwrite a file with a file
    o.write(r"C:\Temp\example.png", "word/settings.xml")
```

## Attribution

The implementation is was in no way or form written by me,
it is thanks to [Or Weis](https://stackoverflow.com/users/2899910/or-weis) answer on stack overflow.

As of my knowledge this is code is under the `Creative Commons` license,
based on the terms and conditions of stack overflow.

If you are the original author of the underlying implementation
please contact me and i will transfer the package over to you.
