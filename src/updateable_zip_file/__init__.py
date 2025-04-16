import os
from tempfile import NamedTemporaryFile, mktemp
from zipfile import ZipFile, ZipInfo


class UpdateableZipFile(ZipFile):
    """
    Add delete (via remove_file) and update (via writestr and write methods)
    To enable update features use UpdateableZipFile with the 'with statement',
    Upon  __exit__ (if updates were applied) a new zip file will override the exiting one with the updates
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._replace = {}
        self._delete = set()
        self._allow_updates = False

    def open(self, name, mode="r", pwd=None, *, force_zip64=False):
        if replacement := self._replace.get(name, None):
            return replacement

        if mode == "w" and name in self.namelist():
            if not self._allow_updates:
                raise RuntimeError(
                    "Updates only allowed within a with-statement context"
                )

            temp_file = self._replace[name] = NamedTemporaryFile(delete=False)
            return temp_file

        return super(UpdateableZipFile, self).open(
            name, mode, pwd, force_zip64=force_zip64
        )

    def __enter__(self):
        # Allow updates
        self._allow_updates = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # call base to close zip file, organically
        try:
            if self._replace or self._delete:
                print(self._replace, self._delete)
                self._rebuild_zip()
            else:
                super().__exit__(exc_type, exc_val, exc_tb)
        finally:
            # In case rebuild zip failed,
            # be sure to still release all the temp files
            self._cleanup_temp_files()
            self._allow_updates = False

    def _cleanup_temp_files(self):
        for temp_file in self._replace.values():
            temp_file.close()
            os.unlink(temp_file.name)

    def remove_file(self, filename):
        self._delete.add(filename)

    def _rebuild_zip(self):
        file = mktemp(suffix=".zip")
        updated_zip = ZipFile(file, mode="w")

        for item in self.infolist():
            if isinstance(item, ZipInfo):
                filename = item.filename
            else:
                filename = item


            # If marked for replacement, copy temp_file, instead of old file
            if replacement := self._replace.get(filename, None):
                del self._replace[item.filename]
                with open(replacement.name) as f:
                    # Write replacement to archive,
                    # and then close it (deleting the temp file)
                    f.seek(0)
                    data = f.read()
                os.unlink(replacement.name)
            elif filename in self._delete:
                continue
            else:
                data = self.read(filename)
            updated_zip.writestr(item, data)

        os.rename(file, self.filename)
