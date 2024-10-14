import math
import json
from typing import List, Union, Any
from prettytable import PrettyTable
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

class SearchError(Exception):
    pass

class InvalidInputError(SearchError):
    pass

class AlgorithmNotFoundError(SearchError):
    pass

class FileReadError(SearchError):
    pass

class FileWriteError(SearchError):
    pass

def read_from_file(file_path: str) -> tuple:
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r') as file:
                data = json.load(file)
                numbers = data.get('numbers', [])
                target = data.get('target')
        else:
            with open(file_path, 'r') as file:
                content = file.read().strip().split('\n')
                if len(content) == 1:
                    numbers = [int(x.strip()) for x in content[0].split(',') if x.strip()]
                    target = numbers[-1]
                    numbers = numbers[:-1]
                else:
                    numbers = [int(x.strip()) for x in content[:-1] if x.strip()]
                    target = int(content[-1].strip())
        return numbers, target
    except Exception as e:
        raise FileReadError(f"Error reading file: {str(e)}")

def format_output(result: Union[int, List[int], None], numbers: List[int], target: Union[int, List[int]], algorithm: str, output_format: str) -> str:
    info = {
        "algorithm": algorithm,
        "target": target,
        "result": result,
        "numbers": numbers
    }
    
    if output_format == 'brackets':
        return f"[{', '.join(map(str, numbers))}]"
    elif output_format == 'curly_braces':
        return f"{{{', '.join(map(str, numbers))}}}"
    elif output_format == 'parentheses':
        return f"({', '.join(map(str, numbers))})"
    elif output_format == 'no_commas':
        return ' '.join(map(str, numbers))
    elif output_format == 'spaces':
        return ' '.join(map(str, numbers))
    elif output_format == 'vertical':
        return '\n'.join(map(str, numbers))
    elif output_format == 'horizontal':
        return ' '.join(map(str, numbers))
    elif output_format == 'csv':
        return ','.join(map(str, numbers))
    elif output_format == 'tab_separated':
        return '\t'.join(map(str, numbers))
    elif output_format == 'json':
        json_str = json.dumps(info, indent=2)
        return highlight(json_str, JsonLexer(), TerminalFormatter())
    elif output_format == 'pretty_json':
        json_str = json.dumps(info, indent=2)
        return highlight(json_str, JsonLexer(), TerminalFormatter())
    elif output_format == 'bullet_points':
        return '\n'.join(f'• {num}' for num in numbers)
    elif output_format == 'numbered_list':
        return '\n'.join(f'{i+1}. {num}' for i, num in enumerate(numbers))
    elif output_format == 'html_list':
        return f"<ul>\n{''.join(f'  <li>{num}</li>\n' for num in numbers)}</ul>"
    elif output_format == 'xml':
        return f"<numbers>\n{''.join(f'  <number>{num}</number>\n' for num in numbers)}</numbers>"
    elif output_format == 'yaml':
        return '- ' + '\n- '.join(map(str, numbers))
    elif output_format == 'markdown_table':
        table = PrettyTable()
        table.field_names = ["Index", "Number"]
        for i, num in enumerate(numbers):
            table.add_row([i+1, num])
        return table.get_string()
    elif output_format == 'latex_array':
        return f"\\begin{{array}}{{c}}\n{' \\\\ '.join(map(str, numbers))}\n\\end{{array}}"
    elif output_format == 'binary':
        return ' '.join(format(num, '08b') for num in numbers)
    elif output_format == 'hexadecimal':
        return ' '.join(format(num, '02X') for num in numbers)
    elif output_format == 'scientific_notation':
        return ' '.join(f'{num:.2e}' for num in numbers)
    elif output_format == 'percentage':
        max_num = max(numbers)
        return ' '.join(f'{(num/max_num)*100:.2f}%' for num in numbers)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def write_to_file(result: Union[int, List[int], None], numbers: List[int], target: Union[int, List[int]], algorithm: str, file_path: str, output_format: str = 'json') -> None:
    try:
        formatted_output = format_output(result, numbers, target, algorithm, output_format)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
    except Exception as e:
        raise FileWriteError(f"Error writing to file: {str(e)}")

def linear_search(arr, target):
    return [i for i, value in enumerate(arr) if value == target] or None

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None

def jump_search(arr, target):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return None
    while arr[prev] < target:
        prev += 1
        if prev == min(step, n):
            return None
    if arr[prev] == target:
        return prev
    return None

def interpolation_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high and arr[low] <= target <= arr[high]:
        if low == high:
            return low if arr[low] == target else None
        pos = low + int(((float(high - low) / (arr[high] - arr[low])) * (target - arr[low])))
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return None

