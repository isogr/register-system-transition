<?xml version="1.0" encoding="UTF-8"?>
<gml:GeodeticCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-443">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/443</gml:identifier>
  <gml:name>NZGD1949 - LatLon</gml:name>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>165.87</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>179.27</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>-47.65</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>-33.89</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing.</gml:scope>
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
    <gml:GeodeticDatum gml:id="iso-datum-108">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/108</gml:identifier>
      <gml:name>New Zealand Geodetic Datum 1949</gml:name>
      <gml:remarks>Replaced by New Zealand Geodetic Datum 2000 from March 2000.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>165.87</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>179.27</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>-47.65</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>-33.89</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>Fundamental point: Papatahi. Latitude: 41°19&amp;apos; 8.900&amp;quot;S, longitude: 175°02&amp;apos;51.000&amp;quot;E (of Greenwich).</gml:anchorDefinition>
      <gml:realizationEpoch>1949</gml:realizationEpoch>
      <gml:primeMeridian>
        <gml:PrimeMeridian gml:id="iso-primemeridian-25">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/25</gml:identifier>
          <gml:name>Greenwich</gml:name>
          <gml:greenwichLongitude uom="8">0.0</gml:greenwichLongitude>
        </gml:PrimeMeridian>
      </gml:primeMeridian>
      <gml:ellipsoid>
        <gml:Ellipsoid gml:id="iso-ellipsoid-31">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/31</gml:identifier>
          <gml:name>International 1924</gml:name>
          <gml:remarks>Adopted by IUGG 1924 in Madrid. Based on Hayford 1909/1910 figures. </gml:remarks>
          <gml:semiMajorAxis uom="3">6378388.0</gml:semiMajorAxis>
          <gml:secondDefiningParameter>
            <gml:SecondDefiningParameter>
              <gml:inverseFlattening uom="3">297.0</gml:inverseFlattening>
            </gml:SecondDefiningParameter>
          </gml:secondDefiningParameter>
        </gml:Ellipsoid>
      </gml:ellipsoid>
    </gml:GeodeticDatum>
  </gml:geodeticDatum>
</gml:GeodeticCRS>