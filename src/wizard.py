#!/usr/bin/python3
import getpass
import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QComboBox,QPushButton,QVBoxLayout,\
				QDialog,QGridLayout,QLineEdit,QFileDialog,QCheckBox,QFrame
from PyQt5 import QtGui
from PyQt5.QtCore import QSize,Qt
import gettext
import subprocess
import locale
QString=type("")
QInt=type(0)
TAB_BTN_SIZE=96
BTN_SIZE=128
gettext.textdomain('lliuwin')
_ = gettext.gettext


SRC="/usr/share/lliuwin"
RSRC="%s/rsrc"%SRC
#Translations
WLC_MSG=_("Welcome to LliureX 19. Let's do some final adjustments")
USR_MSG=_("Configure new account")
AVA_MSG=_("You can also define an avatar for your user")
LNG_MSG=_("Locale")
HOST_MSG=_("Hostname")
ERR_PASS_MATCH=_("Passwords don't match")
ERR_PASS_LEN=_("Password length must be at least 6 characters long")
ERR_PASS_LONG=_("Password length must be 30 characters maximun")
ERR_USR_LEN=_("User name must be at least 2 characters long")
ERR_USR_LONG=_("User name must be at most 30 characters long")
ERR_UNKNOWN=_("Unknown error")
MSG_CONFIRM_TITLE=_("Read carefully")
MSG_END_TITLE=_("All ready")
LBL_USER=_("Username")
LBL_PASS=_("Password")
LBL_PASS2=_("Repeat password")
LBL_LOCALE=_("Locale")
LBL_NEW=_("A new user will be created. Please verify the details below are correct")
LBL_END=_("LliureX is now configured. When ready press start")
LBL_LOGIN=_("Enable autologin")
ACCEPT=_("Apply")
CANCEL=_("Cancel")
START=_("Start")

