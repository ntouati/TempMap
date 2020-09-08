# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TempMap
                                 A QGIS plugin
 Test
                              -------------------
        begin                : 2017-04-22
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Thomas
        email                : thomasgardes.31@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from temp_map_dialog import TempMapDialog
import qgis.core
from qgis.core import *
import os
from qgis.utils import *
import processing
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis import *
import time 
from progress import Ui_Form
import sys 


			
class TempMap:
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
            'TempMap_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
		
		 
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Temperature Map')
        

        # TODO: We are going to let the user set this up in a future iteration
        
        self.toolbar = self.iface.addToolBar(u'TempMap')
        self.toolbar.setObjectName(u'TempMap')
         
		
        

		


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
        return QCoreApplication.translate('TempMap', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = TempMapDialog()
         
        

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/TempMap/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'temperature_maps'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Temperature Map'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
	
		
    def outputICU(self) :
        """Define path to save output files"""
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file", "", '*.tif')
        self.dlg.barre_icu.setText(filename)
		
    def outputRegression(self) :
        """Define path to save output files"""
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file", "", '*.tif')
        self.dlg.barre_regression.setText(filename)
		
    def outputResidus(self) :
        """Define path to save output files"""
        filename = QFileDialog.getSaveFileName(self.dlg, "Select output file", "", '*.tif')
        self.dlg.barre_residus.setText(filename)
	
    def outputModel(self) : 
		"""Define path to save output files"""
		filename = QFileDialog.getSaveFileName(self.dlg, "Select output file", "", '*.csv')
		self.dlg.barre_modele.setText(filename)


    def run(self,index):
		"""Run method that performs all the real work"""
		
		#Connect buttons "browse" to line edit
		self.dlg.bouton_icu.clicked.connect(self.outputICU)
		self.dlg.bouton_regression.clicked.connect(self.outputRegression)
		self.dlg.bouton_residus.clicked.connect(self.outputResidus)
		self.dlg.bouton_modele.clicked.connect(self.outputModel)
	
		
		# show the dialog
		self.dlg.show()
		
		#clear all combo boxes
		self.dlg.menu_mnt.clear()
		self.dlg.menu_temperature.clear()
		self.dlg.menu_field.clear()
		self.dlg.menu_mapuce.clear()
		self.dlg.menu_fraction.clear()
		
		
				
		#add layers to interface
		layers = self.iface.legendInterface().layers() #get all layers from map canvas
		#Initialize lists for diffents types of layers 
		rasterList=[]
		rasterLayerList = []
		pointList = []
		pointLayerList = []
		polyList = []
		polyLayerList = []
		
		#Add layers in lists depending of their types 
		if layers != [] :
			
			for i in range (len(layers)): #for each layer in map canvas
				layer = layers[i]
				if layer.type() == QgsMapLayer.VectorLayer : #check layer type
					
					if layer.wkbType() == QGis.WKBPoint :
						pointList.append(layer.name()) #add name for combo boxes
						pointLayerList.append(layer) #add layers for processing 
					else :
						polyList.append(layer.name())
						polyLayerList.append(layer)
						
				else :
					rasterList.append(layer.name())
					rasterLayerList.append(layer)
		
		# Load lists in combo boxes 
		self.dlg.menu_mnt.addItems(rasterList)
		self.dlg.menu_temperature.addItems(pointList)
		self.dlg.menu_mapuce.addItems(polyList)
		self.dlg.menu_fraction.addItems(rasterList)
	 	
		
		def layer_field() :
			""" Method used to change the content of the 'field' combo box depending of the layer set in "temperature" combo box"""
			selectedLayerIndex = self.dlg.menu_temperature.currentIndex() #get name of layer set in 'temperature' combo box 
			selectedLayer = pointLayerList[selectedLayerIndex] #get layer set in 'temperature' combo box
			fields=selectedLayer.pendingFields() #get fields from the layer 
			fieldnames=[field.name() for field in fields] #get fields names 
			self.dlg.menu_field.clear() #clear combo box before add items 
			self.dlg.menu_field.addItems(fieldnames) #add items (fields names) to 'field' combo box 

			
		def state_changed() :
			"""Method used to perform real time changes on the interface when checkBox is checked or unchecked"""
			if self.dlg.checkBox.isChecked() : #Check if checkBox is checked 
				self.dlg.menu_mapuce.setEnabled(False) #Disable 'mapuce' combo box 
				self.dlg.menu_fraction.setEnabled(True) #Enable 'fraction' combo box 
				self.dlg.label_frac.setStyleSheet('color : black') #Set color of label 'fraction' to black 
				self.dlg.label_mapuce.setStyleSheet('color : grey') #Set color of label 'mapuce' to grey 
			else : #if checkBox not checked 
				self.dlg.menu_mapuce.setEnabled(True) #Enable 'mapuce' combo box 
				self.dlg.menu_fraction.setEnabled(False) #Disable 'fraction' combo box 
				self.dlg.label_frac.setStyleSheet('color : grey') #Set color of label 'fraction' to grey 
				self.dlg.label_mapuce.setStyleSheet('color : black') #Set color of label 'mapuce' to black 
			
		def resolve(name, basepath=None):
			"""Function used to get around a bug making pictures on the dialog doesn't display"""
			if not basepath:
				basepath = os.path.dirname(os.path.realpath(__file__))
			return os.path.join(basepath, name)
		
		if pointList != [] :		
			layer_field() #load fields from the layer in 'temperature' combo box
			
		self.dlg.menu_temperature.currentIndexChanged.connect(layer_field) #connect layer_field method to temperature combo box 
		self.dlg.checkBox.stateChanged.connect(state_changed) #connect state_changed method to checkBox 
		
		
		
		
		#Set 'help' pictures for each combo box 
		pathIcon = resolve('help.png') #get around a bug 
		self.dlg.infoMnt.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoTemp.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoField.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoMapuce.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoInterpolation.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoRegression.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoResidus.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoModele.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoFrac.setPixmap(QtGui.QPixmap(pathIcon))
		self.dlg.infoResolution.setPixmap(QtGui.QPixmap(pathIcon))

		
		

		
		
        # Run the dialog event loop
		result = self.dlg.exec_()
        # See if OK was pressed
		if result:
		
				tps1 = time.clock() #initialize time count 
				
				#Disconnect button to avoid accumulating connection when opening plugin again
				self.dlg.bouton_icu.clicked.disconnect(self.outputICU)
				self.dlg.bouton_regression.clicked.disconnect(self.outputRegression)
				self.dlg.bouton_residus.clicked.disconnect(self.outputResidus)
				self.dlg.bouton_modele.clicked.disconnect(self.outputModel)
				self.dlg.menu_temperature.currentIndexChanged.disconnect(layer_field)
				
				#show progression window when "OK" is pressed
				widget = QtGui.QWidget()
				ui = Ui_Form()
				ui.setupUi(widget)
				widget.show() 
				progress=ui.progressBar #define progress bar widget added from ui file 
				progress.setMaximum(100) #set maximum in percentage for progress bar 
				

			
		
				#Check QGIS version 
				version = qgis.utils.QGis.QGIS_VERSION #get QGIS version as string 
				versionSplit = version.split('.') #split version string 
				NumVersion = versionSplit[1] #get only number of version after the 2.xx (get the "xx")
				qgisVersion = int(NumVersion) #get version number as integer 

									
				#Define outputs path 
				outputPath1 = self.dlg.barre_icu.text() #Get path values from all lines edits 
				outputPath2 = self.dlg.barre_regression.text()
				outputPath3 = self.dlg.barre_residus.text()
				outputPath4 = self.dlg.barre_modele.text()
				
	

				#get current value of combo boxes 
				selectedMntIndex = self.dlg.menu_mnt.currentIndex() 
				selectedMapuceIndex = self.dlg.menu_mapuce.currentIndex()
				selectedTempIndex = self.dlg.menu_temperature.currentIndex()
				selectedFracIndex = self.dlg.menu_fraction.currentIndex() 
				selectedFieldIndex = self.dlg.menu_field.currentIndex()				

				#Check comboboxes content 
				
				#Check if CheckBox checked 
				BoxChecked = False 
				if self.dlg.checkBox.isChecked() :
					BoxChecked = True 
					
				#Looking for errors :
				

				
				if self.dlg.menu_mnt.currentText() == "" : #if combo box is empty 
					QMessageBox.warning(None, "Temperature Map", str("Please choose a valid MNT raster"))
				#check if fraction and MNT are differents from each other (only if checkBox is checked) 
				elif self.dlg.menu_fraction.currentText() == self.dlg.menu_mnt.currentText() and BoxChecked :
					QMessageBox.warning(None, "Temperature Map", str("City fraction and MNT must be differents !"))
				#check fraction combo box (used only when checkBox is checked)
				elif self.dlg.menu_fraction.currentText() == "" and BoxChecked :
					QMessageBox.warning(None,"Temperature Map", str("Please choose a valid City Fraction raster"))
				#check Mapuce combo box 
				elif self.dlg.menu_mapuce.currentText() == "" and BoxChecked == False :
					QMessageBox.warning(None, "Temperature Map", str("Please choose a valid MApUCE layer"))
				#check temperature combo box
				elif self.dlg.menu_temperature.currentText() == "" :
					QMessageBox.warning(None, "Temperature Map", str("Please choose a valid point layer"))
				#chek field combo box 
				elif self.dlg.menu_field.currentText() == "" :
					QMessageBox.warning(None, "Temperature Map", str("Please chose a valid temperature field"))	
								


				
				else :

					selectedLayerIndex2 = self.dlg.menu_temperature.currentIndex()
					selectedLayer2 = pointLayerList[selectedLayerIndex2]
					fields=selectedLayer2.pendingFields()
					fieldnames=[field.name() for field in fields]	
					
					#set layers and fields depending of current values of combo boxes 
					fieldTemp = fieldnames[selectedFieldIndex]
					field = fields[selectedFieldIndex]
					stations  = pointLayerList[selectedTempIndex]
					mnt = rasterLayerList[selectedMntIndex]		
					
					crsStations = stations.crs().authid()
					crsMnt = mnt.crs().authid()
					
					if crsStations != crsMnt :
						QMessageBox.warning(None, "Temperature Map", str("Inputs have not the same CRS. This can cause unexpected results or errors"))	
					
									 					
					resolution=self.dlg.spinBox_resolution.value()
					
					if BoxChecked :						
						frac_user=rasterLayerList[selectedFracIndex]
					else : 
						mapuce=polyLayerList[selectedMapuceIndex]
						


					crsRefLayer = layers[0] #get crs value from the first layer  
					idCrsRef = crsRefLayer.crs().authid()
					epsgSplit = idCrsRef.split(':')
					epsg0 = epsgSplit[1]
					epsg = int(epsg0)
					#check inputs 
					print('station =', stations)
					print('mnt=', mnt)
					print('layers =', layers)
					print('ESPG=', epsg)	
					print('field type :', field.typeName() ) 
					print('Version :', qgisVersion)
					
					
					#===========================================PROCESSING===========================================
									
					#if custom fraction is used, extent depend on station layer
					if BoxChecked :
						objEmp = stations					

						
					#if MApUCE data used, we only use stations into extent of MApUCE layer 	
					else :
					

						emprise=processing.runalg("qgis:extractbylocation", stations, mapuce, ['within'],0, None) #extract stations within MApUCE layer
						stations = emprise['OUTPUT'] 
						addStations = iface.addVectorLayer(stations, "STATIONS", 'ogr') 
						objEmp = processing.getObject(emprise['OUTPUT'])
						


					
					
					rectangle= objEmp.extent() #get extent 
					newRect = QgsRectangle(rectangle.xMinimum()-100, rectangle.yMinimum()-100, rectangle.xMaximum()+100, rectangle.yMaximum()+100) #add 100m to the extent (to take into account border points)
					coordinates = newRect.toString(16) #convert extent as a string 
					replace = coordinates.replace(":",",",1) #adapt string to use "clip raster by extent"
					split = replace.split(",") #split string...
					extent= split[0]+","+split[2]+","+split[1]+","+split[3] #...concatenate string to be used in "clip raster by extent" 

						
						
					# Get a path to save outputs as temporary files 	
					getPathSave = objEmp.dataProvider().dataSourceUri() #get access path from any temporary file 
					split1 = getPathSave.split('|')
					split2 = split1[0]
					split3 = split2[:-10] #delete file name at the end of the string 
					outputInterpolation = split3 + 'Interpolation.tif' #replace file name by name wanted for output 
					outputResidus = split3 + 'Residus.tif'
					outputRegression = split3 + 'Regression.tif'
					outputTable = split3 + 'Model.csv'
						
					#Set temporary outputs paths if not outputs paths specified 
					if outputPath1 == '' :
						outputPath1 = outputInterpolation
					if outputPath2 == '' :
						outputPath2 = outputRegression
					if outputPath3 == '' :
						outputPath3 = outputResidus
					if outputPath4 == '' :
						outputPath4 = outputTable 

						
					#Clip MNT
					
					if qgisVersion <= 12 : #check Qgis version, for compatibility ("clip raster by extent" take a different number of arguments)
						
						mntExtent = processing.runalg("gdalogr:cliprasterbyextent", mnt, 0, extent, '', None) #clip mnt by points extent
						addMnt = iface.addRasterLayer(mntExtent['OUTPUT'], "MNT_CLIP")
						
					else :
						
						mntExtent = processing.runalg("gdalogr:cliprasterbyextent", mnt, 0, extent, 5,4,75,6,1,0,0,0,'',None) #clip mnt by points extent
						
						addMnt = iface.addRasterLayer(mntExtent['OUTPUT'], "MNT_CLIP")
						
					mntTemp = split3 + 'mntTemp.tif' #save mnt as temporary file 					
					mntClip = processing.runalg("saga:resampling", mntExtent['OUTPUT'], True, 0,0, extent,resolution,mntTemp) #resample mnt at the chosen resolution  

										
					
					if self.dlg.checkBox.isChecked() : #if checkbox checked : 
					

						outputCalc2 = split3 + 'frac_user.tif' #define path to save user city fraction as temporary file 
						resamplFracVille = processing.runalg("saga:resampling", frac_user, True, 0,0, extent,resolution,outputCalc2) #resampling user city fraction
						progress.setValue(50) #set value of progress bar 

					
					else :
					
						#Build city fraction from MApUCE data 
						

						
						if qgisVersion <= 14 : #check qgisVersion used 
							#Allow to get around a difference between version following 2.14 : gdal rasterize algorithm take one more argument in the latests versions. 
							
							#Rasterize using the 3 selected variables : road_dens, build_dens,env_area/area
							build= processing.runalg("gdalogr:rasterize",mapuce,"BUILD_DENS",1,resolution,resolution,False,5,"",4,75,6,1,False,0,"",None) #rasterize on build_dens
							road= processing.runalg("gdalogr:rasterize",mapuce,"ROAD_DENS",1,resolution,resolution,False,5,"",4,75,6,1,False,0,"",None)#rasterize on road_dens
							env_area=processing.runalg("qgis:fieldcalculator", mapuce, "ENV/AREA",0,8,3,1,"EXT_ENV_AR/$AREA",None)#calucate field env/area
							env= processing.runalg("gdalogr:rasterize",env_area['OUTPUT_LAYER'],"ENV/AREA",1,resolution,resolution,False,5,"",4,75,6,1,False,0,"",None)#rasterize on new field 
							#Add rasters to project (deleted later, but necesseray to use so algorithms)
							build_density=iface.addRasterLayer(build['OUTPUT'], "BUILD")
							road_density=iface.addRasterLayer(road['OUTPUT'], "ROAD")
							enveloppe= iface.addRasterLayer(env['OUTPUT'], "SURFACE")	
							#Set rasters EPSG 
							build_density.setCrs( QgsCoordinateReferenceSystem(2154, QgsCoordinateReferenceSystem.EpsgCrsId) )
							road_density.setCrs( QgsCoordinateReferenceSystem(2154, QgsCoordinateReferenceSystem.EpsgCrsId) )
							enveloppe.setCrs( QgsCoordinateReferenceSystem(2154, QgsCoordinateReferenceSystem.EpsgCrsId) )

							
						else : 
					
							#Same thing but using synthax from latests QGIS versions 
							build= processing.runalg("gdalogr:rasterize",mapuce,"BUILD_DENS",1,resolution,resolution,extent,False,5,"",4,75,6,1,False,0,"",None)
							road= processing.runalg("gdalogr:rasterize",mapuce,"ROAD_DENS",1,resolution,resolution,extent,False,5,"",4,75,6,1,False,0,"",None)
							env_area=processing.runalg("qgis:fieldcalculator", mapuce, "ENV/AREA",0,8,3,1,"EXT_ENV_AR/$AREA",None)
							env= processing.runalg("gdalogr:rasterize",env_area['OUTPUT_LAYER'],"ENV/AREA",1,resolution,resolution,extent,False,5,"",4,75,6,1,False,0,"",None)
							build_density=iface.addRasterLayer(build['OUTPUT'], "BUILD")
							road_density=iface.addRasterLayer(road['OUTPUT'], "ROAD")
							enveloppe= iface.addRasterLayer(env['OUTPUT'], "SURFACE")
							build_density.setCrs( QgsCoordinateReferenceSystem(2154, QgsCoordinateReferenceSystem.EpsgCrsId) )
							road_density.setCrs( QgsCoordinateReferenceSystem(2154, QgsCoordinateReferenceSystem.EpsgCrsId) )
							enveloppe.setCrs( QgsCoordinateReferenceSystem(2154, QgsCoordinateReferenceSystem.EpsgCrsId) )
						

						
						#Use raster calculator to create city fraction from MApUCE data 
						
												
						entries=[] #initialize input list 
						rast1=QgsRasterCalculatorEntry() #create first raster 
						rast1.ref = 'rast@1' #define first raster name 
						objBuild=processing.getObject(build['OUTPUT']) #get raster as QGIS object 
						rast1.raster=objBuild #define raster 
						rast1.bandNumber=1 #define raster band to use 
						entries.append(rast1) #add raster to inputs 
						
						rast2 = QgsRasterCalculatorEntry() #same thing for second raster
						objRoad=processing.getObject(road['OUTPUT'])
						rast2.ref = 'rast@2'
						rast2.raster=objRoad
						rast2.bandNumber=1
						entries.append(rast2)
						
						rast3 = QgsRasterCalculatorEntry() #same thing for third raster 
						objEnv=processing.getObject(env['OUTPUT'])
						rast3.ref = 'rast@3'
						rast3.raster=objEnv
						rast3.bandNumber=1
						entries.append(rast3)
						
						#define path to save result as temporary file 
						outputCalc = split3 + 'addition.tif' 
						outputCalc2 = split3 + 'additionResampl.tif'

						calc=QgsRasterCalculator('rast@1+rast@2+rast@3', outputCalc ,'GTiff', objBuild.extent(), objBuild.width(), objBuild.height(),entries) #configure raster calculator 
						calc.processCalculation() #launch calculation 
						
						#Remove unsued layers from QGIS project  
						QgsMapLayerRegistry.instance().removeMapLayers( [build_density.id()] )
						QgsMapLayerRegistry.instance().removeMapLayers( [road_density.id()] )
						QgsMapLayerRegistry.instance().removeMapLayers( [enveloppe.id()] )
						QgsMapLayerRegistry.instance().removeMapLayers( [addMnt.id()])
						QgsMapLayerRegistry.instance().removeMapLayers( [addStations.id()])
										
												
						#Set raster dimensions for regression 
						resamplFracVille = processing.runalg("saga:resampling", outputCalc, True, 0,0, extent,resolution,outputCalc2) 
						addFraction = iface.addRasterLayer(outputCalc2, 'FRACTION_DE_VILLE')
					progress.setValue(50) #set new progress bar value 
							


					#==================================================================

					#MULTIPLE LINEAR REGRESSION 

					#Set inputs 					
					objFracVille = processing.getObject(resamplFracVille['USER_GRID']) 
					pathFracVille = objFracVille.dataProvider().dataSourceUri() #get path to city fraction 					
					inputs = mntTemp + ';' + pathFracVille #define final inputs for regression algorithm 
					addMntReg = iface.addRasterLayer(mntTemp, "MNT_REG")
					addFracReg = iface.addRasterLayer(pathFracVille, "FRAC_REG")
					
					saveResiduals = split3 + 'residualsTemp.shp' #define path to save residuals as temporary files 
					
					#Regression 
					lmr = processing.runalg("saga:multipleregressionanalysispointsgrids", inputs, stations,fieldTemp,0,True,True,0,5,5,None,outputPath4,None,saveResiduals,outputPath2) #Multiple linear regression 
					iface.addRasterLayer(outputPath2, "REGRESSION") #add regression to project 
					
					#set EPSG of regression output 
					regObj = processing.getObject(outputPath2)
					regObj.setCrs(QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId)) 
					
					iface.addVectorLayer(outputPath4, "MODEL", 'ogr')
					progress.setValue(70)
						
						
					#Residuals kriging 
					residualsObj = processing.getObject(lmr['RESIDUALS'])
					#get and format path of residuals layer from regression algorithm
					pathResiduals = residualsObj.dataProvider().dataSourceUri()
					splitPathResiduals = pathResiduals.split("|")
					residualsPathFinal = splitPathResiduals[0]
					
					#Running kriging 
					ordinaryKriging = processing.runalg("saga:ordinarykrigingglobal",residualsPathFinal,"RESIDUAL",1,False,False,100,-1,100,1,"a + b * x",True,extent,100,0,outputPath3,None)
					iface.addRasterLayer(outputPath3, "RESIDUALS") #Add kriged residuals layer to QGIS project 
					
					#set EPSG of kriged residuals layer 
					resObj = processing.getObject(outputPath3)
					resObj.setCrs(QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId))
					
					progress.setValue(80)#set new progress bar value 

					#==================================================================

					#Addition of residual + regression rasters
					entries2 = [] #define inputs 
					
					#define first raster (regression) 
					rastReg = QgsRasterCalculatorEntry()  
					objReg = processing.getObject(lmr['REGRESSION']) 
					rastReg.ref = 'rastReg@1'
					rastReg.raster = objReg
					rastReg.bandNumber=1

					entries2.append(rastReg)
					
					#define second raster (kriged residuals)
					rastRes = QgsRasterCalculatorEntry() 
					objRes = processing.getObject(ordinaryKriging['USER_GRID'])
					rastRes.ref = 'rastRes@1'
					rastRes.raster = objRes
					rastRes.bandNumber=1

					entries2.append(rastRes)

					outputCalc2 = split3+ 'icu.tif' #define temporary path to save final output 
					
					#run calculation 
					calc=QgsRasterCalculator('rastReg@1+rastRes@1', outputPath1 ,'GTiff', objFracVille.extent(), objFracVille.width(), objFracVille.height(),entries2) 
					calc.processCalculation()
					
					progress.setValue(100) #set progress bar new value 

					iface.addRasterLayer(outputPath1, "INTERPOLATION") #add interpolation to QGIS project
					
					#Set CRS 
					interObj = processing.getObject(outputPath1)
					interObj.setCrs(QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId))				
					my_crs = core.QgsCoordinateReferenceSystem(epsg, core.QgsCoordinateReferenceSystem.EpsgCrsId)
					iface.mapCanvas().mapRenderer().setDestinationCrs(my_crs)
					
					#Stop time measurment and display processing duration 
					tps2 = time.clock()
					duration = round(tps2 - tps1,3)
					QMessageBox.information(None, "Temperature Map", "Process duration : "+str(duration)+"s")
					
					#Delete unsued layers
					QgsMapLayerRegistry.instance().removeMapLayers( [addFraction.id()])
					QgsMapLayerRegistry.instance().removeMapLayers( [addMntReg.id()])
					QgsMapLayerRegistry.instance().removeMapLayers( [addFracReg.id()])
					

					
		else : #if processing not launched...
			
			#Disconnect button to avoid accumulating connection when opening plugin again
			self.dlg.bouton_icu.clicked.disconnect(self.outputICU)
			self.dlg.bouton_regression.clicked.disconnect(self.outputRegression)
			self.dlg.bouton_residus.clicked.disconnect(self.outputResidus)
			self.dlg.bouton_modele.clicked.disconnect(self.outputModel)
			self.dlg.menu_temperature.currentIndexChanged.disconnect(layer_field)

