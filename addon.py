#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
from resources.lib import myjdapi
from resources.lib.listing import add_entries, parameters_string_to_dict, convert_size
from resources.lib.menus import get_item_sever, get_item_package, get_item_update_available
from resources.lib.dialogs import put_notification
from resources.lib.helpers import put_log

addon_id = "plugin.program.jdownloader2"
addon = xbmcaddon.Addon(id=addon_id)
addon_name = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')
fanart = ''
pluginhandle = int(sys.argv[1])
TRANSLATE = addon.getLocalizedString

jd_user = addon.getSetting('jd_mail')
jd_pass = addon.getSetting('jd_pass')

#make better
try:
    jd = myjdapi.Myjdapi()
    jd.connect(jd_user, jd_pass)
    jd.update_devices()
except:
    put_notification(addon_name, "AUTH FAILED")


def root():
    list = get_jd_servers()
    if list:  # AUTH SUCCESS
        add_entries(list)
        xbmcplugin.endOfDirectory(pluginhandle)
    else:
        put_notification(addon_name, "NO SERVERS ONLINE")


def get_jd_servers():
    data = jd.list_devices()
    list = []
    if data is not None:  # AUTH FAILED
        for i in data:
            #xbmc.log(str(i))
            list.append({
                "name": i['name'],
                "mode": "server",
                "type": "dir",
                "server_id": i['id']
            })
        return list


def list_server(server_id):
    list = []
    #xbmc.log("server_id_ls")
    #xbmc.log(str(server_id))
    server = jd.get_device(device_id=server_id)
    # check for update
    update = update_available(server)
    if update:
        list.extend(get_item_update_available())
    # add 'downloads' and 'linkgrabber'
    list.extend(get_item_sever())  
    speed = convert_size(server.downloadcontroller.get_speed_in_bytes())
    state = server.downloadcontroller.get_current_state()
    for i in list:
        i['server_id'] = server_id
        if i['mode'] == 'speed':
            buf = i['name']
            buf += ': %s/s' % speed
            i['name'] = buf
        elif i['mode'] == 'set_state':
            buf = i['name']
            buf += ': %s' % state
            i['name'] = buf
    add_entries(list)
    xbmcplugin.endOfDirectory(pluginhandle)


def list_dl_package(url, server_id):
    put_log("LIST-DL-PACK")
    items = []
    uuid = url
    list = query_jd(server_id, True)
    #xbmc.log("LIST")
    #xbmc.log(str(list))
    # items = get_item_dl_package()
    # for i in items:
    #    i['url'] = url
    #    i['server_id'] = server_id
    put_log(str(list))
    for i in list:
        if uuid == str(i.get('uuid', 0)):
            package = i
            for key in package.keys():
                name = key + ': [COLOR FF535452]%s[/COLOR]' % package.get(key, 0)
                if key == "bytesTotal" or key == "bytesLoaded":
                    val = int(package.get(key, 0))
                    #xbmc.log("VAL")
                    #xbmc.log(str(val))
                    name = key + ': [COLOR FF535452]%s[/COLOR]' % convert_size(val)
                items.append({
                    'name': name,
                    'type': 'dir',
                    'url': url,
                    "server_id": server_id,
                    'mode': 'end'
                })
    add_entries(items)
    xbmcplugin.endOfDirectory(pluginhandle)


def list_lg_package(url, server_id):
    put_log("LIST-LG-PACK")
    items = get_item_package()
    # place url, server_id in items
    for i in items:
        i['url'] = url
        i['server_id'] = server_id
    uuid = url
    list = query_jd(server_id, False)
    put_log(str(list))
    for i in list:
        if uuid == str(i.get('uuid', 0)):
            package = i
            for key in package.keys():
                name = key + ': [COLOR FF535452]%s[/COLOR]' % package.get(key, '')
                items.append({
                    'name': name,
                    'type': 'dir',
                    'url': url,
                    'server_id': server_id,
                    'mode': 'end'
                })
    add_entries(items)
    xbmcplugin.endOfDirectory(pluginhandle)


def list_linkgrabber(server_id):
    put_log("LIST-DOWNLOADS")
    #xbmc.log("server_id_l_lg")
    #xbmc.log(str(server_id))
    #xbmc.log("s_id_l_lg_IDIDID")
    #xbmc.log(str(url))
    list = get_jd_linkgrabber(server_id)
    # for i in list:
    #    i['url'] = url
    add_entries(list)
    xbmcplugin.endOfDirectory(pluginhandle)


def list_downloads(server_id):
    put_log("LIST-LINKGRABBER")
    list = get_jd_dls(server_id)
    add_entries(list)
    xbmcplugin.endOfDirectory(pluginhandle)


def get_jd_linkgrabber(server_id):
    #xbmc.log("server_id_jd_lg")
    #xbmc.log(str(server_id))
    # server = jd.get_device(device_id=id)
    data_lg = query_jd(server_id, False)
    #xbmc.log(str(data_lg))
    list = []
    for i in data_lg:
        name = i['name'][:24]
        status = i.get('status', '')[:14]
        if len(name) == 24:
            name += ".."
        name += ' [COLOR FF535452]%s[/COLOR]' % status
        list.append({
            'name': name,
            'mode': 'get_lg_package',
            'url': i['uuid'],
            'type': 'dir',
            "server_id": server_id
        })
    return list


