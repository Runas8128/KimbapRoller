import typing

import json

from parseHelper import Filters
from parseHelper import EventType, MapType, PathType
from parseHelper import MakeFilter
from parseHelper import ParseException, ExpectedParseException, UnExpectedParseException

def addFilter(Map: MapType, filters: typing.List[EventType]):
    actions: typing.List[EventType] = Map['actions']
    actions += filters
    actions.sort(key=lambda action: action["floor"])
    Map["actions"] = actions
    return Map

def run(
    fileName: str, targetFloor: int, filter: str,
    startAngleOffset: float, endAngleOffset: float,
    startIntensity: int, endIntensity: int,
    density: int,
    logger: typing.Callable[[str], None]):

    logger("Loading Map file")
    
    with open(fileName, 'r', encoding='utf-8-sig') as adofaiFile:
        rawString = adofaiFile.read()
        rawString = rawString.replace(',\n}\n', '\n}\n').replace(',\n}', '\n}')
        Map: MapType = json.loads(rawString)
    
    logger("Making Filter list")

    if density < 2:
        raise ParseException("필터 갯수는 두 개 이상으로 해주세요!")

    # (density - 1) * (delta) = end - start
    intensityDelta = (endIntensity - startIntensity) / density
    angleOffsetDelta = (endAngleOffset - startAngleOffset) / density
    filterList = [MakeFilter(
        targetFloor, filter, startIntensity + intensityDelta * i, startAngleOffset + angleOffsetDelta * i
    ) for i in range(density + 1)]
    
    logger("Make and Dump new map")
    
    newMap = addFilter(Map, filterList)
    with open(fileName[:-7] + '_Filtered.adofai', 'w', encoding='utf-8-sig') as newFile:
        json.dump(newMap, newFile, indent=4)
