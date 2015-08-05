
import os
import time
import wx
import networkx as nx
import matplotlib.pyplot as plt

from kanonymity import *
#-------------------------------------------------------------------------------
True=1
False=0

APP_NAME = "IMS Data Privacy Demo"

# --- Menu and control ID's
ID_NEW=101
ID_OPEN=102
ID_SAVE=103
ID_SAVEAS=104
ID_EXIT=109

ID_LOAD_TXT=120
ID_LOAD_NET=121

ID_SAVE_NET=129

ID_KANON=130
ID_RANDOM=131

ID_ANALYZE=142
ID_DEGREE=143
ID_CLUSTERING=144
ID_CLUSTERING=145
ID_APL=146
ID_DRAW=147

ID_ABOUT=141

ID_RTB=201

SB_INFO = 0
SB_ROWCOL = 1
SB_DATETIME = 2
#---------------------------------------------------------------
class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
 
    def __call__(cls, *args, **kw):
        if not cls.instance:
            # Not created or has been Destroyed
            obj = super(Singleton, cls).__call__(*args, **kw)
            cls.instance = obj
            cls.instance.SetupWindow()
 
        return cls.instance
#--------------------------------------------------------------
class SingletonDialog(wx.Dialog):
    __metaclass__ = Singleton

    def SetupWindow(self):
        """Hook method for initializing window"""
        self.field = wx.TextCtrl(self)
        self.check = wx.CheckBox(self, label="Enable Foo")

        # Layout
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="FooBar")
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddMany([(label, 0, wx.ALIGN_CENTER_VERTICAL),
                        ((5, 5), 0),
                        (self.field, 0, wx.EXPAND)])
        btnsz = self.CreateButtonSizer(wx.OK)
        btnsc = self.CreateButtonSizer(wx.CANCEL)
        vsizer.AddMany([(hsizer, 0, wx.ALL|wx.EXPAND, 10),
                        (self.check, 0, wx.ALL, 10),(btnsc, 0, wx.EXPAND|wx.ALL, 10),
                        (btnsz, 0, wx.EXPAND|wx.ALL, 10)])
        self.SetSizer(vsizer)
        self.SetInitialSize()
        
