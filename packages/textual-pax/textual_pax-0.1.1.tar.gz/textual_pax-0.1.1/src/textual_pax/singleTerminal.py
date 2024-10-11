from .revertpaxmodule import apiPaxFunctions, terminalDetails, getInstalledConfig
import pandas as pd



async def parseList(serialNoList)->dict:
    thing = apiPaxFunctions()
    termDetail = await thing.startPaxGroup(serialNoList)
    config = await getInstalledConfig(serialNoList)
    for item in config:
        apklist = item['installedApks']
        df = pd.DataFrame(apklist)
    details = await terminalDetails(detail['id']for detail in config)
    termDetails_dict = termDetail.to_dict('records')

    return termDetails_dict, apklist

async def parseApk(serialNoList):
    config = await getInstalledConfig(serialNoList)
    for item in config:
        apklist = item['installedApks']
        df = pd.DataFrame(apklist)
    return df