from io import StringIO

from django.test import TestCase
from django.core.management import call_command

from cards.management.modules.phonetics_converter import PhoneticsConverter, \
    Token


class CLIImportingMemorizedCardsTestCase(TestCase):
    """
    Importing cards and their user review-data.
    """
    command = "import_fr_memorized_cards"

    def setUp(self):
        self.command_output = StringIO()

    def get_stripped_command_output(self):
        return self.command_output.getvalue().rstrip()

    def test_calling_from_cli(self):
        """
        An import command is available at all.
        """
        expected_command_output = "no input file specified"
        call_command(self.command, stdout=self.command_output)

        self.assertEqual(self.get_stripped_command_output(),
                         expected_command_output)

    def test_file_not_found(self):
        """
        An attempt to import data from a non-existent file.
        """
        expected_command_output = ("the /fake/directory/file.xml file was"
                                   " not found")
        filename = "/fake/directory/file.xml"
        opts = {"inputfile": filename}

        call_command(self.command, stdout=self.command_output, **opts)

        self.assertEqual(self.get_stripped_command_output(),
                         expected_command_output)


class ConvertPhoneticsTestCase(TestCase):
    def test_immutable_tokens(self):
        """
        The "tokens" property can not be mutated from outside the class object.
        """
        converter = PhoneticsConverter("Fake")
        def this_fails():
            converter.tokens = "abc"

        self.assertRaises(AttributeError, this_fails)

    def test_single_char_token(self):
        lexeme = "a"
        expected_token_representation = "SINGLE_CHAR a"
        received_token_representation = str(Token(lexeme))

        self.assertEqual(expected_token_representation,
                         received_token_representation)

    def test_multichar_token(self):
        lexeme = "(2)"
        expected_token_representation = "MULTI_CHAR (2)"
        received_token_representation = str(Token(lexeme))

        self.assertEqual(expected_token_representation,
                         received_token_representation)

    def test_token_for_unrecognized_lexeme(self):
        lexeme = "璃"
        expected_representation = ["UNRECOGNIZED 璃"]
        converter = PhoneticsConverter(lexeme)
        received_token_representation = [
            str(_token) for _token in converter.tokens]

        self.assertEqual(expected_representation,
                         received_token_representation)

    # def test_single_character_conversion(self):
    #     converter = PhoneticsConverter("2")
    #     converted_phonetics = converter.get_converted()
    #     expected_phonetics = ('<span class=phonetics '
    #                           'title="ə - as in another">ə</span>')
    #
    #     self.assertEqual(converted_phonetics, expected_phonetics)

    def test_scan_singlechar_token(self):
        lexeme = "r"
        converter = PhoneticsConverter(lexeme)
        tokens = [str(_token) for _token in converter.tokens]
        expected_tokens = [str(Token(lexeme))]

        self.assertEqual(tokens, expected_tokens)

    def test_scan_multichar_token(self):
        lexeme = "a2(r)"
        converter = PhoneticsConverter(lexeme)
        tokens = [str(_token) for _token in converter.tokens]
        expected_tokens = [str(Token(lexeme))]

        self.assertEqual(tokens, expected_tokens)

    def test_longest_available_lexeme(self):
        converter = PhoneticsConverter("fake_phonetics")
        longest_lexeme = 5
        self.assertEqual(converter.longest_lexeme, longest_lexeme)

    def test_shortest_longest_lexeme(self):
        """
        Should recognize the longest lexeme surrounded by single characters.
        """
        lexeme = "ra2(r)r"
        converter = PhoneticsConverter(lexeme)
        tokens = [str(token) for token in converter.tokens]
        expected_tokens = [str(Token(token))
                           for token in ["r", "a2(r)", "r"]]

        self.assertEqual(tokens, expected_tokens)

    def test_phonetics_description(self):
        """
        Calling a Token object in a function-like manner returns target output
        string, such as:
        <span class=”phonetics” title=”a - description of a”>a</span>
        """
        description = "aʊə - our - as in sour"
        phonetic_character = "aʊə"
        lexeme = "a2(r)"
        token = Token(lexeme, description=description,
                      phonetic_character=phonetic_character)
        expected_output = ('<span class="phonetics-entity" title="aʊə - our '
                           '- as in sour">aʊə</span>')
        received_output = token.html_output

        self.assertEqual(expected_output, received_output)

    def test_phonetics_for_unrecognized_character(self):
        lexeme = "璃"
        token = Token(lexeme, token_type="UNRECOGNIZED")
        expected_output = ('<span class="phonetics-entity" title='
                           f'"unrecognized phonetics">{lexeme}</span>')
        received_output = token.html_output

        self.assertEqual(expected_output, received_output)

    def test_converting_phonetics(self):
        # actually an acceptance test
        input_phonetics = "A(e)t3I"
        converter = PhoneticsConverter(input_phonetics)
        expected_html_phonetics = ('<span class="phonetics-entity" title="a -'
                                   ' as in trap">a</span><span class='
                                   '"phonetics-entity" title="(ə) - as in '
                                   'beaten">(ə)</span><span class="phonetics-'
                                   'entity" title="tʃ - tch - as in chop,'
                                   ' ditch">tʃ</span><span class="phonetics'
                                   '-entity" title="ɪ - i - as in pit, hill or'
                                   ' y - as in happy">ɪ</span>')
        self.assertEqual(converter.converted_phonetics,
                         expected_html_phonetics)
