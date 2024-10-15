from pydantic import BaseModel
from typing import List, Dict, Union
from datetime import datetime


class Chunk(BaseModel):
    text: str
    non_vectorised_addendum_text: str = ""
    embedding: List = None
    page_numbers: List[int] = None
    file_source: str = ""
    article_id: str = ""
    metadata: Dict[str, Union[str, datetime]] = None
    bounding_boxes: List = None

    @property
    def fields_in_chromadb_metadata_format(self):
        metadata = self.metadata or {}
        if self.non_vectorised_addendum_text:
            metadata["non_vectorised_addendum_text"] = self.non_vectorised_addendum_text
        if self.page_numbers:
            metadata["page_numbers"] = str(self.page_numbers)
        if self.file_source:
            metadata["file_source"] = self.file_source
        if self.bounding_boxes:
            metadata["bounding_boxes"] = str(self.bounding_boxes)
        metadata = metadata or None
        return metadata


class VectorSearchResponse(BaseModel):
    document: str
    distance: float
    metadata: Union[Dict[str, str], None] = None


class WebSearchResponse(BaseModel):
    url: str
    title: str = ""
    snippet: str = ""
