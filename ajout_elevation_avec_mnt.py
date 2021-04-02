"""
ajout_elevation_avec_mnt.py
Pierre-Olivier Vandanjon
2 avril 2021
en test

Ce script entrée une carte openstreemat
sortie : 
    carte openstreetmat avec élévation issue des modèles numériques de terrain 
    disponivles sur le site geoportail en libre depuis le 1er janvier 2021
    et utiliser les données libres depuis le 1er janvier 2021
https://geoservices.ign.fr/documentation/diffusion/telechargement-donnees-libres.html
https://geoservices.ign.fr/documentation/diffusion/telechargement-donnees-libres.html#rge-alti-1-m

hypothèses
    les altitudes sont positives
    
Amélioration 
    Il manque des fichiers de modèle numérique de terrains, dans ce cas, on ne met pas de champs ele
    voir la listes fichiers_manquants

   La formule pour calculer l'altitude n'est pas terrible 
       car si on est sur un point nous ne donnons pas la valeur de ce point 
       il faut faire une fonction mieux adaptée

"""
import math
import numpy as np
from lxml import etree
from copy import deepcopy
from pyproj import Transformer

"""
Entrées et Sorties du script
"""
file_territoire="La_Brossiere.osm"
file_output=file_territoire.replace(".","_avec_elevation_mnt.")

"""
constantes globale
chemin_mnt : chemin dans lequel se trouve les modèles numériques de terrain
wgs_to_lambert93 : 
"""
chemin_mnt="data//"
wgs_to_lambert93 = Transformer.from_crs("epsg:4326","epsg:2154")

"""
test unitaire fait le prmeier avritl
xinv, yinv est bien égal à x,y

#x,y = 882408.3,6543019.6
#transformer = Transformer.from_crs("epsg:2154","epsg:4326")
#lat, lon=transformer.transform(x, y)
#transformer_inv = Transformer.from_crs("epsg:4326","epsg:2154")
#xinv,yinv=transformer_inv.transform(lat,lon)

#test unitaire fait le prmeier avritl
# sur le départ 
# erreur de 5 cm avec dep_x_geoportail maris erreur de 80cm sur dep_y_geoportail !

dep_lat_geoportail, dep_lon_geoportail, dep_alt_geoportail=46.810403, -1.139134, 101.72 
dep_x_geoportail, dep_y_geoportail, dep_alt_xy= 384522.35, 6642742.66, 101.72
dep_x_pyproj,dep_y_pyproj=transformer_inv.transform(dep_lat_geoportail,dep_lon_geoportail) # erreur de 5 cm avec dep_x_geoportail maris erreur de 80cm sur dep_y_geoportail !

"""


"""
fonction get_alti
entrées
x=latitude en WGS 84 issue de openstreet map, degrés décimaux
y=longitude en WGS 84 issue de openstreet map, degrés décimaux
sortie
altitude : en m 
cette altitude est calculée à partir des modèles numériques de terrain

Variable globale utilisée

fichiers_charges : liste des fichiers chargés
list_entete
liste_altis

constante globale utilisée
chemin_mnt 
wgs_to_lambert93 : 

test unitaire
a=get_alti(dep_lat_geoportail, dep_lon_geoportail)
a
Out[20]: 101.70000000000002

"""

"""
Variables globales
"""
fichiers_charges=[]
fichiers_manquants=[]
liste_entetes=[]
liste_altis=[]

def get_alti(lat,lon):
    global fichiers_charges, liste_altis, liste_entetes, fichiers_manquants
    def complete(x,longueur):
        if len(x)<longueur:
            x=(longueur-len(x))*'0'+x
        return x
    def projet_carre(nc,nl): # projette les indices dans le carré de la matrice et signale un problème sinon 
        delta=0.0001        
        if nc<=0:
            if nc<=-1:
                print("il y a un problème sur les xllcorner et les yllcorne par rapport au x et y")
                return -1
            else:
                nc=delta
        if nc>=999:
            if nc>=1000:
                print("il y a un problème sur les xllcorner et les yllcorne par rapport au x et y")
                return -1
            else:
                nc=999-delta
        if nl<=0:
            if nl<=-1:
                print("il y a un problème sur les xllcorner et les yllcorne par rapport au x et y")
                return -1
            else:
                nl=delta
        if nl>=999:
            if nl>=1000:
                print("il y a un problème sur les xllcorner et les yllcorne par rapport au x et y")
                return -1
            else:
                nl=999-delta
                
        ncf,nlf=math.ceil(nc), math.ceil(nl)
        nci,nli=math.floor(nc), math.floor(nl)
        return nci, ncf-nc, ncf, nc-nci, nli, nlf-nl, nlf, nl-nli
    x,y=wgs_to_lambert93.transform(lat,lon)
    len_nom=4
    X=complete(str(math.floor(x/1000)),len_nom)
    Y=complete(str(math.ceil(y/1000)),len_nom)
    nomfich="RGEALTI_FXX_"+X+"_"+Y+"_MNT_LAMB93_IGN69.asc"   
    file_mnt=chemin_mnt+nomfich
    if not(nomfich in fichiers_charges):
        try:
            alti=np.loadtxt(file_mnt,skiprows=6)
            entete=np.loadtxt(file_mnt,skiprows=2,max_rows=2,usecols=1)
        except:
            print(file_mnt+" n existe pas ")
            fichiers_manquants.append(nomfich)
            return -1
        fichiers_charges.append(nomfich)
        liste_altis.append(alti)
        liste_entetes.append(entete)
    k=fichiers_charges.index(nomfich)
    altis=liste_altis[k]
    entete=liste_entetes[k]
    xllcorner=entete[0]
    yllcorner=entete[1]
    nc,nl=x-xllcorner, y-yllcorner
    try: 
        nci, coef_nci, ncf, coef_ncf, nli, coef_nli, nlf, coef_nlf=projet_carre(nc,nl)
    except:
        return -1 # 
    
    return (altis[-nli-1, nci]*coef_nci*coef_nli+ altis[-nli-1, ncf]*coef_ncf*coef_nli+ altis[-nlf-1, nci]*coef_nci*coef_nlf+ altis[-nlf-1, ncf] *coef_ncf*coef_nlf)/\
    (coef_nci*coef_nli+coef_ncf*coef_nli+coef_nci*coef_nlf+coef_ncf*coef_nlf)
    
    




"""
Charger le fichier le fichier osm qui va être modifié
"""
tree = etree.parse(file_territoire)

"""
liste des noeuds qui contiennent une latitue et une longitude
"""
        
nodes=tree.xpath("/osm/node[@lat and @lon]") 
for node in nodes:
    for child in node:
        if child.attrib["k"]=="ele":
            node.remove(child)#  si il y a déjà un attribut ele on le supprime par souci de cohérence
    lat=float(node.get("lat"))
    lon=float(node.get("lon"))
    altitude=get_alti(lat,lon)
    if altitude>0:
        altitude_pt=str(round(altitude,2)) # on arrondit l'altitude à deux chiffres après la virgule
        tag=etree.Element("tag",k="ele",v=altitude_pt)
        node.append(tag)


"""
Ecrirer le fichier le fichier osm de sortie
"""
tree.write(file_output, pretty_print=True, xml_declaration=True,   encoding="utf-8")

    
    
    
    

