#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.text_splitter import SpacyTextSplitter

from pilot.configs.config import Config
from pilot.source_embedding import SourceEmbedding, register

CFG = Config()


class PDFEmbedding(SourceEmbedding):
    """pdf embedding for read pdf document."""

    def __init__(self, file_path, vector_store_config):
        """Initialize with pdf path."""
        super().__init__(file_path, vector_store_config)
        self.file_path = file_path
        self.vector_store_config = vector_store_config

    @register
    def read(self):
        """Load from pdf path."""
        loader = PyPDFLoader(self.file_path)
        # textsplitter = CHNDocumentSplitter(
        #     pdf=True, sentence_size=CFG.KNOWLEDGE_CHUNK_SIZE
        # )
        textsplitter = SpacyTextSplitter(
            pipeline="zh_core_web_sm",
            chunk_size=CFG.KNOWLEDGE_CHUNK_SIZE,
            chunk_overlap=100,
        )
        return loader.load_and_split(textsplitter)

    @register
    def data_process(self, documents: List[Document]):
        i = 0
        for d in documents:
            documents[i].page_content = d.page_content.replace("\n", "")
            i += 1
        return documents