# --- our frame class
class dpFrame(wx.Frame):
    """ Derive a new class of wxFrame. """  
    
    def __init__(self, parent, id, title):
        # --- a basic window frame/form
        wx.Frame.__init__(self, parent = None, id = -1,
                         title = APP_NAME,
                         pos = wx.Point(200, 200), size = wx.Size(800, 600),
                         name = '', style = wx.DEFAULT_FRAME_STYLE)

        # --- real windows programs have icons, so here's ours!
        # XXX see about integrating this into our app or a resource file
        try:            # - don't sweat it if it doesn't load
            self.SetIcon(wx.Icon("face-monkey.png", wx.BITMAP_TYPE_PNG))
            pass
        finally:
            pass

        # --- add a menu, first build the menus (with accelerators
        fileMenu = wx.Menu()

        fileMenu.Append(ID_NEW, "&New\tCtrl+N", "Creates a new file")
        wx.EVT_MENU(self, ID_NEW, self.OnFileNew)
        #fileMenu.Append(ID_OPEN, "&Open\tCtrl+O", "Opens an existing file")
        #wx.EVT_MENU(self, ID_OPEN, self.OnFileOpen)
        fileMenu.Append(ID_SAVE, "&Save\tCtrl+S", "Save the active file")
        wx.EVT_MENU(self, ID_SAVE, self.OnFileSave)
        fileMenu.Append(ID_SAVEAS, "Save &As...", "Save the active file with a new name")
        wx.EVT_MENU(self, ID_SAVEAS, self.OnFileSaveAs)

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, "E&xit\tAlt+Q", "Exit the program")
        wx.EVT_MENU(self, ID_EXIT, self.OnFileExit)
        
        graphMenu=wx.Menu()
        graphMenu.Append(ID_LOAD_TXT,"&Load '.txt'\tCtrl+L","Load a new data file .txt")
        wx.EVT_MENU(self,ID_LOAD_TXT,self.OnLoadFileTxt)
        graphMenu.Append(ID_LOAD_NET,"&Load '.net'","Load a new data file .net ")
        wx.EVT_MENU(self,ID_LOAD_NET,self.OnLoadFileNet)

        graphMenu.Append(ID_SAVE_NET,"&Save '.net'","Save data file .net ")
        wx.EVT_MENU(self,ID_SAVE_NET,self.OnSaveFileNet)

        
        protectMenu=wx.Menu()
        protectMenu.Append(ID_KANON,"&Kanony\tCtrl+K","k-Anonymity")
        wx.EVT_MENU(self,ID_KANON,self.OnKanon)        
        protectMenu.Append(ID_RANDOM,"&Random\tCtrl+R","Random")
        wx.EVT_MENU(self,ID_RANDOM,self.OnRandom)
 
        analyzeMenu=wx.Menu()
        analyzeMenu.Append(ID_DRAW,"&Draw\tCtrl+D","Draw the graph")
        wx.EVT_MENU(self,ID_DRAW,self.OnDrawGraph)
        analyzeMenu.Append(ID_ANALYZE,"&Degree centrality\t","Degree centrality")
        wx.EVT_MENU(self,ID_ANALYZE,self.OnAnalyze)
        analyzeMenu.Append(ID_DEGREE,"&Degree distrabution\t","Degree distrabution")
        wx.EVT_MENU(self,ID_DEGREE,self.OnDegree)
        analyzeMenu.Append(ID_CLUSTERING,"&Clustering\t","Clustering")
        wx.EVT_MENU(self,ID_CLUSTERING,self.OnClustering)
        analyzeMenu.Append(ID_APL,"&apl\t","Average shortest path")
        wx.EVT_MENU(self,ID_APL,self.OnApl)


        helpMenu = wx.Menu()
        helpMenu.Append(ID_ABOUT, "&About", "Display information about the program")
        wx.EVT_MENU(self, ID_ABOUT, self.OnHelpAbout)


        # --- now add them to a menubar & attach it to the frame
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(graphMenu,"&Graph")
        menuBar.Append(protectMenu, "&Protect")
        menuBar.Append(analyzeMenu, "&Analyze")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        
        #  Not needed!, just put them in text form after tab in menu item!
        # --- add accelerators to the menus
        #self.SetAcceleratorTable(wx..AcceleratorTable([(wxACCEL_CTRL, ord('O'), ID_OPEN), 
        #                          (wxACCEL_ALT, ord('Q'), ID_EXIT)]))

        # --- add a statusBar (with date/time panel)
        sb = self.CreateStatusBar(3)
        sb.SetStatusWidths([-1, 65, 150])
        sb.PushStatusText("Ready", SB_INFO)
        # --- set up a timer to update the date/time (every 5 seconds)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(5000)
        self.Notify()       # - call it once right away

        # --- add a control (a RichTextBox) & trap KEY_DOWN event
        self.rtb = wx.TextCtrl(self, ID_RTB, size=wx.Size(800,600),
                              style=wx.TE_MULTILINE | wx.TE_RICH2)
        ### - NOTE: binds to the control itself!
        wx.EVT_KEY_UP(self.rtb, self.OnRtbKeyUp)

        # --- need to add a sizer for the control - yuck!
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.SetMinSize(200,400)
        self.sizer.Add(self.rtb, 1, wx.EXPAND)
        # --- now add it to the frame (at least this auto-sizes the control!)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.SetSizeHints(self)

        # --- initialize other settings
        self.dirName = ""
        self.fileName = ""
        self.g=nx.Graph()

        # - this is ugly, but there's no static available 
        #   once we build a class for RTB, move this there
        self.oldPos = -1
        self.ShowPos()

        # --- finally - show it!
        self.Show(True)

#---------------------------------------
    def __del__(self):
        """ Class delete event: don't leave timer hanging around! """
        self.timer.stop()
        del self.timer

#---------------------------------------
    def Notify(self):
        """ Timer event """
        t = time.localtime(time.time())
        st = time.strftime(" %b-%d-%Y  %I:%M %p", t)
        # --- could also use self.sb.SetStatusText
        self.SetStatusText(st, SB_DATETIME)

#---------------------------------------
    def OnFileExit(self, e):
        """ File|Exit event """
        self.Close(True)

#---------------------------------------
    def OnFileNew(self, e):
        """ File|New event - Clear rtb. """
        self.fileName = ""
        self.dirName = ""
        self.rtb.SetValue("")
        self.PushStatusText("Starting new file", SB_INFO)
        self.ShowPos()

#---------------------------------------
    def OnFileOpen(self, e):
        """ File|Open event - Open dialog box. """
        dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|Pajek File (*.net)|*.net|All Files|*.*", wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            

            ### - this will read in Unicode files (since I'm using Unicode wxPython
            #if self.rtb.LoadFile(os.path.join(self.dirName, self.fileName)):
            #    self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) + 
            #                       " characters.", SB_INFO)
            #    self.ShowPos()
            #else:
            #    self.SetStatusText("Error in opening file.", SB_INFO)

            ### - but we want just plain ASCII files, so:
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'r')
                self.rtb.SetValue(f.read())
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) +
                                   " characters.", SB_INFO)
                self.ShowPos()
                f.close()
            except:
                self.PushStatusText("Error in opening file.", SB_INFO)
        dlg.Destroy()

