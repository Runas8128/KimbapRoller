from typing import Union, List, Dict

PathType = Union[str, List[Union[int, float]]]
SettingType = Dict[str, Union[int, str, bool]]
EventType = Dict[str, Union[int, str, float]]

MapType = Dict[str, Union[PathType, SettingType, List[EventType]]]

Filters = {
    "흑백": "Greyscale",
    "세피아": "Sepia",
    "VHS": "VHS",
    "LED": "LED",
    "비": "Rain",
    "눈폭풍": "Blizzard",
    "픽셀 눈": "PixelSnow",
    "압축": "Compression",
    "픽셀화": "Pizelate",
    "물결": "Waves",
    "잡음": "Static",
    "필름 그레인": "Grain",
    "모션 블러": "MotionBlur",
    "어안 렌즈": "Fisheye",
    "색수차": "Aberration",
    "드로잉": "Drawing"
}

class ParseException(Exception):
    pass

class UnExpectedParseException(ParseException):
    def __init__(self, err: str):
        super().__init__(err + '디스코드에 루나스#5980으로 해당 오류를 제보해주시기 바랍니다')

class ExpectedParseException(UnExpectedParseException):
    def __init__(self, err: str, suggest: str):
        super().__init__(err + suggest + '한 후에도 오류가 지속된다면 ')

def MakeFilter(floor: int, name: str, intensity: int, angleOffset: float):
    return {
        "floor": floor, "eventType": "SetFilter", "filter": name, "enabled": "Enabled", "intensity": intensity,
        "disableOthers": "Disabled", "angleOffset": angleOffset, "eventTag": ""
    }