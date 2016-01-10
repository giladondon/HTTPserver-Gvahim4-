import wx
import SimplePostClient
import codecs

"""
File Documentation: Graphic present of POST client from 4.10-4.11 Gvahim Book
Takes SimplePostClient.py to a whole new level with cut-end revolutionary design.
Using the brand new wxPython package this feature allows the user to enjoy a more friendly, welcoming experience.
"""

__author__ = 'Gilad Barak'
__name__ = "main"

BUTTONSIZE = (75, 23)
PANELSIZE = (237,100)
PANELPOS = (10,10)
CLEARPOS = (92,120)
SENDPOS = (172, 120)
LISTSIZE = (237,100)
WINDOWSIZE = (275, 210)
WINDOWCAPTION = 'POST'

class ClientWx(wx.Frame):

    paths = []


    def __init__(self, *args, **kwargs):
        super(ClientWx, self).__init__(*args, **kwargs)

        self.InitUI()


    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        importf = fileMenu.Append(wx.ID_ANY, 'Import files')
        qItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, qItem)
        self.Bind(wx.EVT_MENU, self.OnImport, importf)

        wx.Button(self, 2, 'Send', SENDPOS, BUTTONSIZE)
        wx.Button(self, 1, 'Clear', CLEARPOS, BUTTONSIZE)
        self.panel = wx.Panel(self, pos=PANELPOS, size=PANELSIZE)
        self.filesList = wx.TextCtrl(self.panel, value="Files to POST:\n",\
                                       size=LISTSIZE, style=wx.ALIGN_LEFT | wx.TE_READONLY | wx.TE_MULTILINE)

        self.Bind(wx.EVT_BUTTON, self.OnImport,id=3)
        self.Bind(wx.EVT_BUTTON, self.OnSend, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=1)

        self.SetSize(WINDOWSIZE)
        self.SetTitle(WINDOWCAPTION)
        self.Centre()
        self.Show(True)


    def OnClear(self, e):
        """
        Clear chosen files from both paths and filesList, makes it seem like window just opened.
        """
        self.filesList.SetValue("Files to POST:\n")
        self.paths = []


    def ShowMessage(self, length):
        """
        Pops up a message OK dialog
        """
        wx.MessageBox(length + ' files POSTed!', 'process succeeded',
            wx.OK | wx.ICON_INFORMATION)


    def OnSend(self, e):
        """
        Deals with sending files to server.
        Sends files from paths, clears printing and pops up a message OK dialog
        """
        codecs.encode('replace')
        for path in self.paths:
            content = SimplePostClient.img_file_content(path.encode("UTF_8"))
            SimplePostClient.manage_post(content, path)

        self.filesList.SetValue("Files to POST:\n")
        length = len(self.paths)
        self.paths = []

        self.ShowMessage(str(length))


    def OnQuit(self, e):
        """
        Quits application
        """
        self.Close()


    def OnImport(self, e):
        """
        Deals with importing, opens a dialog box for user to import files.
        Appends chosen files to paths and prints to filesList
        """
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