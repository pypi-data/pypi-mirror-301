#!/usr/bin/env python
# Copyright 2024 NetBox Labs Inc
"""Diode NetBox Plugin - Search Indices."""

from extras.models import Tag
from netbox.search import SearchIndex, register_search


@register_search
class TagIndex(SearchIndex):
    """Search index for tags."""

    model = Tag
    fields = (
        ("name", 100),
        ("slug", 110),
    )
    display_attrs = ("color",)
