# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spatial_interaction_models_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SpatialInteractionModelsDialogBase(object):
    def setupUi(self, SpatialInteractionModelsDialogBase):
        SpatialInteractionModelsDialogBase.setObjectName("SpatialInteractionModelsDialogBase")
        SpatialInteractionModelsDialogBase.resize(624, 583)
        SpatialInteractionModelsDialogBase.setMinimumSize(QtCore.QSize(624, 583))
        SpatialInteractionModelsDialogBase.setMaximumSize(QtCore.QSize(624, 583))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/spatial_interaction_models/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SpatialInteractionModelsDialogBase.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(SpatialInteractionModelsDialogBase)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(SpatialInteractionModelsDialogBase)
        self.tabWidget.setObjectName("tabWidget")
        self.inputs = QtWidgets.QWidget()
        self.inputs.setObjectName("inputs")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.inputs)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_ayuda1 = QtWidgets.QPushButton(self.inputs)
        self.btn_ayuda1.setMinimumSize(QtCore.QSize(44, 27))
        self.btn_ayuda1.setMaximumSize(QtCore.QSize(44, 27))
        self.btn_ayuda1.setStyleSheet("")
        self.btn_ayuda1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/plugins/spatial_interaction_models/question_sq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_ayuda1.setIcon(icon1)
        self.btn_ayuda1.setIconSize(QtCore.QSize(27, 27))
        self.btn_ayuda1.setObjectName("btn_ayuda1")
        self.gridLayout_2.addWidget(self.btn_ayuda1, 0, 1, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.inputs)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_3 = QtWidgets.QLabel(self.groupBox_5)
        self.label_3.setObjectName("label_3")
        self.gridLayout_12.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_5)
        self.label_4.setObjectName("label_4")
        self.gridLayout_12.addWidget(self.label_4, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_5)
        self.label.setObjectName("label")
        self.gridLayout_12.addWidget(self.label, 0, 0, 1, 1)
        self.id_origin_combobox = gui.QgsFieldComboBox(self.groupBox_5)
        self.id_origin_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.id_origin_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.id_origin_combobox.setObjectName("id_origin_combobox")
        self.gridLayout_12.addWidget(self.id_origin_combobox, 3, 0, 1, 1)
        self.origin_combobox = gui.QgsMapLayerComboBox(self.groupBox_5)
        self.origin_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.origin_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.origin_combobox.setObjectName("origin_combobox")
        self.gridLayout_12.addWidget(self.origin_combobox, 1, 0, 1, 1)
        self.field_origin_combobox = gui.QgsFieldComboBox(self.groupBox_5)
        self.field_origin_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.field_origin_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.field_origin_combobox.setObjectName("field_origin_combobox")
        self.gridLayout_12.addWidget(self.field_origin_combobox, 5, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_5, 12, 0, 1, 2)
        self.widget = QtWidgets.QWidget(self.inputs)
        self.widget.setObjectName("widget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem, 0, 1, 1, 1)
        self.btn_sig1 = QtWidgets.QPushButton(self.widget)
        self.btn_sig1.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_sig1.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_sig1.setObjectName("btn_sig1")
        self.gridLayout_9.addWidget(self.btn_sig1, 0, 2, 1, 1)
        self.btn_about = QtWidgets.QPushButton(self.widget)
        self.btn_about.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_about.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_about.setObjectName("btn_about")
        self.gridLayout_9.addWidget(self.btn_about, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 16, 0, 1, 2)
        self.groupBox_6 = QtWidgets.QGroupBox(self.inputs)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.dest_combobox = gui.QgsMapLayerComboBox(self.groupBox_6)
        self.dest_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.dest_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.dest_combobox.setObjectName("dest_combobox")
        self.gridLayout_13.addWidget(self.dest_combobox, 1, 0, 1, 1)
        self.id_dest_combobox = gui.QgsFieldComboBox(self.groupBox_6)
        self.id_dest_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.id_dest_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.id_dest_combobox.setObjectName("id_dest_combobox")
        self.gridLayout_13.addWidget(self.id_dest_combobox, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_6)
        self.label_2.setObjectName("label_2")
        self.gridLayout_13.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_6)
        self.label_5.setObjectName("label_5")
        self.gridLayout_13.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_6)
        self.label_6.setObjectName("label_6")
        self.gridLayout_13.addWidget(self.label_6, 4, 0, 1, 1)
        self.field_dest_combobox = gui.QgsFieldComboBox(self.groupBox_6)
        self.field_dest_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.field_dest_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.field_dest_combobox.setObjectName("field_dest_combobox")
        self.gridLayout_13.addWidget(self.field_dest_combobox, 5, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_6, 13, 0, 2, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 15, 0, 1, 1)
        self.tabWidget.addTab(self.inputs, "")
        self.restrictions = QtWidgets.QWidget()
        self.restrictions.setObjectName("restrictions")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.restrictions)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.filt_combobox = QtWidgets.QComboBox(self.restrictions)
        self.filt_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.filt_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.filt_combobox.setObjectName("filt_combobox")
        self.filt_combobox.addItem("")
        self.filt_combobox.addItem("")
        self.filt_combobox.addItem("")
        self.filt_combobox.addItem("")
        self.gridLayout_3.addWidget(self.filt_combobox, 1, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(self.restrictions)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.val1_dist = QtWidgets.QLineEdit(self.groupBox)
        self.val1_dist.setMinimumSize(QtCore.QSize(0, 27))
        self.val1_dist.setMaximumSize(QtCore.QSize(16777215, 27))
        self.val1_dist.setDragEnabled(False)
        self.val1_dist.setReadOnly(True)
        self.val1_dist.setClearButtonEnabled(False)
        self.val1_dist.setObjectName("val1_dist")
        self.gridLayout_4.addWidget(self.val1_dist, 1, 0, 1, 1)
        self.tipo_filt_dist = QtWidgets.QComboBox(self.groupBox)
        self.tipo_filt_dist.setEnabled(False)
        self.tipo_filt_dist.setMinimumSize(QtCore.QSize(0, 27))
        self.tipo_filt_dist.setMaximumSize(QtCore.QSize(16777215, 27))
        self.tipo_filt_dist.setObjectName("tipo_filt_dist")
        self.tipo_filt_dist.addItem("")
        self.tipo_filt_dist.addItem("")
        self.tipo_filt_dist.addItem("")
        self.tipo_filt_dist.addItem("")
        self.gridLayout_4.addWidget(self.tipo_filt_dist, 0, 0, 1, 2)
        self.val2_dist = QtWidgets.QLineEdit(self.groupBox)
        self.val2_dist.setEnabled(True)
        self.val2_dist.setMinimumSize(QtCore.QSize(0, 27))
        self.val2_dist.setMaximumSize(QtCore.QSize(16777215, 27))
        self.val2_dist.setReadOnly(True)
        self.val2_dist.setObjectName("val2_dist")
        self.gridLayout_4.addWidget(self.val2_dist, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 6, 0, 1, 2)
        self.mesuare_combobox = QtWidgets.QComboBox(self.restrictions)
        self.mesuare_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.mesuare_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.mesuare_combobox.setObjectName("mesuare_combobox")
        self.mesuare_combobox.addItem("")
        self.mesuare_combobox.addItem("")
        self.mesuare_combobox.addItem("")
        self.mesuare_combobox.addItem("")
        self.mesuare_combobox.addItem("")
        self.mesuare_combobox.addItem("")
        self.gridLayout_3.addWidget(self.mesuare_combobox, 3, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.restrictions)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 8, 0, 1, 1)
        self.btn_ayuda2 = QtWidgets.QPushButton(self.restrictions)
        self.btn_ayuda2.setMinimumSize(QtCore.QSize(44, 27))
        self.btn_ayuda2.setMaximumSize(QtCore.QSize(44, 27))
        self.btn_ayuda2.setText("")
        self.btn_ayuda2.setIcon(icon1)
        self.btn_ayuda2.setIconSize(QtCore.QSize(27, 27))
        self.btn_ayuda2.setObjectName("btn_ayuda2")
        self.gridLayout_3.addWidget(self.btn_ayuda2, 0, 1, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.restrictions)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.btn_sig2 = QtWidgets.QPushButton(self.widget_2)
        self.btn_sig2.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_sig2.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_sig2.setObjectName("btn_sig2")
        self.gridLayout_10.addWidget(self.btn_sig2, 0, 3, 1, 1)
        self.btn_reg2 = QtWidgets.QPushButton(self.widget_2)
        self.btn_reg2.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_reg2.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_reg2.setObjectName("btn_reg2")
        self.gridLayout_10.addWidget(self.btn_reg2, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem3, 0, 1, 1, 1)
        self.btn_about2 = QtWidgets.QPushButton(self.widget_2)
        self.btn_about2.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_about2.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_about2.setObjectName("btn_about2")
        self.gridLayout_10.addWidget(self.btn_about2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.widget_2, 9, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.restrictions)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.val2_fluj = QtWidgets.QLineEdit(self.groupBox_2)
        self.val2_fluj.setMinimumSize(QtCore.QSize(0, 27))
        self.val2_fluj.setMaximumSize(QtCore.QSize(16777215, 27))
        self.val2_fluj.setReadOnly(True)
        self.val2_fluj.setObjectName("val2_fluj")
        self.gridLayout_5.addWidget(self.val2_fluj, 1, 1, 1, 1)
        self.val1_fluj = QtWidgets.QLineEdit(self.groupBox_2)
        self.val1_fluj.setMinimumSize(QtCore.QSize(0, 27))
        self.val1_fluj.setMaximumSize(QtCore.QSize(16777215, 27))
        self.val1_fluj.setReadOnly(True)
        self.val1_fluj.setObjectName("val1_fluj")
        self.gridLayout_5.addWidget(self.val1_fluj, 1, 0, 1, 1)
        self.tipo_filt_fluj = QtWidgets.QComboBox(self.groupBox_2)
        self.tipo_filt_fluj.setEnabled(False)
        self.tipo_filt_fluj.setMinimumSize(QtCore.QSize(0, 27))
        self.tipo_filt_fluj.setMaximumSize(QtCore.QSize(16777215, 27))
        self.tipo_filt_fluj.setObjectName("tipo_filt_fluj")
        self.tipo_filt_fluj.addItem("")
        self.tipo_filt_fluj.addItem("")
        self.tipo_filt_fluj.addItem("")
        self.tipo_filt_fluj.addItem("")
        self.gridLayout_5.addWidget(self.tipo_filt_fluj, 0, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_2, 7, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.restrictions)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 4, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.restrictions)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)
        self.friction_distance = QtWidgets.QLineEdit(self.restrictions)
        self.friction_distance.setObjectName("friction_distance")
        self.gridLayout_3.addWidget(self.friction_distance, 5, 0, 1, 2)
        self.tabWidget.addTab(self.restrictions, "")
        self.outputs = QtWidgets.QWidget()
        self.outputs.setObjectName("outputs")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.outputs)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.prefijo = QtWidgets.QLineEdit(self.outputs)
        self.prefijo.setObjectName("prefijo")
        self.gridLayout_6.addWidget(self.prefijo, 5, 0, 1, 2)
        self.widget_3 = QtWidgets.QWidget(self.outputs)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_11.setObjectName("gridLayout_11")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem4, 0, 1, 1, 1)
        self.btn_reg3 = QtWidgets.QPushButton(self.widget_3)
        self.btn_reg3.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_reg3.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_reg3.setObjectName("btn_reg3")
        self.gridLayout_11.addWidget(self.btn_reg3, 0, 2, 1, 1)
        self.btn_aceptar = QtWidgets.QPushButton(self.widget_3)
        self.btn_aceptar.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_aceptar.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_aceptar.setObjectName("btn_aceptar")
        self.gridLayout_11.addWidget(self.btn_aceptar, 0, 3, 1, 1)
        self.btn_about3 = QtWidgets.QPushButton(self.widget_3)
        self.btn_about3.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_about3.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_about3.setObjectName("btn_about3")
        self.gridLayout_11.addWidget(self.btn_about3, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.widget_3, 8, 0, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.outputs)
        self.label_10.setObjectName("label_10")
        self.gridLayout_6.addWidget(self.label_10, 4, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.outputs)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.geojson_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.geojson_check.setObjectName("geojson_check")
        self.gridLayout_7.addWidget(self.geojson_check, 2, 0, 1, 1)
        self.geopackage_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.geopackage_check_load.setEnabled(True)
        self.geopackage_check_load.setObjectName("geopackage_check_load")
        self.gridLayout_7.addWidget(self.geopackage_check_load, 3, 1, 1, 1)
        self.sqlite_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.sqlite_check.setObjectName("sqlite_check")
        self.gridLayout_7.addWidget(self.sqlite_check, 1, 0, 1, 1)
        self.hd_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.hd_check.setObjectName("hd_check")
        self.gridLayout_7.addWidget(self.hd_check, 4, 0, 1, 1)
        self.memory_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.memory_check.setChecked(True)
        self.memory_check.setObjectName("memory_check")
        self.gridLayout_7.addWidget(self.memory_check, 0, 0, 1, 1)
        self.sqlite_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.sqlite_check_load.setEnabled(True)
        self.sqlite_check_load.setTristate(False)
        self.sqlite_check_load.setObjectName("sqlite_check_load")
        self.gridLayout_7.addWidget(self.sqlite_check_load, 1, 1, 1, 1)
        self.geojson_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.geojson_check_load.setEnabled(True)
        self.geojson_check_load.setObjectName("geojson_check_load")
        self.gridLayout_7.addWidget(self.geojson_check_load, 2, 1, 1, 1)
        self.geopackage_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.geopackage_check.setObjectName("geopackage_check")
        self.gridLayout_7.addWidget(self.geopackage_check, 3, 0, 1, 1)
        self.hd_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.hd_check_load.setEnabled(True)
        self.hd_check_load.setObjectName("hd_check_load")
        self.gridLayout_7.addWidget(self.hd_check_load, 4, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_3, 1, 0, 1, 2)
        self.label_12 = QtWidgets.QLabel(self.outputs)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.gridLayout_6.addWidget(self.label_12, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.outputs)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.xls_check = QtWidgets.QCheckBox(self.groupBox_4)
        self.xls_check.setObjectName("xls_check")
        self.gridLayout_8.addWidget(self.xls_check, 0, 0, 1, 1)
        self.ods_check = QtWidgets.QCheckBox(self.groupBox_4)
        self.ods_check.setObjectName("ods_check")
        self.gridLayout_8.addWidget(self.ods_check, 1, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_4, 3, 0, 1, 2)
        self.btn_ayuda3 = QtWidgets.QPushButton(self.outputs)
        self.btn_ayuda3.setEnabled(True)
        self.btn_ayuda3.setMinimumSize(QtCore.QSize(44, 27))
        self.btn_ayuda3.setMaximumSize(QtCore.QSize(44, 27))
        self.btn_ayuda3.setText("")
        self.btn_ayuda3.setIcon(icon1)
        self.btn_ayuda3.setIconSize(QtCore.QSize(27, 27))
        self.btn_ayuda3.setObjectName("btn_ayuda3")
        self.gridLayout_6.addWidget(self.btn_ayuda3, 0, 1, 1, 1)
        self.groupBox_7 = QtWidgets.QGroupBox(self.outputs)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.output = QtWidgets.QLineEdit(self.groupBox_7)
        self.output.setMinimumSize(QtCore.QSize(0, 27))
        self.output.setMaximumSize(QtCore.QSize(16777215, 27))
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.gridLayout_14.addWidget(self.output, 4, 0, 1, 1)
        self.btn_output = QtWidgets.QPushButton(self.groupBox_7)
        self.btn_output.setMinimumSize(QtCore.QSize(44, 27))
        self.btn_output.setMaximumSize(QtCore.QSize(44, 27))
        self.btn_output.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/plugins/spatial_interaction_models/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_output.setIcon(icon2)
        self.btn_output.setIconSize(QtCore.QSize(27, 27))
        self.btn_output.setObjectName("btn_output")
        self.gridLayout_14.addWidget(self.btn_output, 4, 1, 1, 1)
        self.widget_4 = QtWidgets.QWidget(self.groupBox_7)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.projects_combobox = QtWidgets.QComboBox(self.widget_4)
        self.projects_combobox.setObjectName("projects_combobox")
        self.gridLayout_15.addWidget(self.projects_combobox, 0, 1, 1, 1)
        self.check_projects = QtWidgets.QCheckBox(self.widget_4)
        self.check_projects.setObjectName("check_projects")
        self.gridLayout_15.addWidget(self.check_projects, 0, 0, 1, 1)
        self.gridLayout_14.addWidget(self.widget_4, 0, 0, 1, 2)
        self.gridLayout_6.addWidget(self.groupBox_7, 6, 0, 1, 2)
        self.tabWidget.addTab(self.outputs, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        self.retranslateUi(SpatialInteractionModelsDialogBase)
        self.tabWidget.setCurrentIndex(0)
        self.origin_combobox.layerChanged['QgsMapLayer*'].connect(self.id_origin_combobox.setLayer) # type: ignore
        self.origin_combobox.layerChanged['QgsMapLayer*'].connect(self.field_origin_combobox.setLayer) # type: ignore
        self.dest_combobox.layerChanged['QgsMapLayer*'].connect(self.id_dest_combobox.setLayer) # type: ignore
        self.dest_combobox.layerChanged['QgsMapLayer*'].connect(self.field_dest_combobox.setLayer) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SpatialInteractionModelsDialogBase)

    def retranslateUi(self, SpatialInteractionModelsDialogBase):
        _translate = QtCore.QCoreApplication.translate
        SpatialInteractionModelsDialogBase.setWindowTitle(_translate("SpatialInteractionModelsDialogBase", "Modelos de Interacción Espacial"))
        self.groupBox_5.setTitle(_translate("SpatialInteractionModelsDialogBase", "Orígenes"))
        self.label_3.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo ID"))
        self.label_4.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo que contiene la población de demanda"))
        self.label.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona una capa vectorial"))
        self.btn_sig1.setText(_translate("SpatialInteractionModelsDialogBase", "Siguiente"))
        self.btn_about.setText(_translate("SpatialInteractionModelsDialogBase", "Acerca de..."))
        self.groupBox_6.setTitle(_translate("SpatialInteractionModelsDialogBase", "Destinos"))
        self.label_2.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona una capa vectorial"))
        self.label_5.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo ID"))
        self.label_6.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo que contiene la cantidad de oferta disponible"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inputs), _translate("SpatialInteractionModelsDialogBase", "Entradas"))
        self.filt_combobox.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Elige una opción..."))
        self.filt_combobox.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Restricción en el origen"))
        self.filt_combobox.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Restricción en el destino"))
        self.filt_combobox.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Doblemente restrictivos"))
        self.groupBox.setTitle(_translate("SpatialInteractionModelsDialogBase", "Filtro de Distancias/Costos"))
        self.val1_dist.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Primer valor"))
        self.tipo_filt_dist.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Selecciona un tipo de filtro..."))
        self.tipo_filt_dist.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Mayor que..."))
        self.tipo_filt_dist.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Menor que..."))
        self.tipo_filt_dist.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Rango de valores"))
        self.val2_dist.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Segundo valor"))
        self.mesuare_combobox.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Elige una opción..."))
        self.mesuare_combobox.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Metros"))
        self.mesuare_combobox.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Kilómetros"))
        self.mesuare_combobox.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Millas"))
        self.mesuare_combobox.setItemText(4, _translate("SpatialInteractionModelsDialogBase", "Pies"))
        self.mesuare_combobox.setItemText(5, _translate("SpatialInteractionModelsDialogBase", "Yardas"))
        self.label_7.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el tipo de restricción"))
        self.btn_sig2.setText(_translate("SpatialInteractionModelsDialogBase", "Siguiente"))
        self.btn_reg2.setText(_translate("SpatialInteractionModelsDialogBase", "Regresar"))
        self.btn_about2.setText(_translate("SpatialInteractionModelsDialogBase", "Acerca de..."))
        self.groupBox_2.setTitle(_translate("SpatialInteractionModelsDialogBase", "Filtro de Flujos"))
        self.val2_fluj.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Segundo valor"))
        self.val1_fluj.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Primer valor"))
        self.tipo_filt_fluj.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Selecciona un tipo de filtro..."))
        self.tipo_filt_fluj.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Mayor que..."))
        self.tipo_filt_fluj.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Menor que..."))
        self.tipo_filt_fluj.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Rango de valores"))
        self.label_9.setText(_translate("SpatialInteractionModelsDialogBase", "Introduce el valor para la fricción de la distancia"))
        self.label_8.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona las unidades de medida para la matriz de distancias"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.restrictions), _translate("SpatialInteractionModelsDialogBase", "Restricción"))
        self.prefijo.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Ejemplo: Ejec1"))
        self.btn_reg3.setText(_translate("SpatialInteractionModelsDialogBase", "Regresar"))
        self.btn_aceptar.setText(_translate("SpatialInteractionModelsDialogBase", "Aceptar"))
        self.btn_about3.setText(_translate("SpatialInteractionModelsDialogBase", "Acerca de..."))
        self.label_10.setText(_translate("SpatialInteractionModelsDialogBase", "Introduce un prefijo para cada ejecución"))
        self.groupBox_3.setTitle(_translate("SpatialInteractionModelsDialogBase", "Formatos de Salida"))
        self.geojson_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en GeoJSON"))
        self.geopackage_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.sqlite_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en SQLite"))
        self.hd_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en Shapefile"))
        self.memory_check.setText(_translate("SpatialInteractionModelsDialogBase", "Conservar capas temporales"))
        self.sqlite_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.geojson_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.geopackage_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en Geopackage"))
        self.hd_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.groupBox_4.setTitle(_translate("SpatialInteractionModelsDialogBase", "Estadísticas"))
        self.xls_check.setText(_translate("SpatialInteractionModelsDialogBase", "Generar XLS"))
        self.ods_check.setText(_translate("SpatialInteractionModelsDialogBase", "Generar ODS"))
        self.groupBox_7.setTitle(_translate("SpatialInteractionModelsDialogBase", "Salidas"))
        self.check_projects.setText(_translate("SpatialInteractionModelsDialogBase", "Seleccionar proyecto actual"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.outputs), _translate("SpatialInteractionModelsDialogBase", "Salidas"))
from qgis import gui
# import resources_rc
from .resources import *

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     SpatialInteractionModelsDialogBase = QtWidgets.QDialog()
#     ui = Ui_SpatialInteractionModelsDialogBase()
#     ui.setupUi(SpatialInteractionModelsDialogBase)
#     SpatialInteractionModelsDialogBase.show()
#     sys.exit(app.exec_())
