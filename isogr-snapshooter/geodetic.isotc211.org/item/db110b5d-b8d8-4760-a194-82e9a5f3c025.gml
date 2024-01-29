<?xml version="1.0" encoding="UTF-8"?>
<gml:GeodeticCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-455">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/455</gml:identifier>
  <gml:name>NAD 83 (PACP00) - LatLonEHt</gml:name>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>157.47</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>-151.27</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>-17.56</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>31.8</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing</gml:scope>
  <gml:ellipsoidalCS>
    <gml:EllipsoidalCS gml:id="iso-cs-46">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/46</gml:identifier>
      <gml:name>Ellipsoidal 3D CS. Axes: latitude, longitude, ellipsoidal height. Orientations: north, east, up. UoM: degree, degree, metre.</gml:name>
      <gml:remarks>Used in geographic 3D coordinate reference systems. Horizontal coordinates referenced to this CS are in degrees. Any degree representation (e.g. DMSH, decimal, etc.) may be used but that used must be declared for the user.</gml:remarks>
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
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-36" uom="3">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/36</gml:identifier>
          <gml:name>Ellipsoidal height</gml:name>
          <gml:remarks>Used only as part of an ellipsoidal 3D coordinate system in a geographic 3D coordinate reference system, never on its own.</gml:remarks>
          <gml:axisAbbrev>h</gml:axisAbbrev>
          <gml:axisDirection>up</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
    </gml:EllipsoidalCS>
  </gml:ellipsoidalCS>
  <gml:geodeticDatum>
    <gml:GeodeticDatum gml:id="iso-datum-113">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/113</gml:identifier>
      <gml:name>North American Datum of 1983 (PACP00)</gml:name>
      <gml:remarks>Replaces NAD83 (HARN). Replaced by NAD83(PA11) from 2011-09-06. </gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>157.47</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>-151.27</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>-17.56</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>31.8</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>Realization of the NAD83. The frame is defined by a time-dependent seven parameter transformation of ITRF2000 3D geocentric Cartesian coordinates and velocities at reference epoch  1993.62. The frame is kept aligned to the Pacific plate at other epochs based on an Euler pole calculated from 16 sites located on the North American, Mariana, and Pacific plates. The original web listing erroneously showed values for this frame as being identical to  NAD83 (CORS96) Epoch 2002. However, the original HTDP (version 2.7) implementation used the transformation given in the reference.</gml:anchorDefinition>
      <gml:realizationEpoch>2003</gml:realizationEpoch>
      <gml:primeMeridian>
        <gml:PrimeMeridian gml:id="iso-primemeridian-25">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/25</gml:identifier>
          <gml:name>Greenwich</gml:name>
          <gml:greenwichLongitude uom="8">0.0</gml:greenwichLongitude>
        </gml:PrimeMeridian>
      </gml:primeMeridian>
      <gml:ellipsoid>
        <gml:Ellipsoid gml:id="iso-ellipsoid-27">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/27</gml:identifier>
          <gml:name>GRS 1980</gml:name>
          <gml:remarks>Adopted by IUGG 1979 Canberra. Inverse flattening is derived from geocentric gravitational constant GM = 3986005e8 m*m*m/s/s, dynamic form factor J2 = 108263e-8 and Earth's angular velocity = 7292115e-11 rad/s.</gml:remarks>
          <gml:semiMajorAxis uom="3">6378137.0</gml:semiMajorAxis>
          <gml:secondDefiningParameter>
            <gml:SecondDefiningParameter>
              <gml:inverseFlattening uom="3">298.257222101</gml:inverseFlattening>
            </gml:SecondDefiningParameter>
          </gml:secondDefiningParameter>
        </gml:Ellipsoid>
      </gml:ellipsoid>
    </gml:GeodeticDatum>
  </gml:geodeticDatum>
</gml:GeodeticCRS>