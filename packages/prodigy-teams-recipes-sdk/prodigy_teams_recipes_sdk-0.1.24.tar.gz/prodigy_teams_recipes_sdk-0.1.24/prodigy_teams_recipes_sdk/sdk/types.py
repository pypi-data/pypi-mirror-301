from dataclasses import dataclass
from enum import Enum
from typing import Literal, Optional

import spacy

from . import assets, props
from .decorator import teams_type
from .util import get_spacy_langs

Goal = Literal["nooverlap", "overlap"]

Lang = Enum("Lang", {key: key for key in get_spacy_langs()})


@teams_type(
    "use",
    title="Include suggestions from model",
    description="Base questions on the model's predicted annotations.",
    field_props={"update": props.update_model},
)
@dataclass
class UseModel:
    name: assets.Model
    update: bool = False


@teams_type("blank", title="Blank model", field_props={"lang": props.lang})
@dataclass
class BlankModel:
    lang: Lang = Lang.en  # type: ignore

    def load(self) -> spacy.language.Language:
        lang = self.lang if isinstance(self.lang, str) else self.lang.value
        return spacy.blank(lang)


@teams_type(
    "blank-spans",
    title="Blank model",
    field_props={"lang": props.lang, "highlight_chars": props.highlight_chars},
)
@dataclass
class BlankModelSpans:
    lang: Lang = Lang.en  # type: ignore
    highlight_chars: bool = False

    def load(self) -> spacy.language.Language:
        lang = self.lang if isinstance(self.lang, str) else self.lang.value
        return spacy.blank(lang)


@teams_type(
    "spacy-config",
    title="Model From Config",
    field_props={"lang": props.lang, "highlight_chars": props.highlight_chars},
)
@dataclass
class SpacyConfig:
    lang: Lang = Lang.en  # type: ignore
    highlight_chars: bool = False

    def load(self) -> spacy.language.Language:
        lang = self.lang if isinstance(self.lang, str) else self.lang.value
        return spacy.blank(lang)


@teams_type(
    "classify-image",
    title="Annotate image categories",
    description="Select one or more category labels that apply to the image",
    field_props={"labels_exclusive": props.labels_exclusive},
)
@dataclass
class ImageClassification:
    labels_exclusive: bool = False


@teams_type(
    "workflow-settings",
    title="Settings for annotation workflow",
    description="Common workflow settings such as how to divide up work between annotators",
)
@dataclass
class WorkflowSettings:
    """Pre-defined custom type of common annotation workflow settings, including how to divide up work between annotators.

    If your recipe wants to configure those settings, you won’t have to add them all individually as arguments and form fields
    and can instead use this type instead."""

    feed_overlap: bool
    annotations_per_task: Optional[int]
    allow_work_stealing: bool
    instructions: str

    def dict(self) -> dict:
        return {
            "feed_overlap": self.feed_overlap,
            "allow_work_stealing": self.allow_work_stealing,
            "annotations_per_task": self.annotations_per_task,
            "instructions": self.instructions,
        }


__all__ = [
    "Goal",
    "Lang",
    "UseModel",
    "BlankModel",
    "ImageClassification",
    "WorkflowSettings",
]
