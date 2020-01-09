from pathlib import Path
from typing import List, Union


class StopWordEliminator(object):

    def __init__(self, path: Union[str, Path]) -> None:
        self._stop_words = self.load(path)

    def load(self, path: Union[str, Path]) -> List[str]:
        words = []
        with open(str(path), encoding='utf-8') as fin:
            for line in fin:
                word = line.strip()
                if word:
                    words.append(word)
        return words

    def __call__(self, tokens: List[str]) -> List[str]:
        cleansed_tokens = []
        for token in tokens:
            if token not in self._stop_words:
                cleansed_tokens.append(token)
        return cleansed_tokens
