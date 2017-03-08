# -*- coding: utf-8 -*-
import xbmcgui


def put_notification(head, line, dura=3):
    # TODO icon
    dialog = xbmcgui.Dialog()
    dialog.notification(head, line, xbmcgui.NOTIFICATION_INFO, dura)
