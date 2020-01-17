#!/usr/bin/env python
#change above to python or python 3
# if necessary
import sys , os

#below should make QString work ????
# in python3

if sys.version_info[0] >2:
    import sip
    sip.setapi('QString', 1)
    sip.setapi('QVariant', 1)
#below can be set up as above
#QDate v1, v2
#QDateTime v1, v2
#QString v1, v2
#QTextStream v1, v2
#QTime v1, v2
#QUrl v1, v2
#QVariant v1, v2

## remove Webkit Debian and some Windows
## do not have it and it does nor do much
# YES it works NOW can run this in python3
## use enchant for spell Check 
from PyQt4  import  QtGui , QtCore , QtNetwork, QtSql

import sys , os





from params import *

# find case sensitive is NOT worth the bother 

class sqlIntbl2(QtGui.QTableView):
    def __init__(self,tbl,dB):
        QtGui.QTableView.__init__(self)
        mdlBs = QtSql.QSqlTableModel(self,dB)
        
        mdlBs.setEditStrategy(SQLEDIT)
        mdlBs.setTable(tbl)
        mdlBs.select()
        self.setModel(mdlBs)
        print ('dB is' , dB)
        self.show()

        
    def zoomFactor(self):
        sz = self.font().pointSizeF () 
        print ('sz' , sz)
        return sz/10.0
        
    def setZoomFactor(self,z):
        print ('128 zoom' , z)
        F = self.font()
        sz = z*10
        F.setPointSizeF(sz)
        self.setFont(F)
        print ('35 sz' , sz)
        
    
        

class sqlIntbl(QtGui.QTableView):
    def __init__(self,quer,dB):
        print ('get table using' , quer)
        QtGui.QTableView.__init__(self)
        self.mdlBs = QtSql.QSqlTableModel(self,dB)
        self.mdlBs.setEditStrategy(SQLEDIT)
        
        self.query =  QtSql.QSqlQuery(quer,dB)
        #print ('!king query IS' , self.query.isActive () ,dB)
        self.mdlBs.setQuery (self.query) 
        
        
        print ('! query IS' , self.query.isActive ()) 
        self.setModel(self.mdlBs)
        dB.commit()
        self.show()
        #self.query.finish()  < if I do that NO DATA ????
        print ('! query IS' , self.query.isActive ()) 
        #QTableWidget.setModel() is a private method
        print ('! Self IS' , self)
        
       
    def  commitData(self , e):
        print ('Editor' , e.text(), self.currentIndex ()) 
        print ('submit ????', self.mdlBs)
        #.submit()
        
    def zoomFactor(self):
        sz = self.font().pointSizeF () 
        print ('sz' , sz)
        return sz/10.0
        
    def setZoomFactor(self,z):
        
        F = self.font()
        sz = z*10
        F.setPointSizeF(sz)
        self.setFont(F)
        print ('35 sz' , sz)
        
        
        


# put thing for ouputing sql data
# into html table into a class
# could have made below a query I guess ??
# in windoze python3 qt4 NO QString
# Fixt above
class sqltoHtm(QtCore.QString):
    def __init__(self,sqq,tbl,dB):
        QtCore.QString.__init__(self)
        rownum =0
        qnum =0 
        self.pgs = 0
        self.ttl = ""
        self.col = 0
        self.thetbl = tbl
        print ('14' , self,  self.thetbl)
        # if I do not pick tbl here 
        # do not necessarily know what tbl
        # IS if I come here with query
        
        self.query =  QtSql.QSqlQuery(dB )
        
        self.query.exec_(sqq)
        # should also test  isSelect() and isActive () 
        if self.query.first():
            self.hdr = self.dohedr(sqq)
            self.append(self.hdr)
            self.query.seek(-1)
        else:
            self.append('<h2>' + (self.query.lastError().text()))
            self.append(' </h2> </HTML>')
            return
            
            
            
        print ('38')        
        self.sqlhtmbdy()   
        self.append('</HTML>')
        
        
    def dohedr(self,querstr):
        res=  QtCore.QString()
        if self.query.size() > -1 :
            ro = str(self.query.size())
        else :
            ro = ' ??? '
        print ('Got Something')
        rec =  self.query.record()
        self.col =  rec.count()
        got = "Got " + str(self.col) + " Columns " + ro +\
        " Rows Total <P>"
        res.append('<HTML> <P>'+ querstr +'<P>' + got +'<P>')
        i = 0
        res.append('<table BORDER= "1"> <tbody> <tr>')
        while i < self.col:
            res.append('<th>')
            print ('Test Bitmap Direct' ,  rec.field(i).type()== QtCore.QVariant.Pixmap)
            print ('129 type' , rec.field(i).type(),)
            if rec.field(i).type() == 12 :
                print( '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~could be a pixmap')
                #res.append(rec.fieldName (i) + " (pixMap ??)")
                # just put fieldname
                res.append(rec.fieldName (i))
            else:
                res.append(rec.fieldName (i))
            res.append('</th>' )
            i+=1
        return res
        
    def sqlhtmbdy(self):
        print ('---------------------------------------------542')
        self.pgs += 1
        self.ttl = 'SQL HTML page '+ str( self.pgs)+ ' from ' + self.thetbl
        #print 'ttl' , self.ttl
        x = 0
        
        while  x < MAXSQLROW and   self.query.next() :
            self.append('<tr> ')
            x+= 1
            cl = 0 
            #print 'self.col' , self.col
            while cl <self.col:
                self.append('<td>')
                if  self.query.record().field(cl).type()== 12:
                    vl = self.query.value(cl).toByteArray() 
                    #print '! bytearray can' , dir(vl)
                    basz = vl.__sizeof__()
                    print ('basz' ,  basz)
                    ts1 = QtCore.QTextStream(vl)
                    
                    ts1.setCodec('UTF-16')
                    # could maybe just use 'UTF-16'
                    print ('codec' , ts1.codec().name()) 
                    
                    st1 = ts1.readAll()
                    qstrsz = st1.length()
                    print ('qstr sz' , qstrsz)
                    
                    if qstrsz == 0 and basz > 2:
                        print ('try bytes' , vl.toHex()) 
                                        #print 'st2 has' , st2
                    # in sqlite
                    # basically blob is ascii
                    # and a 0 and ascii and a 0
                    # etc. 0 means end of text
                    
                    b64 = vl.toBase64 () 
                    # WORKS !!! swows null pic if does not have picture
                    htmpic=QtCore.QString('<img src="data:image/png;base64,')
                    # may need convert to string firs ?
                    htmpic.append(b64)
                    htmpic.append('" /><a name="pix"></a> ')
                    
                    #self.append(
                    ba =  self.query.value(cl).toByteArray () 
                    pix =  QtGui.QPixmap() 
                    Ispic = pix.loadFromData (ba )
                    
                    print ('Ispic' , Ispic)
                    if Ispic:
                        self.append(htmpic)
                    else: 
                        #self.append(st1)
                        self.append( self.query.value(cl).toString())
                        
                        
                        
                        
                        
                else:
                    vlu =  self.query.value(cl)
                    #print ('value class' , vlu.__class__.__name__ )
                    self.append( vlu.toString())
                    #self.append( str(vlu))
                self.append('</td>')
                #print '74 self' , self
                cl += 1
            self.append('</tr>')
        self.append( " </tbody> </table> ") 
        #print '555' , x ,  MAXSQLROW
        if x == MAXSQLROW  :
            print ('more to get')
            nxtgt = '<A HREF="NEXTSQL">Get Next '+ str(MAXSQLROW)\
              +' or less </A>'
            self.append(nxtgt)
    def getmor(self):
        #print ('72 getmor',self)
        # first we have to blank self
        self.clear()
        self.append(self.hdr)
        # how we have to make sqlhtmbdy
        # so it continues ON from where we left off
        self.sqlhtmbdy()
        self.append('</HTML>')
        

#------------------------------ using enchant
  
#import enchant

