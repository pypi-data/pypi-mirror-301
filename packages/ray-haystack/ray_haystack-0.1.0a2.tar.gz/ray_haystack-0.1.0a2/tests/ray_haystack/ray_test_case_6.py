import os

import ray
from datasets import load_dataset
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.components.generators import OpenAIGenerator
from haystack.dataclasses import Document
from haystack.document_stores.types import DocumentStore

from ray_haystack.components import (
    RayInMemoryDocumentStore,
    RayInMemoryEmbeddingRetriever,
)
from ray_haystack.ray_pipeline import RayPipeline

os.environ["OPENAI_API_KEY"] = "Your OpenAI API Key"


def prepare_document_store(document_store: DocumentStore):
    doc_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
    doc_embedder.warm_up()

    dataset = load_dataset("bilgeyucel/seven-wonders", split="train")
    docs = [Document(content=doc["content"], meta=doc["meta"]) for doc in dataset]

    docs_with_embeddings = doc_embedder.run(docs)
    document_store.write_documents(docs_with_embeddings["documents"])


template = """
Given the following information, answer the question.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
"""

# Start Ray cluster before defining `RayInMemoryDocumentStore` as internally it creates an actor
ray.init()

document_store = RayInMemoryDocumentStore()  # from `ray-haystack`
prepare_document_store(document_store)

text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
retriever = RayInMemoryEmbeddingRetriever(document_store)  # from `ray-haystack`
generator = OpenAIGenerator()

prompt_builder = PromptBuilder(template=template)

pipeline = RayPipeline()

pipeline.add_component("text_embedder", text_embedder)
pipeline.add_component("retriever", retriever)
pipeline.add_component("prompt_builder", prompt_builder)
pipeline.add_component("llm", generator)

pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
pipeline.connect("retriever", "prompt_builder.documents")
pipeline.connect("prompt_builder", "llm")

question = "What does Rhodes Statue look like?"

response = pipeline.run(
    {
        "text_embedder": {"text": question},
        "prompt_builder": {"question": question},
    }
)

print("RESULT: ", response["llm"]["replies"][0])
