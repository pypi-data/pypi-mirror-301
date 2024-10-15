import io
import os
from typing import List, Optional
from xml.etree.ElementTree import parse as parse_xml

import ray
from haystack import Document, Pipeline, component
from haystack.components.builders import PromptBuilder
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.generators import OpenAIGenerator
from haystack.components.joiners import DocumentJoiner
from haystack.dataclasses import ByteStream

from ray_haystack import RayPipeline

os.environ["OPENAI_API_KEY"] = ""

ray.init()


@component
class XmlConverter:
    """
    Custom component which parses given RSS feed (from ByteStream) and extracts values by a given XPath, e.g.
    ".//channel/item/title" will find "title" for ech RSS feed item. Each "title" is converted to a Document with respective content.
    The `category` attribute can be used as an additional metadata field.
    """

    def __init__(self, xpath: str = ".//channel/item/title", category: Optional[str] = None):
        self.xpath = xpath
        self.category = category

    @component.output_types(documents=List[Document])
    def run(self, sources: List[ByteStream]):
        documents: List[Document] = []
        for source in sources:
            xml_content = io.StringIO(source.to_string())
            documents.extend(
                Document(content=elem.text, meta={"category": self.category})
                for elem in parse_xml(xml_content).findall(self.xpath)  # noqa: S314
                if elem.text
            )
        return {"documents": documents}


template = """
Given news headlines below provide a summary of what is happening in the world right now in a couple of sentences.
You will be given headline titles in the following format: "<headline category>: <headline title>".
When creating summary pay attention to common news headlines as those could be most insightful.

HEADLINES:
{% for document in documents %}
    {{ document.meta["category"] }}: {{ document.content }}
{% endfor %}

SUMMARY:
"""

pipeline = RayPipeline()

pipeline.add_component("tech-news-fetcher", LinkContentFetcher())
pipeline.add_component("business-news-fetcher", LinkContentFetcher())
pipeline.add_component("politics-news-fetcher", LinkContentFetcher())
pipeline.add_component("tech-xml-converter", XmlConverter(category="tech"))
pipeline.add_component("business-xml-converter", XmlConverter(category="business"))
pipeline.add_component("politics-xml-converter", XmlConverter(category="politics"))
pipeline.add_component("document_joiner", DocumentJoiner(sort_by_score=False))
pipeline.add_component("prompt_builder", PromptBuilder(template=template))
pipeline.add_component("generator", OpenAIGenerator())  # "gpt-4o-mini" is the default model

pipeline.connect("tech-news-fetcher", "tech-xml-converter.sources")
pipeline.connect("business-news-fetcher", "business-xml-converter.sources")
pipeline.connect("politics-news-fetcher", "politics-xml-converter.sources")
pipeline.connect("tech-xml-converter", "document_joiner")
pipeline.connect("business-xml-converter", "document_joiner")
pipeline.connect("politics-xml-converter", "document_joiner")
pipeline.connect("document_joiner", "prompt_builder")
pipeline.connect("prompt_builder", "generator.prompt")

pipeline.draw("pipe.png")

pipeline_inputs = {
    "tech-news-fetcher": {
        "urls": [
            "https://www.theverge.com/rss/frontpage/",
            "https://techcrunch.com/feed",
            "https://cnet.com/rss/news",
            "https://wired.com/feed/rss",
        ]
    },
    "business-news-fetcher": {
        "urls": [
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147",
            "https://www.business-standard.com/rss/home_page_top_stories.rss",
            "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
        ]
    },
    "politics-news-fetcher": {
        "urls": [
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000113",
            "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
        ]
    },
}

# result = pipeline.run(pipeline_inputs)

# print("RESULT: ", result["generator"]["replies"][0])

result = pipeline.run_nowait(pipeline_inputs)

for pipeline_event in result.pipeline_events_sync():
    # For better viewing experience inputs/outputs are truncated
    # but you can comment out lines below (before `print`)
    # if you would like to see full event data
    if pipeline_event.type == "ray.haystack.pipeline-start":
        pipeline_event.data["pipeline_inputs"] = "{...}"
    if pipeline_event.type == "ray.haystack.component-start":
        pipeline_event.data["input"] = "{...}"
    if pipeline_event.type == "ray.haystack.component-end":
        pipeline_event.data["output"] = "{...}"

    print(
        f"\n>>> [{pipeline_event.time}] Source: {pipeline_event.source} | Type: {pipeline_event.type} | Data={pipeline_event.data}"
    )
