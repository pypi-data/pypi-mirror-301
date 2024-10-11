import re
import tempfile

import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
from izihawa_textutils.html_processing import canonize_tags

from ._banned_sections import BANNED_SECTIONS, BANNED_SECTION_PREFIXES
from .utils import md


class EpubParser:
    def __init__(
        self,
        banned_sections: set[str] = BANNED_SECTIONS,
        banned_section_prefixes: set[str] = BANNED_SECTION_PREFIXES,
        remove_notes: bool = True,
    ):
        _joined = "|".join(banned_section_prefixes)
        self._banned_section_prefixes_regexp = re.compile(
            rf"^({_joined})",
            flags=re.IGNORECASE,
        )
        if banned_sections is None:
            self.banned_sections = set()
        else:
            self.banned_sections = set(banned_sections)
        self._remove_notes = remove_notes
        if self._remove_notes:
            self.banned_sections.add("notes")

    def parse_soup(self, soup: BeautifulSoup):
        body = soup.find("body")
        if not body:
            return

        for _ in list(
            soup.select("body > .copyright-mtp, body > .halftitle, body > .book-title")
        ):
            return

        for section in list(soup.find_all("section")):
            if self._remove_notes and section.attrs.get("epub:type") == "note":
                section.extract()
                break
            for child in section.children:
                child_text = child.text.lower().strip(" :,.;")
                if child.name in {
                    "header",
                    "h1",
                    "h2",
                    "h3",
                    "h4",
                    "h5",
                    "h6",
                    "div",
                } and (
                    child_text in self.banned_sections
                    or self._banned_section_prefixes_regexp.match(child_text)
                ):
                    section.extract()
                    break

        for summary in list(soup.select("details > summary.section-heading")):
            summary_text = summary.text.lower().strip(" :,.;")
            if (
                summary_text in self.banned_sections
                or self._banned_section_prefixes_regexp.match(summary_text)
            ):
                summary.parent.extract()

        for header in list(soup.select("body h1")):
            header_text = header.text.lower().strip(" :,.;")
            if (
                header_text in self.banned_sections
                or self._banned_section_prefixes_regexp.match(header_text)
            ):
                header.parent.extract()

        for b_tag in list(soup.select("b, i")):
            b_tag.unwrap()

        for p_tag in list(soup.find_all("p")):
            sibling = p_tag.next_sibling
            while sibling == "\n":
                sibling = sibling.next_sibling
            if sibling and sibling.name == "blockquote":
                new_p_tag = soup.new_tag("p")
                new_p_tag.extend([p_tag.text, " ", sibling.text])
                p_tag.replace_with(new_p_tag)
                sibling.extract()

        for el in list(
            soup.select(
                'table, nav, ref, formula, math, figure, img, [role="note"], .Affiliations, '
                ".ArticleOrChapterToc, .FM-head, .EM-copyright-text, .EM-copyright-text-space, "
                ".AuthorGroup, .ChapterContextInformation, "
                ".Contacts, .CoverFigure, .Bibliography, "
                ".BookTitlePage, .BookFrontmatter, .CopyrightPage, .Equation, "
                ".FootnoteSection, .reference, .side-box-text, .thumbcaption"
            )
        ):
            el.extract()

        for el in list(soup.select("a, span")):
            el.unwrap()
        text = md.convert_soup(canonize_tags(soup)).strip()
        return text


def extract_epub(content: bytes, epub_parser: EpubParser):
    with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as t_file:
        t_file.write(content)
        file_name = t_file.name
        book = epub.read_epub(file_name)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        texts = []
        for item in items:
            if _ := (
                re.search("(chapter|part|notes)", item.get_name(), flags=re.IGNORECASE)
                or re.search(
                    r"^(?!.*(photographs?|contributors|acknowledgements|content|list_figure|cover|title_page|title|titlePage|copyright|backmatter|dedication|epigraph|image|"
                    r"index|credits|bibliography|footnote|navdoc|frontmatter|reference|toc|series|nav|copy|ack\.)).*$",
                    item.get_name(),
                    flags=re.IGNORECASE,
                )
            ):
                soup = BeautifulSoup(item.get_body_content(), "lxml")
                text = epub_parser.parse_soup(soup)
                text = re.sub("\n([a-z])", r" \g<1>", text)
                text = re.sub(
                    r"\n\s*\n\s*$",
                    "\n\n",
                    text,
                    flags=re.DOTALL | re.MULTILINE | re.UNICODE,
                )
                texts.append(text)

        return "\n\n".join(texts).strip()
