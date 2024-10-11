from __future__ import annotations as annotations
from typing import TYPE_CHECKING as TYPE_CHECKING

from licenseman.spdx.license import SPDXLicense as _SPDXLicense

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Sequence
    from licenseman.spdx.license_list import SPDXLicenseList


class SPDXLicenseDB:

    def __init__(
        self,
        license_list: SPDXLicenseList,
        db_path: Path,
    ):
        self._license_list = license_list
        self._db_path = db_path
        self._licenses: dict[str, _SPDXLicense] = {}
        return

    def alts(self, license_ids: Sequence[str] | None = None):
        license_ids = license_ids or self._license_list.license_ids