def get_jd_dls(server_id):
    # server = jd.get_device(device_id=id)
    data_dl = query_jd(server_id, True)
    list = []
    for i in data_dl:
        name = i['name'][:24]
        status = i.get('status', '')[:14]
        if len(name) == 24:
            name += ".."
        name += ' [COLOR FF535452]%s[/COLOR]' % status
        list.append({
            'name': name,
            'mode': 'get_dl_package',
            'url': i['uuid'],
            'type': 'dir',
            "server_id": server_id
        })
    return list


def move_to_dl(url, server_id):
    server = jd.get_device(device_id=server_id)
    links_ids = get_lg_package_links(url, server_id)
    packa_ids = []
    #xbmc.log("LINK-IDS")
    #xbmc.log(str(links_ids))
    for i in links_ids:
        packa_ids.append(url)
    server.linkgrabber.move_to_downloadlist(links_ids, packa_ids)
    list_linkgrabber(server_id)


def get_lg_package_links(url, server_id):
    server = jd.get_device(device_id=server_id)
    links = server.linkgrabber.query_links()
    #put_log("GET_LG_PACKAGE_LINKS")
    #put_log(str(links))
    list_links = []
    for i in links:
        if str(i['packageUUID']) == url:
            list_links.append(i['uuid'])
    return list_links


def rename_package(url, server_id):
    dialog = xbmcgui.Dialog()
    term = dialog.input(TRANSLATE(30031), type=xbmcgui.INPUT_ALPHANUM)
    # if user cancels, return
    if not term:
        return -1
    server = jd.get_device(device_id=server_id)
    server.linkgrabber.rename_package(url, term)


def update_available(server):
    return server.update.is_update_available()


def set_state(server_id):
    states = [TRANSLATE(30090), TRANSLATE(30091), TRANSLATE(30092)]
    dialog = xbmcgui.Dialog()
    call = dialog.select("Choose an action", states)
    if call != -1:
        server = jd.get_device(device_id=server_id)
        state = states[call]
        if state == TRANSLATE(30090):
            server.downloadcontroller.start_downloads()
        elif state == TRANSLATE(30091):
            server.downloadcontroller.stop_downloads()
        elif state == TRANSLATE(30092):
            state = server.downloadcontroller.get_current_state()
            if state == "PAUSE":
                server.downloadcontroller.pause_downloads(False)
            else:
                server.downloadcontroller.pause_downloads(True)


def update_jd(server_id):
    dialog = xbmcgui.Dialog()
    bool = dialog.yesno(addon_name, TRANSLATE(30201))
    if bool:
        server = jd.get_device(device_id=server_id)
        server.update.restart_and_update()


def set_system(server_id):
    system = [TRANSLATE(30094), TRANSLATE(30095), TRANSLATE(30096), TRANSLATE(30097), TRANSLATE(30098)]
    dialog = xbmcgui.Dialog()
    call = dialog.select("Choose an action", system)
    if call != -1:
        server = jd.get_device(device_id=server_id)
        res = system[call]
        if res == TRANSLATE(30094):
            server.system.exit_jd()
        elif res == TRANSLATE(30095):
            server.system.restart_jd()
        elif res == TRANSLATE(30096):
            server.system.hibernate_os()
        elif res == TRANSLATE(30097):
            # ask if force shutdown (yes & no)
            server.system.shutdown_os(False)
        elif res == TRANSLATE(30098):
            server.system.standby_os()


def add_container(server_id, type, content):
    server = jd.get_device(device_id=server_id)
    server.linkgrabber.add_container(type, content)


def query_jd(server_id, downloads=True):
    server = jd.get_device(device_id=server_id)
    query = [{
        "bytesLoaded": True,
        "bytesTotal": True,
        "comment": False,
        "enabled": True,
        "eta": True,
        "priority": False,
        "finished": True,
        "running": True,
        "speed": True,
        "status": True,
        "childCount": True,
        "hosts": True,
        "saveTo": True,
        "maxResults": -1,
        "startAt": 0,
    }]
    if downloads == True:
        data = server.downloads.query_packages(query)
    else:
        data = server.linkgrabber.query_packages(query)
    return data

params = parameters_string_to_dict(sys.argv[2])
mode = params.get('mode')
url = params.get('url')
server_id = params.get('server_id')
content = params.get('content')
if type(url) == type(str()):
    url = str(url)

if mode is None:
    root()
if mode == 'server':
    list_server(server_id)
elif mode == 'get_downloads':
    list_downloads(server_id)
elif mode == 'get_linkgrabber':
    list_linkgrabber(server_id)
elif mode == 'get_dl_package':
    list_dl_package(url, server_id)
elif mode == 'get_lg_package':
    list_lg_package(url, server_id)
elif mode == 'rename_package':
    rename_package(url, server_id)
elif mode == 'move_to_dl':
    move_to_dl(url, server_id)
elif mode == 'set_state':
    set_state(server_id)
elif mode == 'update':
    update_jd(server_id)
elif mode == 'system':
    set_system(server_id)
elif mode == 'add_container':
    add_container(server_id, url, content)
