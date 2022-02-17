import wx


class Features(wx.Panel):
    """
    Panel in the stats_query_frame
    """
    def __init__(self, parent, node_list):
        self.count = 1
        self.ids = [1]
        self.parent = parent
        self.nodes = node_list
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Features distributions")
        title.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_LEFT, 5)
        setattr(self, f"feat_row{self.count}", FeatRow(self))
        self.main_sizer.Add(getattr(self, f"feat_row{self.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()


class FeatRow(wx.Panel):
    def __init__(self, parent):
        self.parent = parent
        self.id = self.parent.count
        self.nodes = parent.nodes
        wx.Panel.__init__(self, parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(self, label=f"select node:")
        self.main_sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        setattr(self, "node", wx.ComboBox(self, choices=self.nodes))
        feat = wx.StaticText(self, label="write feature")
        setattr(self, "feat", wx.TextCtrl(self))
        self.main_sizer.Add(self.node, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(feat, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.main_sizer.Add(self.feat, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        btn_add = wx.Button(self, label='+')
        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        self.main_sizer.Add(btn_add, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        if parent.count > 1:
            btn_rmv = wx.Button(self, label='-')
            btn_rmv.Bind(wx.EVT_BUTTON, self.on_rmv)
            self.main_sizer.Add(btn_rmv, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.main_sizer)
        self.Layout()

    def on_add(self, event):
        self.parent.count += 1
        self.parent.ids.append(self.parent.count)
        setattr(self.parent, f"feat_row{self.parent.count}", FeatRow(self.parent))
        self.parent.main_sizer.Add(getattr(self.parent, f"feat_row{self.parent.count}"), 0, wx.ALL | wx.ALIGN_LEFT, 5)
        self.parent.SetSizer(self.parent.main_sizer)
        self.parent.SetSizer(self.parent.main_sizer)
        self.parent.Parent.Layout()
        self.parent.Parent.SetupScrolling(scrollToTop=False)
        self.parent.Parent.Scroll(-1, self.parent.Parent.GetScrollRange(wx.VERTICAL))

    def on_rmv(self, event):
        self.parent.ids.remove(self.id)
        self.Destroy()
        self.parent.Parent.Layout()
        self.parent.Layout()
