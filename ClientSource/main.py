import wx
import json
import os
import os.path

from urllib.request import urlopen

VERSION = 'v3'

class MyFrame(wx.Frame):
    version = None
    address = 'http://localhost:8080'

    my_label = None
    my_btn = None
    my_forceBtn = None

    isUpdating = False

    def __init__(self):
        super().__init__(parent=None, title='Simple Mod List Version Control ' + VERSION, size=(400, 200), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        panel = wx.Panel(self)

        self.my_checkbox = wx.CheckBox(panel, label='Forbid reupload', pos=(45, 20))
        self.my_checkbox.SetValue(True)
        self.my_btn = wx.Button(panel, label='Check version and update', pos=(195 - 150, 70 - 20), size=(300, 70))
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        self.my_forceBtn = wx.Button(panel, label='Force update', pos=(195 - 150, 70 - 50 + 100), size=(300, 30))
        self.my_forceBtn.Bind(wx.EVT_BUTTON, self.on_force_update)

        self.address = self.set_address()

        self.Show()

    def on_press(self, event):
        if not self.isUpdating:
            self.comp_versions()

    def on_force_update(self, event):
        if not self.isUpdating:
            jsonVersion = self.read_url("/version.json")
            f = open("version.json", "wb")
            f.write(jsonVersion)
            f.close()
            self.version = self.check_current_version()
            self.do_update()

    def read_file(self, path):
        if os.path.isfile(path):
            f = open(path, 'r')
            fileText = f.read()
            f.close()
            return fileText
        else:
            return None

    def read_url(self, path):
        with urlopen(self.address + path) as f:
            return f.read()

    def check_current_version(self):
        text = self.read_file('version.json')
        if text:
            return json.loads(text)['version']
        else:
            print("Version file doesn't exist!")
            return None

    def set_address(self):
        text = self.read_file('conf.json')
        if text:
            return json.loads(text)['address']
        else:
            print("Configuration file doesn't exist!")
            return self.address

    def comp_versions(self):
        jsonVersion = self.read_url("/version.json")
        self.version = self.check_current_version()
        if self.version == None:
            f = open("version.json", "wb")
            f.write(jsonVersion)
            f.close()
            self.version = self.check_current_version()
            self.do_update()
            return
        if self.version < json.loads(jsonVersion)['version']:
            f = open("version.json", "wb")
            f.write(jsonVersion)
            f.close()
            self.version = self.check_current_version()
            self.do_update()
            return
        print("Already updated!")
        self.my_btn.SetLabel("Already updated!")

    def do_update(self):
        self.isUpdating = True
        print('Update begins!')
        self.my_btn.SetLabel("Update begins!")
        updateInfo = json.loads(self.read_url('/' + str(self.version) + '.json'))
        if not os.path.exists(updateInfo['destinationFolder']):
            os.makedirs('./' + updateInfo['destinationFolder'])
        for mod in updateInfo['addList']:
            if mod in updateInfo['addList']:
                continue
            if self.my_checkbox.GetValue() and os.path.isfile('./' + updateInfo['destinationFolder'] + mod):
                continue
            print("    - Downloading mod: " + mod)
            modData = self.read_url('/' + updateInfo['destinationFolder'] + mod)
            f = open(updateInfo['destinationFolder'] + mod, "wb")
            f.write(modData)
            f.close()
        for mod in updateInfo['removeList']:
            if not os.path.isfile('./' + updateInfo['destinationFolder'] + mod):
                continue
            print("    - Removing mod: " + mod)
            os.remove(updateInfo['destinationFolder'] + mod)
        print("Mod list update success!")
        self.my_btn.SetLabel("Mod list update success!")
        self.isUpdating = False

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
