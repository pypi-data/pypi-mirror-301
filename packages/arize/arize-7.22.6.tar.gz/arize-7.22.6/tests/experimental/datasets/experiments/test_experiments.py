import sys

import pytest

if sys.version_info < (3, 8):
    pytest.skip("Requires Python 3.8 or higher", allow_module_level=True)

import random
import string

import pandas as pd
from arize.experimental.datasets import ArizeDatasetsClient
from arize.experimental.datasets.experiments.evaluators.base import EvaluationResult, Evaluator


# Define a simple evaluator
class DummyEval(Evaluator):
    def evaluate(self, *, output, dataset_row, **_) -> EvaluationResult:
        return EvaluationResult(
            explanation="eval explanation",
            score=1,
            label=dataset_row["id"],
            metadata={
                "output": output,
                "input": dataset_row["question"],
                "example_id": dataset_row["id"],
            },
        )

    async def async_evaluate(self, *, output, dataset_row, **_) -> EvaluationResult:
        return EvaluationResult(
            explanation="eval explanation",
            score=1,
            label=dataset_row["id"],
            metadata={
                "output": output,
                "input": dataset_row["question"],
                "example_id": dataset_row["id"],
            },
        )


class DummyEval2(Evaluator):
    def evaluate(self, *, output, dataset_row, **_) -> EvaluationResult:
        return EvaluationResult(
            explanation="eval explanation",
            score=1,
            label=dataset_row["id"],
            metadata={
                "output": output,
                "input": dataset_row["question"],
                "example_id": dataset_row["id"],
            },
        )

    async def async_evaluate(self, *, output, dataset_row, **_) -> EvaluationResult:
        return EvaluationResult(
            explanation="eval explanation",
            score=1,
            label=dataset_row["id"],
            metadata={
                "output": output,
                "input": dataset_row["question"],
                "example_id": dataset_row["id"],
            },
        )


def dummy_task(dataset_row):
    question = dataset_row["question"]
    return f"Answer to {question}"


dataset = pd.DataFrame(
    {
        "id": [f"id_{i}" for i in range(10)],
        "question": [
            "".join(random.choices(string.ascii_letters + string.digits, k=10)) for _ in range(10)
        ],
    }
)


def test_run_experiment():
    c = ArizeDatasetsClient(developer_key="dummy_key", api_key="dummy_key")
    exp_id, exp_df = c.run_experiment(
        space_id="dummy_space_id",
        experiment_name="test_experiment",
        dataset_id="dummy_dataset_id",
        dataset_df=dataset,
        task=dummy_task,
        evaluators=[DummyEval(), DummyEval2()],
        dry_run=True,
    )
    assert exp_id == ""
    # output df should have 10 rows x 21 cols
    assert exp_df.shape == (10, 21)
    # expected col names
    assert exp_df.columns.tolist() == [
        "id",
        "example_id",
        "result",
        "result.trace.id",
        "result.trace.timestamp",
        "eval.DummyEval.score",
        "eval.DummyEval.label",
        "eval.DummyEval.explanation",
        "eval.DummyEval.trace.id",
        "eval.DummyEval.trace.timestamp",
        "eval.DummyEval.metadata.output",
        "eval.DummyEval.metadata.input",
        "eval.DummyEval.metadata.example_id",
        "eval.DummyEval2.score",
        "eval.DummyEval2.label",
        "eval.DummyEval2.explanation",
        "eval.DummyEval2.trace.id",
        "eval.DummyEval2.trace.timestamp",
        "eval.DummyEval2.metadata.output",
        "eval.DummyEval2.metadata.input",
        "eval.DummyEval2.metadata.example_id",
    ]
    # no empty cells
    assert exp_df.isnull().sum().sum() == 0

    for _, row in exp_df.iterrows():
        assert (
            row["example_id"]
            == row["eval.DummyEval.metadata.example_id"]
            == row["eval.DummyEval2.metadata.example_id"]
            == row["eval.DummyEval.label"]
            == row["eval.DummyEval2.label"]
        )
        assert (
            row.result
            == row["eval.DummyEval.metadata.output"]
            == row["eval.DummyEval2.metadata.output"]
        )

    # # trace.timestamp should be int (milliseconds timestamp)
    assert exp_df["result.trace.timestamp"].dtype == int
    assert exp_df["eval.DummyEval.trace.timestamp"].dtype == int
    assert exp_df["eval.DummyEval2.trace.timestamp"].dtype == int