#---------------------------------------
    def OnFileSave(self, e):
        """ File|Save event - Just Save it if it's got a name. """
        if (self.fileName != "") and (self.dirName != ""):
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'w')
                f.write(self.rtb.GetValue())
                self.PushStatusText("Saved file: " + str(self.rtb.GetLastPosition()) +
                                    " characters.", SB_INFO)
                f.close()
                return True
            except:
                self.PushStatusText("Error in saving file.", SB_INFO)
                return False
        else:
            ### - If no name yet, then use the OnFileSaveAs to get name/directory
            return self.OnFileSaveAs(e)

#---------------------------------------
    def OnFileSaveAs(self, e):
        """ File|SaveAs event - Prompt for File Name. """
        ret = False
        dlg = wx.FileDialog(self, "Save As", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|All Files|*.*", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.OnFileSave(e):
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                ret = True
        dlg.Destroy()
        return ret

#---------------------------------------
    def OnLoadFileTxt(self,e):
        """ File|Open event - Open dialog box. """
        
        dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|Pajek File (*.net)|*.net|All Files|*.*", wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
    
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'r')
                self.rtb.SetValue(f.read())
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) +
                                   " characters.", SB_INFO)
                self.ShowPos()
                f.close()
            except:
                self.PushStatusText("Error in opening file.", SB_INFO)
          
        dlg.Destroy()
        self.fileName=os.path.join(self.dirName, self.fileName)
        print self.fileName
        #try:
        #    if self.fileName!=self.dirName:
        #        g=readFileTxt(g)
        #except:
        #    self.PushStatusText("Error in opening file.", SB_INFO)

        #print self.g.nodes()

        if self.fileName!=self.dirName:
            read_file_txt(self.g,self.fileName)    
            if len(self.g.nodes())==0:
                wx.MessageBox("Not read data from the file!!")
        
#---------------------------------------
    def OnLoadFileNet(self,e):
        """ File|Open event - Open dialog box. """
        
        dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                           "Pajek File (*.net)|*.net|Text Files (*.txt)|*.txt|All Files|*.*", wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
    
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'r')
                self.rtb.SetValue(f.read())
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) +
                                   " characters.", SB_INFO)
                self.ShowPos()
                f.close()
            except:
                self.PushStatusText("Error in opening file.", SB_INFO)
          
        dlg.Destroy()
        self.fileName=os.path.join(self.dirName, self.fileName)
        #print self.fileName

        if self.fileName!=self.dirName:
            self.g.clear()             
            self.g=read_file_net(self.g,self.fileName)
            if len(self.g.nodes())==0:
                wx.MessageBox("Not read data from the file!!")  
