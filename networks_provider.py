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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtWidgets import QApplication,QMenu,QAction
from qgis.core import QgsProcessingProvider,QgsApplication
from processing.core.Processing import Processing
from processing.core.ProcessingConfig import ProcessingConfig, Setting
from .reseau_ti import ReseauTi
from .ajout_champ import AjoutChamp
from .concat_reseaux import ConcatReseaux
from .connecteurs_geo import ConnecteursGeo
from .contours import Contours
from .creer_graphe import CreerGraphe
from .interpole import Interpole
from .maj_titj import Majtitj
from .import_gtfs import ImportGTFS
from .inverser import Inverser
from .inverser_selection import InverserSelection
from .reseau_tc import ReseauTC
from .prepare_gtfs import PrepareGTFS
from .connect_nodes2lines import ConnectNodes2Lines
from .calcul_musliw import CalculMusliw
from .param_musliw import MusliwParam
from .simple_matrix import SimpleMatrix
from .matrix_simple_liste import MatrixSimpleList
from .matrix_double_liste import MatrixDoubleList
from .noeuds_isoles import IsolatedNodes
from .fichier_aff import FichierAff
from .decaler_lignes import ShiftLines
from .fichier_od import FichierOD
from .fichier_temps import FichierTemps
from .fichier_temps_jour import FichierTempsJour
from .trafic import Trafic
from .spatial_aggregation import SpatialAggregation
from .routes import Routes
from .path_analysis import PathAnalysis
from .create_ti_arcs import ArcsTi
from .maj_links_times import MajLinksTimes
from .fichier_noeuds import NodesFile
from .fichier_noeud_jour import NodesFileDay
from .autoconnectors import AutoConnecteurs
from .matrix_table import MatrixTable
from .maj_links_pole import MajLinksPole

from qgis.PyQt.QtGui import QIcon
import os

pluginPath = os.path.dirname(__file__)

class NetworksProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

        # Load algorithms
        self.alglist = [ReseauTi(),
                        AjoutChamp(),
                        ConcatReseaux(),
                        ConnecteursGeo(),
                        Contours(),
                        CreerGraphe(),
                        Interpole(),
                        Majtitj(),
                        ImportGTFS(),
                        Inverser(),
                        InverserSelection(),
                        ReseauTC(),
                        PrepareGTFS(),
                        ConnectNodes2Lines(),
                        CalculMusliw(),
                        MusliwParam(),
                        SimpleMatrix(),
                        MatrixSimpleList(),
                        MatrixDoubleList(),
                        IsolatedNodes(),
                        FichierAff(),
                        ShiftLines(),
                        FichierOD(),
                        FichierTemps(),
                        FichierTempsJour(),
                        Trafic(),
                        SpatialAggregation(),
                        Routes(),
                        PathAnalysis(),
                        ArcsTi(),
                        MajLinksTimes(),
                        NodesFile(),
                        NodesFileDay(),
                        AutoConnecteurs(),
                        MatrixTable(),
                        MajLinksPole()]
        
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'networks_{0}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)



    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm( ReseauTi() )
        self.addAlgorithm( AjoutChamp() )
        self.addAlgorithm( ConcatReseaux() )
        self.addAlgorithm( ConnecteursGeo() )
        self.addAlgorithm( Contours() )
        self.addAlgorithm(CreerGraphe())
        self.addAlgorithm(Interpole())
        self.addAlgorithm(Majtitj())
        self.addAlgorithm(ImportGTFS())
        self.addAlgorithm(Inverser())
        self.addAlgorithm(InverserSelection())
        self.addAlgorithm(ReseauTC())
        self.addAlgorithm(PrepareGTFS())
        self.addAlgorithm(ConnectNodes2Lines())
        self.addAlgorithm(CalculMusliw())
        self.addAlgorithm(MusliwParam())
        self.addAlgorithm(SimpleMatrix())
        self.addAlgorithm(MatrixSimpleList())
        self.addAlgorithm(MatrixDoubleList())
        self.addAlgorithm(IsolatedNodes())
        self.addAlgorithm(FichierAff())
        self.addAlgorithm(ShiftLines())
        self.addAlgorithm(FichierOD())
        self.addAlgorithm(FichierTemps())
        self.addAlgorithm(FichierTempsJour())
        self.addAlgorithm(Trafic())
        self.addAlgorithm(SpatialAggregation())
        self.addAlgorithm(Routes())
        self.addAlgorithm(PathAnalysis())
        self.addAlgorithm(ArcsTi())
        self.addAlgorithm(MajLinksTimes())
        self.addAlgorithm(NodesFile())
        self.addAlgorithm(NodesFileDay())
        self.addAlgorithm(AutoConnecteurs())
        self.addAlgorithm(MatrixTable())
        self.addAlgorithm(MajLinksPole())
        


    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'Networks'

    def icon(self):
        return QIcon(os.path.join(pluginPath, "icons", "cerema.png"))

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('Networks')

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
