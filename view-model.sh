#!/bin/bash

export DYLD_FALLBACK_LIBRARY_PATH="$(.venv/bin/python -c 'import sys; print(sys.base_prefix)')/lib:/usr/local/lib:/usr/lib"

.venv/bin/mjpython mall_view.py "$1"
