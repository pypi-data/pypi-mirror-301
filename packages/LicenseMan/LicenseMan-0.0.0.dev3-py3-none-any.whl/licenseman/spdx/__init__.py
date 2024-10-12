from pathlib import Path as _Path
import json as _json
import platformdirs as _platdir
import pylinks as _pl
from pylinks.exception.api import WebAPIError as _WebAPIError

from licenseman.spdx.license_db import SPDXLicenseDB
from licenseman.spdx.license_list import SPDXLicenseList
from licenseman.spdx.license import SPDXLicense
from licenseman import logger


URL_TEMPLATE_LICENSE_XML = "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/license-list-XML/{}.xml"
URL_TEMPLATE_LICENSE_JSON = "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/details/{}.json"
URL_LICENSE_LIST = "https://spdx.org/licenses/licenses.json"


def license_db(
    path: str | _Path | None = _platdir.site_cache_path(
        appauthor="RepoDynamics",
        appname="LicenseMan",
    ) / "SPDX_DB",
    force_update: bool = False,
    verify: bool = True,
    in_memory: bool = False,
) -> SPDXLicenseDB:
    db_path = _Path(path)
    db_license_path = db_path / "licenses"
    license_list_ = _get_global_license_list()
    license_ids = license_list_.ids
    if force_update or not db_path.is_dir():
        missing_ids = license_ids
        intro = "Force update is enabled" if force_update else f"SPDX license database not found at {db_path}"
        logger.log(
            "info" if force_update else "notice",
            "SPDX License Database Load",
            f"{intro}; downloading all latest SPDX license data."
        )
    else:
        missing_ids = []
        for license_id in license_ids:
            if not (db_license_path / f"{license_id}.json").is_file():
                missing_ids.append(license_id)
        if not missing_ids:
            logger.success(
                "SPDX License Database Load",
                f"Loaded database from {db_path}; all {len(license_ids)} license files found."
            )
            return SPDXLicenseDB(
                license_list=license_list_,
                db_path=db_path,
                in_memory=in_memory,
                verify=verify,
            )
        num_missing = len(missing_ids)
        num_available = len(license_ids) - num_missing
        logger.log(
            "notice",
            "SPDX License Database Load",
            f"Loaded database from {db_path}; "
            f"found {num_missing} missing license files (available: {num_available})."
        )
    db_license_path.mkdir(parents=True, exist_ok=True)
    licenses = {}
    for missing_id in missing_ids:
        output_path = db_license_path / f"{missing_id}.json"
        license_data = license(missing_id, verify=False if in_memory else verify)
        with open(output_path, "w") as f:
            _json.dump(license_data.raw_data, f)
        logger.success(
            "SPDX License Database Update",
            f"Downloaded '{missing_id}' to 'file://{output_path}'.",
        )
        if in_memory:
            licenses[missing_id] = license_data
    return SPDXLicenseDB(
        license_list=license_list_,
        db_path=db_path,
        in_memory=in_memory,
        verify=verify,
        licenses=licenses,
    )


def license_list() -> SPDXLicenseList:
    """Get the latest version of the [SPDX license list](https://spdx.org/licenses/) from SPDX website."""
    data = _pl.http.request(URL_LICENSE_LIST, response_type="json")
    return SPDXLicenseList(data)


def license(license_id: str, verify: bool = True) -> SPDXLicense:
    """Get an SPDX license.

    Parameters
    ----------
    license_id
        SPDX license ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    data = license_json(license_id)
    data["xml"] = license_xml(license_id)
    license_list_ = _get_global_license_list()
    for list_entry_key, list_entry_val in license_list_[license_id].items():
        # 'detailsUrl', 'reference', 'referenceNumber' are not present in JSON data
        if list_entry_key not in data:
            data[list_entry_key] = list_entry_val
            logger.info(
                "SPDX JSON License Load",
                f"Added missing '{list_entry_key}' entry to '{license_id}' JSON data from license list."
            )
        elif data[list_entry_key] != list_entry_val:
            logger.warning(
                "SPDX JSON License Load",
                f"Mismatched '{list_entry_key}' entry in '{license_id}' JSON data.",
                "JSON content:",
                logger.pretty(data[list_entry_key]),
                "License list content:",
                logger.pretty(list_entry_val),
            )
    return SPDXLicense(data, verify=verify)


def license_xml(license_id: str) -> str:
    """Get an SPDX license definition in XML format from SPDX
    [license-list-data](https://github.com/spdx/license-list-data) repository.

    Parameters
    ----------
    license_id
        SPDX license ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    try:
        xml_str = _pl.http.request(
            URL_TEMPLATE_LICENSE_XML.format(license_id),
            response_type="str"
        )
    except _WebAPIError as e:
        raise Exception(f"Error downloading license XML for ID '{license_id}") from e
    return xml_str


def license_json(license_id: str) -> dict:
    """Get an SPDX license definition in XML format from SPDX
    [license-list-data](https://github.com/spdx/license-list-data) repository.

    Parameters
    ----------
    license_id
        SPDX license ID, e.g., 'MIT', 'GPL-2.0-or-later'.
    """
    try:
        json_data = _pl.http.request(
            URL_TEMPLATE_LICENSE_JSON.format(license_id),
            response_type="json"
        )
    except _WebAPIError as e:
        raise Exception(f"Error downloading license JSON for ID '{license_id}") from e
    return json_data


def _get_global_license_list() -> SPDXLicenseList:
    global _LICENSE_LIST
    if _LICENSE_LIST is None:
        _LICENSE_LIST = license_list()
    return _LICENSE_LIST


_LICENSE_LIST: SPDXLicenseList | None = None