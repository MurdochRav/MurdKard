from PyQt4  import  QtSql, QtCore
try :
    import enchant
    Spelur = True
except:
    
    Spelur = False
import os,sys

BKG = ("QLabel {background-image: url(Shroom.jpg); color : #ef8948; }")


COPYRIGHT="<body><center> <img alt=graphic src=:fernT.png ></center> \
         <h1 >MurdKard Qt4 .01 </h1> <p><h2>Copyright Martin M Raivio \
         November 18 2013,p.<p> under GNU GPG 3 <p>based on murdkard pyqt3 version\
         copyright 2006  </body>"
TEXTEDIT = False
TEXTBROWSER = False
import getpass
SQLUSER = getpass.getuser()
# OR if you wnat it not obvious SQLUSER = "_________" 
# below default font size
PyVer = sys.version[0]
FONTSIZE = 13
# name of default connection to database
# result is connection to only one database Eg mysql
# at a time
DEFAULTDB= "DefaultDb"
SQLBASES= ["browse"]
## show databases; 
# is mysql command

# dictionary of ways to get table names 
SQLTBLS = {'QMYSQL': "show tables" , \
'QMYSQL3': "show tables" , \
'QSQLITE' : "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name" ,\
'QPSQL7': "select tablename from pg_tables where tablename not like 'pg_%' and \
tablename not like 'sql_%'" , \
'QPSQL': "select tablename from pg_tables where tablename not like 'pg_%' and \
tablename not like 'sql_%'"  }
# max row for htmlsql so it does not run forever
# adjust depending on puter speed
MAXSQLROW = 500
# if tons of data in one row still slow 
# will Ask if you wnat a change
#SQLEDIT= QtSql.QSqlTableModel.OnManualSubmit	
SQLEDIT=  QtSql.QSqlTableModel.OnFieldChange 
#OnFieldChange < change happens immediately
# QSqlTableModel::OnRowChange < when you go to other row 

HISTLIST =  os.getcwd()+'/History'
HOME=  str(QtCore.QUrl.fromLocalFile( os.path.expanduser('~')))
THEDIRS = [HOME+'/data/']
SPELDIR = os.getcwd()+'/Spel'
