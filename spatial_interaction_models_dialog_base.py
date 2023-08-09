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
        SpatialInteractionModelsDialogBase.resize(624, 412)
        SpatialInteractionModelsDialogBase.setMinimumSize(QtCore.QSize(624, 412))
        SpatialInteractionModelsDialogBase.setMaximumSize(QtCore.QSize(624, 412))
        self.gridLayout = QtWidgets.QGridLayout(SpatialInteractionModelsDialogBase)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_cancelar = QtWidgets.QPushButton(SpatialInteractionModelsDialogBase)
        self.btn_cancelar.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_cancelar.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_cancelar.setObjectName("btn_cancelar")
        self.gridLayout.addWidget(self.btn_cancelar, 1, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(SpatialInteractionModelsDialogBase)
        self.tabWidget.setObjectName("tabWidget")
        self.inputs = QtWidgets.QWidget()
        self.inputs.setObjectName("inputs")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.inputs)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.inputs)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 27))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 27))
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/spatial_interaction_models/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 8, 1, 1, 1)
        self.field_dest_combobox = gui.QgsFieldComboBox(self.inputs)
        self.field_dest_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.field_dest_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.field_dest_combobox.setObjectName("field_dest_combobox")
        self.gridLayout_2.addWidget(self.field_dest_combobox, 12, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.inputs)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.desti_combobox = gui.QgsMapLayerComboBox(self.inputs)
        self.desti_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.desti_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.desti_combobox.setObjectName("desti_combobox")
        self.gridLayout_2.addWidget(self.desti_combobox, 8, 0, 1, 1)
        self.id_origin_combobox = gui.QgsFieldComboBox(self.inputs)
        self.id_origin_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.id_origin_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.id_origin_combobox.setObjectName("id_origin_combobox")
        self.gridLayout_2.addWidget(self.id_origin_combobox, 4, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.inputs)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)
        self.btn_origin = QtWidgets.QPushButton(self.inputs)
        self.btn_origin.setMinimumSize(QtCore.QSize(44, 27))
        self.btn_origin.setMaximumSize(QtCore.QSize(44, 27))
        self.btn_origin.setIcon(icon)
        self.btn_origin.setDefault(False)
        self.btn_origin.setFlat(False)
        self.btn_origin.setObjectName("btn_origin")
        self.gridLayout_2.addWidget(self.btn_origin, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.inputs)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 9, 0, 1, 1)
        self.origin_combobox = gui.QgsMapLayerComboBox(self.inputs)
        self.origin_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.origin_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.origin_combobox.setObjectName("origin_combobox")
        self.gridLayout_2.addWidget(self.origin_combobox, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.inputs)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 7, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.inputs)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.field_origin_combobox = gui.QgsFieldComboBox(self.inputs)
        self.field_origin_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.field_origin_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.field_origin_combobox.setObjectName("field_origin_combobox")
        self.gridLayout_2.addWidget(self.field_origin_combobox, 6, 0, 1, 2)
        self.id_dest_combobox = gui.QgsFieldComboBox(self.inputs)
        self.id_dest_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.id_dest_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.id_dest_combobox.setObjectName("id_dest_combobox")
        self.gridLayout_2.addWidget(self.id_dest_combobox, 10, 0, 1, 2)
        self.label_6 = QtWidgets.QLabel(self.inputs)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 11, 0, 1, 1)
        self.tabWidget.addTab(self.inputs, "")
        self.restrictions = QtWidgets.QWidget()
        self.restrictions.setObjectName("restrictions")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.restrictions)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 6, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.restrictions)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)
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
        self.gridLayout_3.addWidget(self.groupBox_2, 5, 0, 1, 1)
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
        self.val2_dist.setMinimumSize(QtCore.QSize(0, 27))
        self.val2_dist.setMaximumSize(QtCore.QSize(16777215, 27))
        self.val2_dist.setReadOnly(True)
        self.val2_dist.setObjectName("val2_dist")
        self.gridLayout_4.addWidget(self.val2_dist, 1, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.restrictions)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.filt_combobox = QtWidgets.QComboBox(self.restrictions)
        self.filt_combobox.setMinimumSize(QtCore.QSize(0, 27))
        self.filt_combobox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.filt_combobox.setObjectName("filt_combobox")
        self.filt_combobox.addItem("")
        self.filt_combobox.addItem("")
        self.filt_combobox.addItem("")
        self.filt_combobox.addItem("")
        self.gridLayout_3.addWidget(self.filt_combobox, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.restrictions)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 27))
        self.comboBox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_3.addWidget(self.comboBox, 3, 0, 1, 1)
        self.tabWidget.addTab(self.restrictions, "")
        self.outputs = QtWidgets.QWidget()
        self.outputs.setObjectName("outputs")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.outputs)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.outputs)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.sqlite_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.sqlite_check.setObjectName("sqlite_check")
        self.gridLayout_7.addWidget(self.sqlite_check, 1, 0, 1, 1)
        self.hd_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.hd_check.setObjectName("hd_check")
        self.gridLayout_7.addWidget(self.hd_check, 4, 0, 1, 1)
        self.geojson_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.geojson_check.setObjectName("geojson_check")
        self.gridLayout_7.addWidget(self.geojson_check, 2, 0, 1, 1)
        self.memory_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.memory_check.setChecked(True)
        self.memory_check.setObjectName("memory_check")
        self.gridLayout_7.addWidget(self.memory_check, 0, 0, 1, 1)
        self.geopackage_check = QtWidgets.QCheckBox(self.groupBox_3)
        self.geopackage_check.setObjectName("geopackage_check")
        self.gridLayout_7.addWidget(self.geopackage_check, 3, 0, 1, 1)
        self.sqlite_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.sqlite_check_load.setTristate(False)
        self.sqlite_check_load.setObjectName("sqlite_check_load")
        self.gridLayout_7.addWidget(self.sqlite_check_load, 1, 1, 1, 1)
        self.geojson_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.geojson_check_load.setObjectName("geojson_check_load")
        self.gridLayout_7.addWidget(self.geojson_check_load, 2, 1, 1, 1)
        self.geopackage_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.geopackage_check_load.setObjectName("geopackage_check_load")
        self.gridLayout_7.addWidget(self.geopackage_check_load, 3, 1, 1, 1)
        self.hd_check_load = QtWidgets.QCheckBox(self.groupBox_3)
        self.hd_check_load.setObjectName("hd_check_load")
        self.gridLayout_7.addWidget(self.hd_check_load, 4, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_3, 0, 0, 1, 1)
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
        self.gridLayout_6.addWidget(self.groupBox_4, 2, 0, 1, 1)
        self.btn_output = QtWidgets.QPushButton(self.outputs)
        self.btn_output.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_output.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_output.setText("")
        self.btn_output.setIcon(icon)
        self.btn_output.setObjectName("btn_output")
        self.gridLayout_6.addWidget(self.btn_output, 4, 1, 1, 1)
        self.output = QtWidgets.QLineEdit(self.outputs)
        self.output.setMinimumSize(QtCore.QSize(0, 27))
        self.output.setMaximumSize(QtCore.QSize(16777215, 27))
        self.output.setObjectName("output")
        self.gridLayout_6.addWidget(self.output, 4, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.outputs)
        self.label_9.setObjectName("label_9")
        self.gridLayout_6.addWidget(self.label_9, 3, 0, 1, 1)
        self.tabWidget.addTab(self.outputs, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.btn_aceptar = QtWidgets.QPushButton(SpatialInteractionModelsDialogBase)
        self.btn_aceptar.setMinimumSize(QtCore.QSize(0, 27))
        self.btn_aceptar.setMaximumSize(QtCore.QSize(16777215, 27))
        self.btn_aceptar.setObjectName("btn_aceptar")
        self.gridLayout.addWidget(self.btn_aceptar, 1, 2, 1, 1)

        self.retranslateUi(SpatialInteractionModelsDialogBase)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SpatialInteractionModelsDialogBase)

    def retranslateUi(self, SpatialInteractionModelsDialogBase):
        _translate = QtCore.QCoreApplication.translate
        SpatialInteractionModelsDialogBase.setWindowTitle(_translate("SpatialInteractionModelsDialogBase", "Modelos de Interacción Espacial"))
        self.btn_cancelar.setText(_translate("SpatialInteractionModelsDialogBase", "Cancelar"))
        self.label.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona una capa vectorial de orígenes"))
        self.label_4.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo que contiene la población de demanda"))
        self.label_5.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo ID de destinos"))
        self.label_2.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona una capa vectorial de destinos"))
        self.label_3.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo ID de orígenes"))
        self.label_6.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el campo que contiene la cantidad de oferta disponible"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inputs), _translate("SpatialInteractionModelsDialogBase", "Entradas"))
        self.label_8.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona las unidades de medida para la matriz de distancias"))
        self.groupBox_2.setTitle(_translate("SpatialInteractionModelsDialogBase", "Filtro de Flujos"))
        self.val2_fluj.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Segundo valor"))
        self.val1_fluj.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Primer valor"))
        self.tipo_filt_fluj.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Selecciona un tipo de filtro..."))
        self.tipo_filt_fluj.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Mayor que..."))
        self.tipo_filt_fluj.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Menor que..."))
        self.tipo_filt_fluj.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Rango de valores"))
        self.groupBox.setTitle(_translate("SpatialInteractionModelsDialogBase", "Filtro de Distancias/Costos"))
        self.val1_dist.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Primer valor"))
        self.tipo_filt_dist.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Selecciona un tipo de filtro..."))
        self.tipo_filt_dist.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Mayor que..."))
        self.tipo_filt_dist.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Menor que..."))
        self.tipo_filt_dist.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Rango de valores"))
        self.val2_dist.setPlaceholderText(_translate("SpatialInteractionModelsDialogBase", "Segundo valor"))
        self.label_7.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona el tipo de restricción"))
        self.filt_combobox.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Elige una opción..."))
        self.filt_combobox.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Restricción en el origen"))
        self.filt_combobox.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Restricción en el destino"))
        self.filt_combobox.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Doblemente restrictivos"))
        self.comboBox.setItemText(0, _translate("SpatialInteractionModelsDialogBase", "Elige una opción..."))
        self.comboBox.setItemText(1, _translate("SpatialInteractionModelsDialogBase", "Metros"))
        self.comboBox.setItemText(2, _translate("SpatialInteractionModelsDialogBase", "Kilómetros"))
        self.comboBox.setItemText(3, _translate("SpatialInteractionModelsDialogBase", "Millas"))
        self.comboBox.setItemText(4, _translate("SpatialInteractionModelsDialogBase", "Pies"))
        self.comboBox.setItemText(5, _translate("SpatialInteractionModelsDialogBase", "Yardas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.restrictions), _translate("SpatialInteractionModelsDialogBase", "Restricción"))
        self.groupBox_3.setTitle(_translate("SpatialInteractionModelsDialogBase", "Formatos de Salida"))
        self.sqlite_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en SQLite"))
        self.hd_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en disco"))
        self.geojson_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en GeoJSON"))
        self.memory_check.setText(_translate("SpatialInteractionModelsDialogBase", "Conservar capas temporales"))
        self.geopackage_check.setText(_translate("SpatialInteractionModelsDialogBase", "Guardar en Geopackage"))
        self.sqlite_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.geojson_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.geopackage_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.hd_check_load.setText(_translate("SpatialInteractionModelsDialogBase", "Agregar a QGIS"))
        self.groupBox_4.setTitle(_translate("SpatialInteractionModelsDialogBase", "Estadísticas"))
        self.xls_check.setText(_translate("SpatialInteractionModelsDialogBase", "Generar XLS"))
        self.ods_check.setText(_translate("SpatialInteractionModelsDialogBase", "Generar ODS"))
        self.label_9.setText(_translate("SpatialInteractionModelsDialogBase", "Selecciona una ruta de salida"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.outputs), _translate("SpatialInteractionModelsDialogBase", "Salidas"))
        self.btn_aceptar.setText(_translate("SpatialInteractionModelsDialogBase", "Aceptar"))
from qgis import gui
from .resources import *


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     SpatialInteractionModelsDialogBase = QtWidgets.QDialog()
#     ui = Ui_SpatialInteractionModelsDialogBase()
#     ui.setupUi(SpatialInteractionModelsDialogBase)
#     SpatialInteractionModelsDialogBase.show()
#     sys.exit(app.exec_())
