from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import re as _re
from xml.etree import ElementTree as ET
from textwrap import TextWrapper as _TextWrapper

if _TYPE_CHECKING:
    from typing import Any


class SPDXLicenseText:
    """
    Parses the <text> element from an SPDX license XML and generates a plain-text version of the license.

    Parameters
    ----------
    text : xml.etree.ElementTree.Element
        The <text> XML element to parse.


    References
    ----------
    -  official matcher: https://github.com/spdx/spdx-license-matcher
    -  third-party matcher: https://github.com/MikeMoore63/spdx_matcher
    """

    def __init__(self, text: ET.Element):
        self._text = text
        self._ns_uri = 'http://www.spdx.org/license'
        self._ns = {'': self._ns_uri}
        self._element_processor = {
            "titleText": self.title_text,
            "copyrightText": self.copyright_text,
            "standardLicenseHeader": self.standard_license_header,
            "list": self.list,
            "p": self.p,
            "br": self.br,
            "item": self.item,
            "bullet": self.bullet,
            "optional": self.optional,
            "alt": self.alt,
        }
        self._alt: dict = {}
        return

    def generate(self, alts: dict[str, str] | None = None) -> tuple[Any, Any | None]:
        """Generate license full text and header.

        Parameters
        ----------
        alts : dict[str, int] | None, optional
            A dictionary specifying choices for <alt> elements. Keys are 'name' attributes,
            and values are the value to use.

        Returns
        -------
        The full text of the license, and the license header text, if present.
        """
        self._alt = alts or {}
        fulltext = self.generate_full(self._text)
        header = self._text.find('.//standardLicenseHeader', self._ns)
        notice = (self.generate_notice(header)) if header else None
        return fulltext, notice

    def process(self, element: ET.Element) -> str:
        tag = self.clean_tag(element.tag)
        if tag not in self._element_processor:
            raise ValueError(f"Unsupported element: {tag}")
        processor = self._element_processor[tag]
        return processor(element)

    def get_alt(self, element: ET.Element) -> str:
        """Process an <alt> element by selecting the appropriate alternative based on `self._alt`.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <alt> element.
        """
        name = element.get('name')
        match = element.get('match')
        if not name:
            raise ValueError("Alt element must have a 'name' attribute")
        if not match:
            raise ValueError("Alt element must have a 'match' attribute")
        text = self._alt.get(name)
        if not text:
            return element.text
        if not _re.match(match, text):
            raise ValueError(f"Alt element '{name}' does not match '{match}'")
        return text

    def clean_tag(self, tag: str) -> str:
        """Strip the namespace URI from XML tag.

        Parameters
        ----------
        tag
            The XML tag with possible namespace.

        Returns
        -------
        The tag without namespace.
        """
        return tag.removeprefix(f'{{{self._ns_uri}}}')

    @staticmethod
    def clean_text(text: str) -> str:
        text_norm = _re.sub(r'\s+', ' ', text)
        if text_norm == " ":
            return ""
        return text_norm

    def generate_full(self, text: ET.Element):
        ...

    def generate_notice(self, sandard_license_header: ET.Element):
        ...

    def title_text(self, element: ET.Element):
        ...

    def copyright_text(self, element: ET.Element):
        ...

    def standard_license_header(self, element: ET.Element):
        ...

    def list(self, element: ET.Element):
        ...

    def p(self, element: ET.Element):
        ...

    def br(self, element: ET.Element):
        ...

    def item(self, element: ET.Element):
        ...

    def bullet(self, element: ET.Element):
        ...

    def optional(self, element: ET.Element):
        ...

    def alt(self, element: ET.Element):
        ...


