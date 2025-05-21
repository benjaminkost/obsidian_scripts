import unittest

from findAllReferences import check_str_in_mytags


class MyTestCase(unittest.TestCase):
    def test_check_str_in_mytags(self):
        # Give
        str_file ="""
        ---
        "created date:": 20.05.2025 13:40
        mytags:
          - "[[convolutional neural networks]]"
          - "[[Paper - AKWI - Cybersicherheit und Künstliche Intelligenz Innovationen für eine sichere digitale Zukunft]]"
          - "[[Arbeitskreis Wirtschaftsinformatik an Hochschulen für angewandte Wissenschaften|AKWI]]"
          - "[[Cybersicherheit und Künstliche Intelligenz Innovationen für eine sichere digitale Zukunft]]"
          - "[[Paper in Stichpunkten]]"
          - "[[einleitung]]"
        tags:
          - baby
          - wissenschaftlicheArbeit
          - paper
        aliases: 
        parent: 
        siblings: 
        child: 
        conference: "[[Cybersicherheit und Künstliche Intelligenz Innovationen für eine sichere digitale Zukunft]]"
        publish:
        ---
        # Fragen
        -> Themenbereich: wissenschaftlichen Beitrag, gesellschaftlicher und wirtschaftlicher Beitrag
        - Bilderkennung -> OCR ist lange genutzt Methode wurde aber weiterentwickelt (wurde in der Post in der USA genutzt) -> Einsatz von Sprachmodellen (Transformer) können auch für Bilderkennung genutzt werden
        - Das problem Digitalisierung von Schachpartieformular wurde kommerziell bearbeitet oder nur mit close source beschrieben -> Hiermit ist meine Arbeit, die erstmalig opensource von der Modell Architektur bis zur produktiven Veröffentlichung diesen Prozess beschreibt und anderen zur Verfügung gibt
        - Prototyp, der in einem unkonventionellen und nicht kommerziellen Use Case 
        - Mehrwert Architektur: Microservice, MLOps
        - gesellschaftlicher Beitrag: für Breitensport Tool zur Digital, inklusive Komponente -> Menschen, die ... 
        - wirtschaftlicher Beitrag: gezielt nicht kommerzieller Prototyp -> für die Gesellschaft geeignet
        """

        # When
        bool_first_tag_exists = check_str_in_mytags(str_file, "Paper in Stichpunkten")
        bool_second_tag_exists = check_str_in_mytags(str_file, "einleitung")
        bool_third_tag_exists = check_str_in_mytags(str_file, "Paper in Stichpunkten")
        bool_fourth_tag_exists = check_str_in_mytags(str_file, "convolutional neural networks")
        bool_fifth_tag_exists = check_str_in_mytags(str_file, "abcd")

        # Then
        self.assertEqual(bool_first_tag_exists, True)  # add assertion here
        self.assertEqual(bool_second_tag_exists, True)  # add assertion here
        self.assertEqual(bool_third_tag_exists, True)  # add assertion here
        self.assertEqual(bool_fourth_tag_exists, True)  # add assertion here
        self.assertEqual(bool_fifth_tag_exists, False)  # add assertion here

if __name__ == '__main__':
    unittest.main()
