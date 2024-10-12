# your_package/utils.py

import json
import os
from typing import List, Tuple, Union

# Импортируем все алгоритмы сортировки
from .sorting import (
    merge_sort,
    quick_sort,
    bubble_sort,
    insertion_sort,
    selection_sort,
    heap_sort,
    shell_sort,
    counting_sort,
    radix_sort,
    bucket_sort,
    comb_sort,
    cocktail_sort,
    gnome_sort,
    cycle_sort,
    pigeonhole_sort,
    strand_sort,
    pancake_sort,
    bogo_sort,
    stooge_sort,
    tim_sort,
)

def sort_numbers(numbers: List[int], algorithm: str, output_format: str = 'brackets', output_path: str = None) -> Tuple[List[int], str]:
    algorithms = {
        'merge': merge_sort,
        'quick': quick_sort,
        'bubble': bubble_sort,
        'insertion': insertion_sort,
        'selection': selection_sort,
        'heap': heap_sort,
        'shell': shell_sort,
        'counting': counting_sort,
        'radix': radix_sort,
        'bucket': bucket_sort,
        'comb': comb_sort,
        'cocktail': cocktail_sort,
        'gnome': gnome_sort,
        'cycle': cycle_sort,
        'pigeonhole': pigeonhole_sort,
        'strand': strand_sort,
        'pancake': pancake_sort,
        'bogo': bogo_sort,
        'stooge': stooge_sort,
        'tim': tim_sort,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Unsupported algorithm. Choose from: {', '.join(algorithms.keys())}")
    
    sorted_numbers = algorithms[algorithm](numbers)
    formatted_output = format_output(sorted_numbers, output_format)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(formatted_output)
        print(f"Sorted list saved to {output_path}")
    
    return sorted_numbers, formatted_output

def format_output(numbers: List[int], output_format: str) -> str:
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
        return json.dumps(numbers)
    elif output_format == 'pretty_json':
        return json.dumps(numbers, indent=2)
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
        return f"| Number |\n|--------|\n{''.join(f'| {num} |\n' for num in numbers)}"
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

def read_numbers(file_path: str) -> List[int]:
    _, ext = os.path.splitext(file_path)
    if ext == '.txt':
        with open(file_path, 'r') as f:
            content = f.read()
        numbers = [int(num.strip()) for num in content.replace('\n', ',').split(',') if num.strip()]
    elif ext == '.json':
        with open(file_path, 'r') as f:
            numbers = json.load(f)
    else:
        raise ValueError("Unsupported file format. Use .txt or .json")
    return numbers