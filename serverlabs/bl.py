from flask import jsonify

from serverlabs.db import records


def get_records_by_filter(filter_func):
    return list(filter(
        filter_func,
        records.values()
    ))
