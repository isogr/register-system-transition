<?xml version="1.0" encoding="UTF-8"?>
<gml:GeodeticCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-246">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/246</gml:identifier>
  <gml:name>NAD27 - LatLon</gml:name>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>167.65</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>-47.74</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>7.98</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>83.17</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
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
    <gml:GeodeticDatum gml:id="iso-datum-104">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/104</gml:identifier>
      <gml:name>North American Datum of 1927</gml:name>
      <gml:remarks>Replaced by NAD27(76) in Ontario, CGQ77 in Quebec, Mexican Datum of 1993 in Mexico, NAD83(1986) in Canada (excl. Ontario &amp; Quebec) &amp; USA.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>167.65</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>-47.74</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>7.98</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>83.17</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>Fundamental point: Meade&amp;apos;s Ranch. Latitude: 39°13&amp;apos;26.686&amp;quot;N, longitude: 98°32&amp;apos;30.506&amp;quot;W (of Greenwich). Note: this CRS includes longitudes which are POSITIVE EAST. </gml:anchorDefinition>
      <gml:realizationEpoch>1927-01-01</gml:realizationEpoch>
      <gml:primeMeridian>
        <gml:PrimeMeridian gml:id="iso-primemeridian-25">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/25</gml:identifier>
          <gml:name>Greenwich</gml:name>
          <gml:greenwichLongitude uom="8">0.0</gml:greenwichLongitude>
        </gml:PrimeMeridian>
      </gml:primeMeridian>
      <gml:ellipsoid>
        <gml:Ellipsoid gml:id="iso-ellipsoid-28">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/28</gml:identifier>
          <gml:name>Clarke 1866</gml:name>
          <gml:remarks>Original definition a=20926062 and b=20855121 (British) feet. Uses Clarke's 1865 inch-metre ratio of 39.370432 to obtain metres. Metric value then converted to US survey feet for use in the US and international feet for use in Cayman Islands.</gml:remarks>
          <gml:semiMajorAxis uom="3">6378206.4</gml:semiMajorAxis>
          <gml:secondDefiningParameter>
            <gml:SecondDefiningParameter>
              <gml:semiMinorAxis uom="3">6356583.8</gml:semiMinorAxis>
            </gml:SecondDefiningParameter>
          </gml:secondDefiningParameter>
        </gml:Ellipsoid>
      </gml:ellipsoid>
    </gml:GeodeticDatum>
  </gml:geodeticDatum>
</gml:GeodeticCRS>