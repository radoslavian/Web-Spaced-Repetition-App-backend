from django.test import TestCase

from cards.management.modules.fr_card_side import Question, Answer


class SoundExtractionTestCase(TestCase):
    """
    Sound paths and file names extraction tests.
    """

    @classmethod
    def setUpTestData(cls):
        cls.question_sound_file_rel_path = \
            "snds/Make_sentences_about_Ann_when_she_was_six.mp3"
        cls.question = ("<b>Definition</b>\n"
                        "Example"
                        f"<snd>{cls.question_sound_file_rel_path}</snd>")
        cls.question_sound_filename = \
            "Make_sentences_about_Ann_when_she_was_six.mp3"

        cls.answer = ("jocular ['d7Ckjul2(r)]\n"
                      "He, he, he! You will pardon me for being jocular."
                      "<snd>snds/he_joined_with_the_best_grace.mp3</snd>")
        cls.answer_sound_file_rel_path = \
            "snds/he_joined_with_the_best_grace.mp3"
        cls.answer_sound_filename = "he_joined_with_the_best_grace.mp3"

        # for testing question/answer with no snd tags
        cls.text_no_snd_tag = """bearing false witness
He accused his neighbour of bearing false witness against him."""

    def test_path_extraction_Question(self):
        """
        Should return path to the sound file embedded in an item's question.
        """
        item_question = Question(self.question)
        self.assertEqual(self.question_sound_file_rel_path,
                         item_question.sound_file_path)

    def test_path_extraction_Answer(self):
        """
        Should return path to the sound file embedded in an item's answer.
        """
        item_answer = Answer(self.answer)
        self.assertEqual(self.answer_sound_file_rel_path,
                         item_answer.sound_file_path)

    def test_path_extraction_Question_no_snd_tag(self):
        """
        Should return None if there is no <snd> tag in an item's question.
        """
        item_question = Question(self.text_no_snd_tag)
        self.assertEqual(None, item_question.sound_file_path)

    def test_path_extraction_Answer_no_snd_tag(self):
        """
        Should return None if there is no <snd> tag in an item's answer.
        """
        item_answer = Answer(self.text_no_snd_tag)
        self.assertEqual(None, item_answer.sound_file_path)

    def test_filename_extraction_Question(self):
        item_question = Question(self.question)
        self.assertEqual(self.question_sound_filename,
                         item_question.sound_file_name)

    def test_filename_extraction_Answer(self):
        item_answer = Answer(self.answer)
        self.assertEqual(self.answer_sound_filename,
                         item_answer.sound_file_name)

    def test_filename_extraction_Question_no_tag(self):
        item_question = Question(self.text_no_snd_tag)
        self.assertEqual(None, item_question.sound_file_name)

    def test_filename_extraction_Answer_no_tag(self):
        item_answer = Answer(self.text_no_snd_tag)
        self.assertEqual(None, item_answer.sound_file_name)


class ImageExtractionTestCase(TestCase):
    """
    Image paths and file names extraction tests.
    """

    @classmethod
    def setUpTestData(cls):
        cls.question = (
            "<b>Consuming or eager to consume great amounts of food;"
            " ravenous.</b>\nHe was fond of inviting them to tea; and, "
            "though vowing they never got a look in with him at the cakes and"
            " muffins, for it was the fashion to believe that his corpulence "
            "pointed to [...] appetite, and his [...] appetite to tapeworms,"
            " they accepted his invitations with real pleasure."
            "<img>../obrazy/sucker-Blutegelmeyer.jpg</img><snd>snds"
            "/english_examples_0622.mp3</snd>"
        )
        cls.question_rel_image_path = "../obrazy/sucker-Blutegelmeyer.jpg"
        cls.question_image_filename = "sucker-Blutegelmeyer.jpg"
        cls.question_no_image = "złożyć listy uwierzytelniające"

        cls.answer = (
            "It takes two to make a quarrel.\nJill: Why are you"
            " always so quarrelsome?\nJane: Hey, it's not just my fault. It"
            " takes two to make a quarrel."
            "<img>../obrazy/quarrel.png</img>"
            "<snd>snds/english_examples_3788.mp3</snd>"
        )
        cls.answer_rel_image_path = "../obrazy/quarrel.png"
        cls.answer_image_filename = "quarrel.png"
        cls.answer_no_image = (
            "mill cannot grind with water that is past\nIf you want to go "
            "abroad, do it now, while you're young and have the money."
            " The mill cannot grind with water that is past."
            "<snd>snds/english_examples_2856.mp3</snd>"
        )

    def test_Question_file_path(self):
        question = Question(self.question)
        self.assertEqual(self.question_rel_image_path,
                         question.image_file_path)

    def test_Answer_file_path(self):
        answer = Answer(self.answer)
        self.assertEqual(self.answer_rel_image_path,
                         answer.image_file_path)

    def test_Question_file_path_no_image_tag(self):
        """
        Should return None if there is no image in an item's question.
        """
        question = Question(self.question_no_image)
        self.assertEqual(None, question.image_file_path)

    def test_Answer_file_path_no_image_tag(self):
        """
        Should return None if there is no image in an item's answer.
        """
        answer = Answer(self.answer_no_image)
        self.assertEqual(None, answer.image_file_path)

    def test_Question_image_filename(self):
        item_question = Question(self.question)
        self.assertEqual(self.question_image_filename,
                         item_question.image_file_name)

    def test_Question_image_filename_no_image_tag(self):
        item_question = Question(self.question_no_image)
        self.assertEqual(None, item_question.image_file_name)

    def test_Answer_image_filename(self):
        item_answer = Answer(self.answer)
        self.assertEqual(self.answer_image_filename,
                         item_answer.image_file_name)

    def test_Answer_image_filename_no_image_tag(self):
        item_answer = Answer(self.answer_no_image)
        self.assertEqual(None, item_answer.image_file_name)


