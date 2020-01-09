import re


class NumberCrasher(object):
    def __init__(self):
        self._pattern = re.compile(r'\d+')

    def __call__(self, sentence: str) -> str:
        cleased = self._pattern.sub('0', sentence)
        return cleased
