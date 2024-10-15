import re
from typing import List, Tuple, Union, Dict
from collections import defaultdict, Counter
import json
import xml.etree.ElementTree as ET
import argparse
import sys

class StringAlgorithms:
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Inputs must be strings")

        if len(s1) < len(s2):
            return StringAlgorithms.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

    @staticmethod
    def longest_common_substring(s1: str, s2: str) -> str:
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Inputs must be strings")

        m = [[0] * (1 + len(s2)) for _ in range(1 + len(s1))]
        longest, x_longest = 0, 0
        for x in range(1, 1 + len(s1)):
            for y in range(1, 1 + len(s2)):
                if s1[x - 1] == s2[y - 1]:
                    m[x][y] = m[x - 1][y - 1] + 1
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
                else:
                    m[x][y] = 0
        return s1[x_longest - longest: x_longest]

    @staticmethod
    def kmp_search(text: str, pattern: str) -> int:
        if not isinstance(text, str) or not isinstance(pattern, str):
            raise TypeError("Inputs must be strings")

        if not pattern:
            return 0

        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        i = j = 0
        while i < len(text):
            if pattern[j] == text[i]:
                i += 1
                j += 1
            if j == len(pattern):
                return i - j
            elif i < len(text) and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return -1

    @staticmethod
    def rabin_karp_search(text: str, pattern: str) -> List[int]:
        if not isinstance(text, str) or not isinstance(pattern, str):
            raise TypeError("Inputs must be strings")

        if not pattern:
            return [0] if text else []

        d = 256
        q = 101
        m, n = len(pattern), len(text)
        p = t = 0
        h = 1
        result = []

        for i in range(m - 1):
            h = (h * d) % q

        for i in range(m):
            p = (d * p + ord(pattern[i])) % q
            t = (d * t + ord(text[i])) % q

        for i in range(n - m + 1):
            if p == t:
                if pattern == text[i:i+m]:
                    result.append(i)
            if i < n - m:
                t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
                if t < 0:
                    t += q

        return result

    @staticmethod
    def z_function(s: str) -> List[int]:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        n = len(s)
        z = [0] * n
        l, r = 0, 0
        for i in range(1, n):
            if i <= r:
                z[i] = min(r - i + 1, z[i - l])
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                z[i] += 1
            if i + z[i] - 1 > r:
                l, r = i, i + z[i] - 1
        return z

    @staticmethod
    def manacher_algorithm(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        t = '#' + '#'.join(s) + '#'
        n = len(t)
        p = [0] * n
        c = r = 0
        for i in range(n):
            mirror = 2 * c - i
            if i < r:
                p[i] = min(r - i, p[mirror])
            while i + 1 + p[i] < n and i - 1 - p[i] >= 0 and t[i + 1 + p[i]] == t[i - 1 - p[i]]:
                p[i] += 1
            if i + p[i] > r:
                c, r = i, i + p[i]
        max_len, center = max((p[i], i) for i in range(n))
        return s[(center - max_len) // 2: (center + max_len) // 2]

    @staticmethod
    def aho_corasick(patterns: List[str]) -> callable:
        if not all(isinstance(p, str) for p in patterns):
            raise TypeError("All patterns must be strings")

        def make_trie():
            trie = {0: {}}
            states = 1

            for pattern in patterns:
                state = 0
                for char in pattern:
                    if char not in trie[state]:
                        trie[state][char] = states
                        trie[states] = {}
                        states += 1
                    state = trie[state][char]
                trie[state]['#'] = pattern
            return trie

        def make_failure(trie):
            failure = {0: 0}
            queue = []
            for char, state in trie[0].items():
                failure[state] = 0
                queue.append(state)

            while queue:
                state = queue.pop(0)
                for char, next_state in trie[state].items():
                    if char != '#':
                        queue.append(next_state)
                        f = failure[state]
                        while f > 0 and char not in trie[f]:
                            f = failure[f]
                        if char in trie[f]:
                            f = trie[f][char]
                        failure[next_state] = f

            return failure

        trie = make_trie()
        failure = make_failure(trie)

        def search(text):
            state = 0
            results = defaultdict(list)

            for i, char in enumerate(text):
                while state > 0 and char not in trie[state]:
                    state = failure[state]
                if char in trie[state]:
                    state = trie[state][char]
                f = state
                while f > 0:
                    if '#' in trie[f]:
                        results[trie[f]['#']].append(i - len(trie[f]['#']) + 1)
                    f = failure[f]

            return results

        return search

    @staticmethod
    def boyer_moore(text: str, pattern: str) -> List[int]:
        if not isinstance(text, str) or not isinstance(pattern, str):
            raise TypeError("Inputs must be strings")

        def build_last_occurrence(pattern):
            last = defaultdict(lambda: -1)
            for i, char in enumerate(pattern):
                last[char] = i
            return last

        def build_good_suffix(pattern):
            m = len(pattern)
            suffix = [m] * (m + 1)
            for i in range(m - 1, -1, -1):
                j = i
                while j >= 0 and pattern[j] == pattern[m - 1 - i + j]:
                    j -= 1
                suffix[i] = i - j
            return suffix

        m, n = len(pattern), len(text)
        last = build_last_occurrence(pattern)
        suffix = build_good_suffix(pattern)

        i = 0
        results = []
        while i <= n - m:
            j = m - 1
            while j >= 0 and pattern[j] == text[i + j]:
                j -= 1
            if j < 0:
                results.append(i)
                i += suffix[0]
            else:
                i += max(suffix[j + 1], j - last[text[i + j]])

        return results

    @staticmethod
    def longest_palindromic_subsequence(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        n = len(s)
        dp = [[0] * n for _ in range(n)]

        for i in range(n):
            dp[i][i] = 1

        for cl in range(2, n + 1):
            for i in range(n - cl + 1):
                j = i + cl - 1
                if s[i] == s[j] and cl == 2:
                    dp[i][j] = 2
                elif s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

        def backtrack(i, j):
            if i > j:
                return ""
            if i == j:
                return s[i]
            if s[i] == s[j]:
                return s[i] + backtrack(i + 1, j - 1) + s[j]
            if dp[i + 1][j] > dp[i][j - 1]:
                return backtrack(i + 1, j)
            return backtrack(i, j - 1)

        return backtrack(0, n - 1)

    @staticmethod
    def longest_repeating_substring(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        n = len(s)
        dp = [[0] * n for _ in range(n)]
        max_len = 0
        max_end = 0

        for i in range(n):
            for j in range(n):
                if s[i] == s[j] and i != j:
                    if i > 0 and j > 0:
                        dp[i][j] = dp[i-1][j-1] + 1
                    else:
                        dp[i][j] = 1
                    if dp[i][j] > max_len:
                        max_len = dp[i][j]
                        max_end = i

        return s[max_end - max_len + 1 : max_end + 1]

    @staticmethod
    def parse_json(json_string: str) -> Union[dict, list]:
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

    @staticmethod
    def generate_json(data: Union[dict, list]) -> str:
        try:
            return json.dumps(data, indent=2)
        except TypeError as e:
            raise ValueError(f"Cannot convert to JSON: {e}")

    @staticmethod
    def parse_xml(xml_string: str) -> ET.Element:
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML string: {e}")

    @staticmethod
    def generate_xml(root: ET.Element) -> str:
        return ET.tostring(root, encoding='unicode')

    @staticmethod
    def compress_string(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        compressed = []
        count = 1
        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                count += 1
            else:
                compressed.append(s[i-1] + str(count))
                count = 1
        compressed.append(s[-1] + str(count))
        compressed_str = ''.join(compressed)
        return compressed_str if len(compressed_str) < len(s) else s

    @staticmethod
    def decompress_string(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        result = []
        i = 0
        while i < len(s):
            char = s[i]
            i += 1
            count = ''
            while i < len(s) and s[i].isdigit():
                count += s[i]
                i += 1
            result.append(char * int(count or 1))
        return ''.join(result)

    @staticmethod
    def is_anagram(s1: str, s2: str) -> bool:
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Inputs must be strings")

        return Counter(s1) == Counter(s2)

    @staticmethod
    def is_palindrome(s: str) -> bool:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        s = ''.join(c.lower() for c in s if c.isalnum())
        return s == s[::-1]

    @staticmethod
    def longest_common_prefix(strs: List[str]) -> str:
        if not all(isinstance(s, str) for s in strs):
            raise TypeError("All inputs must be strings")

        if not strs:
            return ""

        prefix = strs[0]
        for s in strs[1:]:
            while s.find(prefix) != 0:
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix

    @staticmethod
    def edit_distance(s1: str, s2: str) -> int:
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Inputs must be strings")

        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

        return dp[m][n]

    @staticmethod
    def longest_increasing_subsequence(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        n = len(s)
        dp = [1] * n
        prev = [-1] * n

        for i in range(1, n):
            for j in range(i):
                if s[i] > s[j] and dp[i] < dp[j] + 1:
                    dp[i] = dp[j] + 1
                    prev[i] = j

        max_len = max(dp)
        max_index = dp.index(max_len)

        result = []
        while max_index != -1:
            result.append(s[max_index])
            max_index = prev[max_index]

        return ''.join(reversed(result))

    @staticmethod
    def string_matching(text: str, pattern: str) -> List[int]:
        if not isinstance(text, str) or not isinstance(pattern, str):
            raise TypeError("Inputs must be strings")

        return [m.start() for m in re.finditer(f'(?={re.escape(pattern)})', text)]

    @staticmethod
    def count_substrings(s: str) -> int:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        n = len(s)
        dp = [[0] * n for _ in range(n)]
        count = 0

        for i in range(n-1, -1, -1):
            for j in range(i, n):
                if i == j:
                    dp[i][j] = 1
                elif j == i + 1:
                    dp[i][j] = 2 if s[i] == s[j] else 1
                else:
                    dp[i][j] = dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]
                    if s[i] == s[j]:
                        dp[i][j] += dp[i+1][j-1] + 1
                count += dp[i][j]

        return count

    @staticmethod
    def longest_substring_without_repeating(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        n = len(s)
        char_index = {}
        start = max_length = 0
        max_start = 0

        for i in range(n):
            if s[i] in char_index and start <= char_index[s[i]]:
                start = char_index[s[i]] + 1
            else:
                if i - start + 1 > max_length:
                    max_length = i - start + 1
                    max_start = start
            char_index[s[i]] = i
        
        return s[max_start:max_start + max_length]

    @staticmethod
    def string_rotation(s1: str, s2: str) -> bool:
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Inputs must be strings")

        if len(s1) != len(s2):
            return False
        return s2 in s1 + s1

    @staticmethod
    def reverse_words(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        return ' '.join(reversed(s.split()))

    @staticmethod
    def string_permutations(s: str) -> List[str]:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        def backtrack(start):
            if start == len(s):
                result.append(''.join(s))
            else:
                for i in range(start, len(s)):
                    s[start], s[i] = s[i], s[start]
                    backtrack(start + 1)
                    s[start], s[i] = s[i], s[start]

        s = list(s)
        result = []
        backtrack(0)
        return result

    @staticmethod
    def longest_common_subsequence(s1: str, s2: str) -> str:
        if not isinstance(s1, str) or not isinstance(s2, str):
            raise TypeError("Inputs must be strings")

        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if s1[i-1] == s2[j-1]:
                lcs.append(s1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1

        return ''.join(reversed(lcs))

    @staticmethod
    def regex_match(s: str, p: str) -> bool:
        if not isinstance(s, str) or not isinstance(p, str):
            raise TypeError("Inputs must be strings")

        return bool(re.match(f'^{p}$', s))

    @staticmethod
    def wildcard_match(s: str, p: str) -> bool:
        if not isinstance(s, str) or not isinstance(p, str):
            raise TypeError("Inputs must be strings")

        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True

        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[0][j] = dp[0][j-1]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j-1] == '*':
                    dp[i][j] = dp[i][j-1] or dp[i-1][j]
                elif p[j-1] == '?' or s[i-1] == p[j-1]:
                    dp[i][j] = dp[i-1][j-1]

        return dp[m][n]

    @staticmethod
    def string_compression(s: str) -> str:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        result = []
        count = 1
        for i in range(1, len(s)):
            if s[i] == s[i-1]:
                count += 1
            else:
                result.append(s[i-1] + str(count))
                count = 1
        result.append(s[-1] + str(count))
        compressed = ''.join(result)
        return compressed if len(compressed) < len(s) else s

    @staticmethod
    def is_valid_parentheses(s: str) -> bool:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)
        return not stack

    @staticmethod
    def longest_valid_parentheses(s: str) -> int:
        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        stack = [-1]
        max_length = 0
        for i, char in enumerate(s):
            if char == '(':
                stack.append(i)
            else:
                stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    max_length = max(max_length, i - stack[-1])
        return max_length

    @staticmethod
    def count_and_say(n: int) -> str:
        if not isinstance(n, int) or n < 1:
            raise ValueError("Input must be a positive integer")

        s = '1'
        for _ in range(n - 1):
            count = 1
            temp = []
            for i in range(1, len(s)):
                if s[i] == s[i-1]:
                    count += 1
                else:
                    temp.append(str(count) + s[i-1])
                    count = 1
            temp.append(str(count) + s[-1])
            s = ''.join(temp)
        return s

    @staticmethod
    def minimum_window_substring(s: str, t: str) -> str:
        if not isinstance(s, str) or not isinstance(t, str):
            raise TypeError("Inputs must be strings")

        if not t or not s:
            return ""

        dict_t = Counter(t)
        required = len(dict_t)
        l, r = 0, 0
        formed = 0
        window_counts = {}
        ans = float("inf"), None, None

        while r < len(s):
            character = s[r]
            window_counts[character] = window_counts.get(character, 0) + 1

            if character in dict_t and window_counts[character] == dict_t[character]:
                formed += 1

            while l <= r and formed == required:
                character = s[l]

                if r - l + 1 < ans[0]:
                    ans = (r - l + 1, l, r)

                window_counts[character] -= 1
                if character in dict_t and window_counts[character] < dict_t[character]:
                    formed -= 1

                l += 1

            r += 1

        return "" if ans[0] == float("inf") else s[ans[1] : ans[2] + 1]

def main():
    parser = argparse.ArgumentParser(description="String Algorithms")
    parser.add_argument("--algorithm", choices=[
        'levenshtein', 'lcs', 'kmp', 'rabin_karp', 'z_function', 'manacher',
        'aho_corasick', 'boyer_moore', 'lps', 'lrs', 'parse_json', 'generate_json',
        'parse_xml', 'generate_xml', 'compress_string', 'decompress_string',
        'is_anagram', 'is_palindrome', 'longest_common_prefix', 'edit_distance',
        'longest_increasing_subsequence', 'string_matching', 'count_substrings',
        'longest_substring_without_repeating', 'string_rotation', 'reverse_words',
        'string_permutations', 'longest_common_subsequence', 'regex_match',
        'wildcard_match', 'string_compression', 'is_valid_parentheses',
        'longest_valid_parentheses', 'count_and_say', 'minimum_window_substring'
    ], required=True, help="Algorithm to run")
    parser.add_argument("--input1", help="First input string or file path")
    parser.add_argument("--input2", help="Second input string (for algorithms that require two inputs)")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", choices=['json', 'text', 'xml'], default='text', help="Output format")

    args = parser.parse_args()

    try:
        if args.input1:
            with open(args.input1, 'r') as f:
                input1 = f.read().strip()
        else:
            input1 = input("Enter first input: ")

        if args.algorithm in ['levenshtein', 'lcs', 'kmp', 'rabin_karp', 'boyer_moore', 'edit_distance', 'longest_common_subsequence', 'string_rotation', 'minimum_window_substring']:
            if args.input2:
                with open(args.input2, 'r') as f:
                    input2 = f.read().strip()
            else:
                input2 = input("Enter second input: ")

        result = None
        if args.algorithm == 'levenshtein':
            result = StringAlgorithms.levenshtein_distance(input1, input2)
        elif args.algorithm == 'lcs':
            result = StringAlgorithms.longest_common_substring(input1, input2)
        elif args.algorithm == 'kmp':
            result = StringAlgorithms.kmp_search(input1, input2)
        elif args.algorithm == 'rabin_karp':
            result = StringAlgorithms.rabin_karp_search(input1, input2)
        elif args.algorithm == 'z_function':
            result = StringAlgorithms.z_function(input1)
        elif args.algorithm == 'manacher':
            result = StringAlgorithms.manacher_algorithm(input1)
        elif args.algorithm == 'aho_corasick':
            patterns = input1.split()
            search = StringAlgorithms.aho_corasick(patterns)
            text = input("Enter text to search in: ")
            result = search(text)
        elif args.algorithm == 'boyer_moore':
            result = StringAlgorithms.boyer_moore(input1, input2)
        elif args.algorithm == 'lps':
            result = StringAlgorithms.longest_palindromic_subsequence(input1)
        elif args.algorithm == 'lrs':
            result = StringAlgorithms.longest_repeating_substring(input1)
        elif args.algorithm == 'parse_json':
            result = StringAlgorithms.parse_json(input1)
        elif args.algorithm == 'generate_json':
            data = eval(input1)  # Be careful with eval in production!
            result = StringAlgorithms.generate_json(data)
        elif args.algorithm == 'parse_xml':
            result = StringAlgorithms.parse_xml(input1)
        elif args.algorithm == 'generate_xml':
            root = ET.fromstring(input1)
            result = StringAlgorithms.generate_xml(root)
        elif args.algorithm == 'compress_string':
            result = StringAlgorithms.compress_string(input1)
        elif args.algorithm == 'decompress_string':
            result = StringAlgorithms.decompress_string(input1)
        elif args.algorithm == 'is_anagram':
            result = StringAlgorithms.is_anagram(input1, input2)
        elif args.algorithm == 'is_palindrome':
            result = StringAlgorithms.is_palindrome(input1)
        elif args.algorithm == 'longest_common_prefix':
            result = StringAlgorithms.longest_common_prefix(input1.split())
        elif args.algorithm == 'edit_distance':
            result = StringAlgorithms.edit_distance(input1, input2)
        elif args.algorithm == 'longest_increasing_subsequence':
            result = StringAlgorithms.longest_increasing_subsequence(input1)
        elif args.algorithm == 'string_matching':
            result = StringAlgorithms.string_matching(input1, input2)
        elif args.algorithm == 'count_substrings':
            result = StringAlgorithms.count_substrings(input1)
        elif args.algorithm == 'longest_substring_without_repeating':
            result = StringAlgorithms.longest_substring_without_repeating(input1)
        elif args.algorithm == 'string_rotation':
            result = StringAlgorithms.string_rotation(input1, input2)
        elif args.algorithm == 'reverse_words':
            result = StringAlgorithms.reverse_words(input1)
        elif args.algorithm == 'string_permutations':
            result = StringAlgorithms.string_permutations(input1)
        elif args.algorithm == 'longest_common_subsequence':
            result = StringAlgorithms.longest_common_subsequence(input1, input2)
        elif args.algorithm == 'regex_match':
            result = StringAlgorithms.regex_match(input1, input2)
        elif args.algorithm == 'wildcard_match':
            result = StringAlgorithms.wildcard_match(input1, input2)
        elif args.algorithm == 'string_compression':
            result = StringAlgorithms.string_compression(input1)
        elif args.algorithm == 'is_valid_parentheses':
            result = StringAlgorithms.is_valid_parentheses(input1)
        elif args.algorithm == 'longest_valid_parentheses':
            result = StringAlgorithms.longest_valid_parentheses(input1)
        elif args.algorithm == 'count_and_say':
            result = StringAlgorithms.count_and_say(int(input1))
        elif args.algorithm == 'minimum_window_substring':
            result = StringAlgorithms.minimum_window_substring(input1, input2)

        if args.output:
            with open(args.output, 'w') as f:
                if args.format == 'json':
                    json.dump(result, f, indent=2)
                elif args.format == 'xml':
                    root = ET.Element('result')
                    ET.SubElement(root, 'value').text = str(result)
                    tree = ET.ElementTree(root)
                    tree.write(f, encoding='unicode', xml_declaration=True)
                else:
                    f.write(str(result))
        else:
            print(result)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()