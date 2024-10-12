"""
Misc project utilities

Functions:
- get_combined_dict(results: List[Tuple]) -> Dict
- write_csv_file(filepath, data, header=None)
"""
from typing import Dict, Iterable, List, Tuple
import csv

def get_combined_dict(results: List[Tuple]) -> Dict[str, str]:
    """Returns a dictionary from a list of 2 item tuples"""
    d = dict(sections='Song Sections', OPP='One Press Play') 
    pbf_dict = dict()
    for result in results:
        song_type = d.get(result[2])
        pbf_dict.update({result[0]: [result[1], song_type]})    
        
    return pbf_dict


def write_csv_file(filepath: str, data: Iterable, header=None):      
    """Writes an iterable to a csv file."""
    with open(filepath, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(data)