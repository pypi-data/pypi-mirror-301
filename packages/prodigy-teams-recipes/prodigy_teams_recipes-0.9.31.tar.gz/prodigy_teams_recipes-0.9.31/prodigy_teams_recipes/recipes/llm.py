from contextlib import contextmanager
import os
from pathlib import Path
from typing import Iterator, Literal

import prodigy.recipes.llm.textcat
from cloudpathlib import AnyPath
from prodigy_teams_recipes_sdk import (
    Asset,
    Dataset,
    Input,
    action_recipe,
    teams_type,
    Secret,
)

from .util import make_tempdir


@teams_type(
    "config",
    title="spaCy config file",
    description="Remote path to a loadable spaCy config file",
)
class Config(Asset[Literal["config"]]):
    kind = "config"

    @contextmanager
    def localize(self) -> Iterator[Path]:
        """Save the path to a local temporary file"""
        # TODO: Do this more elegantly
        path = AnyPath(self.path)
        with make_tempdir() as tmp:
            output = tmp / path.parts[-1]
            with path.open("r") as in_file:
                data = in_file.read()
                with output.open("w") as out_file:
                    out_file.write(data)
            yield output


@action_recipe(
    title="Textcat LLM fetch",
    description="Gather text categorization predictions from an LLM",
)
def llm_fetch_textcat(
    output: Dataset,
    config: Config,
    input: Input,
    *,
    openai_key: Secret,
    resume: bool = False,
) -> None:
    os.environ["OPENAI_API_ORG"] = openai_key.get_secret_value("openai_org")
    os.environ["OPENAI_API_KEY"] = openai_key.get_secret_value("openai_key")
    with config.localize() as config_path:
        prodigy.recipes.llm.textcat.llm_fetch_textcat(
            config_path=config_path,
            source=input.path,
            output=output.name,
            resume=resume,
            loader=input.meta.get("loader"),
        )