class spelDi(QtGui.QDialog) :
    def __init__(self,parent):
        # parent is textedit thingy
        QtGui.QDialog.__init__(self,parent)
        #print ('Speldi')
        self.tOchek = parent
        self.tOchek.moveCursor(1, 0)
        ##QTextCursor::Start	1
        ## Mode MoveAnchor	0, KeepAnchor	1
        print ('parent' , parent)
        self.encodr = 'utf-8'
        mzspl =  QtGui.QLabel("Misspelled")
        self.wrngwrd =  QtGui.QLineEdit()
        self.wrngwrd.setReadOnly (True )
        self.fxwrd =  QtGui.QComboBox()
        self.fxwrd.setEditable ( True )
        self.fxwrd.setMinimumSize (200,20)
        self.btns = QtGui.QDialogButtonBox ()
        self.btns.addButton ("Ignore",QtGui.QDialogButtonBox.RejectRole  )
        self.btns.addButton ( "Replace",QtGui.QDialogButtonBox.ActionRole )
        self.btns.addButton ( "Quit", QtGui.QDialogButtonBox.ActionRole )
        self.btns.clicked.connect(self.spElchk)
        layt = QtGui.QGridLayout() 
        layt.addWidget(mzspl , 0,0)
        layt.addWidget( self.wrngwrd, 0,1)
        layt.addWidget(self.fxwrd , 0,2)
        layt.addWidget(self.btns , 1,0,3,3)
        self.setLayout(layt)
        # Must use QString
        txt = parent.toPlainText () 
        txt.append( '  murdEndhere\n')
        # voodo to avoid pycode puke and checker wants unicode?
        if sys.version_info[0] >2:
            utxt = str(txt)
        else:
            utxt = unicode(txt).encode(self.encodr)

        print ('txt is' , txt.__class__)
        if  Spelur :
            self.chkr =  enchant.Dict("en_CA") 
        ### too many American eg. siphon for syphon  
        #self.chkr =  enchant.Dict("en_GB") 
        #self.chkr =  enchant.Dict("en_US") 
        
        
        
        self.wrdz  = utxt.split()
        
        
        self.Check()
        
    def Check(self):
        #print ('47',self.wrdz)
        if self.wrdz == []:
            return
        
       
        while 1:
            #print (len(self.wrdz))
            w = self.wrdz.pop(0)
            
            w2 = w.strip('.,();:"$?><[]')
            if w2 == '':
                continue
            elif w2 == 'murdEndhere' :
                print (' Shut er down')
                self.wrngwrd.setText("DONE")
                self.fxwrd.setEnabled (False )
                #self.btns.setEnabled (False )
                return
            #print ('check' ,w2)
            if not self.chkr.check(w2):
                print ('break ???')
                break
            #else:
                #print ('boogy on')
        print ('74')
        #print (self.chkr.suggest(w2))
        self.wrngwrd.setText(w2)
        self.tOchek.find(w2)
        self.fxwrd.clear()
        for f in self.chkr.suggest(w2):
            self.fxwrd.addItem(f)
                
        
    #--------------------------------------    

        
    def spElchk(self,b):
        print ('250 clicked',b.text())           
        if b.text() =='Replace':
            self.tOchek.textCursor().insertText( self.fxwrd.currentText () ) 
            
        elif b.text() == "Ignore" :
            print ('DO NOTHING')
        elif b.text() == "Quit":
            
            print('--------------------------382')
            self.wrdz = []
            self.tOchek.moveCursor(1, 0)
            #self.tOchek.find('dlkdlkdkldkldkldkldlk')
            self.close()
            # if I quit and try spell agin
            # does not highlight
        
        self.Check()
    
        
                
class sqlCon( QtGui.QDialog) :
    def __init__(self,parent):
        self.dbName ='a'
        QtGui.QDialog.__init__(self,parent)
        F = self.font()
        F.setPointSize(FONTSIZE)
        self.setFont(F)
        self.Db = QtSql.QSqlDatabase()
        ulbl =  QtGui.QLabel("User Name")
        self.uname =  QtGui.QLineEdit(SQLUSER)
        
        layt = QtGui.QGridLayout() 
        layt.addWidget(ulbl,0,0)
        layt.addWidget(self.uname,0,1)
        dlbl = QtGui.QLabel("Database Name")
        self.dbnm =  QtGui.QComboBox()
        for n in SQLBASES:
            self.dbnm.addItem(n)
        self.dbnm.setEditable(True)
        self.dbnm.setInsertPolicy( QtGui.QComboBox.InsertAtBottom)
        self.dbnm.setInsertPolicy( QtGui.QComboBox.InsertAtBottom)
        layt.addWidget(dlbl,1,0)
        layt.addWidget(self.dbnm,1,1)
        drvlbl = QtGui.QLabel("Driver")
        self.drvnm =  QtGui.QComboBox()
        self.drvnm.addItems(self.Db.drivers())
        layt.addWidget(drvlbl,2,0)
        layt.addWidget(self.drvnm,2,1)
        pslbl =  QtGui.QLabel("Password")
        self.pswd =  QtGui.QLineEdit()
        self.pswd.setEchoMode(QtGui.QLineEdit.Password)
        # or PasswordEchoOnEdit)
        self.pswd.returnPressed.connect(self.pwdun)
        layt.addWidget(pslbl,3,0)
        layt.addWidget(self.pswd,3,1)
        prtlbl =  QtGui.QLabel("Port (usually 3306)")
        prtnum =  QtGui.QSpinBox()
        prtnum.setMaximum(65535)
        prtnum.setSpecialValueText("Default")
        # shows "Default" at 0
        #prtnum.setValue(3306)
        layt.addWidget(prtlbl,4,0)
        layt.addWidget(prtnum,4,1)
        hstlbl =  QtGui.QLabel("Host Name")
        self.hostnm =  QtGui.QLineEdit('localhost')
        layt.addWidget(hstlbl,5,0)
        layt.addWidget(self.hostnm,5,1)
        layt.addWidget( prtlbl,4,0)
        layt.addWidget( prtnum,4,1)
        cnect = QtGui.QPushButton("ConnectSql")
        cncl = QtGui.QPushButton("Cancel")
        layt.addWidget(cnect,6,0)
        layt.addWidget(cncl,6,1)
        # murdoch put text edit here for error messages
        self.msgs = QtGui.QTextEdit()
        layt.addWidget( self.msgs,7,0,2,2)
         
        cnect.clicked.connect(self.cOnect)
        cncl.clicked.connect(self.close)
        self.tbls =  QtGui.QComboBox()
        self.tbls.addItem("Table Name????")
        self.tbls.setEnabled(False)
        layt.addWidget( self.tbls,9,0,1,2)
        self.setLayout(layt) 
        
    def keyPressEvent(self,k):
        # only connect with Connect
        # NOT return key press
        print (',,', k)
        
    def pwdun(self):
        pwd = self.pswd.text()
        print ('passwrd dun')
        self.Db = QtSql.QSqlDatabase.addDatabase(self.drvnm.currentText())
        self.Db.setHostName(self.hostnm.text()) 
        self.Db.setUserName(self.uname.text())
        self.Db.setPassword( self.pswd.text())
        print ('Open ????' , self.Db.open())
        ## below works for mysql mariadb
        # postgresql needs
        #SELECT datname FROM pg_database;
        if self.Db.open():
            # get databases
            qrtxt = "show databases"
            qr = QtSql.QSqlQuery(qrtxt,  self.Db )
            print ('qr' , qr.isActive())
            while qr.next():
                rec = qr.record()
                # shouldonly have 0NE FIELD
                # hence (0)
                vlu = rec.value(0).toString() 
                # value gives variant
                print ('add ' , vlu)
                self.dbnm.addItem(vlu)
                #self.dbnms.setEnabled(True)
                #self.dbnms.currentTextChanged.connect(self.setDb)    
            qr.finish()## may not benecessary
            self.Db.close()
        else:
            return
        
        
        
        
            
    def cOnect(self):
        #self.Db.addDatabase(self.dbnm.currentText(),DEFAULTDB)
        #print 'Driver??' , self.Db.isDriverAvailable (self.dbnm.currentText())
        # pressing return on user name OR Databasename 
        # or anything comes here
        
        TheName = self.drvnm.currentText()
        print ('63')
        self.Db= QtSql.QSqlDatabase.addDatabase(TheName,  TheName )
        print ('65', TheName)
        print ('driver' , self.Db.driver())
        print ('driver name' , self.Db.driverName())
        print ('connectiom' , self.Db.connectionName())
        print ('valid ??' , self.Db.isValid())
            
               
        
        # only static works with driver Name
        print (' self.Db',  self.Db,'>', self.drvnm.currentText())
        
        print ('self.Db' ,self.Db.connectionName ()) 
        self.Db.setHostName(self.hostnm.text()) 
        self.Db.setUserName(self.uname.text())
        self.Db.setPassword( self.pswd.text())
        # another   pain  qt thing
        # We have connection name and database name ???
        # so below rquired
        print ('74')
        if  self.dbnm.currentText() =='browse':
            sqliteDb =  QtGui.QFileDialog.getOpenFileName(self,\
            "get sqlite database file")
            #drat ,"all (*);; kards (*.krd);;htm (*.htm *.html")
            #
            self.Db.setDatabaseName( sqliteDb )
            
        else:
           self.Db.setDatabaseName( self.dbnm.currentText() )
           ## in mysql showdabases works
           ## do not know about others
           
        print ('75')
        if not self.Db.open():
            print ('urps did not open')
            #, self.Db.lastError().databaseText() ,":",\
            #self.Db.lastError(). driverText ()
            self.msgs.append("Urps did not Open")
            self.msgs.append(self.Db.lastError().databaseText())
            self.msgs.append( self.Db.lastError(). driverText ())
        else: 
            #print 'open self.Db is ' , self.Db    
            self.msgs.append(self.Db.databaseName ()  + ' is Open using ' + TheName )
            tblquer = QtSql.QSqlQuery(self.Db)
            ntb = len(self.Db.tables())
            self.msgs.append("Got " + str(ntb) + " tables")
            #print 'execute' , SQLTBLS[TheName]
            tblquer.exec_(SQLTBLS[str(TheName)])
            print ('544 tblquer' ,  tblquer, TheName)
            print ('active? query ' , tblquer.isActive () )
            print ('Select ????' , tblquer.isSelect())
            #result must be in the active state and isSelect() 
            if tblquer.first():
                tables = QtCore.QStringList()
                tblquer.seek(-1)
                while tblquer.next():
                    v0 =tblquer.value(0)
                    vtp = v0.__class__.__name__
                    print ('vtp' , vtp)
                    if vtp ==  'QVariant' :
                        print ('501')
                        ###print ('table' , )
                        tables.append(v0.toString ())
                    else:
                        print ('504')
                        tables.append(v0)
                    ## already string in Win7.toString ())
                print ('tables' , tables)
                # clear away prvious tables
                # Still throws error 
                # shoulf be fixed                
                self.tbls.clear ()
                self.tbls.addItem("Table Name????")
                self.tbls.addItems(tables)
                
            else:
                print ("Fuond no tables???")
                self.msgs.append("No Tables Found ????")
                
                print ('goof' , self.Db.lastError())
