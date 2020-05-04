import re


def get_range_regex() -> re.Pattern:
  return re.compile(r'(?:(?P<sheet>(?:(?!!)\S)*)!)?(?P<startRow>[a-zA-Z]+)(?P<startColumn>[1-9][0-9]*)(?::(?P<endRow>[a-zA-Z]+)(?P<endColumn>[1-9][0-9]*))?')