class QuestionSplitMediaTags(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.definition = "Some definition text"
        cls.example = "Example line 1"
        cls.question_only = (
            f"{cls.definition}"
            "<img>../obrazy/swimmer-mike-paget.jpg</img><snd>snds/not "
            "aware of or careful.mp3</snd>")
        cls.cleaned_question = cls.definition
        cls.question_example_snd = (
            f"<b>{cls.definition}</b>\n"
            f"{cls.example}"
            "<snd>snds/english_examples_2806.mp3</snd>")
        cls.question_example_img = (
            f"<b>{cls.definition}</b>\n"
            f"{cls.example}"
            "<img>../obrazy/wedding_077.jpg</img>")
        cls.question_example_all_media = (
            f"<b>{cls.definition}</b>\n"
            f"{cls.example}"
            "<img>../obrazy/wedding_077.jpg</img><snd>snds/english_"
            "examples_2806.mp3</snd>")

    def test_stripping_media_from_definition(self):
        """
        Removes media tags from cards with definition only (no example).
        """
        item_question = Question(self.question_only)
        self.assertEqual(item_question.definition,
                         self.cleaned_question)
        self.assertFalse(item_question.example)

    def test_stripping_snd(self):
        """
        Removes snd tag (with contents) from the card (definition and example).
        """
        question = Question(self.question_example_snd)
        self.assertEqual(question.definition, self.cleaned_question)
        self.assertEqual(question.example, self.example)

    def test_stripping_img(self):
        """
        No img tag (with contents) in the card (definition and example).
        """
        question = Question(self.question_example_img)
        self.assertEqual(question.definition, self.cleaned_question)
        self.assertEqual(question.example, self.example)

    def test_stripping_all_media_definition_example(self):
        """
        No media tags (and their contents) in the card (definition
        and example).
        """
        question = Question(self.question_example_all_media)
        self.assertEqual(question.definition, self.cleaned_question)
        self.assertEqual(question.example, self.example)


class QuestionDefinitionExampleTestCase(TestCase):
    """
    Tests definition and example from the Question
    + takes the definition from:
     - a card with a definition only
     - a card with a definition and an example sentence
    + removes the bold and italic tags (present in test data).
    """

    @classmethod
    def setUpTestData(cls):
        cls.basic_question = "basic question"
        cls.definition = "Definition for word in example"
        cls.example = "Example line 1 [...]\nLine 2"
        cls.example_transformed = "Example line 1 [...]<br/>Line 2"
        cls.question_example = (
            f"<b>{cls.definition}</b>\n"
            f"<i>{cls.example}</i>")

    def test_definition_only(self):
        """
        Card with definition and no example.
        """
        item_question = Question(self.basic_question)
        self.assertEqual(item_question.definition, self.basic_question)
        self.assertFalse(item_question.example)

    def test_definition(self):
        """
        Extracts definition from a card with a definition and example.
        """
        item_question = Question(self.question_example)
        self.assertEqual(item_question.definition, self.definition)

    def test_example(self):
        """
        Extracts example from a card with a definition and example.
        """
        item_question = Question(self.question_example)
        self.assertEqual(item_question.example, self.example_transformed)


class QuestionStrikeTag(TestCase):
    """
    All formatting tags in the Question side should be removed except <strike>.
    """
    @classmethod
    def setUpTestData(cls):
        question = ("definition: <i><strike>definition</strike></i>\n"
                    "example: <b><strike>example</strike></b>")
        cls.card_question = Question(question)

    def test_strike_in_definition(self):
        """
        Should keep <strike> tag in definition.
        """
        expected_output = "definition: <strike>definition</strike>"
        self.assertEqual(self.card_question.definition, expected_output)

    def test_strike_in_example(self):
        """
        Should keep <strike> tag in example.
        """
        expected_output = "example: <strike>example</strike>"
        self.assertEqual(self.card_question.example, expected_output)
