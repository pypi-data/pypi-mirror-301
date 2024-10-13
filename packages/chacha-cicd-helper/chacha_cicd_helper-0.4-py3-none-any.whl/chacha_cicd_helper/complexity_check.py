# chacha_cicd_helper (c) by chacha
#
# chacha_cicd_helper is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

"""module that handle code complexity measurement"""

from __future__ import annotations

import statistics
import csv
from json import loads as JSON_LOADS
from radon.complexity import SCORE  # type: ignore
from radon.cli import Config  # type: ignore
from radon.cli.harvest import CCHarvester, HCHarvester, MIHarvester  # type: ignore

from .helper_base import cl_helper_withresults_base


class cl_complexity_check(cl_helper_withresults_base):
    """complexity check implementation class"""

    @classmethod
    def do_job(cls) -> None:
        """helper job method implementation"""

        config = Config(
            exclude=r"__init__.py",  ##!!!!! . => \. ???
            ignore=None,
            order=SCORE,
            show_closures=False,
            no_assert=True,
            min="A",
            max="F",
            multi=False,
        )

        h = MIHarvester([str(_) for _ in sorted((cls.project_rootdir_path / "src").rglob("*.py"))], config).as_json()
        res = JSON_LOADS(h)

        with open(cls.get_result_dir() / "MI.json", "w", newline="", encoding="utf8") as oFile:
            oFile.write(h)

        mean = statistics.mean(_["mi"] for _ in res.values())

        if mean >= 65:
            rank = "A+"
        elif mean >= 20:
            rank = "A"
        elif mean >= 10:
            rank = "B"
        else:
            rank = "C"

        RES_MI = {"MeanMaintainability": mean, "MaintainabilityIndex": rank}
        with open(cls.get_result_dir() / "MI.csv", "w", newline="", encoding="utf8") as oFile:
            writer = csv.DictWriter(oFile, fieldnames=RES_MI.keys())
            writer.writeheader()
            writer.writerow(RES_MI)

        config = Config(exclude=None, ignore=None, order=SCORE, show_closures=False, no_assert=True, min="A", max="F", multi=False)
        h = CCHarvester([str(_) for _ in sorted((cls.project_rootdir_path / "src").rglob("*.py"))], config).as_json()
        with open(cls.get_result_dir() / "CC.json", "w", newline="", encoding="utf8") as oFile:
            oFile.write(h)

        config = Config(exclude=None, ignore=None, order=SCORE, show_closures=False, no_assert=True, min="A", max="F", by_function=None)
        h = HCHarvester([str(_) for _ in sorted((cls.project_rootdir_path / "src").rglob("*.py"))], config).as_json()
        with open(cls.get_result_dir() / "HC.json", "w", newline="", encoding="utf8") as oFile:
            oFile.write(h)
