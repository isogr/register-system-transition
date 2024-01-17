<?xml version="1.0" encoding="UTF-8"?>
<gml:GeodeticCRS xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-1011">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/1011</gml:identifier>
  <gml:name>Korean 1985 - LatLon</gml:name>
  <gml:domainOfValidity/>
  <gml:scope>Spatial referencing</gml:scope>
  <gml:ellipsoidalCS>
    <gml:EllipsoidalCS gml:id="iso-cs-43">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/43</gml:identifier>
      <gml:name>Ellipsoidal 2D CS. Axes: latitude, longitude. Orientations: north, east. UoM: degree</gml:name>
      <gml:remarks>Used in geographic 2D coordinate reference systems. Coordinates referenced to this CS are in degrees. Any degree representation (e.g. DMSH, decimal, etc.) may be used but that used must be declared for the user by the supplier of data.</gml:remarks>
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-38" uom="6">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/38</gml:identifier>
          <gml:name>Geodetic latitude</gml:name>
          <gml:remarks>Used in geographic 2D and geographic 3D coordinate reference systems.</gml:remarks>
          <gml:axisAbbrev>Lat</gml:axisAbbrev>
          <gml:axisDirection>north</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-34" uom="6">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/34</gml:identifier>
          <gml:name>Geodetic longitude</gml:name>
          <gml:remarks>Used in geographic 2D and geographic 3D coordinate reference systems.</gml:remarks>
          <gml:axisAbbrev>Lon</gml:axisAbbrev>
          <gml:axisDirection>east</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
    </gml:EllipsoidalCS>
  </gml:ellipsoidalCS>
  <gml:geodeticDatum>
    <gml:GeodeticDatum gml:id="iso-datum-1004">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/1004</gml:identifier>
      <gml:name>Korean 1985 Datum</gml:name>
      <gml:remarks>Replaced by KGD2002</gml:remarks>
      <gml:domainOfValidity/>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>Korean 1985 Datum is the first Korean Triangulation Network based on the Bessel 1841 ellipsoid. Approximately 7,000 points had been observed with EDM and TRANSIT since 1975, and adjusted through  two campaigns by NGII. The origin of the datum was observed and determined by astronomical surveying over 4 years (1981 - 1985).</gml:anchorDefinition>
      <gml:realizationEpoch>1985-01-01T00:00:00.000Z</gml:realizationEpoch>
      <gml:primeMeridian>
        <gml:PrimeMeridian gml:id="iso-primemeridian-25">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/25</gml:identifier>
          <gml:name>Greenwich</gml:name>
          <gml:greenwichLongitude uom="8">0.0</gml:greenwichLongitude>
        </gml:PrimeMeridian>
      </gml:primeMeridian>
      <gml:ellipsoid>
        <gml:Ellipsoid gml:id="iso-ellipsoid-996">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/996</gml:identifier>
          <gml:name>Bessel 1841</gml:name>
          <gml:remarks>The Bessel ellipsoid was derived in 1841 by Friedrich Wilhelm Bessel, based on several meridian arcs and other data of continental geodetic networks of Europe, Russia and the British Survey of India. It is based on 10 meridional arcs and 38 precise measurements of astrogeodetic latitude and longitude. The dimensions of the ellipsoid axes were defined by logarithms in keeping with former calculation methods. The original axes were defined as a=3272077.14 and b=3261139.33 toise. This was based a weighted mean of values from several authors but did not account for differences in the length of the various toise. The &quot;Bessel toise&quot; is therefore of uncertain length.</gml:remarks>
          <gml:semiMajorAxis uom="3">6377397.155</gml:semiMajorAxis>
          <gml:secondDefiningParameter>
            <gml:SecondDefiningParameter>
              <gml:inverseFlattening uom="3">299.1528128</gml:inverseFlattening>
            </gml:SecondDefiningParameter>
          </gml:secondDefiningParameter>
        </gml:Ellipsoid>
      </gml:ellipsoid>
    </gml:GeodeticDatum>
  </gml:geodeticDatum>
</gml:GeodeticCRS>