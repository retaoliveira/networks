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

from PyQt5.QtCore import QCoreApplication,QVariant,QDate,QDateTime,QTime
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
import io
import datetime,re

class ImportGTFS(QgsProcessingAlgorithm):
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

    REP_GTFS = 'REP_GTFS'
    DEBUT_PERIODE = 'DEBUT_PERIODE'
    FIN_PERIODE = 'FIN_PERIODE'
    T1 = 'T1'
    T2 = 'T2'
    PREFIXE = 'PREFIXE'
    PROJ = 'PROJ'
    REP_SORTIE='REP_SORTIE'
    ENCODAGE='ENCODAGE'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterFile(
                self.REP_GTFS,
                self.tr('GTFS Folder'),
                QgsProcessingParameterFile.Folder
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DEBUT_PERIODE,
                self.tr('Calendar start'),
                datetime.date.today().strftime("%d/%m/%Y")
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.FIN_PERIODE,
                self.tr('Calendar end'),
                datetime.date.today().strftime("%d/%m/%Y")
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.T1,
                self.tr('Start time'),
                "00:00:00"
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.T2,
                self.tr('End time'),
                "23:59:59"
            )
        )        
        self.addParameter(
            QgsProcessingParameterString(
                self.PREFIXE,
                self.tr('Table names'),
                
            )
        )
        self.addParameter(
            QgsProcessingParameterCrs(
                self.PROJ,
                self.tr('CRS'),
                QgsCoordinateReferenceSystem('EPSG:2154')
            )
        )
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.REP_SORTIE,
                self.tr('Ouput folder')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.ENCODAGE,
                self.tr('Encoding'),
                defaultValue='utf_8_sig'
                
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
        rep_GTFS = self.parameterAsFile(parameters, self.REP_GTFS, context)
        debut_periode=self.parameterAsString(parameters,self.DEBUT_PERIODE,context)
        fin_periode=self.parameterAsString(parameters,self.FIN_PERIODE,context)
        t1=self.parameterAsString(parameters,self.T1,context)
        t2=self.parameterAsString(parameters,self.T2,context)
        prefixe=self.parameterAsString(parameters,self.PREFIXE,context)
        proj=self.parameterAsCrs(parameters,self.PROJ,context)
        rep_sortie = self.parameterAsFile(parameters, self.REP_SORTIE, context)
        encodage = self.parameterAsString(parameters, self.ENCODAGE, context)


        debut_periode=QDate.fromString(debut_periode, "d/M/yyyy").toPyDate()
        fin_periode=QDate.fromString(fin_periode, "d/M/yyyy").toPyDate()


        t1=QTime.fromString(t1,"h:m:s")
        t2=QTime.fromString(t2,"h:m:s")
        nom_rep=rep_GTFS
        lname=prefixe
        isnodes=True
        islines=True


        if "stops.txt" in os.listdir(nom_rep) :
            fich_noeuds=io.open(nom_rep+"/stops.txt","r",encoding=encodage)
            t_noeuds=QgsFields()
            t_noeuds.append(QgsField("ident",QVariant.String,len=15))
            t_noeuds.append(QgsField("name",QVariant.String,len=40))
            t_noeuds.append(QgsField("int_tot",QVariant.Double))
            t_noeuds.append(QgsField("out_tot",QVariant.Double))
            t_noeuds.append(QgsField("in_mon-fri",QVariant.Double))
            t_noeuds.append(QgsField("out_mon-fri",QVariant.Double))
            t_noeuds.append(QgsField("in_sat",QVariant.Double))
            t_noeuds.append(QgsField("out_sat",QVariant.Double))
            t_noeuds.append(QgsField("in_sun",QVariant.Double))
            t_noeuds.append(QgsField("out_sun",QVariant.Double))
            
            t_links=QgsFields()
            t_links.append(QgsField("line_num",QVariant.String,len=15))
            t_links.append(QgsField("ligne_name",QVariant.String,len=50))
            t_links.append(QgsField("ligne_descr",QVariant.String,len=150))
            t_links.append(QgsField("i",QVariant.String,len=15))
            t_links.append(QgsField("j",QVariant.String,len=15))
            t_links.append(QgsField("nb_tot",QVariant.Double))
            t_links.append(QgsField("d1_tot",QVariant.Double))
            t_links.append(QgsField("d2_tot",QVariant.Double))
            t_links.append(QgsField("nb_mon-fri",QVariant.Double))
            t_links.append(QgsField("d2_mon-fri",QVariant.Double))
            t_links.append(QgsField("nb_sat",QVariant.Double))
            t_links.append(QgsField("d2_sat",QVariant.Double))
            t_links.append(QgsField("nb_sun",QVariant.Double))
            t_links.append(QgsField("d2_sun",QVariant.Double))
            
            src=QgsCoordinateReferenceSystem("EPSG:4326")
            dest=QgsCoordinateReferenceSystem(proj)
            xtr=QgsCoordinateTransform(src,dest,QgsProject.instance())
                
            t_arcs=QgsFields()
            t_arcs.append(QgsField("i",QVariant.String,len=15))
            t_arcs.append(QgsField("j",QVariant.String,len=15))
            t_arcs.append(QgsField("ij",QVariant.String,len=40))
            l_noeuds=QgsVectorFileWriter(rep_sortie+"/"+lname+"_stops.shp","UTF-8",t_noeuds,QgsWkbTypes.Point,dest,"ESRI Shapefile")
            l_arcs=QgsVectorFileWriter(rep_sortie+"/"+lname+"_arcs.shp","UTF-8",t_arcs,QgsWkbTypes.MultiLineString,dest,"ESRI Shapefile")
            l_links=QgsVectorFileWriter(rep_sortie+"/"+lname+"_lines.shp","UTF-8",t_links,QgsWkbTypes.MultiLineString,dest,"ESRI Shapefile")
            
            
            arrets={}
            nb_jours=(fin_periode-debut_periode).days
            nb_mon=0
            nb_sat=0
            nb_sun=0
            for k in range(nb_jours+1):
                date_offre=debut_periode+datetime.timedelta(days=k)
                if debut_periode<=date_offre<=fin_periode:
                    jour=date_offre.isoweekday()
                if jour in [1,2,3,4,5]:
                    nb_mon+=1
                elif jour==6:
                    nb_sat+=1
                elif jour==7:
                    nb_sun+=1
            feedback.setProgressText("Lecture des stops")
            for i,ligne in enumerate(fich_noeuds):
                if i==0:
                    entete=re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",ligne[:-1])
                    for e1,e in enumerate(entete):
                        entete[e1]=entete[e1].strip("\"")
                    idx=entete.index('stop_lon')
                    idy=entete.index('stop_lat')
                    iid=entete.index('stop_id')
                    iname=entete.index('stop_name')
                else:

                    elements=re.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)",ligne[:-1])
                    arrets[elements[iid]]=[elements[iid],elements[iname].strip("\""),elements[idx].strip("\""),elements[idy].strip("\""),0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]


        calendar={}
        if ("calendar.txt" in  os.listdir(nom_rep)):
            fich_calendar=io.open(nom_rep+"/calendar.txt","r",encoding=encodage)
            feedback.setProgressText(self.tr("Reading calendars..."))
            for i,cal in enumerate(fich_calendar):
                if i==0:
                    entete=cal.strip().split(',')
                    iid=entete.index('service_id')
                    idato=entete.index('start_date')
                    idatd=entete.index('end_date')
                    i1=entete.index('monday')
                    i2=entete.index('tuesday')
                    i3=entete.index('wednesday')
                    i4=entete.index('thursday')
                    i5=entete.index('friday')
                    i6=entete.index('saturday')
                    i7=entete.index('sunday')
                else:

                    elements=cal.strip().split(",")
                    dato=elements[idato]
                    dato=datetime.date(int(dato[0:4]),int(dato[4:6]),int(dato[6:8]))
                    datd=elements[idatd]
                    datd=datetime.date(int(datd[0:4]),int(datd[4:6]),int(datd[6:8]))
                    calendar[elements[iid]]=[elements[iid],dato,datd,elements[i1],elements[i2],elements [i3],elements[i4],elements[i5],elements[i6],elements[i7]]
                    

        calendar_dates={}
        calendar_dates2={}
        if ("calendar_dates.txt" in  os.listdir(nom_rep)):
            fich_calendar_dates=io.open(nom_rep+"/calendar_dates.txt","r",encoding=encodage)
            feedback.setProgressText(self.tr("reading calendar dates..."))
            for i,calendar_date in enumerate(fich_calendar_dates):
                if i==0:

                    entete=calendar_date.strip().split(',')
                    for i1,i2 in enumerate(entete):
                        entete[i1]=i2.strip('"')
                    iid=entete.index('service_id')
                    idate=entete.index('date')
                    iex=entete.index('exception_type')
                else:

                    elements=calendar_date.strip().split(",")
                    vdate=elements[idate].strip('"')
                    vdate=datetime.date(int(vdate[0:4]),int(vdate[4:6]),int(vdate[6:8]))
                    calendar_dates[(elements[iid],vdate,elements[iex])]=[elements[iid],vdate,elements[iex]]
                    if elements[iex]=="1":
                        if elements[iid] not in calendar_dates2:
                            calendar_dates2[elements[iid]]=[]
                        calendar_dates2[elements[iid]].append([elements[iid],vdate])


        routes={}
        test_l=int(("routes.txt" in os.listdir(nom_rep))*("trips.txt" in os.listdir(nom_rep))* ("stop_times.txt" in os.listdir(nom_rep)))
        if test_l==1 and islines:
            fich_routes=io.open(nom_rep+"/routes.txt","r",encoding=encodage)
            feedback.setProgressText(self.tr("Reading routes..."))
            for i,route in enumerate(fich_routes):
                if i==0:
                    entete=route.strip().split(',')
                    for i1,i2 in enumerate(entete):
                        entete[i1]=i2.strip('"')
                    iid=entete.index('route_id')
                    if 'route_short_name' not in entete:
                        iname=entete.index('route_long_name')
                    else:
                        iname=entete.index('route_short_name')
                    if 'route_long_name' not in entete:
                        ilong=entete.index('route_desc')
                    else:
                        ilong=entete.index('route_long_name')
                else:

                    elements=route.strip().split(",")
                    if elements[iname]=="":
                        elements[iname]=u' '
                    if elements[ilong]=="":
                        elements[ilong]=u' '
                    routes[elements[iid]]=[elements[iid],elements[iname],elements[ilong]]
            trips={}
            fich_trips=io.open(nom_rep+"/trips.txt","r",encoding=encodage)
            feedback.setProgressText(self.tr("Reading trips..."))
            for i,trip in enumerate(fich_trips):
                if i==0:
                    entete=trip.strip(" ").split(',')
                    for i1,i2 in enumerate(entete):
                        entete[i1]=i2.strip('"')
                        entete[i1]=i2.strip('\n').strip('\r')
                    iid=entete.index('route_id')
                    itrip=entete.index('trip_id')
                    iservice=entete.index('service_id')
                    if 'shape_id' in entete:
                        ishape=entete.index('shape_id')
                else:

                    elements=trip.strip(" ").strip('\n').strip('\r').split(",")

                    trips[elements[itrip]]=[elements[itrip],elements[iid],elements[iservice]]
            stop_times={}
            fich_stop_times=io.open(nom_rep+"/stop_times.txt","r",encoding=encodage)
            id_trip=None
            id_stop=None
            hi2=None
            segments={}
            links={}
            feedback.setProgressText(self.tr("Reading stop times..."))
            nb=float(os.stat(nom_rep+"/stop_times.txt").st_size)
            for i,stop_time in enumerate(fich_stop_times):
                if i==0:
                    entete=stop_time.strip().split(",")
                    iid=entete.index('trip_id')
                    iharr=entete.index('arrival_time')
                    ihdep=entete.index('departure_time')
                    istop=entete.index('stop_id')
                    iseq=entete.index('stop_sequence')
                else:
                    #progress.setPercentage(float(fich_stop_times.tell())*100/nb)
                    elements=stop_time.strip().split(',')
                    
                    #print((istop,iid,elements[istop],elements[iid]))
                    if elements[istop] in arrets and trips[elements[iid]][1] in routes:
                        id_stop2=elements[istop]
                        id_trip2=elements[iid]
                        ligne=trips[elements[iid]][1]
                        num_ligne=routes[ligne][0].strip()
                        nom_ligne=routes[ligne][1].strip()
                        descr=routes[ligne][2].strip()
                        hi1=QTime(int(elements[ihdep][0:2]),int(elements[ihdep][3:5]),int(elements[ihdep][6:8]))
                        hj=QTime(int(elements[iharr][0:2]),int(elements[iharr][3:5]),int(elements[iharr][6:8]))
                        if (id_trip2==id_trip):
                            nbservices=0.0
                            nbservices_mon=0.0
                            nbservices_sat=0.0
                            nbservices_sun=0.0
                            nbs1=0.0
                            nbs2=0.0
                            nbs1_mon=0.0
                            nbs2_mon=0.0
                            nbs1_sat=0.0
                            nbs2_sat=0.0
                            nbs1_sun=0.0
                            nbs2_sun=0.0
                            if ("calendar.txt" in  os.listdir(nom_rep)):
                                if trips[elements[iid]][2] in calendar:
                                    dp=calendar[trips[elements[iid]][2]][1]
                                    fp=calendar[trips[elements[iid]][2]][2]
                                    nb_jours=(fin_periode-debut_periode).days
                                    #nb_mon=0
                                    #nb_sat=0
                                    #nb_sun=0
                                    for kk,k in enumerate(range(nb_jours+1)):
                                        date_offre=debut_periode+datetime.timedelta(days=k)
                                        if dp<=date_offre<=fp:
                                            jour=date_offre.isoweekday()
                                            if int(calendar[trips[id_trip][2]][2+jour])==1:
                                                if (trips[id_trip][2],date_offre,'2') not in calendar_dates:
                                                    nbservices+=1
                                                    if jour in [1,2,3,4,5]:
                                                        nbservices_mon+=1
                                                    elif jour==6:
                                                        nbservices_sat+=1
                                                    elif jour==7:
                                                        nbservices_sun+=1
                                            elif int(calendar[trips[id_trip][2]][2+jour])==0:
                                                if (trips[id_trip][2],date_offre,'1') in calendar_dates:
                                                    nbservices+=1
                                                    if jour in [1,2,3,4,5]:
                                                        nbservices_mon+=1
                                                    elif jour==6:
                                                        nbservices_sat+=1
                                                    elif jour==7:
                                                        nbservices_sun+=1
                                    
                            elif trips[elements[iid]][2] in calendar_dates2:
                                for k in calendar_dates2[trips[elements[iid]][2]]:
                                    if debut_periode<=k[1]<=fin_periode:
                                        nbservices+=1
                                        jour=k[1].isoweekday()
                                        if jour in [1,2,3,4,5]:
                                            nbservices_mon+=1
                                        elif jour==6:
                                            nbservices_sat+=1
                                        elif jour==7:
                                            nbservices_sun+=1
                            segment_id=(num_ligne, id_stop,id_stop2)
                            if (t1<=hi2<=t2):
                                nbs1=nbservices
                                nbs1_mon=nbservices_mon
                                nbs1_sat=nbservices_sat
                                nbs1_sun=nbservices_sun
                            if (t1<=hj<=t2):
                                nbs2=nbservices
                                nbs2_mon=nbservices_mon
                                nbs2_sat=nbservices_sat
                                nbs2_sun=nbservices_sun
                            if (id_stop,id_stop2) not in links:
                                links[(id_stop,id_stop2)]={}
                            if num_ligne not in links[(id_stop,id_stop2)]:
                                links[(id_stop,id_stop2)][num_ligne]=(nbs1,nbs1_mon,nbs1_sat,nbs1_sun,descr,nom_ligne)
                            else:
                                seg= links[(id_stop,id_stop2)][num_ligne]
                                links[(id_stop,id_stop2)][num_ligne]=(seg[0]+nbs1,seg[1]+nbs1_mon,seg[2]+nbs1_sat,seg[3]+nbs1_sun,descr,nom_ligne)
                                
                            arrets[id_stop][5]+=nbs1
                            arrets[id_stop2][4]+=nbs2
                            arrets[id_stop][7]+=nbs1_mon
                            arrets[id_stop2][6]+=nbs2_mon
                            arrets[id_stop][9]+=nbs1_sat
                            arrets[id_stop2][8]+=nbs2_sat
                            arrets[id_stop][11]+=nbs1_sun
                            arrets[id_stop2][10]+=nbs2_sun
                        hi2=hi1
                        id_stop=id_stop2
                        id_trip=id_trip2
            feedback.setProgressText(self.tr("Generating arcs and lines..."))
            for i,s in enumerate(links):
                i1=0.0
                i2=0.0
                i2_mon=0.0
                i2_sat=0.0
                i2_sun=0.0                
                g_links=QgsFeature()
                g_arcs=QgsFeature()
                #print([unicode(s[0]),unicode(s[1]),unicode(s[0])+"-"+unicode(s[1])])
                g_links.setGeometry(QgsGeometry.fromPolylineXY([(xtr.transform(QgsPointXY(float(arrets[s[0]][2]),float(arrets[s[0]][3])))),xtr.transform(QgsPointXY(float(arrets[s[1]][2]),float(arrets[s[1]][3])))]))
                g_arcs.setAttributes([unicode(s[0]),unicode(s[1]),unicode(s[0])+"-"+unicode(s[1])])
                g_arcs.setGeometry(g_links.geometry())
                
                if g_arcs.geometry().length()<1600000:
                    l_arcs.addFeature(g_arcs)
                for t in links[s]:

                    if t=="" or t==None:
                        tt= " "
                    else:
                        tt=t
                    #print([tt.decode("cp1252"),links[s][t][2].decode("cp1252"),unicode(s[0]),unicode(s[1]),links[s][t][0],links[s][t][1],i1,i2])
                    try:
                        """print([unicode(t),unicode(links[s][t][4]),unicode(links[s][t][5]),unicode(s[0]),unicode(s[1])
                                ,links[s][t][0]/(nb_jours+1),i1,i2/(nb_jours+1),links[s][t][1]/nb_mon,i2_mon/nb_mon
                                ,links[s][t][2]/nb_sat,i2_sat/nb_sat,links[s][t][3]/nb_sun,i2_sun/nb_sun])"""
                        g_links.setAttributes([unicode(t),unicode(links[s][t][4]),unicode(links[s][t][5]),unicode(s[0]),unicode(s[1])
                                ,links[s][t][0]/(nb_jours+1),i1,i2/(nb_jours+1),links[s][t][1]/nb_mon,i2_mon/nb_mon
                                ,links[s][t][2]/nb_sat,i2_sat/nb_sat,links[s][t][3]/nb_sun,i2_sun/nb_sun])
                    except:
                        print(t,links[s][t][2])
                    
                    i1+=1
                    i2+=links[s][t][0]
                    i2_mon+=links[s][t][1]
                    i2_sat+=links[s][t][2]
                    i2_sun+=links[s][t][3]
                    if g_links.geometry().length()<1600000:
                        l_links.addFeature(g_links)
            del(stop_times)
            del(trips)
            del(routes)
            del(calendar)
            del(calendar_dates)

        if (isnodes):

            for s in arrets:
                g_noeuds=QgsFeature()
                g_noeuds.setGeometry(QgsGeometry.fromPointXY(xtr.transform(QgsPointXY(float(arrets[s][2]),float(arrets[s][3])))))
                #print([unicode(arrets[s][0]),unicode(arrets[s][1]),arrets[s][4]/(nb_jours+1),arrets[s][5]/(nb_jours+1)
                #            ,arrets[s][6]/nb_mon,arrets[s][7]/nb_mon,arrets[s][8]/nb_sat,arrets[s][9]/nb_sat,arrets[s][10]/nb_sun,arrets[s][11]/nb_sun])
                try:
                    g_noeuds.setAttributes([unicode(arrets[s][0]),unicode(arrets[s][1]),arrets[s][4]/(nb_jours+1),arrets[s][5]/(nb_jours+1)
                            ,arrets[s][6]/nb_mon,arrets[s][7]/nb_mon,arrets[s][8]/nb_sat,arrets[s][9]/nb_sat,arrets[s][10]/nb_sun,arrets[s][11]/nb_sun])
                except:
                    print(arrets[s][1])
                l_noeuds.addFeature(g_noeuds)
        del(arrets)
        del(l_noeuds)
        del(l_links)
        del(l_arcs)
        return {self.REP_GTFS: self.REP_GTFS}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'gtfs_import'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('GTFS import')

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
		
    def shortHelpString(self):
        return self.tr("""
        Scan a GTFS folder and generates the layer of stops, and the layer of simplified arcs and lines
		Computes the transport offer for the specified time period  and calendar (number of stops)
        
        Parameters:
            GTFS_folder : GTFS folder path
			calendar start: calendar date of the first day of the period (dd/mm/YYYY)
			calendar_end: calendar date of the last day of the period (dd/mm/YYYY)
			start_time: start time of the period (hh:mm:ss)
			end_time: end time of the period (hh:mm:ss)
			table names: root for generated tables (ex: IC => IC_nodes.shp, IC_arcs.shp and IC_lines.shp)
			CRS: generated tables CRS
			encoding: encoding
			
			
        """)
        
		
		
    def tr(self, string):
        return QCoreApplication.translate('ImportGTFS', string)

    def createInstance(self):
        return ImportGTFS()
