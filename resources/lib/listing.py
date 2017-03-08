import xbmc
import xbmcgui
import xbmcplugin
import sys

from urllib import quote_plus
from helpers import put_log

pluginhandle = int(sys.argv[1])


def add_entries(entries_list):
    entries = []
    is_folder = False
    put_log('add_entries_start')
    for entry in entries_list:
        put_log(str(entry))
        entry_name = entry['name']
        item = xbmcgui.ListItem(entry_name)
        item.setArt(entry.get('images'))
        item.addContextMenuItems(entry.get('cm', []))
        entry_url = get_entry_url(entry)
        info_labels = entry.get('infolabels')
        if entry['type'] == 'video':
            item.setInfo(type="video", infoLabels=info_labels)
            item.setProperty('IsPlayable', 'true')
            is_folder = False
        if entry['type'] == 'dir':
            item.setInfo(type="video", infoLabels=info_labels)
            is_folder = True
        entries.append([entry_url, item, is_folder])
    xbmcplugin.addDirectoryItems(pluginhandle, entries)


def get_entry_url(entry_dict):
    put_log("GET-ENTRY-URL")
    entry_url = sys.argv[0] + '?'
    for param in entry_dict:
        put_log(str(param))
        if not isinstance(entry_dict[param], dict) and not isinstance(entry_dict[param], list) and str(param != 'desc'):
            if isinstance(entry_dict[param], unicode):
                entry_dict[param] = entry_dict[param].encode("UTF-8")
            elif isinstance(entry_dict[param], long) or isinstance(entry_dict[param], int):
                entry_dict[param] = str(entry_dict[param])
            entry_url += "%s=%s&" % (param, quote_plus(entry_dict[param]))
    if entry_url.endswith("&"):
        entry_url = entry_url[:-1]
    return entry_url


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def convert_size(size_bytes):
    # credits to http://stackoverflow.com/a/14822210
    import math
    if (size_bytes == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '%s %s' % (s, size_name[i])
