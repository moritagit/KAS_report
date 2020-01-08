from typing import List, Dict, Union

import MeCab


class MeCabWordSplitter(object):
    def __init__(
        self,
        pos: bool = False,
        tag: bool = False,
        lemma: bool = False,
        dicdir: str = '',
        userdic: str = '',
        other_options: str = ''
    ) -> None:

        self._pos = pos
        self._tag = tag
        self._lemma = lemma
        self._wakati = not (pos or tag or lemma)

        options = ''
        if self._wakati:
            options += '-Owakati'
        if dicdir:
            options += f' -d {dicdir}'
        if userdic:
            options += f' -u {userdic}'
        if other_options:
            options += f' {other_options}'

        self.tagger = MeCab.Tagger(options)

    def __call__(self, sentence: str) -> Union[List[str], List[Dict]]:
        tokens = []
        if self._wakati:
            tokens = self.tagger.parse(sentence).strip().split()
        else:
            elems = self.tagger.parse(sentence).strip().splitlines()[:-1]  # eliminate EOS
            for elem in elems:
                text, fields = elem.split('\t')
                pos, tag_1, tag_2, tag_3, conjugation_type, conjugation, lemma, kana, utterance \
                    = fields.split(',')
                pos = pos if self._pos else None
                tag = ','.join((tag_1, tag_2, tag_3)) if self._tag else None
                lemma = lemma if self._lemma else None
                tokens.append(dict(text=text, lemma_=lemma, pos_=pos, tag_=tag))

        return tokens
