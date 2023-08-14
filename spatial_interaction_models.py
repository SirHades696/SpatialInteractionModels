# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SpatialInteractionModels
                                 A QGIS plugin
 Este plugin calcula 3 modelos de interacción espacial y son: restricción en el origen, restricción en el destino y los doblemente restrictivos.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-07-25
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Adonai Emmanuel Nicanor Bautista
        email                : djnonasrm@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from numpy import True_
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsMapLayerProxyModel, QgsFieldProxyModel

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .spatial_interaction_models_dialog import SpatialInteractionModelsDialog
import os.path
from qgis.core import *
from PyQt5.QtWidgets import *
from qgis.gui import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QSettings

class SpatialInteractionModels:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SpatialInteractionModels_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Modelos de Interacción Espacial')

        self.action = None
        self.toolbar = self.iface.addToolBar(u'SpatialInteractionModels')
        self.toolbar.setObjectName(u'SpatialInteractionModels')
        self.dlg = SpatialInteractionModelsDialog()
        self.connections()


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SpatialInteractionModels', message)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = ':/plugins/spatial_interaction_models/icon.png'
        icon = QIcon(icon_path)
        self.action = QAction(icon,u'&Modelos de Interacción Espacial',self.iface.mainWindow())
        self.action.setEnabled(True)
        self.toolbar.addAction(self.action)
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(self.menu,self.action)
        self.actions.append(self.action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Modelos de Interacción Espacial'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""

        self.clear_and_start()
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            # get all data
            pass

    def clear_and_start(self):
        self.dlg.tabWidget.setCurrentIndex(0)
        # Origin
        self.dlg.origin_combobox.setFilters(QgsMapLayerProxyModel.PointLayer|QgsMapLayerProxyModel.PolygonLayer)
        self.dlg.origin_combobox.setCurrentIndex(-1)
        self.dlg.id_origin_combobox.setCurrentIndex(-1)
        self.dlg.field_origin_combobox.setCurrentIndex(-1)

        self.dlg.id_origin_combobox.setFilters(QgsFieldProxyModel.String|
                                               QgsFieldProxyModel.Int|
                                               QgsFieldProxyModel.Double|
                                               QgsFieldProxyModel.Numeric|
                                               QgsFieldProxyModel.LongLong)

        self.dlg.field_origin_combobox.setFilters(QgsFieldProxyModel.Int|
                                               QgsFieldProxyModel.Double|
                                               QgsFieldProxyModel.Numeric|
                                               QgsFieldProxyModel.LongLong)
        # Dest
        self.dlg.dest_combobox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.dlg.dest_combobox.setCurrentIndex(-1)
        self.dlg.id_dest_combobox.setCurrentIndex(-1)
        self.dlg.field_dest_combobox.setCurrentIndex(-1)


        self.dlg.id_dest_combobox.setFilters(QgsFieldProxyModel.String|
                                               QgsFieldProxyModel.Int|
                                               QgsFieldProxyModel.Double|
                                               QgsFieldProxyModel.Numeric|
                                               QgsFieldProxyModel.LongLong)

        self.dlg.field_dest_combobox.setFilters(QgsFieldProxyModel.Int|
                                               QgsFieldProxyModel.Double|
                                               QgsFieldProxyModel.Numeric|
                                               QgsFieldProxyModel.LongLong)

        #----------Restrictions
        self.dlg.filt_combobox.setCurrentIndex(0)
        self.dlg.mesuare_combobox.setCurrentIndex(0)
        self.dlg.tipo_filt_dist.setCurrentIndex(0)
        self.dlg.tipo_filt_fluj.setCurrentIndex(0)
        self.dlg.tipo_filt_dist.setEnabled(False)
        self.dlg.tipo_filt_fluj.setEnabled(False)
        self.dlg.val1_dist.setEnabled(False)
        self.dlg.val1_dist.setReadOnly(False)
        self.dlg.val1_dist.clear()
        self.dlg.val1_dist.setValidator(QDoubleValidator())
        self.dlg.val2_dist.setEnabled(False)
        self.dlg.val2_dist.setReadOnly(False)
        self.dlg.val2_dist.clear()
        self.dlg.val2_dist.setValidator(QDoubleValidator())
        self.dlg.val1_fluj.setEnabled(False)
        self.dlg.val1_fluj.setReadOnly(False)
        self.dlg.val1_fluj.clear()
        self.dlg.val1_fluj.setValidator(QDoubleValidator())
        self.dlg.val2_fluj.setEnabled(False)
        self.dlg.val2_fluj.setReadOnly(False)
        self.dlg.val2_fluj.clear()
        self.dlg.val2_fluj.setValidator(QDoubleValidator())
        self.dlg.val1_dist.setVisible(False)
        self.dlg.val2_dist.setVisible(False)

        self.dlg.val1_fluj.setVisible(False)
        self.dlg.val2_fluj.setVisible(False)



        #----------outputs
        self.dlg.sqlite_check_load.setVisible(False)
        self.dlg.geojson_check_load.setVisible(False)
        self.dlg.geopackage_check_load.setVisible(False)
        self.dlg.hd_check_load.setVisible(False)

        self.dlg.sqlite_check.setChecked(False)
        self.dlg.geojson_check.setChecked(False)
        self.dlg.geopackage_check.setChecked(False)
        self.dlg.hd_check.setChecked(False)

        self.dlg.prefijo.clear()
        self.dlg.output.clear()
        self.dlg.check_projects.setChecked(False)
        self.dlg.projects_combobox.clear()
        self.dlg.projects_combobox.setEnabled(False)
        self.load_projects()


    def connections(self):
        # view inputs
        self.dlg.btn_sig1.clicked.connect(self.tab_restrictions)

        # view restrictions
        self.dlg.btn_reg2.clicked.connect(self.tab_inputs)
        self.dlg.btn_sig2.clicked.connect(self.tab_outputs)

        # view outputs
        self.dlg.btn_reg3.clicked.connect(self.tab_restrictions)

        # Restrictions
        self.dlg.filt_combobox.currentIndexChanged.connect(self.restrictions)
        self.dlg.tipo_filt_dist.currentIndexChanged.connect(self.restrictions_valuesD)
        self.dlg.tipo_filt_fluj.currentIndexChanged.connect(self.restrictions_valuesF)

        # Output
        self.dlg.sqlite_check.stateChanged.connect(self.hide_show_sqlite)
        self.dlg.geojson_check.stateChanged.connect(self.hide_show_geojson)
        self.dlg.geopackage_check.stateChanged.connect(self.hide_show_geopackage)
        self.dlg.hd_check.stateChanged.connect(self.hide_show_hd)

        self.dlg.check_projects.stateChanged.connect(self.recent_projects)
        self.dlg.projects_combobox.currentIndexChanged.connect(self.set_project_output)
        self.dlg.btn_output.clicked.connect(self.select_output)

    # ------ TABS
    def tab_inputs(self):
        self.dlg.tabWidget.setCurrentIndex(0)

    def tab_restrictions(self):
        self.dlg.tabWidget.setCurrentIndex(1)

    def tab_outputs(self):
        self.dlg.tabWidget.setCurrentIndex(2)

    def restrictions(self):
        index = self.dlg.filt_combobox.currentIndex()
        if index != 0:
            if index == 1:
                self.dlg.tipo_filt_dist.setEnabled(True)
                self.dlg.tipo_filt_dist.setCurrentIndex(0)
                self.dlg.tipo_filt_fluj.setEnabled(False)
                self.dlg.tipo_filt_fluj.setCurrentIndex(0)
                self.dlg.val1_dist.setVisible(False)
                self.dlg.val2_dist.setVisible(False)
                self.dlg.val1_fluj.setVisible(False)
                self.dlg.val2_fluj.setVisible(False)
            elif index == 2:
                self.dlg.tipo_filt_dist.setEnabled(False)
                self.dlg.tipo_filt_dist.setCurrentIndex(0)
                self.dlg.tipo_filt_fluj.setEnabled(True)
                self.dlg.tipo_filt_fluj.setCurrentIndex(0)
                self.dlg.val1_dist.setVisible(False)
                self.dlg.val2_dist.setVisible(False)
                self.dlg.val1_fluj.setVisible(False)
                self.dlg.val2_fluj.setVisible(False)
            elif index == 3:
                self.dlg.tipo_filt_dist.setEnabled(True)
                self.dlg.tipo_filt_dist.setCurrentIndex(0)
                self.dlg.tipo_filt_fluj.setEnabled(True)
                self.dlg.tipo_filt_fluj.setCurrentIndex(0)
                self.dlg.val1_dist.setVisible(False)
                self.dlg.val2_dist.setVisible(False)
                self.dlg.val1_fluj.setVisible(False)
                self.dlg.val2_fluj.setVisible(False)
        else:
            self.dlg.tipo_filt_dist.setEnabled(False)
            self.dlg.tipo_filt_dist.setCurrentIndex(0)
            self.dlg.tipo_filt_fluj.setEnabled(False)
            self.dlg.tipo_filt_fluj.setCurrentIndex(0)
            self.dlg.val1_dist.setEnabled(False)
            self.dlg.val2_dist.setEnabled(False)
            self.dlg.val1_fluj.setEnabled(False)
            self.dlg.val2_fluj.setEnabled(False)
            self.dlg.val1_dist.setVisible(False)
            self.dlg.val2_dist.setVisible(False)
            self.dlg.val1_fluj.setVisible(False)
            self.dlg.val2_fluj.setVisible(False)


    def restrictions_valuesD(self):
        index = self.dlg.tipo_filt_dist.currentIndex()
        if index != 0:
            if index == 1 or index == 2:
                self.dlg.val1_dist.setEnabled(True)
                self.dlg.val1_dist.setVisible(True)
                self.dlg.val1_dist.setPlaceholderText("Ingresa un valor")
                self.dlg.val2_dist.setEnabled(False)
                self.dlg.val2_dist.setVisible(False)
            elif index == 3:
                self.dlg.val1_dist.setEnabled(True)
                self.dlg.val1_dist.setVisible(True)
                self.dlg.val1_dist.setPlaceholderText("Valor inicial")
                self.dlg.val2_dist.setEnabled(True)
                self.dlg.val2_dist.setVisible(True)
                self.dlg.val2_dist.setPlaceholderText("Valor final")
        else:
            self.dlg.val1_dist.setEnabled(False)
            self.dlg.val2_dist.setEnabled(False)
            self.dlg.val1_dist.setVisible(False)
            self.dlg.val2_dist.setVisible(False)


    def restrictions_valuesF(self):
        index = self.dlg.tipo_filt_fluj.currentIndex()
        if index != 0:
            if index == 1 or index == 2:
                self.dlg.val1_fluj.setEnabled(True)
                self.dlg.val1_fluj.setVisible(True)
                self.dlg.val1_dist.setPlaceholderText("Ingresa un valor")
                self.dlg.val2_fluj.setEnabled(False)
                self.dlg.val2_fluj.setVisible(False)
            elif index == 3:
                self.dlg.val1_fluj.setEnabled(True)
                self.dlg.val1_fluj.setVisible(True)
                self.dlg.val1_dist.setPlaceholderText("Valor inicial")
                self.dlg.val2_fluj.setEnabled(True)
                self.dlg.val2_fluj.setVisible(True)
                self.dlg.val2_dist.setPlaceholderText("Valor final")
        else:
            self.dlg.val1_fluj.setEnabled(False)
            self.dlg.val1_fluj.setVisible(False)
            self.dlg.val2_fluj.setEnabled(False)
            self.dlg.val2_fluj.setVisible(False)

    def hide_show_sqlite(self, state):
        if state:
            self.dlg.sqlite_check_load.setVisible(True)
        else:
            self.dlg.sqlite_check_load.setVisible(False)
            self.dlg.sqlite_check_load.setChecked(False)

    def hide_show_geojson(self,state):
        if state:
            self.dlg.geojson_check_load.setVisible(True)
        else:
            self.dlg.geojson_check_load.setVisible(False)
            self.dlg.geojson_check_load.setChecked(False)

    def hide_show_geopackage(self,state):
        if state:
            self.dlg.geopackage_check_load.setVisible(True)
        else:
            self.dlg.geopackage_check_load.setVisible(False)
            self.dlg.geopackage_check_load.setChecked(False)

    def hide_show_hd(self,state):
        if state:
            self.dlg.hd_check_load.setVisible(True)
        else:
            self.dlg.hd_check_load.setVisible(False)
            self.dlg.hd_check_load.setChecked(False)

    def recent_projects(self,state):
        if state:
            self.dlg.projects_combobox.setEnabled(True)
        else:
            self.dlg.projects_combobox.setCurrentIndex(0)
            self.dlg.projects_combobox.setEnabled(False)

    def load_projects(self):
        settings = QSettings()
        pjts = {}
        self.dlg.projects_combobox.addItem("Seleciona un proyecto...",None)
        for i in range(1,1000):
            rpt = settings.value(f'UI/recentProjects/{i}/title')
            rpp = settings.value(f'UI/recentProjects/{i}/path')
            if rpt == None:
                break
            else:
                pth = rpp.split(f"{rpt}.qgz",1)[0]
                pjts[str(i)]={"PROJECT":rpt,"PATH":pth}

        for i in range(1, len(pjts)+1):
            self.dlg.projects_combobox.addItem(pjts[str(i)]["PROJECT"],pjts[str(i)]["PATH"])

    def set_project_output(self):
        index = self.dlg.projects_combobox.currentIndex()
        if index != 0:
            pth = self.dlg.projects_combobox.itemData(index)
            self.dlg.output.setText(pth)
        else:
            self.dlg.output.clear()

    def select_output(self):
        self.dlg.output.clear()
        path = str(QFileDialog.getExistingDirectory(self.dlg, "Seleccionar ruta de salida"))
        if path != "":
            self.dlg.output.setText(path+"/")
        else:
            print("Error - Selecciona una carpeta")


