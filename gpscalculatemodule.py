#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version:   2.0
# Homepage:   http://custom-build-robots.com

# Dieses Programm berechnet die horizontale Entfernung zwischen
# zwei vorgegebenen GPS Koordinaten sowie den Kurswinkel.
# Um dieses Programm zu testen muessen Sie es in einem anderen
# Programm einbinden welches dieses als Modul einbindet und 
# die berechneten Werte ausgibt.

from math import *

# Die Funktion calc nimmt die Start und Ziel Laengen und
# Breitengrade entgegen und gibt die Entfernung und den
# Kurswinkel zwischen den Punkten als Werte zurueck.
def calc(lat1, lon1, lat2, lon2):

   lat1 = lat1 # Start Laengengrad
   lon1 = lon1 # Start Breitengrad
   lat2 = lat2 # Ziel Laengengrad
   lon2 = lon2 # Zeil Breitengrad


   # Erste Zwischenrechnung:
   # Die Grad Werte der Start- und Zielkoordinaten werden mit der
   # Python Funktion radians() und dem Aufruf map(radians) in 
   # Radiant Werte umgerechnet.
   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

   # Zweite Zwischenrechnung:
   # Entsprechend der Haversine Formel und fuer die einfachere
   # Programmierung wird hier in einem separaten Schritt eine
   # Zwischenberechnung durchgefuerht und die Laengen- und Breiten
   # Radiant Werte der Punkte Z und S voneinander abgezogen.
   hav_lat = lat2 - lat1
   hav_lon = lon2 - lon1

   # Dritte Zwischenrechnung:
   # Es wird als Vorbereitung auf die Wurzelrechnung der Radikant
   # ra der Wurzel separat berechnet.
   ra = sin(hav_lat/2)**2 + cos(lat1) * cos(lat2) * sin(hav_lon/2)**2

   # Vierte Zwischenrechnung
   # Es wird der vertikale Winkel sowie die Wurzel berechnet.
   v_angle = asin(sqrt(ra)) 

   # Berechnung der Entfernung:
   # Es wird die eigentliche Entfernung zwischen den Punkten S und
   # Z berechnet in Metern.
   h_distance = 2 * 6367 * v_angle * 1000

   # In der folgenden Formel wird der Kurswinkel berechnet.
   angle = atan2(sin(hav_lon) * cos(lat2), cos(lat1) \
   * sin(lat2) - sin(lat1) * cos(lat2) * cos(hav_lon))

   # Es wird der berechnete Winkel von Radiant in Grad umgerechnet.
   angle = degrees(angle)
   x=h_distance*sin(angle)
   y=h_distance*cos(angle)
   # Es werden die beiden Werte Entfernung und Kurswinkel zurueck
   # gegeben.
   return h_distance, angle,x,y
# Ende des Programmes
