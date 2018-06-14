import arcpy, os
'''
AUTHOR: Steve
Script: Clean Census Data
Description: This scrip will CLIP a SHP with historicl census tract information to is apportity size.
Then it will reporject that CLIP into the apporiate porject.
Last it will join that  CLIP SHP with a CSV that has historical census data and make a corpleth map.
    Normalised Total Pop per census tract
'''




def ClipJoinJoin(  WKSP, NatTractSHP, CLipTract, tbl_Pop, tbl_Poverty , WKT, outPut ):


    #Set ENV
    WKSP = arcpy.env.workspace = WKSP ###JM
    arcpy.env.overwriteOutput = True
    arcpy.env.qualifiedFieldNames = False
    #Set Var

    ##Load in National Census Tract (SHP)
    NatTractSHP = NatTractSHP ###JM

    ###JM:  Add in a Make a FLyr out of NatTractSHP;  call it NatTractLYR
    NatTractLYR = arcpy.MakeFeatureLayer_management(NatTractSHP, os.path.basename( NatTractSHP ).split(".")[0] )

    ##Load in City Limmit(SHP). (used to clip down national data set)

    CLipTract = CLipTract ###JM
    ###JM:  Add in a Make a FLyr out of CLipTract;  call it CLipTractLYR
    CLipTractLYR = arcpy.MakeFeatureLayer_management(CLipTract, os.path.basename( CLipTract ).split(".")[0])


    ## Load in CSV with Census Data (To be Normilzed)

    #tbl_Pop =  arcpy.MakeTableView_management(tbl_Pop , os.path.basename( tbl_Pop ).split(".")[0])
    ###JM:  (1)complete the path, (2)Add in a Make a tbl view out of csv;  call it tbl_*
    Join_tbl_Pop = "GJOIN{0}T_Pop".format(os.path.basename( NatTractSHP ).split(".")[0])###JM



    ## Load in CSV with Census Data (Factor)

    #tbl_Poverty = arcpy.MakeTableView_management(tbl_Poverty ,os.path.basename( tbl_Poverty ).split(".")[0])
    ###JM:  (1)complete the path, (2)Add in a Make a tbl view out of csv;  call it tbl_*
    JoinFeildCSV = "GJOIN{0}".format(os.path.basename( NatTractSHP ).split(".")[0])###JM

    #Clip National Census Tract by City Limmit
    ClippedSHP = arcpy.Clip_analysis(NatTractLYR, CLipTractLYR, WKSP)

    ClippedLYR = arcpy.MakeFeatureLayer_management(ClippedSHP, os.path.basename( NatTractSHP ).split(".")[0] + "_clipped")

    JoinFeild = "GISJOIN"###JM


    #Join Clip Census Tract to CSV CensusTract
    JSHP = arcpy.AddJoin_management(ClippedLYR, JoinFeild, tbl_Poverty, JoinFeildCSV)
    JSHP = arcpy.AddJoin_management(ClippedLYR, JoinFeild, tbl_Pop, Join_tbl_Pop)

    cp_JSHP = arcpy.CopyFeatures_management( JSHP, "c_" + outPut ###JM
                                             )

    #project in Oregon State Plan North
    


    #out_coordinate_system = arcpy.SpatialReference(' well known')



    JSHP = arcpy.Project_management(cp_JSHP, outPut ###JM
                                    , wkt)


    #Symbole by grad color to make clorplath

    #arcpy.ApplySymbologyFromLayer_management("JSHP", "sf_points_water.lyr")


    

    return JSHP

    

wkt = '''PROJCS["NAD83(NSRS2007) / Oregon North",
        GEOGCS["NAD83(NSRS2007)",
            DATUM["NAD83_National_Spatial_Reference_System_2007",
                SPHEROID["GRS 1980",6378137,298.257222101,
                    AUTHORITY["EPSG","7019"]],
                TOWGS84[0,0,0,0,0,0,0],

                AUTHORITY["EPSG","6759"]],
            PRIMEM["Greenwich",0,
                AUTHORITY["EPSG","8901"]],
            UNIT["degree",0.0174532925199433,
                AUTHORITY["EPSG","9122"]],
            AUTHORITY["EPSG","4759"]],
        PROJECTION["Lambert_Conformal_Conic_2SP"],
        PARAMETER["standard_parallel_1",46],
        PARAMETER["standard_parallel_2",44.33333333333334],
        PARAMETER["latitude_of_origin",43.66666666666666],
        PARAMETER["central_meridian",-120.5],
        PARAMETER["false_easting",2500000],
        PARAMETER["false_northing",0],
        UNIT["metre",1,
            AUTHORITY["EPSG","9001"]],
        AXIS["X",EAST],
        AXIS["Y",NORTH],
        AUTHORITY["EPSG","3645"]]'''###JM

WKSP = arcpy.env.workspace = r"C:\Users\Student\Desktop\WKSP\Test"###JM

#NatTractSHP = r"C:\Users\Student\Desktop\NationalTract\1970.shp"###JM
NatTract_wksp = r"C:\Users\Student\Desktop\NationalTract" ###JM
arcpy.env.workspace = NatTract_wksp
NatTract_dict = { shp.replace(".shp","") : os.path.join( NatTract_wksp, shp) for shp in arcpy.ListFeatureClasses()}
NatTract_list = NatTract_dict.keys()

CLipTract = r"C:\Users\Student\Desktop\Clip\POR_1970_Below_Poverty.shp"###JM

tbl_Pop =  arcpy.MakeTableView_management(r"C:\Users\Student\Desktop\POP\Pop_Tract_1950-2010_POR_SF_SEA.csv"###JM
                                          , "tbl_Pop")
tbl_1970BPoverty = arcpy.MakeTableView_management(r"C:\Users\Student\Desktop\Below\1970-2012_Below_Poverty_CenusTract.csv"###JM
                                                  ,"tbl_1970BPoverty")

clipTrack_Dict = {"Portland" : r"C:\Users\Student\Desktop\Clip\POR_1970_Below_Poverty.shp"
                  , "San_Francisco" : r"C:\Users\Student\Desktop\Clip\SF_1970.shp"
                  , "Seattle" : r"C:\Users\Student\Desktop\Clip\SEA_1970_CLIP.shp" }

clipTrack_List = clipTrack_Dict.keys()



for CLipTract_Key in clipTrack_List:  #Looping City

    for NatTract_key in NatTract_list:  #Looping decade on national level
    
        ClipJoinJoin(WKSP, NatTract_dict[NatTract_key], clipTrack_Dict[CLipTract_Key], tbl_Pop, tbl_1970BPoverty, wkt, CLipTract_Key + "_" + NatTract_key + ".shp")


print "I'm a BOSSS!!!!!"

