from typing import List, Dict, Union, Optional

import MeCab


class MeCabWordSplitter(object):
    def __init__(
        self,
        part_of_speechs: Optional[List[str]] = None,
        lemma: bool = False,
        return_pos: bool = False,
        return_tag: bool = False,
        return_lemma: bool = False,
        dicdir: str = '',
        userdic: str = '',
        other_options: str = ''
    ) -> None:

        self._part_of_speechs = part_of_speechs
        self._lemma = lemma  # used only when `part_of_speechs` input.

        self._return_pos = return_pos
        self._return_tag = return_tag
        self._return_lemma = return_lemma
        self._wakati = not (
            part_of_speechs or lemma
            or return_pos or return_tag or return_lemma
        )

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
        self.tagger.parse('')  # avoid error in `parseToNode` method

    def __call__(self, sentence: str) -> Union[List[str], List[Dict]]:
        tokens = []
        if self._wakati:
            tokens = self.tagger.parse(sentence).strip().split()
        elif self._part_of_speechs:
            nodes = self.tagger.parseToNode(sentence)
            tokens = []
            while nodes:
                token = nodes.surface
                features = nodes.feature.split(',')
                pos = features[0]
                if pos in self._part_of_speechs:
                    lemma = features[6]
                    if self._lemma and (lemma != '*'):
                        token = lemma
                    tokens.append(token)
                nodes = nodes.next
        else:
            elems = self.tagger.parse(sentence).strip().splitlines()[:-1]  # eliminate EOS
            for elem in elems:
                token, fields = elem.split('\t')
                pos, tag_1, tag_2, tag_3, conjugation_type, conjugation, lemma, kana, utterance \
                    = fields.split(',')
                pos = pos if self._pos else None
                tag = ','.join((tag_1, tag_2, tag_3)) if self._tag else None
                lemma = lemma if self._lemma else None
                tokens.append(dict(text=token, lemma_=lemma, pos_=pos, tag_=tag))

        return tokens
