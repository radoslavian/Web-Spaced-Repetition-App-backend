import re

from cards.management.fr_importer.modules.card_side import CardSide
from cards.management.fr_importer.modules.phonetics_converter import \
    PhoneticsConverter
from cards.utils.helpers import compose


class Answer(CardSide):
    def __init__(self, answer):
        """
        answer - content of <item><a></a></item> tags.
        """
        super().__init__(answer)
        self.phonetics_pattern = r"\[[\w\d'^_\-():]+]"

    def _get_phonetics_key(self) -> str | None:
        matched_line = self._match_phonetics_line()
        return matched_line["phonetics_key"]

    def _match_phonetics_line(self) -> dict:
        words = self._get_split_phonetics_line()
        phonetics_line = {"phonetics_key": None,
                          "phonetics": None,
                          "remaining_text": None}
        match len(words):
            case 0:
                pass
            case 1:
                phonetics_line["phonetics_key"] = words[0]
            case _:
                if re.match(f"^{self.phonetics_pattern}$", words[1]):
                    phonetics_line["phonetics_key"] = words[0]
                    phonetics_line["phonetics"] = words[1]

        return phonetics_line

    def _get_split_phonetics_line(self) -> list:
        try:
            phonetics_line = self._get_line(1)
        except IndexError:
            return []
        return phonetics_line.split(" ")

    def _get_raw_phonetics(self) -> str | None:
        phonetics_in_answer_line = None
        output_phonetics = None
        phonetics_in_phonetics_line = self._match_phonetics_line()["phonetics"]

        if not phonetics_in_phonetics_line:
            phonetics_in_answer_line = self._get_phonetics_from_answer_line()

        phonetics = (phonetics_in_phonetics_line
                     or phonetics_in_answer_line or None)

        if phonetics:
            # [1:-1] cuts brackets
            output_phonetics = phonetics[1:-1]

        return output_phonetics

    def _get_phonetics_from_answer_line(self) -> str | None:
        matched_phonetics = re.findall(self.phonetics_pattern,
                                       self._get_line(0))
        if matched_phonetics:
            return matched_phonetics[0]
        return None

    def _get_formatted_phonetics(self) -> str | None:
        raw_phonetics = self.raw_phonetics
        formatted_phonetics = None
        if raw_phonetics is not None:
            formatted_phonetics = PhoneticsConverter(
                self.raw_phonetics).converted_phonetics
        return formatted_phonetics

    def _get_example_sentences(self) -> list:
        if self.phonetics_key:
            starting_line = 2
        else:
            starting_line = 1
        sentences = self._strip_media_tags(self.side_contents)
        split_sentences = sentences.splitlines()[starting_line:]

        return self._clean_sentences(split_sentences)

    @property
    def _clean_sentences(self):
        functions = [
            list,
            lambda lines: map(lambda line: self._merge_characters(
                " ", line), lines),
            lambda lines: map(
                lambda lns: self.strip_tags_except_specific(lns), lines)
        ]

        return compose(*functions)

    def _get_output_text(self) -> str:
        answer_block = self._get_answer_block()
        phonetics_block = self._get_phonetics_component()
        example_sentences = "".join(f"<p><span>{sentence}</span></p>"
                                    for sentence in self.example_sentences)
        example_sentences_block = (
            f'<div class=”answer-example-sentences”>{example_sentences}</div>'
            if example_sentences else None)
        answer_side = [answer_block, phonetics_block, example_sentences_block]

        return "".join(filter(None, answer_side))

    def _get_phonetics_component(self):
        component = None
        if self.formatted_phonetics_key and self.phonetics_block:
            component = (
                f'<div class="phonetics">{self.formatted_phonetics_key} '
                f'{self.phonetics_block}</div>')
        elif self.formatted_phonetics_key:
            component = (f'<div class="phonetics">'
                         f'{self.formatted_phonetics_key}</div>')
        return component

    def _get_answer_block(self):
        if not self.formatted_phonetics_key and self.phonetics_block:
            output = (f'<div class="answer">{self.answer} '
                      + f"{self.phonetics_block}</div>")
        else:
            output = f'<div class="answer">{self.answer}</div>'
        return output

    def _get_answer(self):
        answer_line = self._get_line(0)
        answer_line_split = re.split(self.phonetics_pattern, answer_line)
        return answer_line_split[0].strip()

    answer = property(_get_answer,
                      doc="The main answer is usually located in"
                          " the first line of an answer side"
                          " of a card.")
    phonetics_key = property(_get_phonetics_key)
    raw_phonetics = property(_get_raw_phonetics)
    phonetics_block = property(lambda self:
        f'<span class="phonetic-spelling">'
        f'[{self.formatted_phonetics}]'
        f'</span>' if self.raw_phonetics else None)
    formatted_phonetics_key = property(lambda self:
        f'<span class="phonetic-key">'
        f'{self.phonetics_key}</span>'
        if self.phonetics_key else None)
    formatted_phonetics = property(_get_formatted_phonetics)
    example_sentences = property(_get_example_sentences)
