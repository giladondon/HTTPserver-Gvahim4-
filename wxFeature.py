import wx
import SimplePostClient
import codecs

__author__ = 'Gilad Barak'
__name__ = "main"

class ClientWx(wx.Frame):

    paths = []

    def __init__(self, *args, **kwargs):
        super(ClientWx, self).__init__(*args, **kwargs)

        self.InitUI()


    def InitUI(self):

        wx.Button(self, 2, 'Send', (172, 15), (75,23))
        wx.Button(self, 1, 'Clear', (91,15), (75, 23))
        wx.Button(self, 3, 'Import', (10,15), (75, 23))
        self.panel = wx.Panel(self, pos=(10,40), size=(237,100))
        self.filesList = wx.TextCtrl(self.panel, value="Files to POST:\n", pos=(0,0),\
                                       size=(237,100), style=wx.ALIGN_LEFT | wx.TE_READONLY | wx.TE_MULTILINE)
        self.popUp = wx.MessageDialog(self.panel, str(8)+" files POSTed!", caption="Successful process", style=wx.OK)

        self.Bind(wx.EVT_BUTTON, self.OnImport,id=3)
        self.Bind(wx.EVT_BUTTON, self.OnSend, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=1)

        self.SetSize((275, 200))
        self.SetTitle('POST')
        self.Centre()
        self.Show(True)


    def OnClear(self, e):
        self.filesList.SetValue("Files to POST:\n")
        self.paths = []


    def ShowMessage(self, length):
        wx.MessageBox(length + ' files POSTed!', 'process succeeded',
            wx.OK | wx.ICON_INFORMATION)


    def OnSend(self, e):
        codecs.encode('replace')
        for path in self.paths:
            content = SimplePostClient.img_file_content(path.encode("UTF_8"))
            SimplePostClient.manage_post(content, path)

        self.filesList.SetValue("Files to POST:\n")
        length = len(self.paths)
        self.paths = []

        self.ShowMessage(str(length))


    def OnQuit(self, e):
        self.Close()


    def OnImport(self, e):
        openFileDialog = wx.FileDialog(self, "Post", '', '', "All Files (*.*)|*.*|\
        JPG Files (*.jpg)|*.jpg|\
        GIF Files (*.gif)|*.gif|\
        PNG files (*.png)|*.png|\
        Text Files (.txt)|*.txt|\
        JPEG image(*.jpg)|*.jpeg", \
        wx.MULTIPLE | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        files = openFileDialog.GetPaths()
        for path in files:
            if path not in self.paths:
                self.paths.append(str(path.encode('UTF_8')))
                self.filesList.AppendText(path + "\n")
        openFileDialog.Destroy()


def main():
    app = wx.App()
    ClientWx(None)
    app.MainLoop()

if __name__ == 'main':
    main()