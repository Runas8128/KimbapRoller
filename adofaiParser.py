from typing import Callable, Union

import json

from parseHelper import Filters, MapType, PathType
from parseHelper import MakeFilter
from parseHelper import ParseException, ExpectedParseException, UnExpectedParseException

def run(
    fileName: str, filter: str,
    startAngleOffset: float, endAngleOffset: float,
    startIntensity: int, endIntensity: int,
    density: int,
    logger: Callable[[str], None]):

    logger("Loading Map file")
    
    with open(fileName, 'r', encoding='utf-8-sig') as adofaiFile:
        rawString = adofaiFile.read()
        rawString = rawString.replace(',\n}\n', '\n}\n').replace(',\n}', '\n}')
        Map: MapType = json.loads(rawString)
    
    # pathData for Hallowen or complementable version
    logger("Loading pathData/angleData")
    
    data: Union[PathType, None] = Map.get("pathData", Map.get("angleData", None))
    if not data:
        raise ParseException("얼불춤 파일이 아닙니다. 얼불춤 파일을 선택해주세요!")