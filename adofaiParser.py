import json
from typing import Callable, List

from parseHelper import *

def addFilter(Map: MapType, filters: List[EventType]):
    actions: List[EventType] = Map['actions']
    actions += filters
    actions.sort(key=lambda action: action["floor"])
    Map["actions"] = actions
    return Map

def run(
    fileName: str, targetFloor: int, filter: str,
    startAngleOffset: float, endAngleOffset: float,
    startIntensity: int, endIntensity: int,
    density: int,
    logger: Callable[[str], None]):

    logger("Loading Map file")

    with open(fileName, 'r', encoding='utf-8-sig') as adofaiFile:
        rawString = adofaiFile.read()\
                .replace(',\n}\n', '\n}\n')\
                .replace(',\n}', '\n}')\
                .replace(', }', '}')\
                .replace(',,', ',')
        
        Map: MapType = json.loads(rawString, strict=False)
    
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
