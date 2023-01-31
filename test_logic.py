import unittest
import ecc_logic


class TestLogicMethods(unittest.TestCase):
    def test_can_match_genders(self):
        m = 'Male'
        f = 'Female'
        fu = 'Futa'
        test_cases = [
            # gender1, gender2, expected result
            (m, m, True),
            (f, f, True),
            (fu, fu, True),
            (m, f, False),
            (f, m, False),
            (m, fu, False),
            (fu, m, False),
            (f, fu, True),
            (fu, f, True)
        ]

        for test_case in test_cases:
            g1 = test_case[0]
            g2 = test_case[1]
            expected_result = test_case[2]
            result = ecc_logic.can_match_genders(g1, g2)
            self.assertTrue(expected_result == result, msg=test_case)

    # def test_is_morph_name_in_morph_list(self):
    #     morph_list = [{'name': 'a'}, {'name': 'b'}, {}]
    #     test_cases = [
    #         ('a', True),
    #         ('c', False)
    #     ]
    #     for test_case in test_cases:
    #         morph_name = test_case[0]
    #         expected_result = test_case[1]
    #         result = ecc_logic.morphname_in_morphlist(morph_name, morph_list)
    #         self.assertTrue(expected_result == result, msg=test_case)

    def test_morph_constructor(self):
        m = ecc_logic.Morph()
        self.assertTrue(m.name == '' and m.uid == '' and m.value == 0.0)
        m = ecc_logic.Morph('hi', 'ho', 0.5)
        self.assertTrue(m.name == 'hi' and m.uid == 'ho' and m.value == 0.5)
        m = ecc_logic.Morph('hi')
        self.assertTrue(m.name == 'hi' and m.uid == '' and m.value == 0.0)
        m = ecc_logic.Morph(value=0.3)
        self.assertTrue(m.name == '' and m.uid == '' and m.value == 0.3)


if __name__ == '__main__':
    unittest.main()