class wizard(QWidget):
	def __init__(self):
		super().__init__()
		self.dbg=True
		self.btnClose=False
		self.err={1:ERR_PASS_MATCH,2:ERR_PASS_LEN,3:ERR_USR_LEN,4:ERR_PASS_LONG,5:ERR_USR_LONG}
		(self.keymap,self.modmap)=self._load_keys()
		self._render_gui()
	#def init

	def _debug(self,msg):
		if self.dbg:
			print("wizard: %s"%msg)
		self.setWindowOpacity(.60)
	#def _debug

	def _load_keys(self):
		keymap={}
		self.closeKey=False
		for key,value in vars(Qt).items():
			if isinstance(value, Qt.Key):
				keymap[value]=key.partition('_')[2]
		modmap={
					Qt.ControlModifier: keymap[Qt.Key_Control],
					Qt.AltModifier: keymap[Qt.Key_Alt],
					Qt.ShiftModifier: keymap[Qt.Key_Shift],
					Qt.MetaModifier: keymap[Qt.Key_Meta],
					Qt.GroupSwitchModifier: keymap[Qt.Key_AltGr],
					Qt.KeypadModifier: keymap[Qt.Key_NumLock]
					}
		return(keymap,modmap)
	
	def closeEvent(self,event):
		if self.close==False: 
			event.ignore()
	#def closeEvent
	
	def keyPressEvent(self,event):
		key=self.keymap.get(event.key(),event.text())
		if key=="Alt":
			self.grab=True
			self.grabKeyboard()
		if key=="Super_L":
			event.accept()
		
	#def eventFilter
	
	def keyReleaseEvent(self,event):
		key=self.keymap.get(event.key(),event.text())
		if key=='Alt' or key=='Control':
			self.releaseKeyboard()
			self.grab=False
			if key=='Alt':
				if self.closeKey:
					self.closeKey=False
	#def keyReleaseEvent

	def _init_gui(self):
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		self.setWindowState(Qt.WindowFullScreen)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowModality(Qt.WindowModal)
		self.setStyleSheet(self._define_css())
		self.avatar="%s/user.svg"%RSRC
		self.bg="%s/background.svg"%RSRC
		self.showFullScreen()
		#self.show()
	#def _init_gui(self):

	def _render_gui(self):
		#Enable transparent window
		#self.setAttribute(Qt.WA_TranslucentBackground)

		####
		self._init_gui()
		self.frm_Init=QFrame()
		self.frm_End=QFrame()
		oImage = QtGui.QImage(self.bg)
		##sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
		palette = QtGui.QPalette()
		palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(oImage))                        
		self.setPalette(palette)

		self.box=QGridLayout()
		self.mbox=QGridLayout()
		pxm_logo=QtGui.QPixmap("%s/logo.svg"%RSRC)
		#wlc_msg=QLabel(WLC_MSG)
		wlc_msg=QLabel()
		wlc_msg.setPixmap(pxm_logo)
		wlc_msg.setObjectName("Message")
		self.box.addWidget(wlc_msg,0,0,1,2,Qt.AlignCenter|Qt.AlignBottom)
		usr_frame=QFrame()
		usr_layout=QGridLayout()
		usr_layout.addWidget(QLabel(USR_MSG),0,0,1,3,Qt.AlignCenter|Qt.AlignBottom)
		usr_frame.setLayout(usr_layout)

		self.usr_name=QLineEdit()
		self.usr_name.setPlaceholderText(LBL_USER)
		usr_layout.addWidget(self.usr_name,2,0,1,1,Qt.Alignment(0))
		self.usr_pass=QLineEdit()
		self.usr_pass.setEchoMode(QLineEdit.Password)
		self.usr_pass.setPlaceholderText(LBL_PASS)
		usr_layout.addWidget(self.usr_pass,3,0,1,1)
		self.usr_pass2=QLineEdit()
		self.usr_pass2.setEchoMode(QLineEdit.Password)
		self.usr_pass2.setPlaceholderText(LBL_PASS2)
		usr_layout.addWidget(self.usr_pass2,4,0,1,1)
		self.chk_login=QCheckBox(LBL_LOGIN)
		usr_layout.addWidget(self.chk_login,4,2,1,1,Qt.Alignment(1))
		self.box.addWidget(usr_frame,2,0,1,2,Qt.AlignCenter|Qt.AlignTop)

		self.usr_avatar=QPushButton()
		self.usr_avatar.setObjectName("QPushButton")
		icn=QtGui.QIcon(self.avatar)
		self.usr_avatar.setIcon(icn)
		self.usr_avatar.setIconSize(QSize(128,128))
		usr_layout.addWidget(self.usr_avatar,2,2,2,1,Qt.Alignment(1))
		
		lng_frame=QFrame()
		lng_frame.setObjectName("QFrame2")
		lng_layout=QGridLayout()
		lbl_lang=QLabel(LNG_MSG)
		lbl_lang.setStyleSheet("padding:0px;border:0px;margin:0px;margin-right:6px")
		lbl_lang.setObjectName("QLabel")
		lng_layout.addWidget(lbl_lang,5,0,1,1,Qt.AlignLeft)
		self.lng_locale=QComboBox()
		self.lng_locale.addItems([_("Valencian"),_("Spanish"),_("English")])
		self.lng_locale.addItems(locale.locale_alias)
		lng_layout.addWidget(self.lng_locale,5,1,1,1,Qt.Alignment(1))
		lng_frame.setLayout(lng_layout)
		usr_layout.addWidget(lng_frame,5,0,1,1,Qt.AlignLeft)
		
		self.hostname=QLineEdit()
		self.hostname.setPlaceholderText("%s (optional)"%HOST_MSG)
		usr_layout.addWidget(self.hostname,5,2,1,1)

		self.err_label=QLabel()
		self.box.addWidget(self.err_label,3,0,1,2,Qt.AlignCenter|Qt.AlignBottom)
		btn_Ko=QPushButton(_("Cancel"))
		btn_Ko.clicked.connect(self._on_close)
		self.box.addWidget(btn_Ko,4,0,1,1,Qt.AlignCenter)
		btn_Ok=QPushButton(_("Continue"))
		btn_Ok.clicked.connect(self._on_apply)
		self.box.addWidget(btn_Ok,4,1,1,1,Qt.AlignCenter)
		self.frm_Init.setLayout(self.box)
		self.frm_Init.setObjectName("QFrame")
		self.mbox.addWidget(self.frm_Init,0,0,1,1)
		self.setLayout(self.mbox)
	#def _render_gui

	def _on_exit(self,*args):
		self.btnClose=True
		self.close()

	def _on_apply(self):
		self.err_label.hide()
		self.usr_name.setStyleSheet("background:none")
		self.usr_pass.setStyleSheet("background:none")
		err=self._validate_fields()
		if err==0:
			self._confirm_user()
		else:
			self.err_label.setText(self.err.get(err,ERR_UNKNOWN))
			self.err_label.show()
			if err in [1,2,5]:
				self.usr_pass.setStyleSheet("background:red")
			if err in [3,4]:
				self.usr_name.setStyleSheet("background:red")

	def _validate_fields(self):
		err=0
		usr=self.usr_name.text()
		pwd=self.usr_pass.text()
		pwd2=self.usr_pass2.text()
		if pwd!=pwd2:
			err=1
		if len(pwd)<6:
			err=2
		if len(pwd)>30:
			err=5
		if len(usr)<2:
			err=3
		if len(usr)>20:
			err=4
		return err

	def _confirm_user(self):
		md=QDialog()
		md.accepted.connect(self._setConfig)
		md.setWindowTitle(MSG_CONFIRM_TITLE)
		hostname=self.hostname.text()
		if hostname=="":
			hostname="LliuWin"
		txt="%s\n"%LBL_NEW
		txt+="\n%s: %s"%(LBL_USER,self.usr_name.text())
		txt+="\n%s: %s"%(LBL_LOCALE,self.lng_locale.currentText())
		txt+="\n%s: %s"%(HOST_MSG,hostname)
		lay=QGridLayout()
		md.setLayout(lay)
		lay.addWidget(QLabel("%s"%txt),0,0,1,2)
		btn_Ok=QPushButton(ACCEPT)
		btn_Ok.clicked.connect(md.accept)
		lay.addWidget(btn_Ok,1,1,1,1)
		btn_Ko=QPushButton(CANCEL)
		btn_Ko.clicked.connect(md.reject)
		lay.addWidget(btn_Ko,1,0,1,1)
		md.setWindowModality(Qt.ApplicationModal)
		md.resize(600,300)
		md.exec_()
	#def _confirm_user

	def _setConfig(self):
		autologin=""
		if self.chk_login.isChecked()==True:
			autologin=self.usr_name.text()
		lang=self._get_user_locale()
		hostname=self.hostname.text()
		if hostname=="":
			hostname="LliuWin"
		cmd=['pkexec','%s/wizard_helper.sh'%SRC,self.usr_name.text(),self.usr_pass.text(),lang,hostname,autologin]
		try:
			subprocess.run(cmd)
		except Exception as e:
			print(str(e))
			return False
		self._on_finish()
	#def _setConfig

	def _get_user_locale(self):
		lang=self.lng_locale.currentText()
		if lang in [_("Valencian"),_("Spanish"),_("English")]:
			if lang==_("Valencian"):
				lang="ca_ES.utf8@valencia"
			elif lang==_("Spanish"):
				lang="es_ES.utf8"
			else:
				lang="en_US.utf8"
		return lang
	#def _get_user_locale

	def _on_finish(self):
		frm_End=QFrame()
		frm_End.setObjectName("QFrame")
		lay=QGridLayout()
		lbl=QLabel(LBL_END)
		lbl.setStyleSheet("font-size:24px;color:white")
		lay.addWidget(lbl,0,0,1,1,Qt.AlignCenter)
		btn=QPushButton(START)
		lay.addWidget(btn,1,0,1,1,Qt.AlignTop|Qt.AlignCenter)
		btn.clicked.connect(self._on_close)
		self.frm_Init.hide()
		frm_End.setLayout(lay)
		self.mbox.addWidget(frm_End,0,0,1,1)
	#def _on_finish

	def _on_close(self,*args):
		cmd=["loginctl","terminate-user","lliurex"]
		try:
			subprocess.run(cmd)
		except Exception as e:
			print(str(e))
			return False
		self.close()

	def showMessage(self,msg,status="error",height=252):
		return()
		self.statusBar.height_=height
		self.statusBar.setText(msg)
		if status:
			self.statusBar.show(state=status)
		else:
			self.statusBar.show(state=None)
	#def _show_message

	def _define_css(self):
		css="""
		#Message{
			padding:10px;
			margin:60px;
			border:40px;
		}
		#QPushButton{
			background-color:rgba(255,255,255,0);
			border-radius:25px;
		}
		QFrame{
			background-color:rgba(255,255,255,0.5);
			padding:10px;
			margin:10px;

		}
		#QFrame{
			background-color:rgba(255,255,255,0);
			padding:10px;
			margin:10px;

		}
		#QFrame2{
			background-color:rgba(255,255,255,0);
			padding:0px;
			margin:0px;

		}
		QLabel{
			font-weight:bold;
			background-color:transparent;
			font-size: 18px;	
		}
		#QLabel{
			font-weight:Normal;
			background-color:transparent;
			font-size: 14px;	
		}
		QLineEdit{
			padding:3px;
			margin:6px;
		}

		QCheckBox{
			margin:6px;
		}
		"""
		return(css)
		#def _define_css
#class runomatic

app=QApplication(["LliuWin Wizard"])
wizardLauncher=wizard()
app.exec_()

