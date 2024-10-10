import logging
import datetime
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

TIMECODES_THRESHOLD_COUNT = 3
TIMECODE_PATTERN = r'(\d*:*\d+:+\d+)'
STRIP_CHARS = ' #$%&@()*+[\\]^_`{|}~--−–—'
DOTS_CHARS = '.,;:?!'

REPLACEMENTS = [
    '---',
    '--',
    '===',
    '==',
    ' =',
    '___',
    '__',
    '_ _ _',
    '_ _',
    ' _',
    '\n-',
    '\n=',
    '\n_',
    '\n -',
    '\n =',
    '\n _',
]


def clean_timecodes_text(text):
    for pattern in REPLACEMENTS:
        text = text.replace(pattern, '')

    return text.strip()


def time_to_seconds(time_str):
    if time_str.count(':') == 1:
        format_str = '%M:%S'
        time_obj = datetime.datetime.strptime(time_str, format_str)
        total_seconds = time_obj.minute * 60 + time_obj.second
    elif time_str.count(':') == 2:
        format_str = '%H:%M:%S'
        time_obj = datetime.datetime.strptime(time_str, format_str)
        total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    else:
        raise ValueError("Time format not recognized")
    return total_seconds


def get_timecodes_block_text(text):
    if not text:
        return ''

    for part in text.split('\n\n'):
        matches = re.findall(TIMECODE_PATTERN, part)
        if len(matches) > TIMECODES_THRESHOLD_COUNT:
            return part


def get_all_timecodes(text):
    timecodes_block_text = get_timecodes_block_text(text)
    timecodes_block_text = clean_timecodes_text(timecodes_block_text)

    timecodes = []
    for row in timecodes_block_text.split('\n'):
        if not (matched := re.findall(TIMECODE_PATTERN, row)):
            continue

        timecode_raw = matched[0]
        title = row.replace(timecode_raw, '')
        title = title.strip(STRIP_CHARS).lstrip(DOTS_CHARS)

        timecodes.append({
            'timecode': time_to_seconds(timecode_raw),
            'timecode_row': timecode_raw,
            'title': title,
        })

    return timecodes