def done(self,e):
        print ('Destroy',e)
        # we need this dialog to pick sql tables
        # maybe add note saying do you really??
        #self.finished() < No  longer works
        self.deleteLater()
                                        
class findTxt( QtGui.QDialog):
    txtsurch = QtCore.pyqtSignal(QtCore.QString,bool)
    def __init__(self, parent):
        QtGui.QDialog.__init__(self,parent)
        
        self.setMinimumSize ( 150,50) 
        print ('8')
        vbl =  QtGui.QVBoxLayout(self)
        #print ('10')
        self.inSrch = QtGui.QRadioButton("Search Index" , self)
        
        self.inSrch.setAutoExclusive(False)
        
        self.srchbox =  QtGui.QComboBox(self)
        #QtGui.QLineEdit(self)
        self.srchbox.setEnabled (True)
        self.srchbox.setEditable(True)
          
        vbl.addWidget( self.inSrch)
        
        vbl.addWidget(self.srchbox)
        
        hbl =  QtGui.QHBoxLayout()
        #print ('17')
        bbox = QtGui.QDialogButtonBox(self)
        self.findBut =   QtGui.QPushButton("Find")
        self.findBut.setDefault(1)
        bbox.addButton(self.findBut,  QtGui.QDialogButtonBox.ActionRole)
        # or maybe ::YesRole
        vbl.addWidget( bbox)
        self.dunBut =  QtGui.QPushButton("Done")
        bbox.addButton(self.dunBut, QtGui.QDialogButtonBox.AcceptRole)
        # bbox sends :accepted () signal for accept Or Yes
        print ('537' , self, 'act>', bbox.actions ()) 
        #self.add(self.radioButton)
        #bbox.accepted.connect(self.dUn)
        bbox.clicked.connect(self.surch)
        
        
    def surch(self,t):
        tx = t.text() 
        print ('FIND',tx)
        if tx == "Find" :
            txl= self.srchbox.itemText(0)
            print ('looking for' , txl)
            if txl == '':
                txl = self.srchbox.lineEdit ().text()
                self.srchbox.addItem(txl)
            #print '49 editing????',  
            
            # until I press return 
            # combobox has NOTHING 
            
            
            self.txtsurch.emit(txl ,self.inSrch.isChecked() )
        
        elif tx == 'Done':
            self.close()
    #def dUn(self):
        #print 'Dun'
        

class  OverBak(QtGui.QDialog):
    def __init__(self,fnm ):
        self.f = fnm
        QtGui.QDialog.__init__(self)
        self.resize(300,200 )
        print ('layout is' , self.layout())
        lyout =  QtGui.QGridLayout(self)
        #lyout =QtGui.QHBoxLayout()
        print ('The self is ' , self)
        wrn =  QtGui.QLabel("<html><h2>overwrite ???</h2></html>",self)
        lyout.addWidget(wrn)
        # urps overwrite Doesn't
        # it is appending ???
        
        bbox =  QtGui.QDialogButtonBox(self)
        lyout.addWidget(bbox, 1, 0, 1, 1)
      
        
        #addButton ( const QString &, ButtonRole ) : 
        bbox.addButton("Backup" , QtGui.QDialogButtonBox.ApplyRole)
        bbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        
        bbox.clicked.connect ( self.svmode)
        
    
    
    def svmode(self,b):
        Svtxt = b.text () 
        print ('svmode', Svtxt)
        if  Svtxt == 'Backup':
            print ('backup' , self.f)
            # probably  up with strings versus qstrings
            onm = QtCore.QString(self.f)
            #print 'onm' , onm
            bknm =  QtCore.QString(self.f)
            #print '41 onm' , onm
            while QtCore.QFile.exists(bknm):
                #print '43 onm' , onm
                bknm.append('_b')
            
            if  QtCore.QFile.rename(onm , bknm):
                self.accept()
                print ('did rename Old')
            else:
                self.reject()
                print ('did not rename Old')
        elif  Svtxt == '&OK' or  Svtxt == 'OK' :
            # OK does not put out OK !!!!
            # actually in Slack it does 
            self.accept()
        else: 
            
            print ('Not Saved', Svtxt)
            self.reject()
   
# put my text dinguses so I can just use Zoom
class murdtext( QtGui.QTextBrowser):
    getsqlpic = QtCore.pyqtSignal( QtCore.QString)
    morsql = QtCore.pyqtSignal()
    def __init__(self,typ= '',ro = False ):
        QtGui.QTextBrowser.__init__(self)
        
        self.setOpenLinks (False)
        
        self.setReadOnly(ro)
        self.setZoomFactor(1.2)
        
        # anchor clicked only works for read only
        self.anchorClicked.connect(self.anch)
        #self.textChanged.connect(self.sAvr)
        if typ == 'htm':
            self.setAcceptRichText ( True)
        else:
            
            self.setAcceptRichText ( True)
    def setZoomFactor(self ,z):
        # if Font IN html this does nothing ??
        print ('561 zoom' , z)
        F = self.font()
        sz = z*10
       # want sz to go from 10 to 20
        F.setPointSizeF(sz)
        self.setFont(F)
        print ('133 sz' , sz)
        
    def zoomFactor(self):
        sz = self.font().pointSizeF () 
        #print ('sz' , sz)
        return sz/10.0

    def sAvr(self):
        self.setWindowModified (True) 
    def hasBak(self):
        return False
    def hasFor(self):
        return False
    
    def anch(self , u):
        print ('clicked anch from' , u.path())
        # u is url get back to string
        if str(u.path()) == 'NEXTSQL':
            print ('267 emitting')
            self.morsql.emit() 
        elif u.path().startsWith("Pix"):
            print ("Get Pic from SQL")
            self.getsqlpic.emit(u.path())
            

