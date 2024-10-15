import io
from typing import List
from xml.etree.ElementTree import parse as parse_xml

import ray
from haystack import Document
from haystack.components.converters import OutputAdapter
from haystack.components.fetchers import LinkContentFetcher
from haystack.dataclasses import ByteStream

from ray_haystack import RayPipeline
from ray_haystack.serialization import worker_asset


# Uncomment to fix the serialization issue
@worker_asset
def parse_sources(sources: List[ByteStream]) -> List[Document]:
    documents: List[Document] = []
    for source in sources:
        xml_content = io.StringIO(source.to_string())
        documents.extend(
            Document(content=elem.text)
            for elem in parse_xml(xml_content).findall(".//channel/item/title")  # noqa: S314
            if elem.text
        )
    return documents


pipeline = RayPipeline()

pipeline.add_component("tech-news-fetcher", LinkContentFetcher())
pipeline.add_component(
    "adapter",
    OutputAdapter(
        template="{{ sources | parse_sources }}",
        output_type=List[Document],
        custom_filters={"parse_sources": parse_sources},
    ),
)

pipeline.connect("tech-news-fetcher", "adapter.sources")

pipeline.draw("pipe.png")

pipeline_inputs = {
    "tech-news-fetcher": {
        "urls": [
            "https://techcrunch.com/feed",
            "https://cnet.com/rss/news",
        ]
    },
}

ray.init()

result = pipeline.run(pipeline_inputs)

print("RESULT: ", result["adapter"]["output"])
