import zipfile
import tempfile
import json
from pathlib import Path
from debuger import BreakPointHit, FunctionData
from PyQt5.Qt import QStandardItem, QIcon
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot, QItemSelection
import os
import pkg_resources


def keystoint(x):
    return {int(k): v for k, v in x.items()}


def zipDir(dirpath: str, outFullName: str) -> None:
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename),
                      os.path.join(fpath, filename))
    zip.close()


class StandardItem(QStandardItem):
    def __init__(self, txt=''):
        super().__init__()
        self.setEditable(False)
        self.setText(txt)
        self.count = 1
        self.offset = 0
        self.startOffset = 0
        self.id = 0
        self.functionData: FunctionData = None

    def increaseCount(self):
        self.count += 1
        txt = self.functionName()
        self.setText(f'{txt} * {self.count}')

    def functionName(self):
        arr = self.text().split('*')
        return arr[0].rstrip()


class Document(QObject):
    contentChanged = pyqtSignal()
    curItemChanged = pyqtSignal(StandardItem)
    commentChanged = pyqtSignal(str)
    annotationChanged = pyqtSignal(int, str)

    def __init__(self, filename: str, rootNode: StandardItem) -> None:
        super(Document, self).__init__()
        self.tempdir = None
        self.filename = filename
        self.rootNode = rootNode
        self.isDirty = False
        self.curItem: StandardItem = rootNode
        comment_path = pkg_resources.resource_filename('callbook', 'image/comment.png')
        self.comment_icon = QIcon(comment_path)

    def open(self):
        zf = zipfile.ZipFile(self.filename)
        self.tempdir = tempfile.TemporaryDirectory()
        zf.extractall(self.tempdir.name)
        self.breakpoints, self.functions = self.__get_data()

    def close(self):
        if self.tempdir:
            self.tempdir.cleanup()
            self.tempdir = None

    def __get_data(self) -> tuple:
        """
        Read the file monitor.json
        """
        assert self.tempdir
        monitor_file = Path(self.tempdir.name).joinpath('monitor.json')
        with open(monitor_file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            hits = data['hits']
            functions = keystoint(data['functions'])

            breakpoints = {}
            for item in hits:
                hit = BreakPointHit()
                hit.assign(item)
                if not hasattr(hit, 'startOffset'):
                    hit.startOffset = hit.offset
                breakpoints[hit.id] = hit

            functionDict = {}
            for k, v in functions.items():
                func = FunctionData()
                func.assign(v)
                func.startOffset = k  # 偏移量还是需要保存
                if not hasattr(func, 'comment'):
                    func.comment = ''
                if not hasattr(func, 'source'):
                    func.source = ''
                if not hasattr(func, 'annotations'):
                    func.annotations = {}

                # 兼容以前的文件
                if hasattr(func, 'funtionName'):
                    func.functionName = func.funtionName
                    del func.funtionName
                func.comment_delete_flag = False
                func.annotations_delete_flag = False
                functionDict[k] = func
            return breakpoints, functionDict

    def __split_line(self, line: str) -> tuple:
        """
        Extract depth, id, fname from one line in the file tree.txt
        """
        depth = 0
        for c in line:
            if c == '\t':
                depth = depth + 1
            else:
                break

        first_space_position = line.find(' ')
        idstr = line[:first_space_position].strip()
        id = int(idstr)
        fname = line[first_space_position:].strip()
        return depth, id, fname

    def get_source(self, functionData: FunctionData) -> str:
        """
        Read the source code from the document
        """
        if functionData.source:
            return functionData.source

        source = ''
        src_filename = Path(self.tempdir.name).joinpath(
            f'code/{functionData.startOffset}.cpp')
        if src_filename.exists():
            with open(src_filename.absolute(), 'r', encoding='utf-8') as f:
                source = f.read()
        else:
            source = functionData.content()  # 从源代码读入数据
        return source

    def get_annotations(self, functionData: FunctionData) -> dict:
        """
        Read the annotation from the document
        """
        if functionData.annotations:
            return functionData.annotations

        new_data = {}
        anno_filename = Path(self.tempdir.name).joinpath(
            'annotations').joinpath(f"{functionData.startOffset}.json")
        if not anno_filename.exists():
            return new_data

        with open(anno_filename, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            new_data = keystoint(data)
            functionData.annotations = new_data
        return new_data

    def get_comment(self, functionData: FunctionData) -> str:
        """
        Read the comment from the document
        """
        if functionData.comment:
            return functionData.comment

        comment = ''
        cmt_filename = Path(self.tempdir.name).joinpath(
            f"comment/{functionData.startOffset}.txt")

        if cmt_filename.exists():
            with open(cmt_filename.absolute(), 'r', encoding='utf-8') as f:
                comment = f.read()
                functionData.comment = comment
        return comment

    def fill_tree(self) -> None:
        treefname = Path(self.tempdir.name).joinpath('tree.txt')
        with open(treefname, 'r', encoding='utf-8') as f:
            data = f.readlines()
            stack = [(-1, self.rootNode)]

            for line in data:
                depth, id, fname = self.__split_line(line)
                node = StandardItem(fname)
                node.id = id
                node.offset = self.breakpoints[id].offset
                node.startOffset = self.breakpoints[id].startOffset
                node.functionData = self.functions[node.startOffset]

                cmt_filename = Path(self.tempdir.name).joinpath(
                    f"comment/{node.startOffset}.txt")
                
                ann_filename = Path(self.tempdir.name).joinpath(
                    'annotations').joinpath(f"{node.startOffset}.json")

                if cmt_filename.exists() or ann_filename.exists():
                    node.setIcon(self.comment_icon)

                preDepth, preNode = stack[-1]
                while depth <= preDepth:
                    stack.pop()
                    preDepth, preNode = stack[-1]
                preNode.appendRow(node)
                stack.append((depth, node))

    def save(self) -> None:
        src_dir = Path(self.tempdir.name).joinpath('code')
        if not src_dir.exists():
            Path(src_dir).mkdir()

        comment_dir = Path(self.tempdir.name).joinpath('comment')
        if not comment_dir.exists():
            Path(comment_dir).mkdir()

        saved_elems = set()
        lines = []
        stack = []
        stack.append((self.rootNode, -1))
        while stack:
            elem = stack[-1][0]
            depth = stack[-1][1]
            stack.pop()
            if hasattr(elem, 'functionData'):
                lines.append(
                    '\t'*depth + f"{elem.id} {elem.functionData.functionName}\n")
                if elem.functionData.startOffset not in saved_elems:
                    self.save_elem(elem)
                    saved_elems.add(elem.functionData.startOffset)

            for row in range(elem.rowCount() - 1, -1, -1):
                child = elem.child(row, 0)
                stack.append((child, depth + 1))

        with open(Path(self.tempdir.name).joinpath('tree.txt').absolute(), 'w', encoding='utf-8') as f:
            f.writelines(lines)
        zipDir(self.tempdir.name, self.filename)
        self.isDirty = False  # 文件保存后重新设置标记
        self.contentChanged.emit()

    def save_as(self, filename: str):
        self.filename = filename
        self.save()

    def save_elem(self, elem: StandardItem) -> None:
        functionData = elem.functionData

        src_filename = Path(self.tempdir.name).joinpath(
            f'code/{elem.startOffset}.cpp')

        # 保存源代码
        if functionData.source:
            with open(src_filename.absolute(), 'w', encoding='utf-8') as f:
                content = functionData.source
                f.write(content)
        else:
            if not src_filename.exists():
                with open(src_filename.absolute(), 'w', encoding='utf-8') as f:
                    content = functionData.content()
                    f.write(content)

        # 保存源代码全局注释
        comment = functionData.comment
        cmt_filename = Path(self.tempdir.name).joinpath(
            'comment').joinpath(f"{elem.startOffset}.txt")
        if comment:
            with open(cmt_filename.absolute(), 'w', encoding='utf-8') as f:
                f.write(comment)
        elif functionData.comment_delete_flag and cmt_filename.exists():
            cmt_filename.unlink()

        # 保存源代码行注释
        annotations = functionData.annotations
        anno_filename = Path(self.tempdir.name).joinpath(
            'annotations').joinpath(f"{elem.startOffset}.json")
        if annotations:
            if not anno_filename.parent.exists():
                os.makedirs(anno_filename.parent.absolute())
            with open(anno_filename.absolute(), 'w+', encoding='utf-8') as f:
                json.dump(annotations, f, indent=4)
        elif functionData.annotations_delete_flag and anno_filename.exists():
            anno_filename.unlink()

    @pyqtSlot(str)
    def on_comment_changed(self, comment: str):
        if not hasattr(self.curItem, 'functionData'):
            return

        if not self.curItem.functionData:
            return

        if self.curItem.functionData.comment != comment:
            self.curItem.functionData.comment = comment
            if not comment:
                self.curItem.functionData.comment_delete_flag = True
            self.commentChanged.emit(comment)
            self.isDirty = True
            self.contentChanged.emit()

    @pyqtSlot(str)
    def on_source_changed(self, source: str):
        if not hasattr(self.curItem, 'functionData'):
            return

        if not self.curItem.functionData:
            return

        self.curItem.functionData.source = source
        self.isDirty = True
        self.contentChanged.emit()

    @pyqtSlot()
    def on_callstack_changed(self):
        if not hasattr(self.curItem, 'functionData'):
            return

        if not self.curItem.functionData:
            return

        self.isDirty = True
        self.contentChanged.emit()

    @pyqtSlot(int, str)
    def on_annotation_changed(self, line: int, comment: str):
        if not hasattr(self.curItem, 'functionData'):
            return

        if not self.curItem.functionData:
            return

        annotations = self.curItem.functionData.annotations

        if not comment:
            if line in annotations:
                del annotations[line]
                self.isDirty = True
                if not annotations:
                    self.curItem.functionData.annotations_delete_flag = True
        elif line in annotations and annotations[line] == comment:
            pass
        else:
            annotations[line] = comment
            self.isDirty = True

        self.annotationChanged.emit(line, comment)

        if self.isDirty:
            self.contentChanged.emit()

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_selection_changed(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        " Slot is called when the selection has been changed "
        if not selected.indexes():
            return

        selectedIndex = selected.indexes()[0]
        self.curItem = selectedIndex.model().itemFromIndex(selectedIndex)
        self.curItemChanged.emit(self.curItem)

    def get_cur_item(self) -> StandardItem:
        return self.curItem
