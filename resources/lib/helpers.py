#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmcaddon, xbmc

addon_id = "plugin.program.jdownloader2"
addon = xbmcaddon.Addon(id=addon_id)
addon_name = addon.getAddonInfo('name')
addon_version = addon.getAddonInfo('version')


def put_log(msg, log_lvl=xbmc.LOGDEBUG):
    log_std = '%s - %s - ' % (addon_id, addon_version)
    try:
        log_msg = log_std + msg.encode('utf-8')
    except:
        try:
            log_msg = log_std + str(msg)
        except:
            log_msg = log_std + 'Message cannot be displayed!'
    xbmc.log(log_msg, log_lvl)
