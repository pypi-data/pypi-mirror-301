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
    pipe.add_component("comp_1", AddFixedValue(1))
    pipe.add_component("parity_1", Parity())
    pipe.add_component("comp_1_1", AddFixedValue(1))
    pipe.add_component("comp_2", AddFixedValue(1))
    pipe.add_component("threshold", Threshold(5))
    pipe.add_component("sum_1", Sum())
    pipe.add_component("sum_2", Sum())

    pipe.connect("comp_1", "comp_2.value")
    pipe.connect("comp_1", "parity_1.value")

    pipe.connect("comp_1_1", "sum_2")
    pipe.connect("parity_1.odd", "sum_2")
    pipe.connect("parity_1.even", "comp_1_1.add")

    pipe.connect("comp_2", "threshold.value")
    pipe.connect("threshold.below", "comp_2.add")
    pipe.connect("threshold.above", "sum_1")
    pipe.connect("sum_2", "sum_1")

    pipe.draw("pipe.png")

    print(
        pipe.run(
            {"comp_1": {"value": 2}, "comp_1_1": {"value": 1}},
        )
    )
