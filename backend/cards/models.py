import uuid
from abc import ABC
from functools import reduce

from django.db import models
from treebeard.al_tree import AL_Node

from .apps import CardsConfig
from .utils.model_mixins import TriggeredUpdatesMixin

encoding = CardsConfig.default_encoding


class Template(models.Model, TriggeredUpdatesMixin):
    __hashed_fields__ = ("title", "description", "body",)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    last_modified = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    # body will eventually contain template for rendering
    # with fields for question and answer
    body = models.TextField()

    def __str__(self):
        return f"<{self.title}>"


class Card(models.Model, TriggeredUpdatesMixin):
    __hashed_fields__ = ("front", "back",)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    hash = models.CharField(max_length=64, unique=True)
    last_modified = models.DateTimeField(auto_now=True)
    front = models.TextField()
    back = models.TextField()
    template = models.ForeignKey(Template, on_delete=models.PROTECT,
                                 null=True, related_name="cards")

    def __str__(self):
        MAX_LEN = 50
        serialized = f"Q: {self.front}; A: {self.back}"
        if len(serialized) > MAX_LEN:
            serialized = serialized[:MAX_LEN] + " ..."

        return serialized


class Category(AL_Node, TriggeredUpdatesMixin):
    __hashed_fields__ = ("name", "parent_id",)

    hash = models.CharField(max_length=64, unique=True)
    last_modified = models.DateTimeField(auto_now=True)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=64)
    parent = models.ForeignKey(
        "self",
        related_name="sub_categories",
        on_delete=models.PROTECT,
        db_index=True,
        null=True
    )
    node_order_by = ["name"]

    def __str__(self):
        return f"<{self.name}>"
