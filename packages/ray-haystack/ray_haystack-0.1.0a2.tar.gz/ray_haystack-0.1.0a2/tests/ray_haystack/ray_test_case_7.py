from typing import Any, Literal

import ray
from haystack.components.fetchers import LinkContentFetcher

from ray_haystack import RayPipeline, RayPipelineSettings
from ray_haystack.middleware import ComponentMiddleware, ComponentMiddlewareContext
from ray_haystack.serialization import worker_asset

ray.init()


@worker_asset
class TraceMiddleware(ComponentMiddleware):
    def __init__(self, capture: Literal["input", "output", "input_and_output"] = "input_and_output"):
        self.capture = capture

    def __call__(self, component_input, ctx: ComponentMiddlewareContext) -> Any:
        print(f"Tracer: Before running component '{ctx['component_name']}' with inputs: '{component_input}'")

        outputs = self.next(component_input, ctx)

        print(f"Tracer: After running component '{ctx['component_name']}' with outputs: '{outputs}'")

        return outputs


@worker_asset
class MessageMiddleware(ComponentMiddleware):
    def __init__(self, message: str):
        self.message = message

    def __call__(self, component_input, ctx: ComponentMiddlewareContext) -> Any:
        print(f"Message: Before running component '{ctx['component_name']}' : '{self.message}'")

        outputs = self.next(component_input, ctx)

        print(f"Message: After running component '{ctx['component_name']}' : '{self.message}'")

        return outputs


pipeline = RayPipeline()
pipeline.add_component("cocktail_fetcher", LinkContentFetcher())


settings: RayPipelineSettings = {
    "common": {  # apply to all component in pipeline
        "middleware": {
            "delay": {
                "type": "ray_haystack.middleware.delay_middleware.DelayMiddleware",  # full module path is required
                "init_parameters": {
                    "delay": 2,  # default is 1
                    "delay_type": "before",  # could be "after" or "before_and_after", default is "before"
                },
            }
        }
    },
}

response = pipeline.run(
    {
        "cocktail_fetcher": {"urls": ["https://www.thecocktaildb.com/api/json/v1/1/random.php"]},
    },
    ray_settings=settings,
)