def exponential_search(arr, target):
    if arr[0] == target:
        return 0
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2
    return binary_search(arr[i//2:min(i, len(arr))], target)

def fibonacci_search(arr, target):
    fib_m_minus_2 = 0
    fib_m_minus_1 = 1
    fib_m = fib_m_minus_1 + fib_m_minus_2
    while fib_m < len(arr):
        fib_m_minus_2 = fib_m_minus_1
        fib_m_minus_1 = fib_m
        fib_m = fib_m_minus_1 + fib_m_minus_2
    offset = -1
    while fib_m > 1:
        i = min(offset + fib_m_minus_2, len(arr) - 1)
        if arr[i] < target:
            fib_m = fib_m_minus_1
            fib_m_minus_1 = fib_m_minus_2
            fib_m_minus_2 = fib_m - fib_m_minus_1
            offset = i
        elif arr[i] > target:
            fib_m = fib_m_minus_2
            fib_m_minus_1 = fib_m_minus_1 - fib_m_minus_2
            fib_m_minus_2 = fib_m - fib_m_minus_1
        else:
            return i
    if fib_m_minus_1 and arr[offset + 1] == target:
        return offset + 1
    return None

def sublist_search(arr, sublist):
    n, m = len(arr), len(sublist)
    for i in range(n - m + 1):
        if arr[i:i+m] == sublist:
            return i
    return None

def ternary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        left_third = left + (right - left) // 3
        right_third = right - (right - left) // 3
        if arr[left_third] == target:
            return left_third
        if arr[right_third] == target:
            return right_third
        if target < arr[left_third]:
            right = left_third - 1
        elif target > arr[right_third]:
            left = right_third + 1
        else:
            left = left_third + 1
            right = right_third - 1
    return None

def jump_search_2(arr, target):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return None
    return linear_search(arr[prev:min(step, n)], target)

def exponential_search_2(arr, target):
    if arr[0] == target:
        return 0
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2
    return binary_search(arr[i//2:min(i, len(arr))], target)

def meta_binary_search(arr, target):
    if not arr:
        return None
    if len(arr) == 1:
        return 0 if arr[0] == target else None
    
    def get_first_set_bit(n):
        return int(math.log2(n & -n))
    
    n = len(arr)
    max_bit = get_first_set_bit(n)
    pos = 0
    for i in range(max_bit, -1, -1):
        new_pos = pos | (1 << i)
        if new_pos < n and arr[new_pos] <= target:
            pos = new_pos
    return pos if arr[pos] == target else None

def galloping_search(arr, target):
    if not arr or arr[0] > target:
        return None
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2
    left = i // 2
    right = min(i, len(arr))
    return binary_search(arr[left:right], target)

def search(data: Union[str, List[int]], target: Union[int, List[int]], algorithm: str, output_format: str = 'spaces', output_file: str = None):
    try:
        if isinstance(data, str):
            numbers, file_target = read_from_file(data)
            if target is None:
                target = file_target
        elif isinstance(data, list):
            numbers = data
        else:
            raise InvalidInputError("Invalid input data format")

        search_algorithms = {
            'linear': linear_search,
            'binary': binary_search,
            'jump': jump_search,
            'interpolation': interpolation_search,
            'exponential': exponential_search,
            'fibonacci': fibonacci_search,
            'sublist': sublist_search,
            'ternary': ternary_search,
            'jump_2': jump_search_2,
            'exponential_2': exponential_search_2,
            'meta_binary': meta_binary_search,
            'galloping': galloping_search
        }
        
        if algorithm not in search_algorithms:
            raise AlgorithmNotFoundError(f"Unsupported search algorithm: {algorithm}")
        
        if isinstance(target, list):
            result = {t: search_algorithms[algorithm](numbers, t) for t in target}
        else:
            result = search_algorithms[algorithm](numbers, target)
        
        formatted_result = format_output(result, numbers, target, algorithm, output_format)
        
        if output_file:
            write_to_file(result, numbers, target, algorithm, output_file, output_format)
        
        return formatted_result
    except SearchError as e:
        return str(e)
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Perform various search algorithms on a list of numbers.")
    parser.add_argument("data", help="Path to the input file or a comma-separated list of numbers")
    parser.add_argument("target", help="Target value or values to search for")
    parser.add_argument("algorithm", choices=["linear", "binary", "jump", "interpolation", "exponential", "fibonacci", "sublist", "ternary", "jump_2", "exponential_2", "meta_binary", "galloping"], help="Search algorithm to use")
    parser.add_argument("-f", "--format", choices=[
        "brackets", "curly_braces", "parentheses", "no_commas", "spaces", "vertical", "horizontal",
        "csv", "tab_separated", "json", "pretty_json", "bullet_points", "numbered_list", "html_list",
        "xml", "yaml", "markdown_table", "latex_array", "binary", "hexadecimal", "scientific_notation",
        "percentage"
    ], default="spaces", help="Output format")
    parser.add_argument("-o", "--output", help="Output file path")
    
    args = parser.parse_args()
    
    if ',' in args.data:
        data = [int(x.strip()) for x in args.data.split(',')]
    else:
        data = args.data
    
    if ',' in args.target:
        target = [int(x.strip()) for x in args.target.split(',')]
    else:
        target = int(args.target)
    
    result = search(data, target, args.algorithm, args.format, args.output)
    print(result)

if __name__ == "__main__":
    main()