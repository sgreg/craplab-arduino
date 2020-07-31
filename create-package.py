#!/usr/bin/env python3
#
# CrapLab Arduino Boards - Create Board Manager Data
# Copyright (C) 2020 Sven Gregori <sven@craplab.fi>
# Released under MIT license
#
# This shouldn't be of much use for anyone, but here we are.
# Creates the archive and JSON file to add support for the CrapLab
# Development Boards to the Arduino environment. This whole script
# mainly exists out of laziness to manually create the .tar.bz2
# file, add its size and hashsum etc to the JSON file every time
# when I was experimenting to put this together.
#
# Only a single version and platform is currently supported.
#
import os
import json
import hashlib
import tarfile


PACKAGE_NAME = "CrapLab Arduino"
PACKAGE_MAINTAINER = "CrapLab"
PACKAGE_WEBSITE = "https://craplab.fi/"
PACKAGE_EMAIL = "dev@craplab.fi"

PLATFORM_BASE = "craplab-arduino"
PLATFORM_VERSION = "1.0.0"
PLATFORM_EXTENSION = "tar.bz2"

PLATFORM_DIR = "{base:s}-{version:s}".format(
        base=PLATFORM_BASE,
        version=PLATFORM_VERSION)

PLATFORM_ARCHIVE = "{basedir:s}.{ext:s}".format(
        basedir=PLATFORM_DIR,
        ext=PLATFORM_EXTENSION)

PLATFORM_ROOT_URL = "https://raw.githubusercontent.com/sgreg/craplab-arduino/master"
PLATFORM_URL = "{root:s}/{package:s}".format(
        root=PLATFORM_ROOT_URL,
        package=PLATFORM_ARCHIVE)

OUTPUT_JSON = "package_craplab_index.json"

# create archive from current state of SRC_DIR/
print("Creating {}".format(PLATFORM_ARCHIVE))
with tarfile.open(PLATFORM_ARCHIVE, "w:bz2") as tar:
    print("  {} -> {}".format(PLATFORM_BASE, PLATFORM_DIR))
    tar.add(PLATFORM_BASE, PLATFORM_DIR)

print("Getting archive file information")
filesize = os.stat(PLATFORM_ARCHIVE).st_size
print("  {} bytes".format(filesize))

print("Hashing archive file")
with open(PLATFORM_ARCHIVE, "rb") as f:
    filehash = hashlib.sha256(f.read()).hexdigest()
print("  {}".format(filehash))

data = {
  "packages": [
    {
      "name": PACKAGE_NAME,
      "maintainer": PACKAGE_MAINTAINER,
      "websiteURL": PACKAGE_WEBSITE,
      "email": PACKAGE_EMAIL,

      "platforms": [
        {
          "name": "CrapLab Development Boards",
          "architecture": "avr",
          "version": PLATFORM_VERSION,
          "category": "Contributed",
          "url": PLATFORM_URL,
          "archiveFileName": PLATFORM_ARCHIVE,
          "checksum": "SHA-256:" + filehash,
          "size": str(filesize),
          "boards": [
            {"name": "RUDY"}
          ],
          "toolsDependencies": []
        }
      ],
      "tools": []
    }
  ]
}

with open(OUTPUT_JSON, "w") as f:
    f.write(json.dumps(data, indent=2))

print("")
print("All Done")

