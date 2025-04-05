import unittest
from reducible import (
    step_size,
    insert_word,
    find_word,
    is_reducible,
    get_longest_words,
)


class TestStepSize(unittest.TestCase):
    """step_size Test Suite which fixed constant of 3"""

    def test_1(self):
        """Test step_size with 'hi', expecting a return of 2."""
        actual = step_size("hi")
        self.assertEqual(actual, 2)

    def test_2(self):
        """Test step_size with 'find', expecting a return of 1."""
        actual = step_size("find")
        self.assertEqual(actual, 1)

    def test_3(self):
        """Test step_size with 'string', expecting a return of 3."""
        actual = step_size("string")
        self.assertEqual(actual, 3)

    def test_4(self):
        """Test step_size with 'yellow', expecting a return of 3."""
        actual = step_size("yellow")
        self.assertEqual(actual, 3)

    def test_5(self):
        """Test step_size with 'treats', expecting a return of 1."""
        actual = step_size("treats")
        self.assertEqual(actual, 1)

    def test_6(self):
        """Test step_size with 'strength', expecting a return of 1."""
        actual = step_size("strength")
        self.assertEqual(actual, 1)

    def test_7(self):
        """Test step_size with 'computer', expecting a return of 3."""
        actual = step_size("computer")
        self.assertEqual(actual, 3)

    def test_8(self):
        """Test step_size with 'teamwork', expecting a return of 3."""
        actual = step_size("teamwork")
        self.assertEqual(actual, 3)

    def test_9(self):
        """Test step_size with 'training', expecting a return of 3."""
        actual = step_size("training")
        self.assertEqual(actual, 3)

    def test_10(self):
        """Test step_size with 'inspiration', expecting a return of 1."""
        actual = step_size("inspiration")
        self.assertEqual(actual, 1)


