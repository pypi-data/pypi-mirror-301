from pydantic import BaseModel

from neural_bridge_sdk.types.dataset import DatasetType


class DefaultDataset(BaseModel):
  name: str
  description: str
  dataset_type: DatasetType


# Define a single class that holds all dataset constants
class DefaultDatasetConstants(BaseModel):
  DEFAULT_AGENT_OPT_DATASET: DefaultDataset = DefaultDataset(
    name="default agent optimization",
    description="This dataset is used as the default dataset for agent optimization tasks, where an agent's performance or behavior is improved based on given data.",
    dataset_type=DatasetType.APPLICATION,
  )

  DEFAULT_LLM_OPT_DATASET: DefaultDataset = DefaultDataset(
    name="default llm optimization",
    description="This dataset serves as the default for optimizing Large Language Models (LLMs). It is used to fine-tune or improve LLM performance on specific tasks.",
    dataset_type=DatasetType.APPLICATION,
  )

  DEFAULT_LLM_EVALUATION_DATASET: DefaultDataset = DefaultDataset(
    name="default llm evaluation dataset",
    description="This dataset is the default dataset used for evaluating the performance of Large Language Models. It is used to assess model outputs against a reference dataset to measure accuracy and other evaluation metrics.",
    dataset_type=DatasetType.EVALUATION,
  )

  DEFAULT_AGENT_EVALUATION_DATASET: DefaultDataset = DefaultDataset(
    name="default agent evaluation dataset",
    description="This dataset is the default dataset used for evaluating the performance of agents. It is used to measure agent performance based on various evaluation metrics.",
    dataset_type=DatasetType.EVALUATION,
  )


DATASET_CONSTANTS = DefaultDatasetConstants()
