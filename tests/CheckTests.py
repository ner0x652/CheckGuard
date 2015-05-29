__author__ = 'nero_luci'


from src import CheckParser
import re
import unittest


class ParserIniPosTest(unittest.TestCase):
    def setUp(self):
        self.testObj = CheckParser.CheckParser(0)
        print("ParserIniPos SetUp executed")

    def tearDown(self):
        self.testObj = None
        print("ParserIniPos TearDown executed")

    def test_ini_pos(self):
        self.assertEqual(self.testObj.position, 0, "Initial position is not 0")

    def test_changed_pos(self):
        self.testObj.position = 1
        self.assertEqual(self.testObj.position, 1, "Initial position didn't change")

    def test_negative_pos(self):
        self.assertRaises(ValueError, CheckParser.CheckParser, -1)


class FileWriteReadTest(unittest.TestCase):
    def setUp(self):
        self.filename = r"C:\Users\nero_luci\Desktop\GitHub\CheckGuard\tests\pos.txt"
        print("FileWriteRead SetUp executed")

    def tearDown(self):
        print("FileWriteRead TearDown executed")

    def test_write_2_file(self):
        value_2_file = "0"
        CheckParser.write_init_pos(value_2_file)
        with open(self.filename, "r") as tf:
            expected = tf.read()
        self.assertEqual(expected, value_2_file, "File writing failed")

    def test_read_from_file(self):
        expected = 0
        read_value = CheckParser.read_init_pos()
        self.assertEqual(expected, read_value, "File reading failed")


class RegexTest(unittest.TestCase):
    def setUp(self):
        self.test_line_1 = "1 x #2    mere pere  @ 0,01                0%  0,01"
        self.test_line_2 = "2 x #33    hubba bubba  @ 12,50                24%  0,01"
        self.test_line_3 = "cnaldknpinda    %  @ xx \/'*&"

    def tearDown(self):
        pass

    def test_price_regex_1(self):
        reg_ex = re.search('\d+\,\d+', self.test_line_1)
        self.assertIsNotNone(reg_ex, "Regex price is not valid: test 1")

    def test_price_regex_2(self):
        reg_ex = re.search('\d+\,\d+', self.test_line_2)
        self.assertIsNotNone(reg_ex, "Regex price is not valid: test 2")

    def test_qty_regex_1(self):
        reg_ex = re.search('\d+', self.test_line_1)
        self.assertIsNotNone(reg_ex, "Regex quantity is not valid: test 1")

    def test_qty_regex_2(self):
        reg_ex = re.search('\d+', self.test_line_2)
        self.assertIsNotNone(reg_ex, "Regex quantity is not valid: test 2")

    def test_qty_regex_3(self):
        reg_ex = re.search('\d+', self.test_line_3)
        self.assertIsNone(reg_ex, "Regex quantity is not valid: test 3")

    def test_tva_regex_1(self):
        reg_ex = re.search('\d{1,2}%', self.test_line_1)
        self.assertIsNotNone(reg_ex, "Regex tva is not valid: test 1")

    def test_tva_regex_2(self):
        reg_ex = re.search('\d{1,2}%', self.test_line_2)
        self.assertIsNotNone(reg_ex, "Regex tva is not valid: test 2")

    def test_name_regex_1(self):
        reg_ex = re.search('[a-zA-Z]{2,}[\S\s]?[a-zA-Z]*', self.test_line_1)
        self.assertIsNotNone(reg_ex, "Regex name is not valid: test 1")

    def test_name_regex_2(self):
        reg_ex = re.search('[a-zA-Z]{2,}[\S\s]?[a-zA-Z]*', self.test_line_3)
        self.assertIsNotNone(reg_ex, "Regex name is not valid: test 2")


class ParserReadCheckFile(unittest.TestCase):
    """
    For this test you should comment 2 lines in CheckParser.py read_file():
    self.generate_new_check()
    self.check_data = []
    """
    def setUp(self):
        self.testObj = CheckParser.CheckParser(0, r"C:\Users\nero_luci\Desktop\GitHub\CheckGuard\tests\files.txt")
        self.testObj2 = CheckParser.CheckParser(0, r"C:\Users\nero_luci\Desktop\GitHub\CheckGuard\tests\files2.txt")
        self.expected_check_1 = ["1 x #2    bacsis  @ 0,01                0%  0,01  \r\n",
                        "1 x #1    extra  @ 0,10                24%  0,10  \r\n"]
        self.expected_check_2 = []

    def test_data_1(self):
        self.testObj.read_file()
        self.assertListEqual(self.testObj.check_data, self.expected_check_1, "Lists are not equal: test 1")

    def test_data_2(self):
        self.testObj2.read_file()
        self.assertListEqual(self.testObj2.check_data, self.expected_check_2, "Lists are not equal: test 2")

testList = [ParserIniPosTest, FileWriteReadTest, RegexTest, ParserReadCheckFile]
testLoad = unittest.TestLoader()

caseList = []
for testCase in testList:
    testSuite = testLoad.loadTestsFromTestCase(testCase)
    caseList.append(testSuite)

checkGuardTestSuite = unittest.TestSuite(caseList)
runner = unittest.TextTestRunner()
runner.run(checkGuardTestSuite)