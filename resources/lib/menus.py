import xbmcaddon
import xbmc
import os

addon = xbmcaddon.Addon(id='plugin.program.jdownloader2')
TRANSLATE = addon.getLocalizedString


def get_item_sever():
    item = [
        {
            "name": TRANSLATE(30010),
            "url": "",
            "type": "dir",
            "mode": "get_downloads"

        },
        {
            "name": TRANSLATE(30011),
            "url": "",
            "type": "dir",
            "mode": "get_linkgrabber"

        },
        {
            "name": TRANSLATE(30012),
            "url": "",
            "type": "dir",
            "mode": "set_state"

        },
        {
            "name": TRANSLATE(30013),
            "url": "",
            "type": "dir",
            "mode": "speed"

        },
        {
            "name": TRANSLATE(30014),
            "url": "",
            "type": "dir",
            "mode": "system"
        },

    ]
    return item


def get_item_package():
    item = [
        {
            "name": TRANSLATE(30031),
            "url": "",
            "type": "dir",
            "mode": "rename_package",
            "server_id": ""
        },
        {
            "name": TRANSLATE(30033),
            "url": "",
            "type": "dir",
            "mode": "move_to_dl",
            "server_id": ""
        }
    ]
    return item


def get_item_update_available():
    item = [
        {
            "name": TRANSLATE(30009),
            "mode": "update",
            "url": "",
            "type": "dir",
            "server_id": ""
        }
    ]

    return item