class SPDXLicenseTextPlain(SPDXLicenseText):
    """Parses the <text> element from an SPDX license XML and generates a plain-text version of the license.

    Parameters
    ----------
    text : xml.etree.ElementTree.Element
        The <text> XML element to parse.


    References
    ----------
    -  official matcher: https://github.com/spdx/spdx-license-matcher
    -  third-party matcher: https://github.com/MikeMoore63/spdx_matcher
    """

    def __init__(self, text: ET.Element):
        super().__init__(text)
        self._title: str | bool = True
        self._copyright: str | bool = False
        self._include_optional: bool = True
        self._line_len: int = 88
        self._list_item_indent: int = 1
        self._list_item_vertical_spacing: int = 1
        self._current_list_nesting: int = 0
        self._list_indent: int = 4
        self._list_bullet_prefer_default: bool = True
        self._list_bullet_ordered: bool = True
        self._list_bullet_unordered_char: str = "–"
        self._text_wrapper: _TextWrapper | None = None
        self._curr_bullet_len: int = 0
        return

    def generate(
        self,
        title: str | bool = True,
        copyright: str | bool = False,
        include_optional: bool = True,
        alts: dict[str, str] | None = None,
        line_length: int = 88,
        list_item_indent: int = 2,
        list_item_vertical_spacing: int = 2,
        list_indent: int = 3,
        list_bullet_prefer_default: bool = True,
        list_bullet_ordered: bool = True,
        list_bullet_unordered_char: str = "–",
    ) -> tuple[str, str | None]:
        """Parses the <text> element and generates the plain-text license.

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
        include_optional : bool, optional
            Whether to include <optional> elements in the output, by default True.
        alts : dict[str, int] | None, optional
            A dictionary specifying choices for <alt> elements. Keys are 'name' attributes,
            and values are the value to use.
        line_length
            The maximum line length for the plain-text output.
        list_item_indent
            The number of spaces separating list items from the bullet character.
        Returns
        -------
        The plain-text version of the license,
        and the license header text, if present.
        """
        self._title = title
        self._copyright = copyright
        self._include_optional = include_optional
        self._line_len = line_length
        self._text_wrapper = _TextWrapper(
            width=line_length,
            replace_whitespace=True,
            drop_whitespace=True,
            break_long_words=False,
            break_on_hyphens=False,
        )
        self._current_list_nesting = 0
        self._curr_bullet_len = 0
        self._list_indent = list_indent
        self._list_item_indent = list_item_indent
        self._list_item_vertical_spacing = list_item_vertical_spacing
        self._list_bullet_prefer_default = list_bullet_prefer_default
        self._list_bullet_ordered = list_bullet_ordered
        self._list_bullet_unordered_char = list_bullet_unordered_char
        fulltext, notice = super().generate(alts)
        fulltext_cleaned, notice_cleaned = [
            f"{text.lstrip("\n").rstrip()}\n" if text else "" for text in (fulltext, notice)
        ]
        return fulltext_cleaned, notice_cleaned

    def generate_full(self, text: ET.Element):
        return self.generic(text)

    def generate_notice(self, standard_license_header: ET.Element):
        return self.generic(standard_license_header)

    def generic(
        self,
        element: ET.Element,
        return_list: bool = False,
    ) -> str | list[str]:
        """Recursively processes an XML element and its children.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The XML element to process.
        """
        out = []
        if element.text:
            out.append(self.process_text(element.text))
        for child in element:
            tag_name = self.clean_tag(child.tag)
            if tag_name not in self._element_processor:
                raise ValueError(f"Unsupported element: {tag_name}")
            content = self._element_processor[tag_name](child)
            if content:
                out.append(content)
            if child.tail:
                out.append(self.process_text(child.tail))
        if element.tail:
            out.append(self.process_text(element.tail))
        if return_list:
            return out
        # full_raw = "".join([line.rstrip(" ") if line.strip() else "\n" for elem in out for line in elem.splitlines()])
        # paragraphs = [paragraph.strip() for paragraph in _re.split(r'\n\s*\n+', full_raw)]
        # processed = [self.wrap_text(paragraph) for paragraph in paragraphs]
        # return "\n\n".join(processed)
        return _re.sub(r'\n\s*\n\s*\n+', "\n\n", "".join(out))

    def title_text(self, element: ET.Element) -> str:
        """Process a <titleText> element."""
        if self._title is False:
            return ""
        title = self.generic(element) if self._title is True else self._title
        title_lines_centered = [line.strip().center(self._line_len) for line in title.splitlines() if
                                line.strip()]
        title_centered = "\n".join(title_lines_centered)
        return f"{title_centered}\n{'=' * self._line_len}\n\n"

    def copyright_text(self, element: ET.Element) -> str:
        """Process a <copyrightText> element."""
        if self._copyright is False:
            return ""
        copyright_text = self.generic(element) if self._copyright is True else self._copyright
        return f"\n\n{copyright_text.strip()}\n\n"

    def p(self, element: ET.Element) -> str:
        """
        Processes a <p> element and appends its text to the output.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <p> element.
        """
        out = [[]]
        if element.text:
            out[-1].append(element.text)
        for child in element:
            tag_name = self.clean_tag(child.tag)
            if tag_name not in self._element_processor:
                raise ValueError(f"Unsupported element: {tag_name}")
            if tag_name == "br":
                out.append([])
            elif tag_name != "bullet":
                # Sometimes the <bullet> for <item> is placed inside a <p> element of that item.
                # Here we ignore the <bullet> element since `item()` will handle it.
                content = self._element_processor[tag_name](child)
                if content:
                    out[-1].append(content)
            if child.tail:
                out[-1].append(child.tail)
        if element.tail:
            out[-1].append(element.tail)

        paragraphs = []
        for paragraph_components in out:
            paragraph_raw = " ".join(paragraph_components)
            paragraph_normalized = _re.sub(r'\s+', ' ', paragraph_raw).strip()
            paragraphs.append(self.wrap_text(paragraph_normalized))
        return f"\n\n{"\n\n".join(paragraphs)}\n\n"

    def list(self, elem: ET.Element) -> str:
        """
        Processes a <list> element containing <item> elements.

        Parameters
        ----------
        elem : xml.etree.ElementTree.Element
            The <list> element.
        """
        self._current_list_nesting += 1

        if elem.text and elem.text.strip():
            raise ValueError("List element should not have text content")
        items = []
        for idx, child in enumerate(elem):
            tag = self.clean_tag(child.tag)
            if tag != 'item':
                raise ValueError(f"List element should only contain item elements, not {tag}")
            item_str = self.item(child, idx)
            item_str_indented = "\n".join(
                [f"{' ' * self._list_indent}{line}" for line in item_str.splitlines()])
            items.append(item_str_indented)
        self._current_list_nesting -= 1
        newlines = max(1, self._list_item_vertical_spacing) * "\n"
        list_str = newlines.join(items)
        return f"{newlines}{list_str}{newlines}"

    def item(self, elem: ET.Element, idx: int) -> str:
        bullet_elems = elem.findall("./bullet", self._ns) + elem.findall("./p/bullet", self._ns)
        if len(bullet_elems) > 1:
            raise ValueError("Item element should contain at most one bullet element")
        if len(bullet_elems) == 1:
            bullet = bullet_elems[0].text.strip() if self._list_bullet_prefer_default else (
                f"{idx + 1}." if self._list_bullet_ordered else self._list_bullet_unordered_char
            )
            bullet += self._list_item_indent * " "
            subsequent_indent = len(bullet) * " "
        else:
            bullet = ""
            subsequent_indent = ""
        self._curr_bullet_len += len(bullet)
        content = []
        if elem.text:
            text = self.process_text(elem.text).lstrip()
            if text:
                content.append(text)
        for child in elem:
            tag = self.clean_tag(child.tag)
            if tag != 'bullet':
                child_str = self.process(child)
                if child_str:
                    content.append(child_str.lstrip(" "))
            if child.tail:
                tail = self.process_text(child.tail)
                if tail:
                    needs_dedent = not content or content[-1].endswith("\n")
                    content.append(tail.lstrip() if needs_dedent else tail)
        content_raw = "".join(content).strip()

        lines = content_raw.splitlines()
        wrapped = "\n".join(
            [f"{bullet}{lines[0] if lines else ""}"] + [f"{subsequent_indent}{line}" for line in lines[1:]]
        )
        self._curr_bullet_len -= len(bullet)
        return wrapped

    def optional(self, element: ET.Element) -> str:
        """
        Processes an <optional> element based on the include_optional flag.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <optional> element.
        """
        if not self._include_optional:
            return ""
        return self.generic(element)

    def alt(self, element: ET.Element) -> str:
        """Process an <alt> element by selecting the appropriate alternative based on `self._alt`.

        Parameters
        ----------
        element : xml.etree.ElementTree.Element
            The <alt> element.
        """
        return super().get_alt(element)

    def br(self, element: ET.Element) -> str:
        return "\n\n"

    def process_text(self, text: str) -> str:
        text_norm = _re.sub(r'\s+', ' ', text)
        if text_norm == " ":
            return ""
        return self.wrap_text(text_norm)

    def wrap_text(self, text: str) -> str:
        """Wrap text to the specified line length, preserving indentation.

        Parameters
        ----------
        text : str
            The text to wrap.
        current_indent : int
            The current indentation level.
        """
        if self._current_list_nesting:
            extra_width = (self._current_list_nesting * self._list_indent) + self._curr_bullet_len
        else:
            extra_width = 0
        self._text_wrapper.width = self._line_len - extra_width
        wrapped = self._text_wrapper.fill(text)
        return wrapped

    def bullet(self, element: ET.Element) -> str:
        # This will be only called when a <bullet> element is defined outside of an <item>, which is not allowed.
        raise ValueError("Found a <bullet> element outside of <item> elements.")
