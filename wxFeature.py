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

        wx.Button(self, 2, 'Send', (0,0), (340,300))
        wx.Button(self, 1, 'Clear', (340,0), (343, 300))
        wx.Button(self, 3, 'Import', (0, 300), (683, 260))

        self.Bind(wx.EVT_BUTTON, self.OnImport,id=3)
        self.Bind(wx.EVT_BUTTON, self.OnSend, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=1)

        self.SetSize((700, 600))
        self.SetTitle('POST Client')
        self.Centre()
        self.Show(True)


    def OnClear(self, e):
        self.paths = []


    def OnSend(self, e):
        codecs.encode('replace')
        for path in self.paths:
            content = SimplePostClient.img_file_content(path.encode("UTF_8"))
            SimplePostClient.manage_post(content.encode("UTF_8"), path.encode("UTF_8"))

        self.paths = []


    def OnQuit(self, e):
        self.Close()


    def OnImport(self, e):
        openFileDialog = wx.FileDialog(self, "Post", '', '', "JPEG image(*.jpg)|*.jpeg|\
        JPG Files (*.jpg)|*.jpg|\
        GIF Files (*.gif)|*.gif|\
        PNG files (*.png)|*.png|\
        Text Files (.txt)|*.txt|\
        All Files (*.*)|*.*", \
        wx.MULTIPLE | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        files = openFileDialog.GetPaths()
        for path in files:
            if path not in self.paths:
                self.paths.append(str(path.encode('UTF_8')))
        print self.paths
        openFileDialog.Destroy()


def main():
    app = wx.App()
    ClientWx(None)
    app.MainLoop()

if __name__ == 'main':
    main()