import os
import sys
from maya import OpenMayaUI
import maya.OpenMayaUI as apiUI
import maya
from PySide2 import QtGui, QtWidgets, QtCore
from utils.api_caller import get_asset_type
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from functools import partial
from shiboken2 import wrapInstance


def get_main_window_ptr():
    maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(long(maya_main_window_ptr), QtWidgets.QWidget)
    return maya_main_window


class OnlineAssetsManager(QtWidgets.QWidget):
    # ua = Upload Asset
    # as = All Assets
    def __init__(self, parent=get_main_window_ptr()):
        super(OnlineAssetsManager, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.roots = list()

        self.loading_layout = QtWidgets.QVBoxLayout()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_tab_widget = QtWidgets.QTabWidget()
        self.ai_tab = QtWidgets.QWidget()
        self.ai_tab_layout = QtWidgets.QVBoxLayout()
        self.ca_tab = QtWidgets.QWidget()
        self.ca_tab_layout = QtWidgets.QVBoxLayout()
        self.aa_tab = QtWidgets.QWidget()
        self.aa_tab_layout = QtWidgets.QVBoxLayout()
        self.ua_tab = QtWidgets.QWidget()
        self.ua_tab_layout = QtWidgets.QVBoxLayout()

        self.ai_no_asset_lb = QtWidgets.QLabel("No asset has been found in the scene, "
                                               "create a new OAM asset to view asset's info.")
        self.ai_compile_asset_pb = QtWidgets.QPushButton("Go to Compile Asset")
        self.aa_main_asset_selection_cb = QtWidgets.QComboBox()
        self.init_widgets()
        self.setMinimumSize(500, 0)
        self.selection_changed_event = OpenMaya.MEventMessage.addEventCallback("SelectionChanged",
                                                                               self.update_asset_info)
        get_asset_type()
        self.update_asset_info()
        self.show()

    def init_widgets(self):
        self.setWindowTitle('Online Assets Manager')
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.main_tab_widget)
        self.ua_tab.setLayout(self.ua_tab_layout)
        self.init_asset_info()
        self.init_compile_asset()
        self.init_all_assets()

        self.main_tab_widget.addTab(self.ai_tab, "Asset's Info")
        self.main_tab_widget.addTab(self.ca_tab, "Compile Asset")
        self.main_tab_widget.addTab(self.aa_tab, "All Assets")
        self.main_tab_widget.addTab(self.ua_tab, "Upload Asset")

    def set_state(self, state):
        if state:
            self.setLayout(self.main_layout)
        else:
            self.setLayout(self.loading_layout)

    def init_asset_info(self):
        self.ai_compile_asset_pb.clicked.connect(self.enter_compile_asset)

        self.ai_tab_layout.addWidget(self.ai_no_asset_lb)
        self.ai_tab_layout.addWidget(self.ai_compile_asset_pb)
        self.ai_tab.setLayout(self.ai_tab_layout)

    def init_compile_asset(self):
        self.ca_tab.setLayout(self.ca_tab_layout)

    def init_all_assets(self):
        asset_type = ["All", "Model", "Animation", "VFX", "Sound"]
        self.aa_main_asset_selection_cb.addItems(asset_type)
        asset_selection_layout = QtWidgets.QHBoxLayout()
        asset_selection_layout.addWidget(QtWidgets.QLabel("Asset Type :"))
        asset_selection_layout.addWidget(self.aa_main_asset_selection_cb)
        self.aa_tab_layout.addLayout(asset_selection_layout)
        self.aa_tab.setLayout(self.aa_tab_layout)

    def enter_compile_asset(self):
        self.main_tab_widget.setCurrentWidget(self.ca_tab)

    def check_roots(self):
        roots = list()
        for eachObj in cmds.ls(sl=True):
            attr = cmds.listAttr(eachObj, l=True)
            if attr is not None:
                if "oam_type" in cmds.listAttr(eachObj, l=True):
                    roots.append(eachObj)
        self.roots = roots

    def update_asset_info(self, *args):
        self.check_roots()
        if len(self.roots) == 0:
            self.ai_no_asset_lb.setVisible(True)
            self.ai_compile_asset_pb.setVisible(True)
        else:
            self.ai_no_asset_lb.setVisible(False)
            self.ai_compile_asset_pb.setVisible(False)

    def closeEvent(self, event):
        OpenMaya.MMessage.removeCallback(self.selection_changed_event)
