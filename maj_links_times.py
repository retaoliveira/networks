# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Networks
                                 A QGIS plugin
 Networks
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-02-26
        copyright            : (C) 2018 by Patrick Palmier
        email                : patrick.palmier@cerema.fr
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

__author__ = 'Patrick Palmier'
__date__ = '2018-02-26'
__copyright__ = '(C) 2018 by Patrick Palmier'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt5.QtCore import QCoreApplication,QVariant
from qgis.core import *
from qgis.utils import *
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterString,
                       QgsProcessingParameterExtent,
                       QgsProcessingParameterField,
                       QgsProcessingParameterExpression,
                       QgsProcessingParameterFileDestination,
                       QgsSpatialIndex,
                       QgsGeometry,
                       QgsFeature,
                       QgsCoordinateTransform,
                       QgsCoordinateReferenceSystem
                       )
import codecs

class MajLinksTimes(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    RESEAU = 'RESEAU'
    FICHIER_TEMPS = 'FICHIER_TEMPS'
    DEPART='DEPART'
    TI='TI'
    TJ='TJ'
    TEMPS_TERMINAL='TEMPS_TERMINAL'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.RESEAU,
                self.tr('Network'),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterFile(
                self.FICHIER_TEMPS,
                self.tr('Travel times file'),
            )
        )
        self.addParameter(
            QgsProcessingParameterEnum(
                self.DEPART,
                self.tr('Departure/arrival'),
                options=[self.tr('Departure'),self.tr('Arrival')],
                defaultValue=0
                
            )
        )            
        self.addParameter(
            QgsProcessingParameterExpression(
                self.TI,
                self.tr('i-node time'),
                parentLayerParameterName=self.RESEAU,
                optional=False,
                defaultValue='ti'
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.TJ,
                self.tr('j-node time'),
                parentLayerParameterName=self.RESEAU,
                optional=False,
                defaultValue='tj'            
                )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.TEMPS_TERMINAL,
                self.tr('Initial/final waiting time?'),
                False
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        reseau = self.parameterAsVectorLayer(parameters, self.RESEAU, context)
        fichier_temps=self.parameterAsFile(parameters,self.FICHIER_TEMPS,context)
        depart=self.parameterAsEnum(parameters,self.DEPART,context)
        champ_ti=self.parameterAsExpression(parameters,self.TI,context).strip("'").strip("\"")
        champ_tj=self.parameterAsExpression(parameters,self.TJ,context).strip("'").strip("\"")
        temps_terminal = self.parameterAsBool(parameters, self.TEMPS_TERMINAL, context)
        if depart==0:
            start=True
        else:
            start=False

        fichier=codecs.open(fichier_temps,"r","utf-8")
        champs=reseau.fields()
        start=depart
        noms_champs=[]
        request=(QgsFeatureRequest().setFilterRect(iface.mapCanvas().extent()))


        #lecture du noms des champs
        for f in champs:
            noms_champs.append(f.name())
        #ajout si necessaire champ ti tj
        reseau.startEditing()
        reseau.beginEditCommand(self.tr("updating ti tj"))
        if  champ_ti not in noms_champs:
            reseau.dataProvider().addAttributes([QgsField(champ_ti,QVariant.Double)])
          
        if  champ_tj not in noms_champs:
            reseau.dataProvider().addAttributes([QgsField(champ_tj,QVariant.Double)])

        if  u"ij" not in noms_champs:
            reseau.dataProvider().addAttributes([QgsField("ij",QVariant.String)])
            #reseau.addAttribute(QgsField("ij",QVariant.String))
            for f in reseau.getFeatures(request):
                num=f.id()
                lab_ij=f['i']+'-'+f['j']
                reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()['ij'],lab_ij)


        reseau.updateFields()





        colonnes={}
        links={}
        for k,i in enumerate(fichier):
            elements=i.strip('\n').strip("\r").split(";")
            ncols=len(elements)
            if k==0:
                for j in range(ncols):
                    colonnes[elements[j]]=j
            else:
                t=elements[colonnes["temps"]].replace(",",".")
                u=elements[colonnes["ti"]].replace(",",".")
                ij=elements[colonnes["ij"]]
                if temps_terminal==False:
                    if str(ij) not in links:
                        links[str(ij)]=(1e38,0,1e38)
                    if float(t)<links[str(ij)][0]:
                        links[str(ij)]=(float(t),0,float(u))
                else:
                    if str(ij) not in links:
                        links[str(ij)]=(1e38,0)
                    tatt1=elements[colonnes["tatt1"]].replace(",",".")
                    if float(t)-float(tatt1)<links[str(ij)][0]-links[str(ij)][1]:
                        links[str(ij)]=(float(t),float(tatt1),float(u))


        n=reseau.featureCount()
        feedback.setProgressText(self.tr("updating ti and tj..."))
        ida=reseau.fields().indexFromName(champ_ti)
        idb=reseau.fields().indexFromName(champ_tj)
        valid={}

        for k,f in enumerate(reseau.getFeatures(request)):
            feedback.setProgress((k+1)*100/n)
            num=f.id()
            #temps=float(f["temps"])
            ij=f["ij"]
            if ij in links:
                ti=links[f["ij"]][0]-links[f["ij"]][1]
                tj=links[f["ij"]][2]-links[f["ij"]][1]
                if start==0:
                    valid={ida : tj, idb: ti}
                    reseau.changeAttributeValues(num,valid)
                    #reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti)
                    #reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti-temps)
                else:
                    valid={ida : ti, idb : tj}
                    reseau.changeAttributeValues(num,valid)
                    #reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti)
                    #reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti-temps)
            else:
                ti=NULL
                valid={ida : ti, idb : ti}
                reseau.changeAttributeValues(num,valid)
                
                #reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_ti],ti)
                #reseau.changeAttributeValue(num, reseau.dataProvider().fieldNameMap()[champ_tj],ti)

        feedback.setProgress((k+1)*100/n)            
        reseau.commitChanges()
        reseau.endEditCommand()
        feedback.setProgress(100)     
        return {self.RESEAU: self.RESEAU}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'update_links_times'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Update links times")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Network')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Network'

    def tr(self, string):
        return QCoreApplication.translate('MajLinksTimes', string)
        
    def shortHelpString(self):
        return self.tr("""
        Read the travel times file ".._temps.txt" computed by Musliw and creates (if they don't exist) in the network layer fields where i-node and j-node travel times are saved
		        
        Parameters:
            layer : network layer (linear objects)
			travel times file: travel times text file ..._temps.txt generated by Musliw
            departure/arrival: departure if "d" in Musliw matrix, arrival if "a"
            i_node time: travel time at i-node field
            j-node time; travel time at j-node field
            initial/final waiting time: in order to take into account or not inital/final waiting time (tatt1)
        """)
    def createInstance(self):
        return MajLinksTimes()
