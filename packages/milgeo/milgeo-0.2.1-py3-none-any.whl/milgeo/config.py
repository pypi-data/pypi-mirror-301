from typing import List, Dict

from text_to_sidc import UnitDesignator


class Config:
    unit_designator = None
    custom_patterns = []

    @staticmethod
    def get_unit_designator():
        if Config.unit_designator is None:
            Config.unit_designator = UnitDesignator()
            Config._apply_custom_patterns_to_designator()
        return Config.unit_designator

    @staticmethod
    def add_custom_patterns(patterns: List[Dict[str, List[str]]]):
        for pattern_dict in patterns:
            if not all(k in pattern_dict for k in ["sidc", "list_of_patterns"]) or \
                    not isinstance(pattern_dict["list_of_patterns"], list):
                raise ValueError("Each pattern must have 'sidc' and 'list_of_patterns' (list of strings).")
        Config.custom_patterns.extend(patterns)
        if Config.unit_designator is not None:
            Config._apply_custom_patterns_to_designator()

    @staticmethod
    def _apply_custom_patterns_to_designator():
        for pattern_dict in Config.custom_patterns:
            Config.unit_designator.import_custom_patterns(
                pattern_dict['sidc'], pattern_dict['list_of_patterns']
            )
