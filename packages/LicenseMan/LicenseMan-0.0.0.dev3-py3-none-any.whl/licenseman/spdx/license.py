from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import datetime as _dt
from xml.etree import ElementTree as _ElementTree
from dataclasses import dataclass as _dataclass

from licenseman import logger as _logger
from licenseman.spdx.license_text import SPDXLicenseTextPlain

if _TYPE_CHECKING:
    from typing import Literal, Any


@_dataclass
class SPDXLicenseCrossRef:
    """SPDX License cross reference."""
    url: str
    order: int
    timestamp: _dt.datetime
    match: str
    valid: bool
    live: bool
    wayback: bool


class SPDXLicense:
    """SPDX License definition.

    Parameters
    ----------
    xml
        SPDX license XML content as a string.

    References
    ----------
    - [SPDX Docs](https://github.com/spdx/license-list-XML/blob/main/DOCS/README.md)
    - [SPDX Docs - XML Fields](https://github.com/spdx/license-list-XML/blob/main/DOCS/xml-fields.md)
    - [XML Schema](https://github.com/spdx/license-list-XML/blob/main/schema/ListedLicense.xsd)
    - [GitHub Repository](https://github.com/spdx/license-list-XML)
    """

    def __init__(self,data: dict, verify: bool = True):
        try:
            root = _ElementTree.fromstring(data["xml"])
        except _ElementTree.ParseError as e:
            raise Exception(f"Error parsing license XML content.") from e
        self._ns: dict = {'': 'http://www.spdx.org/license'}
        self._xml: _ElementTree.Element = root.find('license', self._ns)
        self._data: dict = data
        if verify:
            self.verify()
        return

    def verify(self):

        def log(key_json: str, missing_in: Literal["xml", "json"], data: Any, key_xml: str | None = None):
            if key_xml is None:
                key_xml = key_json
            if missing_in == "xml":
                missing_source = "XML"
                existing_source = "JSON"
                missing_key = key_xml
                existing_key = key_json
            else:
                missing_source = "JSON"
                existing_source = "XML"
                missing_key = key_json
                existing_key = key_xml
            _logger.notice(
                log_title,
                f"The value of '{missing_key}' is not defined in the {missing_source} data. "
                f"Using the {existing_source} data value of '{existing_key}':",
                _logger.pretty(data)
            )
            return

        def osi_approved():
            key = "isOsiApproved"
            xml_raw = self._xml.attrib.get(key)
            if xml_raw == "true":
                xml = True
            elif xml_raw == "false":
                xml = False
            else:
                if xml_raw is not None:
                    raise Exception(f"Invalid value for '{key}' in XML data: {xml_raw}")
                xml = None
            json = self.osi_approved
            if json != xml:
                if xml is None:
                    log(key, "xml", json)
                    return
                if json is None:
                    log(key, "json", xml)
                    self._data[key] = xml
                    return
                raise Exception(
                    "OSI approved mismatch between XML and JSON data. "
                    f"XML: {xml}, JSON: {self.osi_approved}"
                )
            return

        def deprecated_version():
            key_xml = "licenseVersionDeprecated"
            key_json = "deprecatedVersion"
            xml = self._xml.attrib.get(key_xml)
            json = self._data.get(key_json)
            if json != xml:
                if xml is None:
                    log(key_json=key_json, key_xml=key_xml, missing_in="xml", data=json)
                elif json is None:
                    log(key_json=key_json, key_xml=key_xml, missing_in="json", data=xml)
                    self._data[key_json] = xml
                else:
                    raise Exception(
                        "Deprecated version mismatch between XML and JSON data. "
                        f"XML: {xml}, JSON: {json}"
                    )
            return

        def cross_refs():
            xml_elem = self._xml.find('crossRefs', self._ns)
            xml = sorted(
                [ref.text.strip() for ref in xml_elem.findall('crossRef', self._ns)]
            ) if xml_elem else []
            json = sorted([ref["url"] for ref in self._data.get("crossRef", [])])
            json_seealso = sorted(self._data.get("seeAlso", []))
            if json != json_seealso:
                raise Exception(
                    "Cross references mismatch between 'crossRefs' and 'seeAlso' JSON data. ",
                    f"CrossRefs: {json}, SeeAlso: {json_seealso}"
                )
            if json != xml:
                if not xml:
                    log("crossRef", "xml", data=json)
                    return
                raise Exception(
                    "Cross references mismatch between XML and JSON data. "
                    f"XML: {xml}, JSON: {json}"
                )

        log_title = f"{self.id} License Verification"
        if self._data["licenseId"] != self._xml.attrib.get('licenseId'):
            raise Exception("License ID mismatch between XML and JSON data.")
        if self._data["name"] != self._xml.attrib.get('name'):
            raise Exception("License name mismatch between XML and JSON data.")
        osi_approved()
        deprecated_version()
        cross_refs()
        return

    def generate_text(
        self,
        title: str | bool = True,
        copyright: str | bool = False,
        optionals: bool = True,
        alts: dict[str, str] | None = None,
        line_length: int = 88,
        list_indent: int = 2,
        list_item_indent: int = 1,
        list_item_vertical_spacing: int = 2,
        list_bullet_prefer_default: bool = True,
        list_bullet_ordered: bool = True,
        list_bullet_unordered_char: str = "–",
        heading_char: str = "=",
        subheading_char: str = "–",
    ) -> tuple[str, str | None]:
        """Generate plain-text license.

        Parameters
        ----------
        title
            Determines how to treat the license title, if any.
            Since the title is [optional](https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/#license-name-or-title)
            and not used in matching, it can be omitted or replaced with a custom title.
            If True, the title is included as-is. If False, the title is omitted.
            If a string, the title is replaced with the custom string, if a title is present.
        copyright
            Determines how to treat the copyright notice, if any.
            Since the copyright notice is [optional](https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/#copyright-notice)
            and not used in matching, it can be omitted or replaced with a custom notice.
            If True, the notice is included as-is. If False, the notice is omitted.
            If a string, the notice is replaced with the custom string, if a notice is present.
        optionals : bool, optional
            Whether to include <optional> elements in the output, by default True.
        alts : dict[str, int] | None, optional
            A dictionary specifying choices for <alt> elements. Keys are 'name' attributes,
            and values are the value to use.
        line_length
            The maximum line length for the plain-text output.
        list_indent
            The number of spaces separating list items from the left margin.
        list_item_indent
            The number of spaces separating list items from the bullet character.
        list_item_vertical_spacing
            The number of newlines separating list items.
        list_bullet_prefer_default
            Whether to use the license's default bullet character or number for list items, if available.
        list_bullet_ordered
            Whether to use numbered (True) or bulleted (False) list items,
            if no default bullet is available or `list_bullet_prefer_default` is False.
        list_bullet_unordered_char
            The character to use for unordered list items if `list_bullet_ordered` is False.

        Returns
        -------
        The plain-text version of the license
        plus the license header text, if present.
        """
        return SPDXLicenseTextPlain(text=self.text_xml).generate(
            title=title,
            copyright=copyright,
            optionals=optionals,
            alts=alts,
            line_length=line_length,
            list_indent=list_indent,
            list_item_indent=list_item_indent,
            list_item_vertical_spacing=list_item_vertical_spacing,
            list_bullet_prefer_default=list_bullet_prefer_default,
            list_bullet_ordered=list_bullet_ordered,
            list_bullet_unordered_char=list_bullet_unordered_char,
            title_separator=heading_char,
            subtitle_separator=subheading_char,
        )

    @property
    def raw_data(self) -> dict:
        """Raw license data."""
        return self._data

    @property
    def id(self) -> str:
        """SPDX license ID."""
        return self._data["licenseId"]

    @property
    def name(self) -> str:
        """Full name of the license"""
        return self._data["name"]

    @property
    def text_plain(self) -> str:
        """Original license text in plain text format."""
        return self._data["licenseText"]

    @property
    def text_html(self) -> str | None:
        """Original license text in HTML format."""
        return self._data.get("licenseTextHtml")

    @property
    def text_template(self) -> str | None:
        """License text template."""
        return self._data.get("standardLicenseTemplate")

    @property
    def text_xml(self) -> _ElementTree.Element:
        return self._xml.find('text', self._ns)

    @property
    def header_plain(self) -> str | None:
        """Original license header in plain text format."""
        return self._data.get("standardLicenseHeader")

    @property
    def header_html(self) -> str | None:
        """Original license header in HTML format."""
        return self._data.get("standardLicenseHeaderHtml")

    @property
    def header_template(self) -> str | None:
        """License header template."""
        return self._data.get("standardLicenseHeaderTemplate")

    @property
    def header_xml(self) -> _ElementTree.Element:
        return self._xml.find('.//standardLicenseHeader', self._ns)

    @property
    def title_text_xml(self) -> _ElementTree.Element | None:
        """Title of the license as defined in the text, if any."""
        return self._xml.find('.//titleText', self._ns)

    @property
    def copyright_notice_xml(self) -> _ElementTree.Element | None:
        """Copyright notice of the license is defined in the text, if any."""
        return self._xml.find('.//copyrightText', self._ns)

    @property
    def optionals_xml(self) -> list[_ElementTree.Element]:
        """Optional fields in the license text, if any."""
        return self._xml.findall('.//optional', self._ns)

    @property
    def alts(self) -> dict[str, dict[str, str]]:
        """

        Returns
        -------
        A dictionary where keys are the alternative field names, and values are dictionaries with keys:
        `text` : str

            Default value.
        `match` : str

            Regular expression (RegEx) pattern to validate user input for `text`.
        """
        alts = {}
        for alt in self._xml.findall('.//alt', self._ns):
            alts[alt.attrib['name']] = {'text': alt.text, 'match': alt.attrib['match']}
        return alts

    @property
    def ref_num(self) -> int:
        """Reference number of the license."""
        return self._data["referenceNumber"]

    @property
    def ref_url(self) -> str:
        """URL to the license reference page at SPDX.org."""
        return self._data["reference"]

    @property
    def json_url(self) -> str:
        """URL to the license JSON data."""
        return self._data["detailsUrl"]

    @property
    def cross_refs(self) -> list[SPDXLicenseCrossRef]:
        """URLs to license resources, if any."""
        return [
            SPDXLicenseCrossRef(
                url=ref["url"],
                order=ref["order"],
                timestamp=_dt.datetime.strptime(ref["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
                match=ref["match"],
                valid=ref["isValid"],
                live=ref["isLive"],
                wayback=ref["isWayBackLink"]
            ) for ref in self._data.get("crossRef", [])
        ]

    @property
    def osi_approved(self) -> bool:
        """Whether the license is OSI approved.

        Returns
        -------
        A boolean, or `None` if the value is not defined in the data.
        """
        return self._data["isOsiApproved"]

    @property
    def fsf_libre(self) -> bool | None:
        """Whether the license is FSF approved.

        Returns
        -------
        A boolean, or `None` if the value is not defined in the data.
        """
        return self._data.get("isFsfLibre")

    @property
    def deprecated(self) -> bool:
        """Whether the license is deprecated.

        Returns
        -------
        A boolean, or `None` if the value is not defined in the data.
        """
        return self._data["isDeprecatedLicenseId"]

    @property
    def version_deprecated(self) -> str | None:
        """Version of the SPDX License List in which the license was deprecated, if applicable.

        Returns
        -------
        Version number string, or `None` if the value is not defined in the data.
        """
        return self._data.get("deprecatedVersion")

    @property
    def obsoleted_by(self) -> list[dict[str, str]] | None:
        """New licenses that obsolete this license, if any.

        Returns
        -------
        A list of dictionaries with keys:
        `id` : str

             SPDX license ID of the successor license.
        `expression` : str

             [SPDX license expression](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/)
             which is obsoleted by the successor license;
             in most cases, this is the same as the current license's ID, unless the current license
             is a complex expression, and only a part of it is obsoleted by the successor.
        """
        return [
            {"id": elem.text, "expression": elem.attrib.get("expression")}
            for elem in self._xml.findall('.//obsoletedBy', self._ns)
        ]

    @property
    def version_added(self) -> str | None:
        """Version of the SPDX License List in which the license was first added.

        Returns
        -------
        Version number string, or `None` if the value is not defined in the data.
        """
        return self._xml.attrib.get('licenseVersion')

    @property
    def comments(self) -> str | None:
        """Comments about the license, if any."""
        return self._data.get("licenseComments")

    @property
    def notes(self) -> str | None:
        """General comments about the license, if any."""
        elem = self._xml.find('notes', self._ns)
        return elem.text if elem is not None else None

    def __repr__(self):
        return f"<SPDXLicense {self.id}>"

    def __str__(self):
        return self.text_plain