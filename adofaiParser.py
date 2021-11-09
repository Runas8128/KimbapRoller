import typing
import json

import parseHelper
from parseHelper import PathType, EventType, MapType # Type Alias
from parseHelper import ParseException, ExpectedParseException # Exceptions

def dataToAngle(data: PathType, twirls: typing.List[int]) -> typing.List[int]:
    if isinstance(data, str):
        try:
            data = [parseHelper.angleForPath[path] for path in parseHelper.fixPath(data)]
        except KeyError:
            raise ExpectedParseException("알 수 없는 pathData입니다.\n", ".adofai파일을 다시 확인")

    try:
        isTwirl = False
        rt = []
        for idx in range(1, len(data)):
            if idx in twirls:
                isTwirl = not isTwirl
            
            diff = 0

            if data[idx] == 999: # This tile is Midspin
                rt.append(999)
                print('store 999 at', idx)
                continue
            elif data[idx - 1] == 999: # Past tile is Midspin
                diff = (data[idx - 2] - data[idx]) % 360
            else:
                diff = (180 - data[idx] + data[idx - 1]) % 360
                if diff == 0: diff = 360 # U-Turn Tile
            
            rt.append(diff)
            if isTwirl and diff != 360:
                rt[-1] = 360 - rt[-1]
        print(rt)
        return rt
    except TypeError:
        raise ExpectedParseException("알 수 없는 pathData 혹은 angleData입니다.\n", ".adofai파일을 다시 확인")

def makeBPMMuls(angles: typing.List[int], bpm: str):
    angles.insert(0, 180)
    bpms: typing.List[EventType] = []
    mul: int = 0
    for idx in range(1, len(angles)):
        if angles[idx] == 999:
            mul = 1
        elif angles[idx - 1] == 999:
            mul = angles[idx] / angles[idx - 2]
        else:
            mul = angles[idx] / angles[idx - 1]
        bpms.append(parseHelper.makeSpeedEvent(idx, mul))
    
    if bpm.isdigit():
        return mulToBPM(bpms, int(bpm))
    else:
        return [event for event in bpms if event["bpmMultiplier"] < 1-1E-6 or event["bpmMultiplier"] > 1+1E-6]

def mulToBPM(muls: typing.List[EventType], BPM: int):
    nowMul = 1
    for mul in muls:
        mul['speedType'] = 'Bpm'
        nowMul *= mul['bpmMultiplier']
        mul['beatsPerMinute'] = BPM * nowMul
    return muls

def delSpeed(Map: MapType):
    actions: typing.List[EventType] = Map['actions']
    actions = [action for action in actions if action["eventType"] != "SetSpeed"]
    Map["actions"] = actions
    return Map

def addSpeed(Map: MapType, Speeds: typing.List[EventType]):
    actions: typing.List[EventType] = Map['actions']
    actions += Speeds
    actions.sort(key=lambda action: action["floor"])
    Map["actions"] = actions
    return Map

def run(fileName: str, BPM: str, style: str, logger: typing.Callable[[str], None]):
    logger("Loading Map file")
    
    with open(fileName, 'r', encoding='utf-8-sig') as adofaiFile:
        rawString = adofaiFile.read()
        rawString = rawString.replace(',\n}\n', '\n}\n').replace(',\n}', '\n}')
        Map: MapType = json.loads(rawString)
    
    # pathData for Hallowen or complementable version
    logger("Loading pathData/angleData")
    
    data: typing.Union[PathType, None] = Map.get("pathData", Map.get("angleData", None))
    if not data:
        raise ParseException("얼불춤 파일이 아닙니다. 얼불춤 파일을 선택해주세요!")
    
    logger("Deleting Speed / Twirl")
    
    Map = delSpeed(Map)
    if style == "styleInner":
        Map = parseHelper.makeInnerTwirl(Map)
    elif style == "styleOuter":
        Map = parseHelper.makeOuterTwirl(Map)
    
    logger("Caculating needed multipliers")

    twirls: typing.List[int] = [action["floor"] for action in Map["actions"] if action["eventType"] == "Twirl"]
    Multipliers = makeBPMMuls(dataToAngle(data, twirls), BPM) # BPM is not digit -> Multiplier

    logger("Make and Dump new map")
    
    newMap = addSpeed(Map, Multipliers)
    with open(fileName[:-7] + '_Magic.adofai', 'w', encoding='utf-8-sig') as newFile:
        json.dump(newMap, newFile, indent=4)
