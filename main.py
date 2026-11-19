# A make.fun news-image entry (Python 3.13, standard library only): its image
# is the entry.png beside this file, drawn by draw.py from the world news of
# Wednesday 18 November 2026, and the program copies it to /output/entry.png.
# The gate takes a whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
import os
import shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
