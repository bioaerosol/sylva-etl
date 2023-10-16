#!/usr/bin/env python3

import glob
import argparse
import uuid
import os
import shutil
from datetime import datetime

from sylva import Configuration, Folder
from sylva.devices import BAA500
from sylva.devices.Poleno import Poleno
from sylva.repositories import DevicesRepository, ArchiveRepository

configuration = Configuration()
device_repository = DevicesRepository()
archive_repository = ArchiveRepository(configuration)

parser = argparse.ArgumentParser(description='Walks trough the incoming directory and puts each file to SYLVA archive.')

parser.add_argument("--incomingDir", help="absolute path of directory where files can be found that need to be archived; default is '{0}'".format(configuration.get_folders()[Folder.INCOMING.value]), action="store", required=False, default=configuration.get_folders()[Folder.INCOMING.value])
parser.add_argument("--archiveDir", help="absolute path of directory where files should be archived; default is '{0}'".format(configuration.get_folders()[Folder.ARCHIVE.value]), action="store", required=False, default=configuration.get_folders()[Folder.ARCHIVE.value])

args = parser.parse_args()

process_id = str(uuid.uuid4())
print("{0} - {1} - START - Process started.".format(datetime.now().isoformat(), process_id))

for filename in glob.iglob(args.incomingDir + '/**/*.zip', recursive=True):
     meta = BAA500(filename, device_repository).get_data_file_meta_data() or Poleno(filename, device_repository).get_data_file_meta_data()

     trash_target_path = os.path.join(configuration.get_folders()[Folder.TRASH.value], process_id)
     trash_target_file = os.path.join(trash_target_path, str(uuid.uuid4()) + "-" + os.path.basename(filename))

     if meta is not None:
          archive_target_path = archive_repository.get_archive_path(meta)
          archive_target_file = os.path.join(archive_target_path, os.path.basename(filename))

          meta.set_archive_path(archive_target_path)
          
          if (archive_repository.has(meta) == False):
               # new file to be archived
               archive_repository.add(meta)
               os.makedirs(archive_target_path, exist_ok=True)
               shutil.move(filename, archive_target_file)
               print("{0} - {1} - OK - File {2} archived to {3}.".format(datetime.now().isoformat(), process_id, filename, archive_target_file))

          else:
               # file already archived -> move to trash
               os.makedirs(trash_target_path, exist_ok=True)
               shutil.move(filename, trash_target_file)     
               print("{0} - {1} - WARN - File already exists in archive. Moved file {2} to trash at {3}.".format(datetime.now().isoformat(), process_id, filename, trash_target_file))

     else:
          # invalid file or unknown device -> move to trash
          os.makedirs(trash_target_path, exist_ok=True)
          shutil.move(filename, trash_target_file)
          print("{0} - {1} - WARN - No device implementation found. Moved file {2} to trash at {3}.".format(datetime.now().isoformat(), process_id, filename, trash_target_file))
     
print("{0} - {1} - END - Process ended.".format(datetime.now().isoformat(), process_id))