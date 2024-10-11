from enum import Enum, auto
import regex
from os.path import dirname
import types
from typing import Union, List, Tuple, Dict, cast, TypedDict
import csv

def load_designator_data():
    # read csv file as txt
    # return list of tuples with pattern and sidc
    path = f"{dirname(__file__)}/patterns_data.csv"
    open_file = open(path, "r", encoding="utf-8")
    lines = open_file.readlines()
    open_file.close()

    # create list of tuples and remove new line character
    data = []
    for line in lines:
        pattern, sidc = line.strip().split(",")
        data.append((pattern, sidc))

    return data

class PatternDict(TypedDict):
    sidc: str
    list_of_patterns: List[str]

def parse_csv_to_dict_list(file_path: str) -> List[PatternDict]:
    result: List[PatternDict] = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != "sidc":
                sidc, pattern_str = row[0], row[1]
                patterns: List[str] = cast(List[str], pattern_str.split('|'))
                result.append({"sidc": sidc, "list_of_patterns": patterns}) 
    return result


class Status(Enum):
    """
    Provides status of the unit.
    """
    PRESENT = "0"
    PLANNED_ANTICIPATED_SUSPECT = "1"
    FULLY_CAPABLE = "2"
    DAMAGED = "3" 
    DESTROYED = "4"
    FULL_TO_CAPACITY = "5"

class Mobility(Enum):
    """
    Provides mobility of the unit. 
    """
    UNSPECIFIED = auto()
    WHEELED_LIMITED_CROSS_COUNTRY = auto()
    WHEELED_CROSS_COUNTRY = auto()
    TRACKED = auto()
    WHEELED_AND_TRACKED_COMBINATION = auto()
    TOWED = auto()

def set_mobility(sidc: str, mobility: Mobility) -> str:
    """
    Set's mobility for disignated unit
    """
    if mobility == Mobility.WHEELED_LIMITED_CROSS_COUNTRY:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '1', 9)
    elif mobility == Mobility.WHEELED_CROSS_COUNTRY:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '2', 9)
    elif mobility == Mobility.TRACKED:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '3', 9)
    elif mobility == Mobility.TOWED:
        sidc = set_char_at_position(sidc, '3', 8)
        sidc = set_char_at_position(sidc, '5', 9)
    else:  # Mobility.UNSPECIFIED or any other case
        sidc = set_char_at_position(sidc, '0', 8)
        sidc = set_char_at_position(sidc, '0', 9)
    return sidc

def set_char_at_position(sidc: str, character: str, position: int) -> str:
    "Replaces characters by gives ones"
    replacement = list(sidc)
    replacement[position] = character
    return ''.join(replacement)


class UnitDesignator:
    """
    Accepts a name of the unit and returns a SIDC code.
    """

    _data: List[Tuple[str, str]] = load_designator_data()

    def __init__(self):
        # Use self._data as needed
        pass

    @staticmethod
    def calculate_icon(name: str) -> str:
        return UnitDesignator.calculate_icon_with_flag(name, True)

    @staticmethod
    def calculate_icon_with_flag(name: str, calculate_icon: bool) -> str:
        if calculate_icon and name:
            sidc = UnitDesignator.get_unit(name.upper())
            return "10012500001313000000" if sidc is None else sidc
        return "10012500001313000000"

    @staticmethod
    def get_unit(name: str) -> Union[str, None]:
        mobility = Mobility.UNSPECIFIED
        if "БУКСИРОВАНИЙ" in name:
            mobility = Mobility.TOWED
            name = name.replace("БУКСИРОВАНИЙ", "")

        sidc = UnitDesignator.designate_icon(name)

        if any(keyword in name for keyword in ["МАКЕТ", "МУЛЯЖ", "МАКЕТЫ", "МУЛЯЖИ", "МАКЕТА", "МУЛЯЖА"]):
            if sidc is not None:
                return set_char_at_position(sidc, "1", 7)

        if any(keyword in name for keyword in ["УРАЖЕНО", "УРАЖЕНА", "ПОШКОДЖЕНА", "ПОШКОДЖЕНО", "ПОШКОДЖЕНІ", 
                                            "ПОРАЖЕНО", "ПОРАЖЕНА", "ПОВРЕЖДЕНА", "ПОВРЕЖДЕНО", "ПОВРЕЖДЕННЫЕ"]):
            if sidc is not None:
                return set_char_at_position(sidc, Status.DAMAGED.value, 6)

        if any(keyword in name for keyword in ["ЗНИЩЕНОГО", "ЗНИЩЕНА", "ЗРУЙНОВАНО", "ЗНИЩЕНО",
                                            "УНИЧТОЖЕННОГО", "УНИЧТОЖЕНА", "РАЗРУШЕНО", "УНИЧТОЖЕНО"]):
            if sidc is not None:
                return set_char_at_position(sidc, Status.DESTROYED.value, 6)

        if "ВІДНОВЛЕНО" in name:
            if sidc is not None:
                return set_char_at_position(sidc, Status.FULL_TO_CAPACITY.value, 6)

        if any(keyword in name for keyword in ["ЙМОВІРНО", "МОЖЛИВО", "ЙМОВІРНА",
                                              "ВЕРОЯТНО", "ВОЗМОЖНО", "ВЕРОЯТНАЯ"]):
            if sidc is not None:
                return set_char_at_position(sidc, Status.PLANNED_ANTICIPATED_SUSPECT.value, 6)

        if  mobility != Mobility.UNSPECIFIED and sidc is not None:
            sidc_with_mobility = set_mobility(sidc, mobility)
            return sidc_with_mobility

        return sidc

    @staticmethod
    def additional_pattern(pattern):
            return (r'(^|[^\p{L}])' + "(" + pattern + ")" + r'($|[^\p{L}])')
    


    @staticmethod
    def designate_icon(name: str, return_pattern:bool=False) -> Union[str, None]:        

        for pattern_row in UnitDesignator._data:
            full_pattern = UnitDesignator.additional_pattern(pattern_row[1])
            
            match = regex.search(full_pattern, name.upper(), flags=regex.IGNORECASE)            
            if match:
                if return_pattern:
                    return f'{pattern_row[0]} {pattern_row[1]}'
                return pattern_row[0]
        return None 
    
    @classmethod
    def transoform_patterns(cls, patterns: List[PatternDict]) -> List[Tuple[str, str]]:
        return [ (pat['sidc'], "|".join(pat['list_of_patterns']))  for pat in patterns]

    
    @staticmethod
    def import_custom_patterns(list_of_dicts: List[PatternDict]):
        transformed_patterns = UnitDesignator.transoform_patterns(list_of_dicts)

        # Insert all elements at the beginning of the list
        UnitDesignator._data = transformed_patterns + UnitDesignator._data
