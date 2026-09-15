# document/document_manager.py
import json
import os
import uuid
from datetime import datetime

from utils.constants import (
    DATA_DIR,
    ELEM_HEADING1, ELEM_HEADING2, ELEM_HEADING3,
    ELEM_PARAGRAPH, ELEM_FIGURE, ELEM_CAPTION,
    ELEM_TABLE, ELEM_SECTION, ELEM_PAGEBREAK,
)


class Element:
    """عنصر واحد داخل المستند."""

    def __init__(self, kind, text="", meta=None, eid=None):
        self.id = eid or str(uuid.uuid4())[:8]
        self.kind = kind
        self.text = text
        self.meta = meta or {}
        self.align = "right"

    def to_dict(self):
        return {
            "id": self.id,
            "kind": self.kind,
            "text": self.text,
            "meta": self.meta,
            "align": self.align,
        }

    @classmethod
    def from_dict(cls, d):
        e = cls(
            d.get("kind", ELEM_PARAGRAPH),
            d.get("text", ""),
            d.get("meta", {}),
            d.get("id"),
        )
        e.align = d.get("align", "right")
        return e


class Document:
    """يمثّل مستندًا واحدًا."""

    def __init__(self, title="مستند جديد", doc_id=None):
        self.id = doc_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.title = title
        self.created = datetime.now().isoformat()
        self.updated = self.created
        self.elements = []
        self.counters = {"figure": 0, "table": 0, "equation": 0}

    # ---------- الإضافة ----------
    def add_element(self, elem, index=None):
        if index is None or index >= len(self.elements):
            self.elements.append(elem)
        else:
            self.elements.insert(index, elem)
        self.updated = datetime.now().isoformat()
        return elem

    def add_heading(self, text, level=1):
        kind = {1: ELEM_HEADING1, 2: ELEM_HEADING2, 3: ELEM_HEADING3}[level]
        return self.add_element(Element(kind, text, {"level": level}))

    def add_paragraph(self, text=""):
        return self.add_element(Element(ELEM_PARAGRAPH, text))

    def add_figure(self, image_path, caption=""):
        self.counters["figure"] += 1
        num = self.counters["figure"]
        fig = self.add_element(
            Element(ELEM_FIGURE, image_path, {"number": num})
        )
        if caption:
            self.add_element(
                Element(
                    ELEM_CAPTION,
                    f"شكل {num}: {caption}",
                    {"parent_id": fig.id, "for": "figure", "number": num},
                )
            )
        return fig

    def add_table(self, rows, cols, caption=""):
        self.counters["table"] += 1
        num = self.counters["table"]
        tbl = self.add_element(
            Element(
                ELEM_TABLE, "",
                {"rows": rows, "cols": cols, "number": num},
            )
        )
        if caption:
            self.add_element(
                Element(
                    ELEM_CAPTION,
                    f"جدول {num}: {caption}",
                    {"parent_id": tbl.id, "for": "table", "number": num},
                )
            )
        return tbl

    def add_section_break(self, kind="next_page"):
        return self.add_element(Element(ELEM_SECTION, "", {"type": kind}))

    def add_page_break(self):
        return self.add_element(Element(ELEM_PAGEBREAK))

    # ---------- الاستعلام ----------
    def get_headings(self):
        return [
            e for e in self.elements
            if e.kind in (ELEM_HEADING1, ELEM_HEADING2, ELEM_HEADING3)
        ]

    def get_figures(self):
        return [e for e in self.elements if e.kind == ELEM_FIGURE]

    def get_tables(self):
        return [e for e in self.elements if e.kind == ELEM_TABLE]

    def get_captions(self, for_type=None):
        caps = [e for e in self.elements if e.kind == ELEM_CAPTION]
        if for_type:
            caps = [c for c in caps if c.meta.get("for") == for_type]
        return caps

    # ---------- الحفظ ----------
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created": self.created,
            "updated": self.updated,
            "counters": self.counters,
            "elements": [e.to_dict() for e in self.elements],
        }

    @classmethod
    def from_dict(cls, d):
        doc = cls(d.get("title", "مستند"), d.get("id"))
        doc.created = d.get("created", doc.created)
        doc.updated = d.get("updated", doc.updated)
        doc.counters = d.get(
            "counters", {"figure": 0, "table": 0, "equation": 0}
        )
        doc.elements = [
            Element.from_dict(e) for e in d.get("elements", [])
        ]
        return doc

    def save(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        path = os.path.join(DATA_DIR, f"{self.id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        return path

    @staticmethod
    def load(doc_id):
        path = os.path.join(DATA_DIR, f"{doc_id}.json")
        with open(path, "r", encoding="utf-8") as f:
            return Document.from_dict(json.load(f))

    @staticmethod
    def list_documents():
        os.makedirs(DATA_DIR, exist_ok=True)
        docs = []
        for fname in sorted(os.listdir(DATA_DIR), reverse=True):
            if fname.endswith(".json"):
                try:
                    path = os.path.join(DATA_DIR, fname)
                    with open(path, "r", encoding="utf-8") as f:
                        d = json.load(f)
                    docs.append({
                        "id": d.get("id", fname[:-5]),
                        "title": d.get("title", "بدون عنوان"),
                        "updated": d.get("updated", ""),
                        "count": len(d.get("elements", [])),
                    })
                except Exception:
                    pass
        return docs

    @staticmethod
    def delete(doc_id):
        path = os.path.join(DATA_DIR, f"{doc_id}.json")
        if os.path.exists(path):
            os.remove(path)
            return True
        return False