from .CallStackView import CallStackView, StandardItem
from .SourceEdit import SourceEdit
from .CommentEdit import CommentEdit
from .Document import Document
from .about import AboutDialog
from .source_file_path_dialog import SourceFilePathDialog
from PyQt5.QtCore import Qt, QCoreApplication, QSettings
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QStatusBar, QFileDialog, QAction, QDockWidget
from PyQt5.QtGui import QCloseEvent
from pathlib import Path
import os


def keystoint(x):
    return {int(k): v for k, v in x.items()}


def adjust_file_path(filename: str) -> str:
    if Path(filename).is_file():
        return filename

    newpath = Path.cwd().joinpath(filename)
    if Path(newpath).is_file():
        return newpath

    return None


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.settings = QSettings('cjtool', 'codebook')
        self.recent_files: list = self.settings.value(
            'recent_files', [], 'QStringList')

        tree_docker = self._addTreeDock()
        source_docker = self._addSourceDock()
        self.comment_docker = self._addCommentDock()

        self.setCentralWidget(source_docker)
        self.setContentsMargins(6, 0, 6, 0)

        self.splitDockWidget(tree_docker, source_docker, Qt.Horizontal)
        self.splitDockWidget(source_docker, self.comment_docker, Qt.Vertical)
        self.resizeDocks([tree_docker, source_docker], [
                         3, 7], Qt.Orientation.Horizontal)
        self.resizeDocks([source_docker, self.comment_docker],
                         [7, 3], Qt.Orientation.Vertical)
        self.resize(1200, 900)
        self.setWindowTitle('CodeBook')

        self._createMenuBar()
        self.document: Document = None

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.settings.setValue('recent_files', self.recent_files)
        self._close_file()
        if self.document:
            a0.ignore()
        else:
            super().closeEvent(a0)

    def _addTreeDock(self):
        self.tree_view = CallStackView()
        self.tree_view.selectionModel().selectionChanged.connect(self.selectionChanged)
        docker = QDockWidget('callstack', self)
        docker.setWidget(self.tree_view)
        docker.setTitleBarWidget(QWidget())
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, docker)
        return docker

    def _addSourceDock(self):
        source_edit = SourceEdit()
        docker = QDockWidget('source', self)
        docker.setWidget(source_edit)
        docker.setTitleBarWidget(QWidget())
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, docker)
        self.source_edit = source_edit
        return docker

    def _addCommentDock(self):
        comment_edit = CommentEdit()
        docker = QDockWidget('comment', self)
        docker.setWidget(comment_edit)
        docker.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable |
                           QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea, docker)
        self.comment_edit = comment_edit
        return docker

    # def _fillContent(self, rootNode) -> None:
    #     filepath = ''
    #     if (len(sys.argv) == 2):
    #         filepath = adjust_file_path(sys.argv[1])

    #     if filepath:
    #         self._parse_file(rootNode, filepath)

    def _createMenuBar(self) -> None:
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')

        fileMenu.addAction('&Open ...').triggered.connect(self._open_file)
        self.recentMenu = fileMenu.addMenu('Open Recent')
        self._create_recent_files_menu()
        fileMenu.addAction('Source File &Path ...').triggered.connect(self._source_file_path)
        fileMenu.addAction('&Save').triggered.connect(self._save_file)
        fileMenu.addAction('Save &As ...').triggered.connect(
            self._save_as_file)
        fileMenu.addAction('&Close').triggered.connect(self._close_file)

        fileMenu.addSeparator()
        fileMenu.addAction('&Exit').triggered.connect(self._exit)

        viewMenu = menuBar.addMenu('&View')
        toggleAction = self.comment_docker.toggleViewAction()
        viewMenu.addAction(toggleAction)

        helpMenu = menuBar.addMenu('&Help')
        helpMenu.addAction('&About').triggered.connect(self._about)

        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.showMessage('')

    def _create_recent_files_menu(self) -> None:
        self.recentMenu.clear()

        if not self.recent_files:
            return

        def foo(file): return lambda: self._open_recent_file(file)
        for file in self.recent_files:
            filepath = os.path.normpath(file)
            act = QAction(filepath, self)
            act.triggered.connect(foo(file))
            self.recentMenu.addAction(act)

        self.recentMenu.addSeparator()
        self.recentMenu.addAction('Clear Items').triggered.connect(
            self._clear_recent_files)

    def _save_file(self) -> None:
        self.document.save()

    def _save_as_file(self) -> None:
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save cst file', '', 'cst Files (*.cst)')
        if filename:
            self.document.save_as(filename)
            if filename in self.recent_files:
                self.recent_files.remove(filename)
            self.recent_files.insert(0, filename)
            self._create_recent_files_menu()

    def _exit(self):
        self.close()
        if not self.document:
            QCoreApplication.instance().quit()

    def _source_file_path(self):
        dlg = SourceFilePathDialog(self)
        dlg.exec_()

    def _close_file(self) -> None:
        if not self.document:
            return

        if self.document.isDirty:
            reply = QMessageBox.warning(self, 'File is modified but not saved',
                                        'Yes to Save, No to Ignore', QMessageBox.Yes | QMessageBox.No | QMessageBox.Abort, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.document.save()
            elif reply == QMessageBox.Abort:
                return

        self.document.close()
        self.document = None
        self.tree_view.clear()
        self.source_edit.clear()
        self.comment_edit.clear()
        self.setWindowTitle(f"CodeBook")

    def _open_file(self, filename=None) -> None:
        if self.document:
            self._close_file()
            if self.document:
                return

        if filename:
            if not Path(filename).exists():
                QMessageBox.warning(
                    self, 'CodeBook', f'File "{filename}" is not found', QMessageBox.Ok)
                return
        else:
            filename, _ = QFileDialog.getOpenFileName(
                self, 'Open cst file', '', 'cst Files (*.cst)')

        if filename:
            self.setWindowTitle(f"CodeBook: {Path(filename).stem}")
            rootNode = self.tree_view.model().invisibleRootItem()

            self.document = Document(filename, rootNode)
            self.document.open()
            self.document.fill_tree()

            self.tree_view.expandAll()
            self.source_edit.setDocument(self.document)
            self.comment_edit.setDocument(self.document)
            self.tree_view.setDocument(self.document)
            self.document.commentChanged.connect(self.tree_view.on_comment_changed)
            self.document.annotationChanged.connect(self.tree_view.on_annotation_changed)
            self.document.contentChanged.connect(self.onContentChanged)

            if filename in self.recent_files:
                self.recent_files.remove(filename)
            self.recent_files.insert(0, filename)

            self._create_recent_files_menu()

    def _open_recent_file(self, filename) -> None:
        if not Path(filename).exists():
            QMessageBox.warning(
                self, 'CodeBook', f'File "{filename}" is not found', QMessageBox.Ok)

            self.recent_files.remove(filename)
            self._create_recent_files_menu()
        else:
            self._open_file(filename)

    def _clear_recent_files(self):
        self.recent_files.clear()
        self._create_recent_files_menu()

    def _about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def selectionChanged(self, selected, deselected) -> None:
        if not selected.indexes():
            return

        selectedIndex = selected.indexes()[0]
        item: StandardItem = selectedIndex.model().itemFromIndex(selectedIndex)
        if not item.functionData:
            return

        # 确定函数名所在的行
        filefullpath = item.functionData.fileName
        self.statusBar().showMessage(
            f"{filefullpath}({item.functionData.startLineNumber})")

    def onContentChanged(self):
        if not self.document:
            return
        filename = self.document.filename
        if self.document.isDirty:
            self.setWindowTitle(f"CodeBook: {Path(filename).stem} *")
        else:
            self.setWindowTitle(f"CodeBook: {Path(filename).stem}")
