from typing import Any

from bs4.builder import HTMLTreeBuilder

class HTML5TreeBuilder(HTMLTreeBuilder):
    NAME: str
    features: Any
    TRACKS_LINE_NUMBERS: bool
    user_specified_encoding: Any
    def prepare_markup(  # type: ignore[override]  # user_specified_encoding doesn't have a default
        self, markup, user_specified_encoding, document_declared_encoding: Any | None = ..., exclude_encodings: Any | None = ...
    ) -> None: ...
    def feed(self, markup) -> None: ...
    underlying_builder: Any
    def create_treebuilder(self, namespaceHTMLElements): ...
    def test_fragment_to_document(self, fragment): ...

class TreeBuilderForHtml5lib(Any):  # html5lib.treebuilders.base.TreeBuilder
    soup: Any
    parser: Any
    store_line_numbers: Any
    def __init__(self, namespaceHTMLElements, soup: Any | None = ..., store_line_numbers: bool = ..., **kwargs) -> None: ...
    def documentClass(self): ...
    def insertDoctype(self, token) -> None: ...
    def elementClass(self, name, namespace): ...
    def commentClass(self, data): ...
    def fragmentClass(self): ...
    def appendChild(self, node) -> None: ...
    def getDocument(self): ...
    def getFragment(self): ...
    def testSerializer(self, element): ...

class AttrList:
    element: Any
    attrs: Any
    def __init__(self, element) -> None: ...
    def __iter__(self): ...
    def __setitem__(self, name, value) -> None: ...
    def items(self): ...
    def keys(self): ...
    def __len__(self) -> int: ...
    def __getitem__(self, name): ...
    def __contains__(self, name): ...

class Element(Any):  # html5lib.treebuilders.base.Node
    element: Any
    soup: Any
    namespace: Any
    def __init__(self, element, soup, namespace) -> None: ...
    def appendChild(self, node) -> None: ...
    def getAttributes(self): ...
    def setAttributes(self, attributes) -> None: ...
    attributes: Any
    def insertText(self, data, insertBefore: Any | None = ...) -> None: ...
    def insertBefore(self, node, refNode) -> None: ...
    def removeChild(self, node) -> None: ...
    def reparentChildren(self, new_parent) -> None: ...
    def cloneNode(self): ...
    def hasContent(self): ...
    def getNameTuple(self): ...
    @property
    def nameTuple(self): ...

class TextNode(Element):
    element: Any
    soup: Any
    def __init__(self, element, soup) -> None: ...
    def cloneNode(self) -> None: ...
