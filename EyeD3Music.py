import sys
import musicdownloader
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QListView
from MusicDownloader_ui import Ui_MusicDownloader

stdout_temp = sys.stdout

class Stream(QtCore.QObject):
    textPrint = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textPrint.emit(str(text))

class DownloadWork(QtCore.QObject):
    end_sig = QtCore.pyqtSignal()

    def __init__(self):
        super(DownloadWork, self).__init__()

    def download_music(self, mode, id):
        musicdownloader.gui_download(mode, id)
        self.end_sig.emit()

class MainWindow(QMainWindow, Ui_MusicDownloader):
    begin_sig = QtCore.pyqtSignal(int, str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        sys.stdout = Stream(textPrint=self.output_print)

        self.init_style()

        # 信号绑定
        self.ModeComboBox.currentIndexChanged.connect(self.mode_current_index_changed)
        self.APILineEdit.textChanged.connect(self.api_text_changed)
        self.FrontArtistCheckBox.stateChanged.connect(self.front_artist_state_changed)
        self.RearArtistCheckBox.stateChanged.connect(self.rear_artist_state_changed)
        self.LyricCheckBox.stateChanged.connect(self.lyric_state_changed)
        self.HDCheckBox.stateChanged.connect(self.hd_state_changed)
        self.DownloadPushButton.clicked.connect(self.download_clicked)

        # 下载线程初始化
        self.download_thread = QtCore.QThread()
        self.download_work = DownloadWork()
        self.download_work.moveToThread(self.download_thread)
        # 下载线程信号绑定
        self.begin_sig.connect(self.download_work.download_music)
        self.download_work.end_sig.connect(self.download_thread_end)
        # 启动线程
        self.download_thread.start()

    # 关闭响应
    def closeEvent(self, event):
        self.download_thread.quit()
        sys.stdout = stdout_temp
        super().closeEvent(event)

    # 重定向输出
    def output_print(self, text):
        # 输出到界面
        cursor = self.PrintTextEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.PrintTextEdit.setTextCursor(cursor)
        self.PrintTextEdit.ensureCursorVisible()

        # 输出到日志
        musicdownloader.gui_print_log(text)

    # 初始化样式
    def init_style(self):
        self.ModeComboBox.setView(QListView())
        self.UrlIdLineEdit.setPlaceholderText("请输入网易云单曲ID或链接")
        self.APILineEdit.setText("http://api.injahow.cn/meting/")

    # 界面激活
    def gui_enabled(self, enabled):
        self.ModeComboBox.setEnabled(enabled)
        self.UrlIdLineEdit.setEnabled(enabled)
        self.APILineEdit.setEnabled(enabled)
        self.FrontArtistCheckBox.setEnabled(enabled)
        self.RearArtistCheckBox.setEnabled(enabled)
        self.LyricCheckBox.setEnabled(enabled)
        self.HDCheckBox.setEnabled(enabled)
        self.DownloadPushButton.setEnabled(enabled)

    # 下载模式修改
    def mode_current_index_changed(self, currentIndex):
        self.UrlIdLineEdit.clear()
        if currentIndex == 0:
            self.UrlIdLineEdit.setPlaceholderText("请输入网易云单曲ID或链接")
        elif currentIndex == 1:
            self.UrlIdLineEdit.setPlaceholderText("请输入网易云歌单ID或链接")
        elif currentIndex == 2:
            self.UrlIdLineEdit.setPlaceholderText("请输入QQ音乐单曲ID或链接")
        elif currentIndex == 3:
            self.UrlIdLineEdit.setPlaceholderText("请输入QQ音乐歌单ID或链接")
        elif currentIndex == 4:
            self.UrlIdLineEdit.setPlaceholderText("请输入网易云专辑ID或链接")
        elif currentIndex == 5:
            self.UrlIdLineEdit.setPlaceholderText("请输入歌手专辑页ID")

    def api_text_changed(self, text):
        musicdownloader.gui_set_api_server(text)

    def front_artist_state_changed(self):
        musicdownloader.gui_mode_setting(2)

    def rear_artist_state_changed(self):
        musicdownloader.gui_mode_setting(1)

    def lyric_state_changed(self):
        musicdownloader.gui_mode_setting(3)

    def hd_state_changed(self):
        musicdownloader.gui_mode_setting(4)

    # 下载
    def download_clicked(self):
        self.gui_enabled(False)

        mode = self.ModeComboBox.currentIndex() + 1
        id = self.UrlIdLineEdit.text()
        self.begin_sig.emit(mode, id)

    # 下载完成
    def download_thread_end(self):
        self.gui_enabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    musicdownloader.gui_main()
    sys.exit(app.exec_())
