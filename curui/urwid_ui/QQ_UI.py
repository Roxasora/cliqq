#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  file   : QQ_UI.py
#  author : atupal
#
#  Copyright 2013 atupal [HUST university uniquestudio algorithm group] <me@atupal.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  site: http://atupal.org

import urwid
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:from qq.runqq import msg_queue
except:pass
import threading
from random import randint

class process_msg_daemon(threading.Thread):
    def __init__(self, msg_queue, qq, ui):
        threading.Thread.__init__(self)
        self.msg_queue = msg_queue
        self.qq = qq
        self.locale_message = open('res/message.dat', 'aw')
        self.ui = ui

    def run(self):
        while 1:
            msg = self.msg_queue.get()
            #print msg[0], ':', msg[1]
            self.locale_message.write(str(msg[0]) + ':' + str(msg[1]) + '\n')
            if msg[3] == 1:
                self.qq.sendMsg(msg[2], '我寂寞装逼迷人', face = randint(1,80))
            elif self.qq.gid[msg[2]] == 'test_1' or self.qq.gid[msg[2]] == '啦啦啦*17-422*啦啦啦' or self.qq.gid[msg[2]] == "alg":
                self.qq.sendQunMsg(msg[2], '我寂寞装逼迷人', face = randint(1,80))
            self.ui.new_msg(msg)
            self.ui.loop.draw_screen()
            self.msg_queue.task_done()


choices = {'friend', 'friend2', 'yukangle','1', '2','3', '4', '5', '6', '7', '8', '9', '10', '12', '123', 'nimei', 'nimei_1', 'nimie_2', 'dsnfaf', 'sfsf', 'sdfjkasdjfl', 'sdfzhe s', }
class QQ_UI():
    def __init__(self, Q=None):
        if Q is None:
            self.categories = choices
            return
        self.flag = 0
        self.categories = set()
        self.msg = dict()
        Q.run()

        Q.pro_msg = process_msg_daemon(msg_queue, Q.qq, self)
        Q.pro_msg.setDaemon(True)
        Q.pro_msg.start()

        self.qq = Q.qq
        for i in Q.qq.categories:
            self.categories.add(str(i['name']))

        self.palette = []

    def line_dialog(self, uid, Text = None):
        text = urwid.Text(uid, align = 'center', wrap='clip')
        for i in Text:
            text.set_text(text.text + '\n' + i)
        return text

    def categories_list(self):

        button_1 = urwid.Button(u'好友列表')
        button_2 = urwid.Button(u'群列表')
        button_3 = urwid.Button(u'最近联系人')
        self.cat_list_body = [button_1, button_2, button_3, urwid.Divider()]
        for c in self.categories:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.category_chosen, c)
            self.cat_list_body.append(urwid.AttrMap(button, None, focus_map = 'reversed'))

        self.cat_list_listBox = urwid.ListBox(urwid.SimpleFocusListWalker(self.cat_list_body))
        return self.cat_list_listBox

    def msg_bubble(self):
        #testButton = urwid.Button('test')
        #urwid.connect_signal(testButton, 'click', self.msg_chosen, str(time.time()))
        self.msg_bubble_body = urwid.SimpleFocusListWalker([urwid.Divider(),urwid.Divider(), urwid.Text(u'消息')])
        self.msg_bubble_listBox = urwid.ListBox(self.msg_bubble_body)
        return self.msg_bubble_listBox

    def category_chosen(self, button, category):
        #pos = self.cat_list_listBox.focus_position
        #self.cat_list_listBox.body.insert(pos + 1, urwid.Text(' nimei'))
        return
        response = urwid.Text(['You are chose', category , '\n'])
        click = urwid.Button('ok')
        urwid.connect_signal(click, 'click', self.exit_program)
        #self.base.original_widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(click, None, focus_map='reserved')]))
        self.loop.widget = urwid.Filler(urwid.Pile([response, urwid.AttrMap(click, None, focus_map='reserved')]))

    def msg_chosen(self, button, msg):
        cnt = len(self.base.contents)
        #text_dlg = urwid.Text(str(time.time()))
        text_dlg = urwid.Text(self.msg[msg[2]])
        self.msg.pop(msg[2])
        input_dlg = urwid.Edit(":")
        send = urwid.Button('send')
        urwid.connect_signal(send, 'click', self.send_msg, (msg[2], str(input_dlg.edit_text) + "$"))
        cancel = urwid.Button('cancel')
        new_line_dlg = urwid.Filler(urwid.Pile([text_dlg, urwid.Divider(), input_dlg, urwid.Divider(), send, urwid.Divider(), cancel]))
        if cnt > 4:
            self.base.contents = [self.base.contents[0]] + self.base.contents[2:]
            #self.base.contents[4:] =[(urwid.ListBox([urwid.Button(str(time.time()))]), self.base.options())]
            self.base.contents[4:] =[(new_line_dlg, self.base.options())]
        else:
            #self.base.contents[cnt:] =[(urwid.ListBox([urwid.Button(str(time.time()))]), self.base.options())]
            self.base.contents[cnt:] =[(new_line_dlg, self.base.options())]

    def new_msg(self, msg):
        #self.msg = dict()
        if msg[2] in self.msg.keys():
            self.msg[msg[2]] += msg[0] + msg[1] + '\n'
        else:
            self.msg[msg[2]] = msg[0] + msg[1] + '\n'
            try:
                new_msg_bt = urwid.Button(str(self.qq.uin[msg[2]]))
            except:
                new_msg_bt = urwid.Button(msg[0].split(' ')[0])
            urwid.connect_signal(new_msg_bt, 'click', self.msg_chosen, msg)
            self.msg_bubble_listBox.body.insert(0, new_msg_bt)
        pass

    def send_msg(self, button, msg_user_content):
        self.qq.sendMsg(msg_user_content[0], msg_user_content[1])
        pass

    def  exit_program(self, button):
        raise urwid.ExitMainLoop()

    def cancel(self,button):
        pass

    def begin(self, button=None):
        #好友列表
        self.cat_list_pad = urwid.Padding(self.categories_list(), left = 2, right = 2)
        self.cat_list_overlay = urwid.Overlay(self.cat_list_pad, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                align = 'left', width = 40,
                valign = 'top', height = 40,
                min_width = 20, min_height = 9)


        #消息气泡
        self.msg_bubble_pad = urwid.Padding(self.msg_bubble(), left = 2, right = 2)
        self.msg_bubble_overlay = urwid.Overlay(self.msg_bubble_pad, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                align = 'left', width = 40,
                valign = 'top', height = 40,
                min_width = 20, min_height = 1)

        self.left_bar_pile = urwid.Pile([self.cat_list_overlay, self.msg_bubble_overlay])

        test = urwid.Button('test')
        self.msg_bubble_listBox.body.insert(0, test)

        self.base = urwid.Columns([self.left_bar_pile], dividechars = 1, min_width = 10)
        self.loop = urwid.MainLoop(self.base, palette = [('reversed', 'standout', '')])
        self.loop.run()

if __name__ == "__main__":
    QQ_UI().begin()
