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
import numpy
import math
import json


class Interpole(QgsProcessingAlgorithm):
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
    FENETRE='FENETRE'
    COUT_I='COUT_I'
    COUT_J='COUT_J'
    SENS = 'SENS'
    DIFFUSION='DIFFUSION'
    TRAVERSABILITE='TRAVERSABILITE'
    NB_PIXELS_X='NB_PIXELS_X'
    NB_PIXELS_Y='NB_PIXELS_Y'
    TAILLE_PIXEL_X='TAILLE_PIXEL_X'
    TAILLE_PIXEL_Y='TAILLE_PIXEL_Y'
    DECIMALES='DECIMALES'
    RAYON='RAYON'
    VITESSE_DIFFUSION='VITESSE_DIFFUSION'
    INTRAVERSABLE='INTRAVERSABLE'
    IND_VALUES='IND_VALUES'
    RESULTAT='RESULTAT'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        e=iface.mapCanvas().extent()
        etendue=str(tuple([e.xMinimum(),e.xMaximum(), e.yMinimum(), e.yMaximum()]))[1:-1]

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.RESEAU,
                self.tr('Network'),
                [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterExtent(
                self.FENETRE,
                self.tr('Window'),
                etendue
                
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.COUT_I,
                self.tr('i-cost'),
                None,
                self.RESEAU
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.COUT_J,
                self.tr('j-cost'),
                None,
                self.RESEAU

            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.SENS,
                self.tr('Direction'),
                "'1'",
                self.RESEAU
                
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.DIFFUSION,
                self.tr('Spread'),
                "'3'",
                self.RESEAU

            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.TRAVERSABILITE,
                self.tr('Impassibility'),
                "'3'",
                self.RESEAU
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NB_PIXELS_X,
                self.tr('Pixels nb x'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=200
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NB_PIXELS_Y,
                self.tr('Pixels nb y'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=200
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TAILLE_PIXEL_X,
                self.tr('Pixel size x'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=-1.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TAILLE_PIXEL_Y,
                self.tr('Pixel size y'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=-1.0
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.DECIMALES,
                self.tr('Decimals'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=5
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.RAYON,
                self.tr('Radius(m)'),
                type=QgsProcessingParameterNumber.Double,
                defaultValue=500.0
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.VITESSE_DIFFUSION,
                self.tr('Spread speed'),
                '4.0',
                self.RESEAU
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INTRAVERSABLE,
                self.tr('Impassable?'),
                False
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.IND_VALUES,
                self.tr('Individual values'),
                None,
                self.RESEAU

            )
        )
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.RESULTAT,
                self.tr('Raster file')
                
                
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
        fenetre=self.parameterAsExtent(parameters,self.FENETRE,context)
        cout_i=QgsExpression(self.parameterAsExpression(parameters,self.COUT_I,context))
        cout_j=QgsExpression(self.parameterAsExpression(parameters,self.COUT_J,context))
        sens=QgsExpression(self.parameterAsExpression(parameters,self.SENS,context))
        diffusion=QgsExpression(self.parameterAsExpression(parameters,self.DIFFUSION,context))
        traversabilite=QgsExpression(self.parameterAsExpression(parameters,self.TRAVERSABILITE,context))
        nb_pixels_x=self.parameterAsInt(parameters,self.NB_PIXELS_X,context)
        nb_pixels_y=self.parameterAsInt(parameters,self.NB_PIXELS_Y,context)
        taille_pixel_x=self.parameterAsDouble(parameters,self.TAILLE_PIXEL_X,context)
        taille_pixel_y=self.parameterAsDouble(parameters,self.TAILLE_PIXEL_Y,context)
        decimales=self.parameterAsInt(parameters,self.DECIMALES,context)
        rayon=self.parameterAsDouble(parameters,self.RAYON,context)
        vitesse_diffusion=QgsExpression(self.parameterAsExpression(parameters,self.VITESSE_DIFFUSION,context))
        intraversable = self.parameterAsBool(parameters, self.INTRAVERSABLE, context)
        valeurs_individuelles=QgsExpression(self.parameterAsExpression(parameters,self.IND_VALUES,context))

        resultat = self.parameterAsOutputLayer(parameters, self.RESULTAT,context)       # Compute the number of steps to display within the progress bar and
        
        poles={}
        formule_cout_i=self.createExpressionContext(parameters,context)
        cout_i.prepare(formule_cout_i)
        formule_cout_j=self.createExpressionContext(parameters,context)
        cout_j.prepare(formule_cout_j)
        formule_sens=self.createExpressionContext(parameters,context)
        sens.prepare(formule_sens)
        formule_diffusion=self.createExpressionContext(parameters,context)
        diffusion.prepare(formule_diffusion)
        formule_traversabilite=self.createExpressionContext(parameters,context)
        traversabilite.prepare(formule_traversabilite)
        formule_vitesse_diffusion=self.createExpressionContext(parameters,context)
        vitesse_diffusion.prepare(formule_vitesse_diffusion)
        formule_valeurs_individuelles=self.createExpressionContext(parameters,context)
        valeurs_individuelles.prepare(formule_valeurs_individuelles)
        
        grille=numpy.array([[-9999.0]*nb_pixels_y]*nb_pixels_x)
        grille_distance=numpy.array([[1e38]*nb_pixels_y]*nb_pixels_x)
        grille_ind=numpy.array([['0']*nb_pixels_y]*nb_pixels_x,dtype='<U25')
        rep=os.path.dirname(resultat)
        a=fenetre.asWktCoordinates().split(',')
        fenetre2=fenetre#QgsRectangle(float(a[0]),float(a[2]),float(a[1]),float(a[3]))
        p1=a[0].split()
        p2=a[1].split()
        ll=(float(p1[0]),float(p1[1]))
        hauteur=float(p2[1])-float(p1[1])
        largeur=float(p2[0])-float(p1[0])
        if not(taille_pixel_x<=0):
            nb_pixels_x=int(largeur/taille_pixel_x)
        else:
            taille_pixel_x=float(largeur/nb_pixels_x)
        if not(taille_pixel_y<=0):
            nb_pixels_y=int(hauteur/taille_pixel_y)
        else:
            taille_pixel_y=float(hauteur/nb_pixels_y)
        layer=reseau
        if layer.type()==QgsMapLayer.VectorLayer:
            if not layer==None:
                if layer.geometryType()==1:
                    simple=QgsSimplifyMethod()
                    simple.setMethodType(QgsSimplifyMethod.PreserveTopology)
                    simple.setTolerance(min(taille_pixel_x,taille_pixel_y)/2)
                    texte=diffusion.dump()+' in (\'1\',\'2\',\'3\') and ('+cout_j.dump()+' IS NOT NULL and '+sens.dump()+' in (\'1\',\'3\')) '
                    
                    #request=(QgsFeatureRequest().setFilterRect(fenetre2)).setFilterExpression(texte).setSimplifyMethod(simple).setFlags(QgsFeatureRequest.ExactIntersect)
                    request=(QgsFeatureRequest().setFilterRect(fenetre2)).setFilterExpression(texte)
                    #req_intra=(QgsFeatureRequest().setFilterRect(fenetre2)).setFilterExpression(traversabilite.dump()+' in (\'1\',\'2\',\'3\')').setSimplifyMethod(simple).setFlags(QgsFeatureRequest.ExactIntersect)
                    req_intra=(QgsFeatureRequest().setFilterRect(fenetre2)).setFilterExpression(traversabilite.dump()+' in (\'1\',\'2\',\'3\')')
                    features=[f for f in layer.getFeatures(request)]

                    if intraversable:
                        features_intra=[f for f in layer.getFeatures(req_intra)]
                    else:
                        features_intra=[]
                    for k,i in enumerate(features):
                        formule_sens.setFeature(i)
                        formule_cout_i.setFeature(i)
                        formule_cout_j.setFeature(i)
                        formule_vitesse_diffusion.setFeature(i)
                        formule_diffusion.setFeature(i)
                        formule_traversabilite.setFeature(i)
                        formule_valeurs_individuelles.setFeature(i)
                        var_diffusion=diffusion.evaluate(formule_diffusion)
                        var_sens=sens.evaluate(formule_sens)
                        var_traversabilite=traversabilite.evaluate(formule_traversabilite)
                        ti=cout_i.evaluate(formule_cout_i)
                        tj=cout_j.evaluate(formule_cout_j)
                        var_ind=valeurs_individuelles.evaluate(formule_valeurs_individuelles)

                        var_vitesse_diffusion=vitesse_diffusion.evaluate(formule_vitesse_diffusion)
                        speed=60/(1000*var_vitesse_diffusion)

                        if var_sens in ['1','2','3'] :
                            
                            geom=i.geometry()
                            zone=geom.buffer(rayon,12).boundingBox()
                            deltax=int((zone.xMinimum()-ll[0])/taille_pixel_x)
                            deltay=int((zone.yMinimum()-ll[1])/taille_pixel_y)
                            dx=int(zone.width()/taille_pixel_x)
                            dy=int(zone.height()/taille_pixel_y)
                            l1=geom.length()
                            if geom.wkbType()==QgsWkbTypes.MultiLineString:
                                geom_l=geom.asMultiPolyline()
                            else:
                                geom_l=geom.asPolyline()
                            
                            for p in range(dx):
                                d2x=deltax+p
                                for q in range(dy):
                                    d2y=deltay+q
                                    if 0<=d2x<nb_pixels_x and 0<=d2y<nb_pixels_y :
                                        pt1=QgsGeometry.fromPointXY(QgsPointXY(ll[0]+(d2x+0.5)*taille_pixel_x,ll[1]+(d2y+0.5)*taille_pixel_y))
                                        res=geom.closestSegmentWithContext(pt1.asPoint())
                                        d=round(res[0],decimales)
                                        if d<=grille_distance[d2x,d2y] and d<rayon*rayon:
                                            if d>0 and l1>0:
                                                pt2=res[1]
                                                #feedback.setProgressText(geom.asWkt())
                                                if geom.wkbType()==QgsWkbTypes.MultiLineString:
                                                    num_poly=-1
                                                    npts=0
                                                    for k,id_poly in enumerate(geom_l):
                                                        if res[2]<npts+len(id_poly):
                                                            infos_poly=(k,res[2])
                                                        else:
                                                            npts+=len(id_poly)
                                                    #feedback.setProgressText(str(infos_poly[0])+"-"+str(infos_poly[1])+"-"+str(npts))
                                                    geoma=geom_l[infos_poly[0]][:(infos_poly[1]-npts)]+[pt2]
                                                else:
                                                    geoma=geom_l[:res[2]]+[pt2]
                                                #geoma=QgsGeometry(geom)
                                                #geoma.insertVertex(pt2[0],pt2[1],res[2])
                                                l2=QgsGeometry.fromPolylineXY(geoma).length()
                                                if res[2]==0:
                                                    pt3=geom.vertexAt(res[2])
                                                    pt4=geom.vertexAt(res[2]+1)
                                                else:
                                                    try:
                                                        pt3=geom.vertexAt(res[2]-1)
                                                        pt4=geom.vertexAt(res[2])
                                                    except:
                                                        print(res,geom_l)
                                                        pt3=geom_l[res[2]-1]
                                                        pt4=geom_l[res[2]]
                                                p1=pt1.asPoint()
                                                test_sens=(pt4.x()-pt3.x())*(p1.y()-pt2.y())-(p1.x()-pt2.x())*(pt4.y()-pt3.y())
                                                if var_sens in ['1','3'] and not tj==None:
                                                    if (var_diffusion in ['1','3'] and test_sens<=0) or (var_diffusion in ['2','3'] and test_sens>=0):
                                                       
                                                        
                                                        if not tj==None:
                                                            
                                                            if not ti==None:
                                                                t=tj*(l2/l1)+ti*(1-(l2/l1))+math.sqrt(d)*speed
                                                                l3=QgsGeometry.fromPolylineXY([pt1.asPoint(),QgsPointXY(pt2)])
                                                        result_test=False
                                                        if l3!=None:
                                                            if len(features_intra)>0:
                                                                for intra in features_intra:
                                                                    if intra.geometry().intersects(l3):
                                                                        result_test=True
                                                                        break
                                                        if result_test==False:
                                                            if (t<grille[d2x,d2y] and d==grille_distance[d2x,d2y]) or d<grille_distance[d2x,d2y]:
                                                                grille_distance[d2x,d2y] =d
                                                                grille[d2x,d2y] =t
                                                                if var_ind not in poles:
                                                                    poles[var_ind]=len(poles)+1
                                                                grille_ind[d2x,d2y]=poles[var_ind]
                    sortie=os.path.splitext(resultat)
                    fichier_grille=open(sortie[0]+sortie[1],'w')
                    fichier_grille.write("NCOLS {0:d}\nNROWS {1:d}\nXLLCORNER {2}\nYLLCORNER {3}\nDX {4}\nDY {5}\nNODATA_VALUE -9999\n".format(nb_pixels_x,nb_pixels_y,ll[0],ll[1],taille_pixel_x,taille_pixel_y))
                    fichier_grille2=open(sortie[0]+"_dist"+sortie[1],'w')
                    fichier_grille2.write("NCOLS {0:d}\nNROWS {1:d}\nXLLCORNER {2}\nYLLCORNER {3}\nDX {4}\nDY {5}\nNODATA_VALUE -9999\n".format(nb_pixels_x,nb_pixels_y,ll[0],ll[1],taille_pixel_x,taille_pixel_y))
                    g1=numpy.rot90(grille,1)
                    #g1=numpy.flipud(g1)
                    g2=numpy.rot90(grille_ind,1)
                    #g2=numpy.flipud(g2)
                    for i in g1:
                        fichier_grille.write(" ".join([str(ii) for ii in i])+"\n")
                    fichier_grille.close()
                    for i in g2:
                        fichier_grille2.write(" ".join([str(ii) for ii in i])+"\n")
                    fichier_grille2.close()

                    fichier_prj=open(sortie[0]+".prj",'w')
                    fichier2_prj=open(sortie[0]+"_dist.prj",'w')
                    fichier2_dict=open(sortie[0]+"_dist.dic",'w')
                    fichier_prj.write(layer.crs().toWkt())
                    fichier2_prj.write(layer.crs().toWkt())
                    fichier2_dict.write(json.dumps(dict(map(reversed, poles.items()))))
                    fichier_prj.close()
                    fichier2_prj.close()
                    fichier2_dict.close()
                    nom_sortie=os.path.basename(sortie[0])
                    rlayer=QgsRasterLayer(resultat,nom_sortie)

        return {self.RESULTAT: resultat}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'linear_interpolation'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Linear interpolation')

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
        return QCoreApplication.translate('Interpole', string)
        
    def shortHelpString(self):
        return self.tr("""
        Implements a linear based interpolation in order to build a raster
        representing iso-values from a linear objects file
        and travel times at i-node and j-node
        
        Paramameters:
            network : network layer
            window : working area
            i-node cost : cost at node i
            j-node : cost at node j
            direction : flow direction ('0','1','2','3'): '0' prohibited, '1' flow in the object direction,
            '2' flow in the reverse object direction, '3' flow in both directions
            spread : side of spread inside blocks ('0','1','2','3') ('0' spread prohibited, '1' right-side spread only,
            '2' lef-side spread only, '3' both sides spread
            Impassability : Impassability ('0','3') ('0' impassable road, '3' traversable road)
            number of pixel x : number of pixels in x of the output raster
            number of pixel y : number of pixels in y of the output raster
            pixel size in x : pixel size in x(m)  (optional)
            pixel size inyx : pixel size in y (m)  (optional)
            decimals : number of decimals for approximation (e.g 6 correspond to 1e-6)
            radius : search radius m inside blocks
            spread speed : speeed of spread inside blocks in km/h (60 for iso-distance maps)
            impassable : when selected impassable elements ara taken into account  for iso-values computations
            Individual values: (Optional) field for individual values polygons (ex: stations access area)
            result : output raster layer
            """)

    def createInstance(self):
        return Interpole()
