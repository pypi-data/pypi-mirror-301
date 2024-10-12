from __future__ import annotations

import json
from pathlib import Path

from attrs import define, field
from cattrs.preconf.json import make_converter
from loguru import logger as log

from file_archiver import __version__


@define
class File:
    rel_path: Path = field(converter=Path)
    label: str = field(default="")
    comment: str = field(default="", converter=str)


@define
class ArchiveMetadata:
    description: str = field(default="")
    readme: str = field(default="")
    readme_file: Path = field(default=Path("README.md"), converter=Path)
    archiver_version: str = field(default="")

    def update_version(self) -> None:
        self.archiver_version = __version__


@define
class ArchiveContent:
    files: list[File] = field(factory=list)
    metadata: ArchiveMetadata = field(factory=ArchiveMetadata)


@define
class Archive:
    path: Path = field(converter=Path, default=Path("./"))
    content: ArchiveContent = field(factory=ArchiveContent, init=False)

    def __attrs_post_init__(self) -> None:
        log.debug("Running post init")
        self.load()

    @property
    def config_file(self) -> Path:
        self.ensure_root()
        return self.path / "content.json"

    def save(self) -> None:
        config_file = self.config_file

        self.content.metadata.update_version()
        converter = make_converter()
        data = converter.unstructure(self.content)

        with config_file.open("w") as f:
            json.dump(data, f, indent=2)

    def load(self) -> None:
        if self.config_file.exists():
            log.debug(f"Loading content of archive from {self.config_file}")
            converter = make_converter()
            with self.config_file.open() as f:
                data = json.load(f)
            self.content = converter.structure(data, ArchiveContent)
        else:
            log.debug("No config file found to load")

    def ensure_root(self) -> None:
        if not self.path.exists():
            log.debug(f"Output path {self.path} does not exists. Creating it.")
            self.path.mkdir(exist_ok=True, parents=True)

    def archive(
        self,
        file: str | Path,
        subpath: str | Path | None = None,
        comment: str = "",
        label: str = "",
    ) -> str:
        """Mark a filepath for future archival.

        subpath adds an additional path from the root of the archive and the file (which
        might contain multiple nodes in the archive tree)

        this is usedul e.g. to derive specialized partial functions of archive that land
        files in different places
        """

        self.ensure_root()

        if not subpath:
            relpath = Path(file)
        else:
            relpath = Path(subpath) / file

        fullpath = self.path.absolute() / relpath

        fullpath.parent.mkdir(exist_ok=True, parents=True)
        log.info(f"fullpath is {fullpath}")

        f = File(relpath, comment=comment, label=label)
        if f not in self.content.files:
            self.content.files.append(f)
        else:
            log.warning("Output files already exists! Yopu might be overwriting stuff!")

        self.save()
        return str(fullpath)

    def check_completeness(self) -> None:
        for file in self.content.files:
            full_path = self.path.absolute() / file.rel_path
            if not full_path.exists():
                msg = f"File {file.rel_path} does not exist in archive"
                raise FileExistsError(msg)

    def __call__(self, *args: tuple, **kwargs: dict) -> str:
        return self.archive(*args, **kwargs)

    def make_zip(self) -> None:
        import shutil

        shutil.make_archive(str(self.path), "zip", self.path)

    @property
    def readme_full_path(self) -> Path:
        return self.path / self.content.metadata.readme_file

    def write_readme(self, *, force: bool = True) -> None:
        self.ensure_root()

        if self.readme_full_path.exists() and not force:
            log.warning("Readme already exists! Not writing")
            return

        with open(self.readme_full_path, "w") as f:
            f.write(self.content.metadata.readme)

    @staticmethod
    def cur_date_string() -> str:
        from datetime import datetime, timezone

        # Get current date
        current_date = datetime.now(timezone.utc)

        # Format the date string with month abbreviation
        formatted_date = current_date.strftime("%d_%b_%Y").lower()
        return formatted_date
