import subprocess
import re

from sylva.MetaData import MetaData

CMD_QUERY_ARCHIVE = ["dsmc", "query", "archive"]
CMD_QUERY_ARCHIVE_BYES_FILE_PATTERN = r'^\s*([\d,]+)\s+.*\d\d:\d\d:\d\d\s+(.*)\s+\d\d\/\d\d\/\d\d\s*Archive Date.*'

class ArchiveRepository:

    def has_in_archive(self, meta: MetaData):
        app = subprocess.Popen(CMD_QUERY_ARCHIVE + [ meta.get_full_file_with_path() ], stdout=subprocess.PIPE, text=True, universal_newlines=True)
        file_found = False
        
        for line in app.stdout:
            match = re.match(CMD_QUERY_ARCHIVE_BYES_FILE_PATTERN, line)
            if match:
                archive_bytes = match.group(1).replace(",","")
                archive_file = match.group(2)

                if (meta.get_full_file_with_path() == archive_file and meta.get_file_size() == int(archive_bytes)):
                    file_found = True
                    break

        return file_found


