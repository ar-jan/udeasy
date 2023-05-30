import sqlite3
import wx


class Translations(wx.Panel):
    """
    Choose file panel class: shows the dialog to select a translations database
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Translations, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, parent):
        if not hasattr(self, 'initialized') or not self.initialized:
            wx.Panel.__init__(self, parent)
            self.parent = parent
            self.main_sizer = wx.BoxSizer(wx.VERTICAL)
            self.first_sizer = wx.BoxSizer(wx.HORIZONTAL)
            title = wx.StaticText(self, label="Select a translations database file -->")
            title.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            self.first_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            openFileDlgBtn = wx.Button(self, label='Choose file')
            openFileDlgBtn.Bind(wx.EVT_BUTTON, self.onOpenFile)
            self.first_sizer.Add(openFileDlgBtn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.main_sizer.Add(self.first_sizer)
            self.SetSizer(self.main_sizer)
            self.initialized = True


    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        wildcard = "Sqlite database files (*.db)|*.db|" \
                   "All files (*.*)|*.*"

        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir="",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            setattr(self, 'file_path', paths[0])
        dlg.Destroy()
        if hasattr(self, "selected_file"):
            self.selected_file.Destroy()
        setattr(self, "second_sizer", wx.BoxSizer(wx.HORIZONTAL))
        setattr(self, "selected_file", wx.StaticText(self, label=f"Selected file: {getattr(self, 'file_path')}"))
        self.second_sizer.Add(self.selected_file, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.second_sizer, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(self.main_sizer)
        self.Parent.Layout()

        if hasattr(self, "file_path"):
            self.translationsdb = self.file_path
            self.conn = sqlite3.connect(self.translationsdb)
            self.cur = self.conn.cursor()


    def get_translation(self, sent_id):
        """ Takes a sentence_id as argument, and returns the corresponding translation
        :param sent_id: the sentence_id
        :return: string with the sentence translation
        """
        if self.cur:
            translation = self.cur.execute(
                ''' SELECT sentence_text_translation
                FROM sentences
                WHERE sentence_id = :sent_id;
                ''', {'sent_id': sent_id}
                ).fetchone()[0]

            return translation

        else:
            return None
