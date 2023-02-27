import os.path
from pathlib import Path
import urllib.request
import shutil
from yt_xarray.utilities.logging import ytxr_log

data_to_fetch = [{
    "url": "https://ds.iris.edu/files/products/emc/emc-files/DBRD-NATURE2020-depth.r0.1.nc",
    "name": "EMC-DBRD_NATURE2020",
    "fname": "DBRD-NATURE2020-depth.r0.1.nc"
},]


class DirectoryConfig:

    dirs_to_make = ("data", "figures")

    def __init__(self, base_dir: os.PathLike="."):
        self.base_dir = os.path.expanduser(base_dir)

    def _setup_dirs(self) -> None:
        for dirname in self.dirs_to_make:
            Path(os.path.join(self.base_dir, dirname)).mkdir(parents=True,
                                                             exist_ok=True)
    def _fetch_data(self) -> None:
        ytxr_log.info("Fetching all sample data")
        for ds_info in data_to_fetch:
            output_file = os.path.join(self.base_dir, "data", ds_info["fname"])
            if os.path.isfile(output_file):
                ytxr_log.info(f"    {output_file} already exists.")
                return

            url = ds_info["url"]
            ytxr_log.info(f"    fetching {url} ...")

            with urllib.request.urlopen(url) as response:
                with open(output_file, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)

            ytxr_log.info(f"        saved as {output_file}\n")
        ytxr_log.info("Finished fetching data.")

    def initialize(self) -> None:
        self._setup_dirs()
        self._fetch_data()


def initialize(base_dir: os.PathLike="."):
    ytxr_log.info("Initializing directories for scipy2023 demo")
    config = DirectoryConfig(base_dir=base_dir)
    config.initialize()
