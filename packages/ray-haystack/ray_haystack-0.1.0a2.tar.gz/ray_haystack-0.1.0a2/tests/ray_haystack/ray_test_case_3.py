from typing import Any, Dict, List, Optional, Set, Tuple

import ray
from haystack import Document, Pipeline, component
from haystack.components.builders import PromptBuilder
from haystack.components.joiners import BranchJoiner
from haystack.components.routers import ConditionalRouter

# from tests.ray_haystack.sample_components import AddFixedValue, Parity, Sum
from sample_components import (
    Accumulate,
    AddFixedValue,
    Double,
    Greet,
    Parity,
    Remainder,
    Repeat,
    Subtract,
    Sum,
    Threshold,
)

from ray_haystack import RayPipeline
from ray_haystack.components import RayInMemoryBM25Retriever, RayInMemoryDocumentStore

if __name__ == "__main__":
    ray.shutdown()
    ray.init()

    pipeline = RayPipeline(max_runs_per_component=20)
    pipeline.add_component("comp_1_1", AddFixedValue())
    pipeline.add_component("comp_1", AddFixedValue())
    pipeline.add_component("comp_2", AddFixedValue())
    pipeline.add_component("comp_2_2", AddFixedValue())
    pipeline.add_component("comp_3", Sum())
    pipeline.add_component("comp_4", AddFixedValue())
    pipeline.add_component("comp_5", AddFixedValue())
    pipeline.add_component("threshold", Threshold(10))

    pipeline.connect("comp_1_1", "comp_1.value")
    pipeline.connect("comp_1", "comp_2.value")
    pipeline.connect("comp_1", "comp_3")
    pipeline.connect("comp_2_2", "comp_2.add")
    pipeline.connect("comp_2", "comp_4.value")
    pipeline.connect("comp_4", "comp_3")
    pipeline.connect("comp_4", "comp_5.add")
    pipeline.connect("comp_5", "threshold.value")
    pipeline.connect("threshold.below", "comp_1.add")

    pipeline.draw("pipe.png")

    print(
        pipeline.run(
            {
                "comp_1_1": {"value": 1},
                "comp_5": {"value": 1},
                "comp_2_2": {"value": 1},
            },
        )
    )
