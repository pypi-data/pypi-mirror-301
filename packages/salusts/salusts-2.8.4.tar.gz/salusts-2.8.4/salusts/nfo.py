_ChipZoneEdges_cache = None

def ChipZoneEdges():
    global _ChipZoneEdges_cache
    if _ChipZoneEdges_cache is not None:
        return _ChipZoneEdges_cache

    ChipZoneEdges = {}
    #print('[i]initializing ChipZoneEdges')
    for IDy in ('1','2',''):
        if IDy=='':
            xTuple = map(chr, range(65,69))
            yRange = (0,45000)  # maxY might be 44524
        else:
            xTuple = map(chr, range(65,70))
            yRange = (1856,42560)
            yRange = (1800,42599)
        for IDx in xTuple:
            ZoneID = IDx + IDy
            match IDx:
                case 'A' if IDy != '':
                    xRange = (3891,44596)
                    xRange = (3800,44599)
                case 'B' if IDy != '':
                    xRange = (48521,89226)
                    xRange = (48500,89299)
                case 'C' if IDy != '':
                    xRange = (93151,133856)
                    xRange = (93100,133899)
                case 'D' if IDy != '':
                    xRange = (137781,178486)
                    xRange = (137700,178499)
                case 'E' if IDy != '':
                    xRange = (182410,223115)
                    xRange = (182400,223199)
                case 'A' if IDy == '':
                    xRange = (3534,55502)
                case 'B' if IDy == '':
                    xRange = (59524,111492)
                case 'C' if IDy == '':
                    xRange = (115515,167483)
                case 'D' if IDy == '':
                    xRange = (171505,223473)
                case _:
                    raise ValueError("[x]It can only be memory error ...")
            ChipZoneEdges[ZoneID] = xRange + yRange
    _ChipZoneEdges_cache = ChipZoneEdges
    return _ChipZoneEdges_cache
