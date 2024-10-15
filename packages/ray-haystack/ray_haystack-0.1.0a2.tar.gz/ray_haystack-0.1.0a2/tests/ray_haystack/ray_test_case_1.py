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

    pipe = RayPipeline(max_runs_per_component=20)
    pipe.add_component("comp_0", AddFixedValue(1))
    pipe.add_component("comp_1", AddFixedValue(1))
    pipe.add_component("comp_2", AddFixedValue(1))
    pipe.add_component("comp_3", Threshold(5))
    pipe.add_component("comp_4", AddFixedValue())

    pipe.connect("comp_0", "comp_1.value")
    pipe.connect("comp_1", "comp_2.value")
    pipe.connect("comp_2", "comp_3.value")
    pipe.connect("comp_3.below", "comp_1.add")
    pipe.connect("comp_3.above", "comp_4.value")

    pipe.draw("pipe.png")

    print(
        pipe.run(
            {
                "comp_0": {"value": 1},
            },
        )
    )
