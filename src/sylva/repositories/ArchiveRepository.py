import subprocess
import re
import typing
import tempfile
import os

from sylva.MetaData import MetaData

CMD_QUERY_ARCHIVE = ["dsmc", "query", "archive"]
CMD_QUERY_ARCHIVE_BYES_FILE_PATTERN = r"^\s*([\d,]+)\s+.*\d\d:\d\d:\d\d\s+(.*)\s+\d\d\/\d\d\/\d\d\s*Archive Date.*"

CMD_ARCHIVE = ["dsmc", "archive"]
CMD_ARCHIVE_OUTPUT_SUCCESS_PATTERN = r"^Normal File-->.*\s(\/.+?) \[Sent\]$"
CMD_ARCHIVE_OUTPUT_RETRIEVE_PATTERN = r"^Retrieving.*\s(\/.+?) \[Done\]$"


class ArchiveRepository:

    def archive(self, files_to_archive: typing.List[str], print_log: bool) -> typing.List[str]:
        app = subprocess.Popen(["dsmc", "archive"] + files_to_archive, stdout=subprocess.PIPE, text=True, universal_newlines=True)
        files_success = []

        if print_log:
            print("\t |")

        for line in app.stdout:
            if print_log:
                print("\t | " + line.replace("\n", ""))
            match = re.match(CMD_ARCHIVE_OUTPUT_SUCCESS_PATTERN, line)
            if match:
                filename = match.group(1)
                if filename in files_to_archive:
                    files_success.append(filename)

        if print_log:
            print("\t |")

        return files_success

    def retrieve(self, files_to_retrieve: typing.List[str], print_log: bool) -> typing.List[str]:
        with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
            temp_file.write("\n".join([f'"{file}"' for file in files_to_retrieve]))

            app = subprocess.Popen(["dsmc", "retrieve", "-filelist=" + temp_file.name], stdout=subprocess.PIPE, text=True, universal_newlines=True)
            files_success = []

            if print_log:
                print("\t |")
                for line in app.stdout:
                    print("\t | " + line.replace("\n", ""))
                print("\t |")

            for file in files_to_retrieve:
                if os.path.isfile(file):
                    files_success.append(file)

        return files_success

    def has_in_archive(self, meta: MetaData):
        app = subprocess.Popen(CMD_QUERY_ARCHIVE + [meta.get_full_file_with_path()], stdout=subprocess.PIPE, text=True, universal_newlines=True)
        file_found = False

        for line in app.stdout:
            match = re.match(CMD_QUERY_ARCHIVE_BYES_FILE_PATTERN, line)
            if match:
                archive_bytes = match.group(1).replace(",", "")
                archive_file = match.group(2)

                if meta.get_full_file_with_path() == archive_file and meta.get_file_size() == int(archive_bytes):
                    file_found = True
                    break

        return file_found