class TestInsertWord(unittest.TestCase):
    """10 Tests for insert_word"""

    def test_1(self):
        """Test insert_word with "word" that should hash to an empty slot"""
        hash_table = ["", "", "", "", ""]
        hash_expected = ["word", "", "", "", ""]
        insert_word("word", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_2(self):
        """Test insert_word with "zebra" that should hash to an empty slot"""
        hash_table = ["", "", "", "", ""]
        hash_expected = ["", "", "zebra", "", ""]
        insert_word("zebra", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_3(self):
        """Test basic insert_word with two words that don't collide"""
        hash_table = ["", "", "", "", ""]
        hash_expected = ["word", "", "", "pie", ""]
        insert_word("word", hash_table)
        insert_word("pie", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_4(self):
        """Test insert_word with collision resolution "dog" and "straw" """
        hash_table = ["", "", "", "", ""]
        hash_expected = ["", "dog", "", "", "straw"]
        insert_word("dog", hash_table)
        insert_word("straw", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_5(self):
        """Test insert_word with collision resolution "bat" and "tab" """
        hash_table = ["", "", "", "", ""]
        hash_expected = ["", "bat", "", "tab", ""]
        insert_word("tab", hash_table)
        insert_word("bat", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_6(self):
        """Test insert_word with a word that collides"""
        hash_table = ["", "apple", "", "", "banana"]
        hash_expected = ["carrot", "apple", "", "", "banana"]
        insert_word("carrot", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_7(self):
        """Test insert_word filling up the hash table"""
        hash_table = ["", "", "", "", ""]
        hash_expected = ["apple", "date", "cherry", "banana", ""]
        insert_word("apple", hash_table)
        insert_word("banana", hash_table)
        insert_word("cherry", hash_table)
        insert_word("date", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_8(self):
        """Test insert_word with almost full table"""
        hash_table = ["grape", "kiwi", "lemon", "", "orange"]
        hash_expected = ["grape", "kiwi", "lemon", "pear", "orange"]
        insert_word("pear", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_9(self):
        """Test insert_word with multiple collisions and proper handling"""
        hash_table = ["", "", "", "", ""]
        hash_expected = ["", "dog", "straw", "bat", "tab"]
        insert_word("bat", hash_table)
        insert_word("dog", hash_table)
        insert_word("tab", hash_table)
        insert_word("straw", hash_table)
        self.assertEqual(hash_table, hash_expected)

    def test_10(self):
        """Test insert_word with duplicates"""
        hash_table = ["", "", "", "", ""]
        hash_expected = ["bus", "", "sub", "", ""]
        insert_word("sub", hash_table)
        insert_word("bus", hash_table)
        insert_word("bus", hash_table)
        insert_word("sub", hash_table)
        self.assertEqual(hash_table, hash_expected)


class TestFindWord(unittest.TestCase):
    """find_word Test Suite"""

    def test_1(self):
        """Test find_word for a word that exists in the hash table (no collision)"""
        hash_table = ["apple", "", "cherry", "banana", ""]
        self.assertTrue(find_word("banana", hash_table))  # Should return True

    def test_2(self):
        """Test find_word for a word that does not exist in the hash table (no collision)"""
        hash_table = ["apple", "", "", "banana", ""]
        self.assertFalse(find_word("cherry", hash_table))  # Should return False

    def test_3(self):
        """Test find_word for an empty hash table"""
        hash_table = ["", "", "", "", ""]
        self.assertFalse(find_word("apple", hash_table))  # Should return False

    def test_4(self):
        """Test find_word for a word at the start of the hash table"""
        hash_table = ["orange", "", "grape", "kiwi", "lemon"]
        self.assertTrue(find_word("orange", hash_table))  # Should return True

    def test_5(self):
        """Test find_word for a word at the end of the hash table"""
        hash_table = ["orange", "", "grape", "kiwi", "lemon"]
        self.assertTrue(find_word("lemon", hash_table))  # Should return True

    def test_6(self):
        """Test find_word a word at the middle of the hash table"""
        hash_table = ["orange", "", "grape", "kiwi", "lemon"]
        self.assertTrue(find_word("grape", hash_table))  # Should return True

    def test_7(self):
        """Test find_word for a word that is not in the hash table with 1 collisions"""
        hash_table = ["", "", "kiwi", "peach", ""]
        self.assertFalse(find_word("cherry", hash_table))  # Should return False

    def test_8(self):
        """Test find_word with 1 collision"""
        hash_table = ["", "", "", "leaps", "", "artel", ""]
        self.assertTrue(find_word("artel", hash_table))  # Should return True

    def test_9(self):
        """Test find_word that requires 2 collisions and wraps around"""
        hash_table = ["earst", "rates", "", "", "stear", "stare", ""]
        self.assertTrue(find_word("stear", hash_table))  # Should return True

    def test_10(self):
        """Test find_word that requires 3 collisions and wraps around before finding it doesn't exist"""
        hash_table = ["earst", "rates", "", "", "stear", "stare", ""]
        self.assertFalse(find_word("aster", hash_table))  # Should return False


class TestIsReducible(unittest.TestCase):
    """is_reducible Test Suite"""

    def test_1(self):
        """Test is_reducible with words that can all be reduced"""
        word_list = ["i", "it", "pit", "spit", "spite", "sprite"]
        m = 37
        hash_list = [
            "",
            "",
            "",
            "",
            "",
            "spite",
            "",
            "it",
            "spit",
            "i",
            "pit",
            "sprite",
            "",
        ]
        hash_memo = ["" for _ in range(m)]
        expected_out = [True] * 6
        expected_memo = [""] * m
        for i, index in enumerate([32, 7, 26, 15, 18]):
            expected_memo[index] = word_list[i + 1]
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_2(self):
        """Test is_reducible with words that cannot be reduced at all"""
        word_list = ["b", "c", "d", "e"]
        m = 37
        hash_list = ["", "", "b", "c", "d", "e", "", "", "", "", "", "", ""]
        hash_memo = ["" for _ in range(m)]
        expected_out = [False] * 4
        expected_memo = [""] * m
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_3(self):
        """Test is_reducible with vowels and short words that are 'reducible'"""
        word_list = ["a", "i", "o", "ai", "ao"]
        m = 37
        hash_list = ["", "a", "o", "ao", "", "", "", "", "", "ai", "", "", "i"]
        hash_memo = ["" for _ in range(m)]
        expected_out = [True] * 5
        expected_memo = [""] * m
        for i, index in enumerate([35, 4]):
            expected_memo[index] = word_list[i + 3]
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_4(self):
        """Test is_reducible with a mix of reducible and non-reducible words"""
        word_list = ["a", "o", "i", "cat", "dog", "bird"]
        m = 37
        hash_list = ["", "a", "o", "", "bird", "", "", "cat", "dog", "i", "", "", ""]
        hash_memo = ["" for _ in range(m)]
        expected_out = [True, True, True, False, False, False]
        expected_memo = [""] * m
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_5(self):
        """Test is_reducible with words that have a common letters"""
        word_list = ["spark", "park", "ark", "art", "a"]
        m = 37
        hash_list = ["", "ark", "", "a", "", "", "", "art", "", "", "", "spark", "park"]
        hash_memo = ["" for _ in range(m)]
        expected_out = [False, False, False, False, True]
        expected_memo = [""] * m
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_6(self):
        """Test is_reducible with longer words that are not reducible"""
        word_list = ["abracadabra", "abracadab", "abracada", "a"]
        m = 37
        hash_list = [
            "",
            "abracadabra",
            "abracadab",
            "a",
            "abracada",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        hash_memo = ["" for _ in range(m)]
        expected_out = [False, False, False, True]
        expected_memo = [""] * m
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_7(self):
        """Test is_reducible with a mix of short and long words"""
        word_list = ["string", "spite", "i", "olive", "o"]
        m = 37
        hash_list = [
            "",
            "",
            "o",
            "",
            "",
            "spite",
            "",
            "string",
            "",
            "i",
            "",
            "olive",
            "",
        ]
        hash_memo = ["" for _ in range(m)]
        expected_out = [False, False, True, False, True]
        expected_memo = [""] * m
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_8(self):
        """Test is_reducible with only single-letter words and some reducible words"""
        word_list = ["i", "o", "loop", "cook", "site"]
        m = 37
        hash_list = ["", "", "o", "loop", "", "site", "", "", "", "i", "", "cook", ""]
        hash_memo = ["" for _ in range(m)]
        expected_out = [True, True, False, False, False]
        expected_memo = [""] * m
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_9(self):
        """Test is_reducible with all words reducible"""
        word_list = [
            "a",
            "cat",
            "bat",
            "rat",
            "at",
        ]
        m = 37
        hash_list = ["", "a", "", "", "", "", "", "cat", "", "rat", "bat", "at", ""]
        hash_memo = ["" for _ in range(m)]
        expected_out = [True, True, True, True, True]  # 'at' and 'a' are reducible
        expected_memo = [
            "",
            "",
            "cat",
            "",
            "rat",
            "",
            "",
            "",
            "",
            "at",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "bat",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        for i, index in enumerate([2, 29, 4, 9]):
            expected_memo[index] = word_list[i + 1]
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)

    def test_10(self):
        """Test is_reducible with words that cannot be reduced"""
        word_list = ["e", "ee", "see", "sea", "se"]
        m = 37
        hash_list = ["", "sea", "", "", "", "e", "", "see", "ee", "se", "", "", ""]
        hash_memo = ["" for _ in range(m)]
        expected_out = [False, False, False, False, False]
        expected_memo = [""] * m
        actual_out = []
        for word in word_list:
            actual_out.append(is_reducible(word, hash_list, hash_memo))
        self.assertEqual(actual_out, expected_out)
        self.assertEqual(hash_memo, expected_memo)


class TestGetLongestWords(unittest.TestCase):
    """get_longest_words Test Suite"""

    def test_1(self):
        """Test get_longest_words with various lengths, final answers of length 6"""
        words = ["apple", "banana", "grape", "kiwi"]
        expected = ["banana"]
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_2(self):
        """Test get_longest_words with various lengths, final answers of length 9"""
        words = ["apple", "pineapple", "orange"]
        expected = ["pineapple"]
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_3(self):
        """Test get_longest_words with one word"""
        words = ["kiwi"]
        expected = ["kiwi"]
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_4(self):
        """Test get_longest_words with empty list"""
        words = []
        expected = []
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_5(self):
        """Test get_longest_words with all words of the same length"""
        words = ["cat", "dog", "bat"]
        expected = ["cat", "dog", "bat"]  # All have the same length
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_6(self):
        """Test get_longest_words with mixed lengths, final answers of length 10"""
        words = ["apple", "peach", "watermelon", "pear"]
        expected = ["watermelon"]
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_7(self):
        """Test get_longest_words with longer words, two tied"""
        words = ["cherry", "blueberry", "raspberry"]
        expected = ["blueberry", "raspberry"]  # All longest words
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_8(self):
        """Test get_longest_words with words in descending order of length"""
        words = ["melons", "cherry", "apple", "peach", "kiwi", "pear"]
        expected = ["melons", "cherry"]
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_9(self):
        """Test get_longest_words with words in ascending order of length"""
        words = ["kiwi", "pear", "apple", "peach", "melons", "cherry"]
        expected = ["cherry", "melons"]
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))

    def test_10(self):
        """Test get_longest_words with single letter words"""
        words = ["a", "b", "c", "d"]
        expected = ["a", "b", "c", "d"]
        actual = get_longest_words(words)
        self.assertEqual(sorted(actual), sorted(expected))


if __name__ == "__main__":
    unittest.main()
