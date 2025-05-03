import os
import sys
import getpass
import json
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

import importlib
from core.create_folder_structure import CreateNewAsset
importlib.reload(sys.modules['core.create_folder_structure'])


def maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


def load_config():
    config_path = "/home/satyajit.p/Desktop/asset_maneger/asset_manager_tool/configs/config.json"
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            
            # Check if 'project_name' exists in the config
            if "project_name" not in config:
                raise ValueError("'project_name' is missing from the config file.")
            
            return config
    except Exception as e:
        print(f"Failed to load config: {e}")
        raise  # Re-raise the error to stop further execution if the config is invalid


class AssetManagerUI(QtWidgets.QDialog):
    def __init__(self, config, parent=maya_main_window()):
        super(AssetManagerUI, self).__init__(parent)
        self.config = config
        self.setWindowTitle("Asset Manager")
        self.setMinimumSize(800, 450)

        self.init_styles()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.update_create_asset_button_visibility()

    def init_styles(self):
        font = "Segoe UI"
        self.LABEL_STYLE = f"font: bold 10pt '{font}'; color: #E0E0E0;"
        self.LIST_STYLE = f"""
            QListWidget {{
                background-color: #3b3b3b; border: 1px solid #666;
                color: #E0E0E0; font: 9pt '{font}';
            }}
            QListWidget::item:selected {{
                background-color: #5DADE2; color: black;
            }}
            QListWidget::item:hover {{
                background-color: #4A90E2; color: white;
            }}
        """
        self.BUTTON_STYLE = f"""
            QPushButton {{
                background-color: #4A90E2; color: white;
                border-radius: 6px; padding: 8px 20px; font: 10pt '{font}';
            }}
            QPushButton:hover {{
                background-color: #357ABD;
            }}
        """

    def create_widgets(self):
        project_name = self.config.get("project_name", "Unknown Project")
        self.project_label = QtWidgets.QLabel(f"Project: {project_name}")
        self.project_label.setStyleSheet(self.LABEL_STYLE)

        self.asset_name_label = QtWidgets.QLabel("Asset: N/A")
        self.asset_name_label.setStyleSheet(self.LABEL_STYLE)

        user = getpass.getuser()
        self.user_name_label = QtWidgets.QLabel(f"User: {user}")
        self.user_name_label.setStyleSheet(self.LABEL_STYLE)

        self.dep_label = QtWidgets.QLabel("Department:")
        self.dep_label.setStyleSheet(self.LABEL_STYLE)
        self.dep_combo = QtWidgets.QComboBox()
        self.dep_combo.addItems(["Modeling", "Rigging"])
        self.dep_combo.setStyleSheet("font: 9pt 'Segoe UI';")

        self.type_label = QtWidgets.QLabel("Asset Type:")
        self.type_label.setStyleSheet(self.LABEL_STYLE)
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Prop", "Character", "Environment"])
        self.type_combo.setStyleSheet("font: 9pt 'Segoe UI';")

        self.assets_list = QtWidgets.QListWidget()
        self.assets_list.setStyleSheet(self.LIST_STYLE)

        self.versions_list = QtWidgets.QListWidget()
        self.versions_list.setStyleSheet(self.LIST_STYLE)

        self.info_image = QtWidgets.QLabel("Preview")
        self.info_image.setFixedSize(180, 100)
        self.info_image.setStyleSheet("background-color: #555; color: #ccc;")
        self.info_image.setAlignment(QtCore.Qt.AlignCenter)

        self.info_name     = QtWidgets.QLabel("-");     self.info_name.setStyleSheet(self.LABEL_STYLE)
        self.info_version  = QtWidgets.QLabel("-");     self.info_version.setStyleSheet(self.LABEL_STYLE)
        self.info_artist   = QtWidgets.QLabel("-");     self.info_artist.setStyleSheet(self.LABEL_STYLE)
        self.info_modified = QtWidgets.QLabel("-");     self.info_modified.setStyleSheet(self.LABEL_STYLE)
        self.info_notes    = QtWidgets.QLabel("-");     self.info_notes.setStyleSheet(self.LABEL_STYLE)

        self.publish_checkbox = QtWidgets.QCheckBox("Publish")
        self.publish_checkbox.setStyleSheet("font: 9pt 'Segoe UI';")

        self.comment_box = QtWidgets.QTextEdit()
        self.comment_box.setPlaceholderText("Enter publish comments...")
        self.comment_box.setStyleSheet("font: 9pt 'Segoe UI';")
        self.comment_box.setVisible(False)

        self.publish_btn = QtWidgets.QPushButton("Publish Asset")
        self.publish_btn.setStyleSheet(self.BUTTON_STYLE)
        self.publish_btn.setVisible(False)

        self.create_asset_btn = QtWidgets.QPushButton("Create New Asset")
        self.create_asset_btn.setStyleSheet(self.BUTTON_STYLE)
        self.create_asset_btn.setVisible(False)

        self.separator = QtWidgets.QFrame()
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator.setStyleSheet("color: #555;")

    def create_layouts(self):
        self.header = QtWidgets.QHBoxLayout()
        self.header.addWidget(self.project_label)
        self.header.addStretch(1)
        self.header.addWidget(self.asset_name_label)
        self.header.addStretch(1)
        self.header.addWidget(self.user_name_label)
        self.header.setContentsMargins(10, 10, 10, 0)

        self.filt = QtWidgets.QHBoxLayout()
        self.filt.setSpacing(20)
        self.dep_layout = QtWidgets.QHBoxLayout()
        self.dep_layout.setSpacing(4)
        self.dep_layout.addWidget(self.dep_label)
        self.dep_layout.addWidget(self.dep_combo)
        self.type_layout = QtWidgets.QHBoxLayout()
        self.type_layout.setSpacing(4)
        self.type_layout.addWidget(self.type_label)
        self.type_layout.addWidget(self.type_combo)
        self.filt.addLayout(self.dep_layout)
        self.filt.addLayout(self.type_layout)
        self.filt.addStretch()
        self.filt.setContentsMargins(10, 0, 10, 0)

        self.lists_group = QtWidgets.QHBoxLayout()
        self.lists_group.addWidget(self.assets_list, 1)
        self.lists_group.addWidget(self.versions_list, 1)

        self.info = QtWidgets.QVBoxLayout()
        self.info.addWidget(self.info_image, alignment=QtCore.Qt.AlignCenter)
        self.form = QtWidgets.QFormLayout()
        self.form.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form.setFormAlignment(QtCore.Qt.AlignLeft)
        self.form.addRow("Name:",     self.info_name)
        self.form.addRow("Version:",  self.info_version)
        self.form.addRow("Artist:",   self.info_artist)
        self.form.addRow("Modified:", self.info_modified)
        self.form.addRow("Notes:",    self.info_notes)
        self.info.addLayout(self.form)
        self.info.addStretch()

        self.mid = QtWidgets.QHBoxLayout()
        self.mid.setSpacing(20)
        self.mid.setContentsMargins(10, 0, 10, 0)
        self.mid.addLayout(self.lists_group, 2)
        self.mid.addLayout(self.info, 1)

        self.mid_widget = QtWidgets.QWidget()
        self.mid_widget.setLayout(self.mid)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.create_asset_btn)
        self.buttons_layout.addWidget(self.publish_btn)
        self.buttons_layout.setSpacing(10)

        self.buttons = QtWidgets.QVBoxLayout()
        self.buttons.addWidget(self.comment_box)
        self.buttons.addSpacing(10)
        self.buttons.addLayout(self.buttons_layout)
        self.buttons.setSpacing(10)
        self.buttons.setContentsMargins(10, 0, 10, 10)

        self.main = QtWidgets.QVBoxLayout(self)
        self.main.addLayout(self.header)
        self.main.addSpacing(6)
        self.main.addLayout(self.filt)
        self.main.addWidget(self.separator)
        self.main.addWidget(self.publish_checkbox, alignment=QtCore.Qt.AlignLeft)
        self.main.setSpacing(20)
        self.main.addWidget(self.mid_widget)
        self.main.addLayout(self.buttons)

        self.setLayout(self.main)

    def create_connections(self):
        self.publish_checkbox.toggled.connect(self.toggle_publish_button)
        self.create_asset_btn.clicked.connect(self.create_new_asset)
        self.dep_combo.currentTextChanged.connect(self.update_create_asset_button_visibility)
        self.publish_btn.clicked.connect(self.check_comment_and_publish)

    def toggle_publish_button(self):
        is_checked = self.publish_checkbox.isChecked()
        self.publish_btn.setVisible(is_checked)
        self.comment_box.setVisible(is_checked)
        self.update_create_asset_button_visibility()
        self.mid_widget.setVisible(not is_checked)

    def update_create_asset_button_visibility(self):
        is_modeling = self.dep_combo.currentText() == "Modeling"
        is_publish_checked = self.publish_checkbox.isChecked()
        self.create_asset_btn.setVisible(is_publish_checked and is_modeling)

    

    def create_new_asset(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "New Asset", "Enter the name of the asset:")
        if ok and text:
            QtWidgets.QMessageBox.information(self, "Asset Created", f"New asset '{text}' has been created.")
        elif not text:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Asset name cannot be empty.")
            return

        asset_creator = CreateNewAsset()
        department_list, asset_type = self.get_ui_info_values()

        # Retrieve base path and project name from the config
        base_path = self.config.get("base_path", "/home/satyajit.p/Desktop/proj")  # Default if not found
        project_name = self.config.get("project_name", "Unknown Project")  # Default if not found

        # Construct the full path
        full_path = os.path.join(base_path, project_name, "asset")

        # Ensure the asset is created under the correct project folder and department
        for department in department_list:
            # Now create the asset under each department
            asset_creator.create_new_asset(full_path, department, asset_type, text)




    def check_comment_and_publish(self):
        comment = self.comment_box.toPlainText().strip()
        if not comment:
            QtWidgets.QMessageBox.warning(self, "Error", "Publish comment cannot be empty.")
        else:
            print(f"Publish comment: {comment}")

    def get_ui_info_values(self):
        # Get the asset type (the selected item in the asset type combo box)
        asset_type = self.type_combo.currentText()

        # Get all department names (items in the department combo box)
        department_list = [self.dep_combo.itemText(i) for i in range(self.dep_combo.count())]

        return department_list, asset_type



def show_asset_manager_ui():
    global asset_manager_dialog
    config = load_config()  # ✅ load config
    try:
        asset_manager_dialog.close()
        asset_manager_dialog.deleteLater()
    except Exception as e:
        print(f"Previous dialog close failed: {e}")
    asset_manager_dialog = AssetManagerUI(config)
    asset_manager_dialog.show()

# show_asset_manager_ui()  # Uncomment to launch
