from glob import glob
import os, sys, time, re
from sys import platform as _platform
app = None
if sys.version_info.major==2:
	from urllib2 import Request, urlopen
elif sys.version_info.major==3:
	from urllib.request import Request, urlopen
import traceback, webbrowser, zipfile, shutil, subprocess

pyversion=str(sys.version_info.major)+str(sys.version_info.minor)
is_64bits = sys.maxsize > 2**32
is_anaconda = 'Anaconda' in sys.version

def _matches_python_bit(fname):
	python_v = ("-cp%s" % pyversion in fname)
	bit_match = fname.endswith("-win%s.whl" % ("_amd64" if is_64bits else '32'))
	return python_v and bit_match
	
base_url='http://www.lfd.uci.edu/~gohlke/pythonlibs/'

submodules = {'scipy': ['ndimage', 'special'], 'skimage': ['draw'], 'matplotlib': ['cbook']}
gohlke_aliases = {"PIL": "Pillow", 'skimage': 'scikit_image'}

def download_file(download_url):
	req = Request(download_url,headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36"})
	response = urlopen(req)
	try:
		length = int(response.getheader('Content-Length'))
	except:
		length = 100000000
	dest = os.path.basename(download_url)
	a = 'a'
	f = open(dest, 'wb')
	i = 0
	while a:
		a = response.read(length // 100000)
		#print(i / length)
		i += 100000.
		if app:
			app.processEvents()
		f.write(a)
	f.close()
	return dest

def install_pip():
	dest = download_file('https://bootstrap.pypa.io/get-pip.py')
	subprocess.call(['python', 'get-pip.py'])
	os.remove(dest)

try:
	import pip
except:
	install_pip()
	import pip

if float(pip.__version__[:3]) < 8.1:
	print("Upgrading Pip to latest version.")
	subprocess.call(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])

def get_url(ml,mi):
	mi = mi.replace('&lt;', '<')
	mi = mi.replace('&gt;', '>')
	mi = mi.replace('&amp;', '&')
	mi = mi.replace("&#46;", '.')
	mi = mi.replace("&#62;", '>')
	mi = mi.replace("&#60;", '<')
	ot="";
	for j in range(len(mi)):
		ot += chr(ml[ord(mi[j])-48])
	return ot

def get_wheel_url(plugin):
	req = Request(base_url, headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36"})
	resp = urlopen(req)
	regex = re.compile('javascript:dl(\([^\)]*\))[^>]*>(%s-[^<]*)<' % plugin, re.IGNORECASE | re.DOTALL)
	fnames = {}
	for line in resp.readlines():
		line = line.decode('utf-8').replace('&#8209;', '-')
		line = line.replace("&#46;", '.')
		fname = re.findall(regex, line)
		if len(fname) > 0:
			res, fname = fname[0]
			res = eval(res)
			if _matches_python_bit(fname):
				fnames[fname] = res
	return get_newest_version(fnames)

def get_newest_version(fnames):
	if len(fnames) == 0:
		return ''
	fname = ''
	version = ['0']
	regex = re.compile('[^-]*-([a-zA-Z0-9\.]*)')
	for f in fnames:
		v = [n for n in re.findall(regex, f)[0].split('.') if n.isdigit()]
		i = 0
		if fname == '' or int(v[0]) > int(version[0]):
			fname = f
			version = v
			continue
		while i < min(len(v), len(version)) - 1 and v[i] == version[i]:
			if int(v[i+1]) > int(version[i+1]):
				version = v
				fname = f
			i += 1
	return get_url(*fnames[fname])


class NotOnGohlkeError(Exception):
	pass
class InstallFailedException(Exception):
	pass
		
def install_wheel(dep):
	if _platform != 'win32':
		raise Exception("No support for installing binaries on non-windows machines")
	wheel = get_wheel_url(dep)
	if wheel != '':
		if not os.path.isfile(wheel):
			print('Downloading {}'.format(base_url+wheel))
			dest = download_file(base_url+wheel)
		print('Installing {}'.format(dest))
		try:
			pip.main(['install', dest, '-qq'])
			os.remove(dest)
		except PermissionError:
			pass
		except IOError:
			pass
		except WindowsError:
			pass
	else:
		raise NotOnGohlkeError("No module named %s found." % dep)

def gohlke_install_plugin(plugin):
	if plugin in gohlke_aliases:
		plugin = gohlke_aliases[plugin]
	if _platform != 'win32':
		return False
	try:
		install_wheel(plugin)
		return True
	except IOError as e:
		print(e)
		print('Must have internet and administrator privileges. Also, make sure that all other Python programs are closed.')
	except NotOnGohlkeError:
		print("Not on Gohlke: %s" % plugin)
	except Exception as e:
		print("Could not install %s from Gohlke's website. %s" % (plugin, traceback.format_exc()))
	return False

def pip_install_plugin(plugin):
	if plugin in gohlke_aliases:
		plugin = gohlke_aliases[plugin]
	pip.main(['install', plugin])


def uninstall_numpy():
	print("Uninstalling old version of numpy")
	path = os.path.join(pip.locations.site_packages, 'numpy')
	if not os.path.exists(path):
		return True
	try:
		shutil.rmtree(path, True)
		if os.path.exists(path):
			i = 0
			while os.path.exists(path + (i * '_old')):
				i += 1
			shutil.move(path, path + (i * '_old'))
	except Exception as e:
		return False
	return True

numpy_uninstalled = False

def test_numpy():
	global numpy_uninstalled
	if is_anaconda:
		return True
	loc = os.path.join(pip.locations.site_packages, 'numpy')
	if os.path.exists(loc):
		try:
			np = __import__('numpy')
			v = np.array(map(eval, np.__version__.split('.')[:2]))
			if not numpy_uninstalled and (any(v < [1, 11]) or np.__config__.blas_mkl_info == {} or np.__config__.lapack_mkl_info == {}):
				if not uninstall_numpy():
					raise InstallFailedException('numpy')
				numpy_uninstalled = True
				return False
			else:
				return True
		except ImportError as e:
			pass
	return False

def install(name, fromlist=[], conda=False, installers=['gohlke', 'pip']):
	if test(name, fromlist, conda=conda):
		return True
	for installer in installers:
		eval('%s_install_plugin' % installer)(name)
		if test(name, fromlist, conda=conda):
			return True
	return False


def test(name, fromlist=[], conda=False):
	if name == 'numpy':
		return test_numpy()
	if conda and is_anaconda:
		return True
	if os.path.join(pip.locations.site_packages, name):
		try:
			__import__(name, fromlist=fromlist)
			return True
		except Exception as e:
			if 'try recompiling' in str(e):
				return True
	return False

if not install('PyQt4', installers=['gohlke'], fromlist=['QtCore', 'QtGui', 'uic'], conda=True):
	print("Failed to install PyQt4 on the machine. Suggest using Anaconda installer for Python")
	sys.exit(0)

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Installer(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(465, 386)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.setFont(font)
        self.gridLayout = QtGui.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(self)
        self.line.setFrameShadow(QtGui.QFrame.Raised)
        self.line.setLineWidth(4)
        self.line.setMidLineWidth(4)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancelButton = QtGui.QPushButton(self)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.continueButton = QtGui.QPushButton(self)
        self.continueButton.setObjectName(_fromUtf8("continueButton"))
        self.horizontalLayout.addWidget(self.continueButton)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.stepLayout = QtGui.QGridLayout()
        self.stepLayout.setContentsMargins(9, -1, 9, -1)
        self.stepLayout.setObjectName(_fromUtf8("stepLayout"))
        self.infoEdit = QtGui.QTextBrowser(self)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.infoEdit.setPalette(palette)
        self.infoEdit.setAutoFillBackground(False)
        self.infoEdit.setOpenExternalLinks(True)
        self.infoEdit.setObjectName(_fromUtf8("infoEdit"))
        self.stepLayout.addWidget(self.infoEdit, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.stepLayout, 2, 0, 1, 1)
        self.titleEdit = QtGui.QTextBrowser(self)
        self.titleEdit.setMaximumSize(QtCore.QSize(16777215, 50))
        self.titleEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.titleEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.titleEdit.setObjectName(_fromUtf8("titleEdit"))
        self.gridLayout.addWidget(self.titleEdit, 0, 0, 1, 1)
        self.progressWidget = QtGui.QWidget(self)
        self.progressWidget.setObjectName(_fromUtf8("progressWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.progressWidget)
        self.verticalLayout.setContentsMargins(9, 0, 9, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressLabel = QtGui.QLabel(self.progressWidget)
        self.progressLabel.setObjectName(_fromUtf8("progressLabel"))
        self.verticalLayout.addWidget(self.progressLabel)
        self.progressBar = QtGui.QProgressBar(self.progressWidget)
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 10))
        self.progressBar.setProperty("value", 1)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.gridLayout.addWidget(self.progressWidget, 3, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.continueButton, self.cancelButton)

    def retranslateUi(self):
        self.setWindowTitle(_translate("Installer", "Dialog", None))
        self.cancelButton.setText(_translate("Installer", "Cancel", None))
        self.continueButton.setText(_translate("Installer", "Continue", None))
        self.infoEdit.setHtml(_translate("Installer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Thank you for downloading Flika!</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">    Flika is a Global Image Processing program written in Python to enable custom analysis of biological movies.  Developed in the UCI Department of Neurobiology and Behavioral Sciences Lab by the <a href=\"http://parkerlab.bio.uci.edu/\"><span style=\" text-decoration: underline; color:#0000ff;\">Parker Research Group</span></a>, Flika is an open-source and customizable tool written by scientists and programmers to automate and augment image processing in the lab.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Click Continue to find out which Python dependencies need to be installed.</p></body></html>", None))
        self.titleEdit.setHtml(_translate("Installer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Flika Installer Dialog</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-weight:600;\"><br /></p></body></html>", None))
        self.progressLabel.setText(_translate("Installer", "Progress", None))


from PyQt4.QtGui import *

class InstallWidget(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.layout = QFormLayout()
		self.setLayout(self.layout)
		fileSelectWidget = QWidget()
		hLayout = QHBoxLayout()
		fileSelectWidget.setLayout(hLayout)
		browseButton = QPushButton("Browse")
		browseButton.pressed.connect(self.browsePressed)
		self.fileEdit = QLineEdit(os.path.join(os.path.expanduser('~'), 'Desktop'))
		hLayout.addWidget(self.fileEdit)
		hLayout.addWidget(browseButton)
		infoText = QTextEdit('Python and Flika dependencies have been successfully installed.  Next, download the Flika github repository to a safe destination on your computer.  Select the folder to extract the folder to:')
		infoText.setFrameStyle(QFrame.NoFrame)
		infoText.viewport().setAutoFillBackground(False)
		infoText.setReadOnly(True)
		self.shortcutCheck = QCheckBox("Create Desktop Shortcut")
		self.shortcutCheck.setChecked(True)

		self.layout.addRow(infoText)
		self.layout.addRow(QLabel("Destination:"))
		self.layout.addRow(fileSelectWidget)
		self.layout.addRow(self.shortcutCheck)

	def browsePressed(self):
		d = QFileDialog.getExistingDirectory(self, "Select a directory", "Choose where to save the Flika directory on your computer:")
		self.fileEdit.setText(d)



class InstallerWindow(Ui_Installer):
	DEPENDENCIES = ['numpy', 'scipy', 'pyqtgraph', 'skimage', "PIL", 'xmltodict', 'future', 'matplotlib', 'openpyxl', 'nd2reader']
	def __init__(self):
		Ui_Installer.__init__(self)
		self.cancelButton.clicked.connect(self.close)
		self.continueButton.clicked.connect(self.continuePressed)
		self._currentStep = 0
		self.progressWidget.setVisible(False)

		version = sys.version_info.major, sys.version_info.minor, sys.version_info.micro
		if version[0] == 2 and version[1] <= 7 and version[2] <= 8:
			self.infoEdit.append("\nWARNING: Flika was written for Python Versions 2.7.9+. Your current version is %d.%d.%d.  It is recommended that you remove Python and install a later version." % (version))
			pythonButton = QPushButton("Update Python")
			def downloadClicked():
				webbrowser.open('https://www.python.org/downloads/',new=2)
				self.close()
			pythonButton.pressed.connect(downloadClicked)
			self.continueButton.pressed.connect(lambda : pythonButton.setVisible(False))
			self.horizontalLayout.insertWidget(2, pythonButton)

	def downloadFlika(self):
		self.progressWidget.setVisible(True)
		self.progressLabel.setText('Downloading Flika...')
		app.processEvents()
			
		dest = str(self.installWidget.fileEdit.text())
		url = 'https://github.com/flika-org/flika/archive/master.zip'
		self.progressBar.setValue(10)
		app.processEvents()

		try:
			data = urlopen(url).read()
		except:
			self.infoEdit.append("\nAn error occurred while attempting to connect. Check your connection and try again.")
			raise Exception()
		self.progressBar.setValue(30)
		app.processEvents()

		output = open("flika.zip", "wb")
		output.write(data)
		output.close()
		self.progressBar.setValue(60)
		app.processEvents()
		
		with zipfile.ZipFile('flika.zip', "r") as z:
			folder_name = os.path.dirname(z.namelist()[0])
			z.extractall(dest)
		self.progressBar.setValue(90)
		app.processEvents()

		os.remove('flika.zip')
		if self.installWidget.shortcutCheck.isChecked():
			self.make_shortcut(dest)
		self.progressWidget.setVisible(False)

	def make_shortcut(self, folder):
		p = os.path.join(os.path.expanduser('~'), 'Desktop', 'Flika.%s' % ('bat' if _platform == 'win32' else 'sh'))
		with open(p, 'w') as outf:
			outf.write('#!/bin/bash\npython %s' % os.path.join(folder, 'flika-master', 'flika.py'))

	@property
	def currentStep(self):
		return self._currentStep
	
	@currentStep.setter
	def currentStep(self, step):
		self._currentStep = step
		if step == -1:
			self.setTitle("Error")
			self.continueButton.pressed.disconnect()
			self.continueButton.pressed.connect(self.close)
			self.continueButton.setText("Close")
			self.progressWidget.setVisible(False)
			self.show()
		if step == 1:
			self.setTitle("Installing Dependencies")
			self.infoEdit.setText("The dependencies required for Flika are:\nnumpy\nscipy\nPyQt4\nfuture\npyqtgraph\nmatplotlib\nskimage\nPIL\nxmltodict\nopenpyxl\nnd2reader\n\n    This installer will go through each dependency to ensure the correct version is installed on your machine. Click continue to make sure all dependencies are up to date.")
		elif step == 2:
			self.setTitle("Downloading Flika Repository")
			self.installWidget = InstallWidget()
			self.stepLayout.addWidget(self.installWidget)
			self.infoEdit.setVisible(False)
		if self._currentStep == 3:
			self.installWidget.setVisible(False)
			self.infoEdit.setVisible(True)
			self.setTitle('Installation Successful')
			self.infoEdit.setText("Successfully installed Flika!\n\nRun Flika by executing the desktop shortcut or running the flika.py file located in the Flika folder.\n\nThank you for downloading Flika.")
			self.continueButton.setText("Finish")
		elif self._currentStep > 3:
			self.close()

	def continuePressed(self):
		if self.currentStep == 1:
			try:
				self.install_dependencies()
			except InstallFailedException as e:
				self.infoEdit.setText("An error occurred while testing %s." % str(e))
				self.currentStep = -1
		elif self.currentStep == 2:
			try:
				self.downloadFlika()
			except:
				return
		self.currentStep += 1

	def setTitle(self, t):
		self.titleEdit.setHtml('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\
<html><head><meta name="qrichtext" content="1" /><style type="text/css">\
p, li { white-space: pre-wrap; }\
</style></head><body style=" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;">\
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:11pt; font-weight:600;">%s</span></p></body></html>' % t)


	def install_dependencies(self):
		self.progressWidget.setVisible(True)
		stepSize = 100 / 11
		app.processEvents()
		def test_dependency(name, installers=['gohlke', 'pip'], fromlist=[], conda=False):
			global val
			self.progressLabel.setText("Testing %s (This may take a while)..." % name)
			app.processEvents()
			if not install(name, installers=installers, fromlist=fromlist, conda=conda):
				raise InstallFailedException(name)
			self.progressBar.setValue(self.progressBar.value() + stepSize)
		
		test_dependency('numpy', installers=['gohlke'], conda=True)
		test_dependency('scipy', fromlist=['special', 'ndimage'], conda=True)
		test_dependency('matplotlib', fromlist=['pytplot', 'cbook'], conda=True)
		test_dependency('skimage', fromlist=['draw'])
		for name in ('future', 'PIL', 'pyqtgraph', 'xmltodict', 'openpyxl', 'nd2reader'):
			if not self.isVisible():
				return
			test_dependency(name, installers=['pip', 'gohlke'])
		self.progressWidget.setVisible(False)


if __name__ == '__main__':
	app = QApplication([])
	mw = InstallerWindow()
	mw.show()
	app.exec_()