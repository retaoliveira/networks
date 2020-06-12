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

from PyQt5.QtCore import QCoreApplication, QVariant
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
                       QgsProcessingParameterFileDestination)
import io

class NodesFileDay(QgsProcessingAlgorithm):
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

    INPUT = 'INPUT'
    VARIABLE='VARIABLE'
    TATT1='TATT1'
    FICHIER_RESULTAT='FICHIER_RESULTAT'
    FILTER='FILTER'

    


    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
       
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr('Nodes times output file'),
                0,
                "txt"

            )
        )
        


        self.addParameter(
            QgsProcessingParameterString(
                self.VARIABLE,
                self.tr('Variable'),
                "temps"
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.FILTER,
                self.tr('Filter'),
                "1"
            )
        )    
        
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.TATT1,
                self.tr('Remove initial/final waiting time?'),
                True
                
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.FICHIER_RESULTAT,
                self.tr('Nodes indicators file'),
                "*.txt"
                
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
        fichier_temps=self.parameterAsFile(parameters,self.INPUT,context)
        variable=self.parameterAsString(parameters,self.VARIABLE,context)
        filter=self.parameterAsString(parameters,self.FILTER,context)        
        temps_attente_terminal=self.parameterAsBool(parameters, self.TATT1, context)
        fichier_resultat=self.parameterAsFileOutput(parameters,self.FICHIER_RESULTAT,context)

        champs_num=['jour','heureo','heured','temps','tveh','tmap','tatt','tcorr','ncorr','tatt1','cout','longueur','toll']
        champs_alpha=['id','destination','origin','numero','pole']
        fichier=io.open(fichier_temps,"r",encoding="utf8")
        res=io.open(fichier_resultat,"w",encoding='utf8')
        cols={}
        links={}

        for ch in champs_num:
            if ch in filter:
                filter=filter.replace(ch,'float(elements[cols[\"'+ch+'\"]])')
        for ch in champs_alpha:
            if ch in filter:
                filter=filter.replace(ch,'elements[cols[\"'+ch+'\"]])')


        for i,ligne in enumerate(fichier):
            elements=ligne.strip().replace(',','.').split(';')
            if i==0:
                for j,e in enumerate(elements):
                    if e=='o':
                        e='origin'
                    elif e=='d':
                        e='destination'
                    cols[e]=j
            else:
                try:
                    texte=eval(filter)
                except:
                    print('Filter syntax error')
                    print(filter)
                    break
                if texte==True:
                    try:
                        elements[cols[variable]]=elements[cols[variable]].replace(',','.')
                    except:
                        print(elements,cols[variable])
                    elements[cols['numero']]=elements[cols['numero']]+';'+elements[cols['jour']]
                    elements[cols[variable]]=elements[cols[variable]].replace(',','.')
                    if temps_attente_terminal==True and 'tatt1' in cols:
                        elements[cols[variable]]=float(elements[cols[variable]])-float(elements[cols['tatt1']])
                    if elements[cols['numero']] not in links:
                        pole=(elements[cols['pole']],1)

                        
                        links[elements[cols['numero']]]=[elements[cols['numero']],float(elements[cols[variable]]),1.0,float(elements[cols[variable]]),float(elements[cols[variable]]),elements[cols['pole']],elements[cols['pole']],[elements[cols['heureo']]],[elements[cols['heured']]],float(elements[cols[variable]])**2,elements[cols['origin']],elements[cols['origin']]]
                    else:
                        hd=elements[cols['heureo']]
                        if hd not in links[elements[cols['numero']]][7]:
                                links[elements[cols['numero']]][7].append(hd)
                        hf=elements[cols['heured']]
                        if hf not in links[elements[cols['numero']]][8]:
                                links[elements[cols['numero']]][8].append(hf)
                        links[elements[cols['numero']]][1]+=float(elements[cols[variable]])
                        links[elements[cols['numero']]][9]+=float(elements[cols[variable]])**2
                        links[elements[cols['numero']]][2]+=1
                        if float(elements[cols[variable]])<float(links[elements[cols['numero']]][3]):
                            links[elements[cols['numero']]][3]=float(elements[cols[variable]])
                            links[elements[cols['numero']]][5]=elements[cols['pole']]
                            links[elements[cols['numero']]][10]=elements[cols['origin']]
                        if float(elements[cols[variable]])>float(links[elements[cols['numero']]][4]):
                            links[elements[cols['numero']]][4]=float(elements[cols[variable]])
                            links[elements[cols['numero']]][6]=elements[cols['pole']]
                            links[elements[cols['numero']]][11]=elements[cols['origin']]            
        res.write('numero;jour;avg;nb;min;max;pole_min;pole_max;departures;arrivals;sdev;o_min;o_max\n')
        for i in links:
                try:
                    res.write(links[i][0]+";"+unicode(links[i][1]/links[i][2])+";"+unicode(links[i][2])+";"+unicode(links[i][3])+";"+unicode(links[i][4])+";"+links[i][5]+";"+links[i][6]+";"+unicode(len(links[i][7]))+";"+unicode(len(links[i][8]))+";"+unicode((abs(-((links[i][1]**2)/links[i][2])+links[i][9]))**0.5)+";"+links[i][10]+";"+links[i][11]+"\n")
                except:
                    progress.setText(self.tr('ignored element'))
        res.close()

        return {self.FICHIER_RESULTAT: fichier_resultat}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'indicators_by_node_and_day'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('indicators by node and day')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Analysis')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Analysis'

    def tr(self, string):
        return QCoreApplication.translate('NodesFileDay', string)
        
    def shortHelpString(self):
        return self.tr("""
        Produce indicators aggregated by node. 
		
        Parameters:
            nodes times ouput file: the Musliw link times  output file (<FILENAME>_noeuds.txt)
			variable: The name of the variable for indicator computation (temps (time) by default)
            filter: expression to filter nodes times outfile (ex: ncorr<3 )
            remove initial/final boarding time:  If checked the initial or final waiting time (between the excepted arrival or departure time
            and the real one is substracted from the total travel time
            link indicators file: name of the result file (delimited text with ";" as separator) which containes the following attributes 
            numero: node id
            avg: average value 
            nb: number of od rows in the matrix file 
            min: minimum value indicator
            max: maximum value indicator
            pole_min: first node of intermodality corresponding to the minimum value 
            pole_max: first node of intermodality corresponding to the maximum value 
            departures: number of different departures (number of different alternatives) 
            arrivals:number of different arrivals (number of different alternatives) 
            sdev: standard deviation value
            o_min: origin with minimum value
            o_max: origin with maximum value
            
            
        """)

    def createInstance(self):
        return NodesFileDay()
