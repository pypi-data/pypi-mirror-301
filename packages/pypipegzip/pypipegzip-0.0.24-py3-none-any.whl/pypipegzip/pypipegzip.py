"""
This module enables working with gunzip to open gzip files

The reason for this module is the following benchmark:
- with python gzip decoded to text:
$ time ./flipkart_read_all_clickstream.py
real    4m23.271s
user    55m55.884s
sys     1m28.552s
- with pipe from zcat:
$ time ./flipkart_read_all_clickstream.py
real    3m13.042s
user    32m49.568s
sys     4m0.020s
- with pipe from zcat + decoding:
$ time ./flipkart_read_all_clickstream.py
real    3m19.863s
user    32m2.292s
sys     4m17.796s
"""
import gzip
import subprocess

from typing import Union

import io


def zipopen(filename: str, mode: str = "rb", use_process: bool = False, newline: Union[str, None] = None):
    if "r" in mode:
        if use_process:
            args = [
                "/bin/zcat",
                filename,
            ]
            with subprocess.Popen(args, stdout=subprocess.PIPE) as process:
                assert process.stdout is not None
                if "b" in mode:
                    return process.stdout
                if "t" in mode:
                    return io.TextIOWrapper(process.stdout, newline=newline)
            raise ValueError("please specify t or b in mode")
        return gzip.open(filename, mode=mode, newline=newline)
    if "w" in mode:
        return gzip.open(filename, mode=mode, newline=newline)
    raise ValueError("please specify r or w in mode")
