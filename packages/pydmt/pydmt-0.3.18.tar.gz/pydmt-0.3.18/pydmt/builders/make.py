"""
This module runs make
"""


import os
from pydmt.utils.filesystem import mkdir_touch
from pydmt.utils.subprocess import check_call_ve

from pydmt.api.one_source_one_target import OneSourceOneTarget


class BuilderMake(OneSourceOneTarget):
    def build(self) -> None:
        args = [
            "make",
        ]
        if "GITHUB_WORKFLOW" in os.environ:
            # TODO: I'm assuming here that there is no previous MAKEFLAGS variable. Not good.
            # -j will cause make to set "number of parallel jobs = number of cores"
            os.environ["MAKEFLAGS"] = "-j"
        check_call_ve(args)
        mkdir_touch(self.target)
