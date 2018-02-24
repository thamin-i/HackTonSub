#!/usr/bin/env python3

import sys
import pyocr
from PIL import Image

tool = pyocr.get_available_tools()[0]
with Image.open(sys.argv[1]) as img:
    print(tool.image_to_string(img))
