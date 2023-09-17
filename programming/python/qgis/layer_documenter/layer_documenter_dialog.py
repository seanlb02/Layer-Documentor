# -*- coding: utf-8 -*-
"""
/***************************************************************************
 layer_documenterDialog
                                 A QGIS plugin
 This plugin creates a txt/JSON file of specified layer information
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-09-16
        git sha              : $Format:%H$
        copyright            : (C) 2023 by seanlb02
        email                : sean_gyuris@hotmail.com
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

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.utils import iface 

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'layer_documenter_dialog_base.ui'))


class layer_documenterDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(layer_documenterDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.run_button.clicked.connect(self.generate_doc)
        self.directory_selector.setStorageMode(self.directory_selector.StorageMode.GetDirectory)
        # self.directory_selector.setStorageMode(self.directory_selector.SaveFile)
        


# key logic held in the following method
    def generate_doc(self):
        path = self.directory_selector.filePath()
        export_name = f'{self.map_layer.currentText()}'
        layer = self.map_layer.currentLayer()
        # features = layer.getFeatures()
        crs = layer.crs().authid()
        file_type = "N/A"
        if self.rasterRadio.isChecked():
            file_type = 'Raster'
            geometry_type = "N/A"
            layer_fields = "N/A"
            layer_aliases = "N/A"
            resolution = f'{layer.rasterUnitsPerPixelX()}'
        if self.vectorRadio.isChecked():
            layer_fields = f'{layer.fields().names()}'
            layer_aliases = f'{layer.attributeAliases()}'
            file_type = 'Vector'
            geometry_type = layer.geometryType()
            if layer.geometryType() == 0:
                geometry_type = 'Point'
            if layer.geometryType() == 1:
                geometry_type = 'Line'
            if layer.geometryType() == 2:
                geometry_type = 'Polygon'
            if layer.geometryType() == 3:
                geometry_type = 'multipolygon'
        file_path = os.path.join(path, export_name + '.txt')
        description_text = self.description_input.toPlainText() 
        topology_description = self.topology_description.toPlainText()
        if self.vectorRadio.isChecked():
            with open(file_path, 'w') as f:
                # make it conditional, if raster only print select fields...
                f.write(f'Format: {file_type} \nType: {geometry_type} \nCRS: {crs} \nField Names: {layer_fields} \nField Aliases: {layer_aliases} \nLayer Description:  {description_text} \n\nTopology Information: {topology_description}')
        if self.rasterRadio.isChecked():
            with open(file_path, 'w') as f:
                # make it conditional, if raster only print select fields...
                f.write(f'Format: {file_type} \nCRS: {crs} \nLayer Description:  {description_text}')
 