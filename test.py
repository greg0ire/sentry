#!/usr/bin/env python

from sentry.runner import configure
configure()

from datetime import timedelta
from pprint import pprint

from django.utils import timezone

from sentry.app import tsdb


tsdb.record_frequency_multi((
    (tsdb.models.projects_by_organization, {
        1: {
            "foo": 1,
            "bar": 2,
            "baz": 3,
        },
    }),
))

pprint(
    tsdb.get_most_frequent(
        tsdb.models.projects_by_organization,
        (1, 2, 3),
        timezone.now(),
    )
)

pprint(
    tsdb.get_most_frequent(
        tsdb.models.projects_by_organization,
        (1, 2, 3),
        timezone.now() - timedelta(minutes=30),
    )
)

pprint(
    tsdb.get_most_frequent(
        tsdb.models.projects_by_organization,
        (1, 2, 3),
        timezone.now() - timedelta(hours=3),
    )
)

pprint(
    tsdb.get_frequency_series(
        tsdb.models.projects_by_organization,
        {
            1: ("foo", "bar", "baz", "other"),
            2: ("foo",),
        },
        timezone.now()
    )
)

pprint(
    tsdb.get_frequency_series(
        tsdb.models.projects_by_organization,
        {
            1: ("foo", "bar", "baz", "other"),
            2: ("foo",),
        },
        timezone.now() - timedelta(hours=3)
    )
)

pprint(
    tsdb.get_frequency_totals(
        tsdb.models.projects_by_organization,
        {
            1: ("foo", "bar", "baz", "other"),
            2: ("foo",),
        },
        timezone.now()
    )
)

pprint(
    tsdb.get_frequency_totals(
        tsdb.models.projects_by_organization,
        {
            1: ("foo", "bar", "baz", "other"),
            2: ("foo",),
        },
        timezone.now() - timedelta(hours=3)
    )
)