# Debian pyqtwebkit4
#removed intentionally because QtWebKit 4.x is dead upstream

class droplab(QtGui.QLabel):
    dropt = QtCore.pyqtSignal(QtCore.QUrl )
    def __init__(self, parent=None, name=None):
        QtGui.QLabel.__init__( self )
        self.resize(400,300)
        self.setObjectName("droplab")
        self.setAcceptDrops(True)
        self.setObjectName("Dlabel")
        self.setText(COPYRIGHT)
        self.setStyleSheet(BKG)
        
        
    def dragEnterEvent (self, e):
        print ('Dragging' , e)
        e.acceptProposedAction()    
        
        
    def dropEvent (self,e):
        f = e.mimeData().urls()
        print ('Drop' , f)
        for i in f:
            print (i)
            self.dropt.emit(i)
        
        
    def acceptRichText (self):
        return True
    
    def hasBak(self):
        return False
    
    def hasFor(self):
        return False
    
    def setZoomFactor(self ,z):
        # do nothing
        print ('NoZoom')
        
    def history(self):
        print ('drop history')
    
class Ui_MainWindow(QtGui.QMainWindow):
    def  __init__(self, arg ):
        print ('pyqt , qt version is' , QtCore.PYQT_VERSION_STR,\
        QtCore.QT_VERSION_STR)
        print ('arg' , arg)      
        print ('Python Version' ,PyVer )
        self.connectSQ = False      
        fl = None
        QtGui.QMainWindow.__init__(self, fl )
        self.resize(1000,700 )
        self.nmkrds = 0
        self.edcomb  = ''
        self.widg = 0
        self.befortmp = -1
        self.theDirs= QtCore.QStringList()
        self.theDirs.append(QtCore.QDir.currentPath())
        for d in THEDIRS:
            self.theDirs.append(d)
        self.setWindowTitle ('Murkard [*]' ) 
        #print ('Title' , self.windowTitle ())
        self.setWindowOpacity (.9)
        self.tlbar =  self.addToolBar("Toolbar")
        # format is menu title, list of menuitems
        fileMen=self.qtBS('File',['Open','Previous','<F7>','Save','<F10>','Quit' ])
        sqlMen =self.qtBS('SQL',['Connect','Get(html)','table' ])
        # 1 in list means next action will be checkable and checked
        # 0 = not checked note 0 = False any other number True
        krdMen = self.qtBS('Kard',['New', 'Delete','Delete All',\
           'Print','Sql query','<F6>',0, 'Plain Text'])
        self.plntxt = krdMen.actions()[3]
        #print ('  self.plntx',   self.plntxt)
        self.plntxt.setEnabled(False)
        # below <F12> becomes shortcut for 'Find'
        # suspect both shortcut and checkable may be  confusing
        # No it seems to work
        edMen = self.qtBS('Edit',['<F12>','Find','Insert graphic', 'Spell Check', 'Make Html'])
        self.spacer = QtGui.QLabel()
        
        self.spacer.setMinimumSize(QtCore.QSize(70,25))
        self.tlbar.addWidget(self.spacer)
        self.spacer.setText('  Empty  ')
        self.spacer.setStyleSheet("QLabel {background-color: \
               rgb(70%, 100%, 100%)  }")
        
        self.tmpkrd =  0
        # remove buttons no webkit anymore
        
        self.tlbar.addSeparator ()
        self.edlblbt = QtGui.QCheckBox("EditLabel",self)
        self.edlblbt.toggled.connect( self.eDlbl)
        
        self.tlbar.addWidget(self.edlblbt )
        self.comboBox = QtGui.QComboBox(self)
        self.uselessQtcomb =  []
        self.comboBox.setMinimumSize(QtCore.QSize(400,25))
        self.comboBox.setMaximumSize(QtCore.QSize(2000,2500))
        self.comboBox.setInsertPolicy( QtGui.QComboBox.InsertAtBottom)
        #self.comboBox.activated.connect(self.piKard)
        self.comboBox.currentIndexChanged.connect(self.piKard)
        self.comboBox.editTextChanged.connect (self.comboTxt)
        #self.comboBox.activated.connect (self.activ)
        
        self.tlbar.addWidget(self.comboBox)
        #sizePolicy is useless
        self.lcdNumber = QtGui.QLCDNumber(self)
        self.lcdNumber.setNumDigits( 4)
        self.lcdNumber.display ( 1.20)
        self.tlbar.addWidget( self.lcdNumber)
        Ubut = QtGui.QPushButton(self)
        self.tlbar.addWidget(Ubut)
        Ubut.clicked.connect(self.bAk)
        Ubut.setMaximumSize(QtCore.QSize(25,16777215))
        
        
        Ubut.setIcon(self.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
        Dbut = QtGui.QPushButton(self)
        self.tlbar.addWidget(Dbut)
        Dbut.setMaximumSize(QtCore.QSize(25,16777215))
        
        Dbut.setIcon(self.style().standardIcon(QtGui.QStyle.SP_ArrowDown))
        
        
        Dbut.clicked.connect(self.fOrwd)
        
        self.horizontalSlider = QtGui.QSlider(self)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        #self.horizontalSlider.setOrientation(QtCore.Qt.Vertical)
        self.horizontalSlider.setRange ( 0, 100 )
        self.horizontalSlider.setSliderPosition ( 20 )
        self.horizontalSlider.setMinimumSize(QtCore.QSize(50,2))
        ####self.horizontalSlider.setMaximumSize(QtCore.QSize(50,16777215))
        self.tlbar.addWidget( self.horizontalSlider)
        # self.horizontalSlider.setEnabled(tf)
        self.horizontalSlider.valueChanged.connect(self.zOom)       
        self.sEking = ''
        #self.nmbrr = QtGui.QLabel()
        #self.nmbrr.setText('Empty')
        #self.tlbar.addWidget(self.nmbrr)
        self.histlist = QtCore.QStringList()       
        self.getHist()
        self.stakr =  QtGui.QStackedWidget()
        self.setCentralWidget(self.stakr)
        #self.comboBox
        self.gOtkRd = ''
        if (len (arg) > 1):
            print ('Load Kards') 
            # could maybe get bunch of cards as in
            # simpqt16S.py etc. for now just get first
            self.getFile(QtCore.QString(arg[1]))
        else :
            strtwid = droplab()
            print ('strtwid' , strtwid) 
            strtwid.dropt.connect(self.drOpt)
            self.stakr.addWidget(strtwid)
            self.cOntrols(False)
            
            
            
    def closeEvent(self,ev):
        print ('803 shut er down',self.histlist) 
        #803 shut er down <PyQt4.QtCore.QStringList object at 0x7f372c060358>
        #*** Error in `python3': corrupted double-linked 
        #list: 0x0000561a9b9ebe10 ***
        #======= Backtrace: =========
        print ('hist' , self.histlist)
        
        
        if len(self.histlist)> 0:
            # just save it for saving 
            # python file is less of a pain 
            f = open( HISTLIST , 'w+')
            l =0 
            while l < len(self.histlist):
                    f.write(str(self.histlist[l])+"\n" )
                    l = l+1
            f.close()
        # now we need if file changed save file
        c= self.stakr.count()
        x = 0
        mod = False
        if self.isWindowModified ():
            svr = QtGui.QMessageBox.question(self, "Text Changed" , \
            "Some kards have been Changed Save File? "\
                  "Save File", "Save" , "Don't Save" ,"Cancel") 
            print ('svr' , svr)
            #QMessageBox::Cancel, QMessageBox::Discard <dont save
            # If OK svr is 0
            if svr == 0:
                self.sVkrds()
            elif svr == 2:
                ev.ignore()
                
            
            
    def toolAc(self,sig = 0):
        txtsig = sig.text()
        print (' triggered ' , txtsig)
        if txtsig == 'New':
            self.addKard()
            
        elif  txtsig == 'Open':
            self.getFile()
        elif  txtsig == 'Previous':
            self.getPrev()
        elif txtsig == 'Insert graphic':
            self.getPic()
        #elif  txtsig == 'Script Find':
        #self.eLement()
        elif  txtsig == 'Quit':
            print ('shut down self  ' , self.close())
            
            
        elif  txtsig == 'Plain Text':
            self.showPlain()
            
        elif  txtsig =='Make Html':
            self.htMlcnv()    
            
        elif txtsig == "Print":
            self.pRint()    
            
        elif txtsig == 'Delete':
            self.delKrd()
            
            
        elif txtsig == 'Delete All':
            self.delAll()
        elif txtsig == 'Spell Check':
            if Spelur:
                self.spElr()
            else:
                QtGui.QMessageBox.warning(self, "In Windows ??",\
                    "Could not load 'enchant' No speller available.")
                

            
            
        elif txtsig == 'Save':
            self.sVkrds()
        elif txtsig == 'Find':
            self.fIndr()   
        elif txtsig == 'Connect':
            self.sQl=self.sQlcon()
            self.connectSQ = True
        elif txtsig =="Sql query":
            self.sQlQuer()
        elif txtsig =="Get(html)":
            if not  self.connectSQ :
                self.sQlcon()
                self.connectSQ = True
            self.sQlhTm()
        
        elif  txtsig == "table":
            if not  self.connectSQ :
                self.sQlcon()
                self.connectSQ = True
            self.sqltBl()
            
    def getPic(self):
        crnt = self.stakr.currentWidget()
        # SPELLING CONVENTIONS !!!!
        print ('crnt IS' , crnt.objectName()) 
        if not crnt.objectName().startsWith("murdtext"):
            return

        # if not real widget return
        picNm =  QtGui.QFileDialog.getOpenFileName(self,\
           "picNm", "Get Graphic","all (*);; jpg (*.jpg *.jpeg);;png (*.png)")
        #if picNm == 0 :
            #return
        Graphstr = ' <p><img alt=graphic  src="' + picNm + '" > ' 
        print ('G' , Graphstr)
        crnt.textCursor().insertHtml ( Graphstr)
        
        
            
    def zOom(self,i):
        crnt = self.stakr.currentWidget()
        print ('crnt IS' , crnt) 
        if crnt == None:
            return
        z = i/100.0   
        self.lcdNumber.display(z + 1.0)
        crnt.setZoomFactor(z+1)
    def cOntrols(self,tf):
        self.edlblbt.setEnabled(tf)
        self.horizontalSlider.setEnabled(tf)
        self.lcdNumber.setEnabled(tf)
        self.comboBox.setEnabled(tf) 
  
    def fIndr(self):
        #print 'first look in indeces'
        # self.comboBox.::findText
        self.Txtsrch = findTxt(self)
        print ('The Txtsrch  IS' , self.Txtsrch) 
        self.Txtsrch.show()
        self.Txtsrch.txtsurch.connect(self.sEek)
        self.Txtsrch.srchbox.setFocus()
    
    def sQlcon(self):
        print ('connect to sql')
        self.sQldi = sqlCon(self)  
        self.sQldi.show()
        
    def sQlQuer(self):
        print ('send kard text to SQL')
        crnt = self.stakr.currentWidget()
        print ('822')
        #print 'crnt has' ,  crnt.toPlainText ()
        # above is what I want gives simple text
        # for plain or html
        
        qer = crnt.toPlainText ()
        print ('828')
        # could parse for table name as being
        # text after from
        thetbl = " Submitted Query "
        print(' self.sQldi', self.sQldi)
        ## error here No sqldi ????
        ## in windows ??
        ## but Slack OK ???
        self.htmltxt = sqltoHtm(qer,thetbl, self.sQldi.Db )
        
            
        #print  'getSqlh' , htmltxt
        self.addKard(0,self.htmltxt.ttl , self.htmltxt,False,True, True)
        ### some work and some do not ?????
        
    def sqltBl(self):
        print ('get sql table')
        self.sQldi.tbls.setEnabled(True)
        self.sQldi.tbls.setStyleSheet("QComboBox {background-color: \
                   rgb(80%,100%, 50%)  }")
        self.sQldi.tbls.setFocus()     
        self.sQldi.tbls.currentIndexChanged.connect(self.getSqltbl)
        print ('sQldi IS' ,  self.sQldi)
        
        #self.sQldi.show()
        
    def getSqltbl(self,i):
        print ('p56 get  SQL' , i)
        if i < 1:
            return
        # for now coppy following from html table  thingy
        # murdoch later hve function tha teither 
        # if no connection opens it
        # and then either gets table name from comb box
        # or querry from a kard
        thetbl = self.sQldi.tbls.itemText(i)
        qer = 'SELECT * FROM ' + thetbl 
        #tblsqkrd = sqlIntbl(qer , self.sQldi.Db )
        tblsqkrd = sqlIntbl2(thetbl , self.sQldi.Db )
        self.addKard( tblsqkrd)
        #print 'The query IS' , tblsqkrd.query.isActive () 
        
        
    def sQlhTm(self):
        print ('Get html Table')
        self.sQldi.tbls.setEnabled(True)
        self.sQldi.tbls.setStyleSheet("QComboBox {background-color: \
                   rgb(100%,50%, 80%)  }")
        self.sQldi.tbls.setFocus()     
        self.sQldi.tbls.currentIndexChanged.connect(self.getSqlh)
        
        
    def getSqlh(self,i):
        
        
        # So simple
        # no can update tbls for other query
        if i < 1:
            return
        # go to htmltxt WITH query
        thetbl = self.sQldi.tbls.itemText(i)
        # get spurious response here when I 
        # wipe out tbls combobox with new connect
        qer = 'SELECT * FROM ' + thetbl 
        #where   did that>>> ,i come from ???????
        print ('663 ' ,qer , 'tbl',thetbl , i)
        #QSqlQuery.exec_(QString): argument 1 has unexpected type 'tuple'

        self.htmltxt = sqltoHtm(qer,thetbl, self.sQldi.Db )
        #print  'getSqlh' , htmltxt
        self.addKard(0,self.htmltxt.ttl , self.htmltxt,False,True, True)
        # came here from currentIndexChanged
        # but should put back to Zero
        self.sQldi.tbls.setEnabled(False)
        self.sQldi.tbls.setCurrentIndex(0)
        self.sQldi.tbls.setEnabled(True)
    def getsQlpic(self, g):
        print ('try graphics view thing',g,  self.htmltxt.query)
        # parse g to get row and column of pix
        # sqlite has QtSql.QSqlQuery object 
        # mysql has 
        co = int(g.section(',',1,1))
        ro=int( g.section(',',2,2))-1
        print ('ro' , ro , 'col' , co)
        # first row shows ro 1 ?
        if self.htmltxt.query.seek(ro):
            btmp =  self.htmltxt.query.value(co)
            print ('got' , btmp)
            picthingy= VuPic( btmp.toByteArray () ) 
            self.addKard(picthingy,"pix")
            

    def morsQl(self):
        print ('get another page of SQL data')
        self.htmltxt.getmor() 
        #print ' Now Have' ,  self.htmltxt
        self.addKard(0 , self.htmltxt.ttl , self.htmltxt,False,True, True)
        # yipee works like a charm !!!!!
        
        
    def pRint(self):
        # shows Local file correct eg graphics
        #BUT for printing looks in start
        # directory of MurdKard
        #SURELY this is a bug but too late for that
        # qt4 is defunct
        crnt = self.stakr.currentWidget()
        prinf = QtGui.QPrinterInfo()
        print ('Print' , prinf)
        #.defaultPrinter ()
        qpr =  QtGui.QPrinter()
        prv =  QtGui.QPrintPreviewDialog(qpr)
        Pdu= prv.exec_()
        print ('Pdu' , Pdu)
        if Pdu:
            print ('Print', qpr)
            # maybe use temporary textbrowser
            # so I can add title to it
            curtxt =  self.comboBox.currentText () 
            hdr = '<h1>' + curtxt + '</h1> <br>'
            prwid =  QtGui.QTextBrowser()
            prwid.append (hdr)
            prwid.append( crnt.toHtml())
            prwid.print_(qpr)
            prwid = 0
            
        
    def htMlcnv(self):
        widg = self.stakr.currentWidget()
        
        print ('438' , self.stakr,  self.stakr.count())
        widgn = widg.objectName() 
        print ('Style Sheet' , QtGui.QTextDocument.defaultStyleSheet(widg.document()))
        print ('widget IS' , widgn ,widg)
        if  widg.acceptRichText ():
            print ('already html')
        else :
            # What if I use to html first
            # turns out manually inserting
            # html tags unnecessary let qt do the work !!!
            htmltxt = widg.toHtml()
            widg.setAcceptRichText (True) 
            widg.setHtml(htmltxt)
            
            
    def sEek(self,t= None, inD=None):
        print ('sEek',t,inD)
        
        if inD:
            # model is a pain 
            
            cntb =self.comboBox.count()
            x = 0
            while x < cntb:
                s = self.comboBox.itemText (x)
                if s.contains(t,QtCore.Qt.CaseInsensitive):
                    print ('874 add Combo')
                    self.Txtsrch.srchbox.addItem( s,x) 
                x+=1
                
            print ('294 indfound', self.Txtsrch.srchbox.count())
            if  self.Txtsrch.srchbox.count() > 1:
               self.Txtsrch.srchbox.activated.connect(self.srchInind) 
            
            
            
            
            #fl= QtCore.Qt.MatchContains|  QtCore.Qt.MatchWrap
                        
            #print 'search Index',t, fOund
            #if fOund > 0:
                #self.comboBox.setCurrentIndex(fOund)
                #find2 = self.comboBox.findText(t,fl)
                #print 'find2' , find2
                #self.piKard(fOund)
        else :
            widg = self.stakr.currentWidget()
            
            print ('widg is ' , widg)
            #fl =  QtGui.QTextDocument.FindFlags()
            #if casE:
                #fl = QtGui.QTextDocument.FindCaseSensitively
            #else :
                #fl = 0
            #QTextCursor::setPosition (0)
            fOund = widg.find(t)
            print ('fOund' , fOund)
            if not fOund:
                print ('Back to start')
                widg.moveCursor ( QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
                f2 =widg.find(t)
                print ('f2' , f2)
                if f2 == False:
                     self.Txtsrch.setWindowTitle("Not Found")  
            if t == self.sEking:
                print ('909' , t , self.sEking)
                # sometimes gets stuck here ???
                return
            else:
                self.sEking = t
                print ('search body',widg,fOund)
                # should only do this Once
                # keeps adding multiple times
                # so either first time through OR
                # what seeking or conditions (CS) are changed 
                # what would be neat is a thread that searches
                # All text bodies 
                # self.stakr.widget
                scnt = self.stakr.count()
                y = 0 
                while y <  scnt:
                    #print 'srching' , y , t ,fl
                    
                    wD = self.stakr.widget(y)
                    print ('wD object' ,  wD) 
                    # urps somewhere number is being added to it
                    if wD.objectName().startsWith('VuPic'):
                        print ("why  NOT continuing??")
                        y+= 1
                        continue
                    wD.moveCursor ( QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
                    fndall=wD.find(t)
                    #print 'fndall' ,fndall
                    if fndall:
                        print ('fndall' , fndall)
                        s = self.comboBox.itemText(y)
                        self.Txtsrch.srchbox.addItem( s,y)
                    y+= 1
                if  self.Txtsrch.srchbox.count() > 1:
                    self.Txtsrch.srchbox.activated.connect(self.srchInind) 
                    self.Txtsrch.srchbox.setStyleSheet("QComboBox {background-color: \
                    rgb(20%,100%, 20%)  }")
                    self.Txtsrch.srchbox.setEditable(False)
                
            
            
    def sVkrds(self):
        print ('1247 Save' , self.gOtkRd)
        # QFileDialog::DontConfirmOverwrite
        #( QWidget * parent = 0, const QString & caption = QString(), 
        #const QString & dir = QString(), 
        #const QString & filter = QString(), 
        #QString * selectedFilter = 0, 
        #Options options = 0 ) [static]
        if  self.gOtkRd != '':
            print('1255')
            svAs = self.gOtkRd
        else: 
            print('1258')
            svAs =   self.theDirs[0]
        while 1:       
            svnm =  QtGui.QFileDialog.getSaveFileName(self,"Save Kards" , \
               svAs ,'','', QtGui.QFileDialog.DontConfirmOverwrite )
            print ('svnm' , svnm)
            if svnm == '':
                return
            # if no name do not try to save murdoch
            if  QtCore.QFile.exists(svnm):
                print ('do overwrite backup dialog')
                ovrbk=OverBak(svnm)
                if not ovrbk.exec_():
                    return
               
            fsv =  QtCore.QFile(svnm)
            Opend = fsv.open(QtCore.QIODevice.WriteOnly)
            print ('save File',fsv, Opend)
            if Opend:
                self.setWindowModified (False)
                break
            else:
                # If I Cancel should NOT come here
                Svwarn  = "Could not Save " + svnm
                hwarn = QtGui.QMessageBox.warning (self,"File Problem" , Svwarn)
              
        ndx = 0
        while ndx < self.comboBox.count() :
            fsv.write("\n<BR><!title><B>")
            # another qt thing you can not write a string
            # to a file !!!!
            bar =  QtCore.QByteArray()
            # murdoch maybe toUtf8() for index also ?
            bar.append( self.comboBox.itemText (ndx) )
            bar.append("</B><BR>\n")
            if  self.stakr.widget(ndx).acceptRichText():
                krdbdy=  self.stakr.widget(ndx).toHtml().toUtf8() 
                #krdbdy.replace('<' , '\n<')    
                # murdoch above wrong !!! leave off and see what
                # so index which is start of new kard on new line ??
                #krdbdy.replace('margin-top:0px; margin-bottom:0px; margin-left:0px;' , ' ')
                #krdbdy.replace('margin-right:0px' , '')
                #krdbdy.replace('-qt-paragraph-type:empty;' , '') 
                #krdbdy.replace('-qt-block-indent:0; text-indent:0px;' , ' ')
                #krdbdy.replace('<p style="   ;  ">' , '<br>')
                krdbdy.replace('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">' , '')
                
                
                
            else:
                krdbdy=  (self.stakr.widget(ndx).toPlainText().trimmed()).toUtf8() 
            # murdoch What is belo BS for ???     
            bar.append(krdbdy)
            # below works but it will do pycode puke 
            #fsv.write(str(self.comboBox.itemText (ndx)))
            fsv.write(bar)
            ndx += 1
                    
        
        fsv.close()
    def delAll(self):
        while self.delKrd():
            print ('deleteing')
        
    def delKrd(self):
        widg = self.stakr.currentWidget()
        self.stakr.removeWidget(self.stakr.currentWidget())
        curind =  self.comboBox.currentIndex () 
        self.comboBox.removeItem (curind)
        cnt =  self.comboBox.count () 
        if cnt == 0 :
            self.cOntrols(False)
            #self.edlblbt.setEnabled(False)
            strtwid = droplab()
            strtwid.dropt.connect(self.drOpt)
            self.stakr.addWidget(strtwid)
            #self.horizontalSlider.setEnabled(False)
            return False
        print ('curind' , curind)
        return True
    def drOpt(self,s):
        print (s , 'Dropt')
        
        # do not really need this
        self.getFile(s.toLocalFile () )
        
                     
    def showPlain(self):
        
        widg = self.stakr.currentWidget()
        widgn = widg.objectName() 
        print ('remove tmpWid', widgn)
        if widgn == "tmpWid":
            #self.comboBox.setEnabled (True)
            widg =  self.stakr.widget(self.befortmp)
            pln = self.stakr.currentWidget().toPlainText () 
            widg.setText (pln)
            
            self.stakr.removeWidget(self.stakr.currentWidget())
            self.stakr.setCurrentIndex(self.befortmp)
            self.cOntrols(True)
            
            
            
        else:
            # record kard that was showing
            # so we can return to it after
            # deleteing tmpkrd
            self.befortmp =  self.stakr.currentIndex () 
            self.cOntrols(False)
            #self.comboBox.setEnabled (False)
            self.tmpkrd=QtGui.QTextEdit()
            self.tmpkrd.setObjectName("tmpWid")
            self.tmpkrd.setAcceptRichText (False)
            self.tmpkrd.setStyleSheet("QTextEdit {background-color: \
               rgb(100%, 70%, 100%)  }")
            # already did setAcceptRichText (False) but another qtbs
            # thing below required!!!
            #self.tmpkrd.setPlainText (pln)
            numtmp=self.stakr.addWidget( self.tmpkrd)
            if widg.acceptRichText ():
                print ('is Rich')
                pln = widg.toHtml()
                
            else:
                pln = widg.toPlainText()
                
            self.tmpkrd.setPlainText (pln)
            
            
            self.stakr.setCurrentIndex(numtmp)
            
            
            
            
            
            
            
    
                
    def fOrwd(self):
        curind =  self.comboBox.currentIndex ()
        l = self.comboBox.count()
        print ('curind l ' , curind, l)
            
        if curind +1  <  self.comboBox.count():
            self.comboBox.setCurrentIndex(curind+1)
        
    def bAk(self):
        curind =  self.comboBox.currentIndex () 
        print ('curind' , curind)
        if curind > 0:
            self.comboBox.setCurrentIndex(curind-1)
            
            
            
            
    def spElr(self):
        #.currentWidget()
        print ('Spell Check')
        speller = spelDi(self.stakr.currentWidget())  
        speller.show()
        
            
        
        
    def addKard(self,wid = 0 , nm='',txt =QtCore.QString(''),flpth=False ,mvCombo=True,readOnly=False):
        #print 'addKard' , wid,nm,txt pycode puke
        self.setWindowOpacity (1.0)
        cur = self.stakr.currentWidget()
        ##### remove
        try:
            print ('579 Zoom' ,cur, cur.zoomFactor ())
        except:
            print ('nozoom')
        ##### remove
        if  self.stakr.count() >0:
            print ('stakr has', self.stakr.widget(0).objectName()) 
            if self.stakr.widget(0).objectName() == 'Dlabel':
                self.stakr.removeWidget(self.stakr.widget(0))
            
        if  flpth :
            self.theDirs.append(flpth)
            print ('583 Removed' , self.theDirs.removeDuplicates ())
        self.plntxt.setEnabled(True)
        #print ('865 PlainText')
        if wid != 0:
            txtwid = wid
            
        else:
            #txtwid = QtGui.QTextBrowser ()
            #print '158 txtwid' ,   txtwid,txt
            
            if txt != 0:
                # could make more fine grained
                # ie if link make webview
                # if <img. or sometheng make textbrow ?
                if not txt.contains('<html>' ,  QtCore.Qt.CaseInsensitive):
                    # some of my kards do not have <html> in them ??
                    print ('No Rich??')
                    txtwid = murdtext()
                    txtwid.setAcceptRichText (False)
                    print ('163 txtwid' ,   txtwid)
                    
                    txtwid.setStyleSheet("QTextEdit {background-color: \
                          rgb(100%, 100%, 85%)  }")
                    #F = txtwid.setFontPointSize(12)
                    #font() 
                    #print '611 font12'
                    #F.setPointSize(12)
                    #txtwid.setFont(F)
                    
                else:
                    txtwid = murdtext('htm',readOnly)
                    txtwid.morsql.connect(self.morsQl)
                    print ('morsql CONNECTED')
                    txtwid.getsqlpic.connect(self.getsQlpic)
                    txtwid.setSearchPaths(self.theDirs)
                print ('164 txtwid' ,   txtwid)
                #font = QtGui.QFont()
                #font.setPointSize(12)
                #txtwid.setFont(font)
                #txtwid.setFontPointSize(12.0)
                # if I setfont Here it 
                # can not be changed later ???
                txtwid.append(txt)
                print ('font' , txtwid.font(),  txtwid.font().pointSizeF())
                print ('Num' , self.nmkrds)
                #if self.nmkrds == 0:
                    #print 'First Text' , txt
                #txtwid.insertPlainText(txt)
                #txtwid = QtGui.QTextBrowser() 
                txtwid.textChanged.connect(self.sAvr)
        self.stakr.addWidget(txtwid)
        print ('txtwid' , txtwid)
        self.nmkrds += 1
        # above just a counter of ALL kards
        # not adjusted after delete
        if nm == ''  :          
            ttl = 'Kard ' + str(self.nmkrds)
        else:
            ttl = nm
        widname = txtwid.__class__.__name__ + str( self.nmkrds )
        txtwid.setObjectName (widname)
        print ("widname" , widname) 
        
        self.comboBox.addItem(ttl)
        #print ('648')
        cnt = self.comboBox.count()
        #print ('650')
        self.cOntrols(True)
        #self.edlblbt.setEnabled(True)
        #self.horizontalSlider.setEnabled(True)
        
        print ('combo count' ,  cnt)
        if mvCombo:
            #print ('655')
            self.piKard(cnt-1)
            #print ('659')
            self.comboBox.setCurrentIndex(cnt-1)
            #print ('661')
            
            #print ('647 card added')
            crnt = self.stakr.currentWidget()
            print ('crnt IS' , crnt.objectName()) 
        ##### remove
        #
        try :
            print ('656 Zoom' ,cur, cur.zoomFactor ())
        except:
            print ('nozoom')
        ##### remove
        
    def sAvr(self):
        self.setWindowModified (True) 
        
        
    def srchInind(self,i):
        # really wpild lik to
        # pause here and then return
        # to index zero 
        print ('srchInd' , i)
        if i == 0 :
            # this is what we ar searching FOR
            return
        itd = self.Txtsrch.srchbox.itemData(i).toInt() 
        print ('data' , itd[0])
        if itd[1]:
            self.comboBox.setCurrentIndex(itd[0])
            self.piKard(itd[0])
        self.Txtsrch.srchbox.setCurrentIndex(0)
        # may infinite loop ! seems to work 
    
            
    def piKard(self,i):
        print ('pikard' , i)
        pikt = self.stakr.widget(i)
        print ('pikt' , pikt)
        if i < 0:
            self.spacer.setText ('  Empty  ')
            self.lcdNumber.display(1.200000)
            self.horizontalSlider.setSliderPosition(12)
            return
        zoomf = pikt.zoomFactor()+.000001
        #print ('zoomf' , zoomf)
        self.lcdNumber.display(zoomf)
        print ('pikt' , i ,zoomf)
        aT = str(i +1 )+ ' of ' + str( self.stakr.count())
        self.spacer.setText(aT)
        self.stakr.setCurrentIndex(i)
        #print('set zoomf ',int((zoomf-1.0 )*100.0))
        self.horizontalSlider.setSliderPosition(int((zoomf-1.0 )*100.0))
        #print ('1601 PIKT' ,pikt)
        #print ('pikt IS' , pikt.__class__) 
        pikt.moveCursor(QtGui.QTextCursor.Start)
        ## nurdoch above throws error in sql table
        ## always a  PAIN
        
    def comboFix(self,i):
        print ('709 combo at' , i)
        #Try this rather than Pikard
        # this comes from 
        # pikard comes from activated ??
        
        
        
        
        
        
        
    def comboTxt(self,t):
        print ('txt' , t)
        self.edcomb = t
        
        
    def eDlbl(self,b):
        curind = self.comboBox.currentIndex ()
        print ('edit Label',b, curind)
        self.comboBox.setEditable(b)
        # more qtBS adds a kard if I press return
        # whereas if I do not press return loose my change.
  
        if b:
            self.comboBox.setInsertPolicy( QtGui.QComboBox.InsertAtCurrent)
        else:
            if  self.edcomb != '':
                curind = self.comboBox.currentIndex () 
                self.comboBox.removeItem (curind)
                self.comboBox.insertItem(curind,self.edcomb) 
                self.edcomb = ''
            self.comboBox.setInsertPolicy( QtGui.QComboBox.InsertAtBottom)
            #more qtbs can not see why below is necessary
            self.comboBox.setCurrentIndex (curind)
            print ('1667')
        
        
        
    def qtBS(self,c,b=0 ):
        # put all qt boilplate here 
        # which should be unnecessary 
        a =  QtGui.QMenu(self)
        print ('a = ' , a)
        chkbl =[0,0] 
        shrkt = [0,0]
        for x in b :
            if isinstance(x,int):
                chkbl[0] = True
                chkbl[1] = x
                continue
            elif x[0] == '<' and x[len(x)-1:] == '>':
                print ('shortcut')
                shrkt[0] = True
                shrkt[1] = x[1:len(x)-1] 
                continue
            z=a.addAction(x)
            if chkbl[0]:
                z.setCheckable ( True )
                z.setChecked ( chkbl[1] )
                chkbl = [0,0]
                ## below is 
            if shrkt[0]:
                print ('686 z' , z)
                z.setShortcut(shrkt[1] )
                shrkt = [0,0]
            
        a.triggered.connect(self.toolAc)
        #print 'a' , a
        tlnm = 'tool' + c
        tl =  QtGui.QToolButton()
        tl.setMenu( a)
        tl.setPopupMode(QtGui.QToolButton.InstantPopup)
        tl.setText(c)
        self.tlbar.addWidget(tl)
        return a
    
    def getPrev(self):
        if len( self.histlist) == 0 :
            return
        print ('Get Previous')
        # another qt4 problem
        # for some reason it puts extra space
        # at end or it could be way I saved in qt3
        fltoget = QtGui.QInputDialog.getItem(self,"Previous Kards", "Pick One\
            ", self.histlist)
        #print 'fltoget' , fltoget[0]
        if fltoget[1]:
            if not self.getFile(fltoget[0].trimmed()):
                hwarn = QtGui.QMessageBox.warning (self,"History" , "File not found\
                    or could not load")
                #hwarb.show()
        
    
                
    def saveHist(self):
        print ('before shut down save History File')
        # Never gets here or Histry is NOT saved ???
        # murdoch Fix
                
                
                
    def getHist(self):
        #f = open(HISTLIST)
        # or in qt
        print ('1424')
        f = QtCore.QFile(HISTLIST)
        #,QtCore.QIODevice.ReadWrite )
        # open works even for no file just creates it
        # as long as dir writeable
        if f.open(QtCore.QIODevice.ReadWrite ):
            while not f.atEnd():
                z = QtCore.QString((f.readLine()).trimmed()) 
                self.histlist.append(z)
                ######print z
            f.close()
     
        
        
        
    def getFile(self , nm=None):
        # this will be a biggee
        print ('See if KardFile' , nm)
        #drat = QtCore.QDir.currentPath()
        # always starts where I have murdkrd not helpfull
        # mayb add to histlist ONLY if a kardfile
        drat =  QtCore.QString()
        # a null string
        #self.comboBox.setEnabled(False)
        self.cOntrols(False)
        if nm == None:
            nm = QtGui.QFileDialog.getOpenFileName(self, 
              "get kards or file",
            drat ,"all (*);; kards (*.krd);;htm (*.htm *.html")

        f = QtCore.QFile(nm)
        try:
            print ('f', f ,nm)
        except:
            print (' pycode puke')
        # does pycode puke , nm
        if not f.open( QtCore.QIODevice.ReadOnly):
            print ('809 False')
            nunm = nm.prepend(HOME)
            f = QtCore.QFile(nunm)
            nm = nunm
            if not f.open( QtCore.QIODevice.ReadOnly):
                print ('1430 False')
                return False
        # removed else
        fpth = QtCore.QDir(nm).absolutePath ()
        # below another pycode puke
        #print 'fpth' , fpth
        finf = QtCore.QFileInfo (nm )
        print ('finf dir' ,  finf.path())
            
        if  self.theDirs.count(finf.path())< 1:
            self.theDirs.insert(0,finf.path())
        print ('theDirs' , self.theDirs)
        # save kards htm so can use browser
        if nm.endsWith(QtCore.QString('.png'), QtCore.Qt.CaseInsensitive)\
        or nm.endsWith(QtCore.QString('.jpg'), QtCore.Qt.CaseInsensitive)\
        or nm.endsWith(QtCore.QString('.jpeg'), QtCore.Qt.CaseInsensitive):
            print ('A Pict')
            # maybe popup Force read as kard file
            
            self.gOtkRd= ''
            self.getPict(nm)
            return
        print ('GOT' , f)
        self.qtxts = QtCore.QTextStream ( f ) 
        self.qtxts.setCodec("UTF-8" )
        ## murdoch if len is zero crashes
        # test for none empty file
        while not self.qtxts.atEnd():
            r = self.qtxts.readLine()
            print ('The 1812', r)
            if  r.trimmed() != QtCore.QString(''):
                break
        Nttl = self.parsttl(r.trimmed())
        if Nttl == 0:
            # first line of text not a title so not a krdfile
            print ('Not a krd File')
            # r is first line read
            # R is first line including blank lines
            gOtkRd =''
            self.getText(nm)
        else :
            print ('IS krd file',nm,Nttl)
            # nm should pop up in save dialog
            self.gOtkRd = nm
            self.getKards(Nttl, finf.path())
            # problem is my old qt3 thingy has extra space at end of 
            # each history file name NO it was me using readline thingy
            print ('in history ??' ,   self.histlist.contains(nm),nm)
            if  self.histlist.contains(nm) :
                z = self.histlist.indexOf(nm)
                if z > 0:
                     self.histlist.move(z,0)
                     # move latest to top
            else:
                 self.histlist.prepend(nm)
                    
            
            
        return True
            
            
    def getKards(self,ttl,fpth):
        # comes here with title of first kard
        print ('272 ' , ttl)
        Krdttl = ttl
        txt =  QtCore.QString('')
        while not self.qtxts.atEnd():
            r = self.qtxts.readLine()
            tsttl =  self.parsttl(r.trimmed())
            if tsttl == 0:
                txt.append(r +'\n')
                # readline is stripping off returns 
                #print '280  tsttl' ,  tsttl
            else :
                #print '282' ,  tsttl
                #print 'HERE The title IS ' , Krdttl
                self.addKard(0,Krdttl,txt,fpth,False)
                # the False means do not move the combobox
                Krdttl =tsttl
                print ('NOW   Krdttl IS' ,  Krdttl)
                txt =  QtCore.QString('')
        #print 'after loop' , txt
        self.addKard(0,Krdttl,txt,False)
        self.stakr.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(0)
        aT = ' 1 of ' +str( self.stakr.count())
        self.spacer.setText(aT)
        #self.comboBox.setEnabled (True)    
        self.cOntrols(True)    
            
            
            
            
            
            
            
            
    def getText(self,n):
        print ('269 get as text',n)
        #drplbl =  QtGui.QLabel()
        #drplbl.setPixmap(n)
        ##Web/P image
        txtwid = murdtext()
        #txtwid.append(txt)
        print ('file name', n)
        lish = n.lastIndexOf('/')
        nm = n.right(n.length()-(lish+1))
        print ('206 Name' , nm ,lish)
        print ('Zero??' , self.qtxts.seek(0))
        # another qtBS thing seems to delete empty lines at start??
        while not self.qtxts.atEnd():
            txtwid.append(  self.qtxts.readLine())
        #print 'as Text' , txt
        txtwid.moveCursor (QtGui.QTextCursor.Start) 
        self.addKard(txtwid,nm)
        
        
    def getPict(self,n):
        print ('1961 getpict' , n)
        wv = murdtext()
        print ('self.size is', self.size())
        #print ('wv size IS', wv.frameSize().height() )
        print ('wv size IS', wv.size() )
        ht = QtCore.QString(str(self.size().height()-40)) 
        
        
        htx = QtCore.QString('<img src = "file:///')
        htx.append(n)
        #htx.append('" height="500"/>')
        htx.append(QtCore.QString('" height="'))
        htx.append(ht)
        htx.append(QtCore.QString('"/>'))
        print ('image text is ' , htx)
        wv.setText(htx)
        
        self.addKard(wv,n)
        
        
    def parsttl(self , t):
        
        test =  QtCore.QString( '<BR><!TITLE><B>')
        subst = '</B><BR>' 
        if t.toUpper().contains( test):
            print ('2066 Parse ' ,t) 
            st = t.indexOf(test) + 15 
            print ('parse for title')
            nd = t.indexOf( subst)
            ln = nd -st
            rttl = t.mid(st+1 ,ln -1)
            #rttl = t.mid(st+1 ,ln-2 )
            print ('2073 title ' , rttl)
            return rttl
        # return parsed title
            
        else: 
            return  0
    
        
        
         
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("Plastique")
    ui = Ui_MainWindow(sys.argv  )
    print ('argv' , sys.argv)
    ui.setObjectName('MurdkarQt4')
    #app.connect(app,QtCore.SIGNAL( "lastWindowClosed()"), ui.Quit)  
    ui.show()
    sys.exit(app.exec_())

         
# confusion Eg get html brings up connect dialog etc
#if not connected
# But brings up new Connect dialog if connected ? 