#---------------------------------------
    def OnSaveFileNet(self,e):
        """ File|Save event - Just Save the memory data in a .net file """
 
        ret = False
        dlg = wx.FileDialog(self, "Save As", self.dirName, "",
                           "Text Files (*.net)|*.net", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            self.mfileName = dlg.GetFilename()
            self.mdirName = dlg.GetDirectory()            ### - Use the OnFileSave to save the file
        
            if (self.mfileName != "") and (self.mdirName != ""):
                saveFileNet(self.g,os.path.join(self.mdirName, self.mfileName))
                self.SetTitle(APP_NAME + " - [" + self.mfileName + "]")
         
        dlg.Destroy()
  


#---------------------------------------
    def OnDrawGraph(self,e):
        DrawGraph(self.g)
#---------------------------------------
    def OnKanon(self,e):
        self.rtb.SetValue("")
        self.PushStatusText("Starting k-anonymity", SB_INFO)
        self.ShowPos()
        k=0
        dlg=wx.NumberEntryDialog(self,message='Please enter k, default 3!',prompt='k:',caption='k-anonymity parameter',value=3,min=2,max=40)
        if (dlg.ShowModal() == wx.ID_OK):
            k=dlg.GetValue()
        else:
            return
  
        if len(self.g.node)!=0:
            deglist=graphtodegree(self.g)
            deglist.sort(key=lambda deg:deg['deg'],reverse=True)
            degreee_anony(deglist,k)
            deglist=diffSelect(deglist)
            addedEdge=[]
            addEdge(self.g,deglist,addedEdge)
                      
            addNode(self.g,deglist,addedEdge)
                
            outStr="k="+str(k)+"\n"+"Add edges:"+str(len(addedEdge))+"\n"+str(addedEdge)
            self.rtb.SetValue(outStr)
        else:
            print 'Grap is empty!! Please load data!'
            wx.MessageBox("No data was selected. Please load data!","Data Error")

#---------------------------------------
    def OnRandom(self,e):
        self.rtb.SetValue("")          
        self.PushStatusText("Starting Random anonymity", SB_INFO)
        self.ShowPos()
        r=0
        dlg=wx.NumberEntryDialog(self,message='Please enter random rate! Range(0%--100%) existing edges!',prompt='Rate',caption='Random parameter',value=10,min=0,max=100)
        if (dlg.ShowModal() == wx.ID_OK):
            r=dlg.GetValue()
        else:
            return
        num=self.g.number_of_edges()*r/100
        randomAnony(self.g,num,self.rtb)



    def OnAnalyze(self,e):
        self.rtb.SetValue("")
        self.PushStatusText("Degree centrality", SB_INFO)
        cStr="The degree centrality of the graph is :\n"+str(nx.degree_centrality(self.g))+"\n"
  
        self.rtb.SetValue(cStr)

#---------------------------------------       
    def OnDegree(self,e):
        #dlg = wx.TextEntryDialog(None, 
        #    "What kind of text would you like to enter?",
        #    "Text Entry", "Default Value", style=wx.OK|wx.CANCEL)
        #if (dlg.ShowModal() == wx.ID_OK):
        #    print 'sssss'
        #dlg=wx.NumberEntryDialog(self,message='k-anonymity',prompt='k:',caption='k-anonymity parameter',value=3,min=2,max=20)
        #if (dlg.ShowModal() == wx.ID_OK):
        #    k=dlg.GetValue()
        #    print k
        #dlg = SingletonDialog(self, title="Singleton Dialog")
        #dlg.Show()
        #dlg.Raise()
        #if (dlg.ShowModal() == wx.ID_OK):
        #    print 'dlg show'
        #    t=dlg.field.GetValue()
        #    print t
        if len(self.g.node)!=0:
            print self.g.degree()
            x=self.g.degree().values()

            self.rtb.SetValue("")
            cStr="Degree Distribution is :\n"+str(x)
            self.rtb.SetValue(cStr)

            n, bins, patches =plt.hist(x)
            plt.xlabel('Degree')
            plt.ylabel('Number')
            plt.title(r'Histogram of Degree Distribution')

            plt.show()   

#---------------------------------------
    def OnClustering(self,e):
        self.rtb.SetValue("")
        self.PushStatusText("Calculte the CC", SB_INFO)

        #cStr="The average clustering of the graph is :\n"+str(nx.average_clustering(self.g))+"\n"
        cStr="The Clustering of the graph is :\n"+str(nx.clustering(self.g))
        self.rtb.SetValue(cStr)

#---------------------------------------
    def OnApl(self,e):
        try:
            self.rtb.SetValue("")
            if self.g.number_of_edges():
                cStr="The average shortest path of the graph is :\n"+str(nx.average_shortest_path_length(self.g))
                self.rtb.SetValue(cStr)
            else:
                self.rtb.SetValue("Plese load the data!")
        except Exception,e:
            cStr=str(e)
            self.rtb.SetValue(cStr)

#---------------------------------------
    def OnHelpAbout(self, e):
        """ Help|About event """
        title = self.GetTitle()
        d = wx.MessageDialog(self, "About " + title, title, wx.ICON_INFORMATION | wx.OK)
        d.ShowModal()
        d.Destroy()
        wx.dialo

#---------------------------------------
    def OnRtbKeyUp(self, e):
        """ Update Row/Col indicator based on position """
        self.ShowPos()
        e.Skip()

#---------------------------------------
    def ShowPos(self):
        """ Update Row/Col indicator """
        (bPos,ePos) = self.rtb.GetSelection()
        if (self.oldPos != ePos):
            (c,r) = self.rtb.PositionToXY(ePos)
            self.SetStatusText(" " + str((r+1,c+1)), SB_ROWCOL)
        self.oldPos = ePos

# --- end [testFrame] class



#-------------------------------------------------------------------------------
# --- Program Entry Point
app = wx.App()
# --- note: Title never gets used!
frame = dpFrame("A Title", -1, "Small wxPython Application")
# frame.Show(True)  # - now shown in class __init__
app.MainLoop()
