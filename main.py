#!/usr/bin/env python

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton, ListView
from lib.csvUtil import csv_get_labels
from lib.csvUtil import csv2dic
from lib.csvmerge import merge_files
from time import time
from sys import argv
import os

kivy.require('1.9.0')

Builder.load_string("""
<Message>
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        Label:
            text: root.message
        Button:
            text: "Close"
            size_hint_y: None
            height: 50
            on_release: root.cancel()

<SelectFileAScreen>:
    BoxLayout:
        orientation: "vertical"
        id: appInterface
        Label:
            text: "Select main csv file"
            valign: "top"
            size_hint_y: None
            height: 50
        FileChooserListView:
            id: filechooser
            path: root.root_path
            filters: ['*.csv']

        BoxLayout:
            size_hint_y: None
            height: 70
            Button:
                text: "Select"
                on_release: root.run(filechooser.path, filechooser.selection)

<SelectFileBScreen>:
    BoxLayout:
        orientation: "vertical"
        id: appInterface
        Label:
            text: "Select data source file"
            valign: "top"
            size_hint_y: None
            height: 50
        FileChooserListView:
            id: filechooser
            path: root.root_path
            filters: ['*.csv']

        BoxLayout:
            size_hint_y: None
            height: 70
            Button:
                text: "Select"
                on_release: root.run(filechooser.path, filechooser.selection)

<SelectDataScreen>
    on_enter: root.load()
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "Select key columns"
            valign: "top"
            size_hint_y: None
            height: 50
        BoxLayout:
            orientation: "horizontal"
            BoxLayout:
                orientation: "vertical"
                id: file_a_box
                Label:
                    text: "Main file key column"
                    size_hint_y: None
                    height: 50
                ListView:
                    id: list_view_a
                    adapter: root.list_a_adapter
            BoxLayout:
                orientation: "vertical"
                id: file_b_box
                Label:
                    text: "Source file key column"
                    size_hint_y: None
                    height: 50
                ListView:
                    id: list_view_b
                    adapter: root.list_b_adapter
            BoxLayout:
                orientation: "vertical"
                id: file_c_box
                Label:
                    text: "Select columns to be added"
                    size_hint_y: None
                    height: 50
                ListView:
                    id: list_view_c
                    adapter: root.list_c_adapter
        Button:
            text: "Execute"
            on_release: root.run()
            size_hint_y: None
            height: 70
<SummaryScreen>:
    on_enter: root.run()
    BoxLayout:
        id: box
        orientation: "vertical"
        Label:
            id: status_label
            text: "Executing..."
        BoxLayout:
            size_hint_y: None
            height: 70
            id: button_box
            Button:
                id: b1
                text: "Merge another file"
                disabled: True
                on_release: root.restart()
            Button:
                id: b2
                text: "Add more columns to current file"
                disabled: True
                on_release: root.more_cols()
            Button:
                id: b3
                text: "Exit"
                disabled: True
                on_release: root.exit()

""")


class Message(FloatLayout):
    message = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MyScreen(Screen):
    def __init__(self, *args, **kwargs):
        self._popup = None
        super(MyScreen, self).__init__(*args, **kwargs)

    def run(self, *args):
        raise NotImplementedError("run method must be implemented in child class")

    def dismiss_popup(self):
        if self._popup:
            self._popup.dismiss()


class MyAppManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        self.file_a = None
        self.file_b = None
        self.file_a_key = None
        self.file_b_key = None
        self.columns = []
        super(MyAppManager, self).__init__(*args, **kwargs)

    def load_next_screen(self):
        self.current = ScreenManager.next(self)


class SelectFileAScreen(MyScreen):
    root_path = os.getcwd()

    def run(self, path, filename):

        if len(filename) > 0:
            am.file_a = filename[0]
            am.load_next_screen()
        else:
            message = Message(cancel=self.dismiss_popup, message="No csv file selected")
            self._popup = Popup(title="Message", content=message, size_hint=(0.7, 0.7))
            self._popup.open()


class SelectDataScreen(MyScreen):
    def __init__(self, *args, **kwargs):
        self.file_a_labels = []
        self.file_b_labels = []
        self.args_converter = lambda row_index, rec: {'text': rec,
                                                      'size_hint_y': None,
                                                      'height': 25}
        self.list_a_adapter = ListAdapter(data=self.file_a_labels,
                                          args_converter=self.args_converter,
                                          cls=ListItemButton,
                                          selection_mode='single',
                                          allow_empty_selection=False)

        self.list_b_adapter = ListAdapter(data=self.file_b_labels,
                                          args_converter=self.args_converter,
                                          cls=ListItemButton,
                                          selection_mode='single',
                                          allow_empty_selection=False)

        self.list_c_adapter = ListAdapter(data=self.file_b_labels,
                                          args_converter=self.args_converter,
                                          cls=ListItemButton,
                                          selection_mode='multiple',
                                          allow_empty_selection=True)

        super(SelectDataScreen, self).__init__(*args, **kwargs)

    def load(self):
        self.list_a_adapter.data = csv_get_labels(am.file_a)
        self.list_b_adapter.data = csv_get_labels(am.file_b)
        self.list_c_adapter.data = csv_get_labels(am.file_b)

    def run(self):

        if len(self.list_a_adapter.selection) > 0 and len(self.list_b_adapter.selection) > 0 and len(
                self.list_c_adapter.selection) > 0:
            am.file_a_key = self.list_a_adapter.selection[0].text
            am.file_b_key = self.list_b_adapter.selection[0].text
            for selection in self.list_c_adapter.selection:
                am.columns.append(selection.text)
            am.load_next_screen()
        else:
            message = Message(cancel=self.dismiss_popup, message="Please select all data columns")
            self._popup = Popup(title="Message", content=message, size_hint=(0.7, 0.7))
            self._popup.open()


class SelectFileBScreen(MyScreen):
    root_path = os.getcwd()

    def run(self, path, filename):

        if len(filename) > 0:
            am.file_b = filename[0]
            am.load_next_screen()
        else:
            message = Message(cancel=self.dismiss_popup, message="No csv file selected")
            self._popup = Popup(title="Message", content=message, size_hint=(0.7, 0.7))
            self._popup.open()


class SummaryScreen(MyScreen):
    def exit(self):
        App.get_running_app().stop()

    def more_cols(self):
        am.current = "scr3"

    def restart(self):
        am.current = "scr1"

    def run(self, *args):
        start_time = time()
        source_data = csv2dic(am.file_b, am.file_b_key)
        mod_rows_counter = merge_files(am.file_a,
                                       source_data,
                                       am.file_a_key,
                                       am.columns)
        self.ids["status_label"].text = "Finished in {0:.2f} seconds. Rows modified: {1:.0f}".format(
            time() - start_time, mod_rows_counter)
        self.ids["b1"].disabled = False
        self.ids["b2"].disabled = False
        self.ids["b3"].disabled = False


am = MyAppManager()
am.add_widget(SelectFileAScreen(name='scr1'))
am.add_widget(SelectFileBScreen(name='scr2'))
am.add_widget(SelectDataScreen(name='scr3'))
am.add_widget(SummaryScreen(name='scr4'))
if len(argv) > 1:
    cur_file = argv[1]
    if os.path.isfile(cur_file):
        am.file_a = cur_file
        am.current = "scr2"


class Main(App):
    def build(self):
        return am


if __name__ == '__main__':
    Main().run()
