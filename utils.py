import os
from datetime import datetime, timedelta


def resolve_source_key(source):
    parts = source.split('-')
    if parts[0] == 'the':
        parts = parts[1:]

    return '-'.join(parts)


def resolve_date_key(date_range):
    return '_'.join(date_range)


def get_articles_dir(source):
    return os.path.join('articles', resolve_source_key(source))

def get_articles_filepath(source, date_range):
    return os.path.join(get_articles_dir(source), resolve_date_key(date_range) + '.csv')


def monthly_date_ranges(overall_date_range):
    # split date into buckets of time, extending beyond the start time if needed
    day_delta = 30
    date_format = "%Y-%m-%d"

    from_date = datetime.strptime(overall_date_range[1], date_format)
    start_date = datetime.strptime(overall_date_range[0], date_format)

    while from_date > start_date:

        to_date = from_date
        from_date = to_date - timedelta(days=day_delta)

        yield (from_date.strftime(date_format), to_date.strftime(date_format))