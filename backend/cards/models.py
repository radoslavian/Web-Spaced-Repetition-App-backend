import uuid
from django.db import models
from .apps import CardsConfig
from .utils.model_mixins import TriggeredUpdatesMixin

encoding = CardsConfig.default_encoding


class Card(models.Model, TriggeredUpdatesMixin):
    __hashed_fields__ = ('front', 'back',)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False
    )
    last_modified = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=64, unique=True)
    front = models.TextField()
    back = models.TextField()

    def __str__(self):
        return f"Q: {self.front}; A: {self.back}"


class Template(models.Model, TriggeredUpdatesMixin):
    # TODO: start with foreign key from the card to the template
    __hashed_fields__ = ("title", "description", "body",)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4(),
        editable=False
    )
    last_modified = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    body = models.TextField()

    def __str__(self):
        return f"<{self.title}>"

