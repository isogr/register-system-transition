<?xml version="1.0" encoding="UTF-8"?>
<gml:GeodeticCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-270">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/270</gml:identifier>
  <gml:name>NAD 83 (1986) - LatLon</gml:name>
  <gml:remarks>This CRS includes longitudes which are POSITIVE EAST. The adjustment included connections to Greenland and Mexico but the system has not been adopted there. Except in Alaska, for applications with an accuracy of better than 1m replaced by NAD83(HARN).</gml:remarks>
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
            <gco:Decimal>14.92</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>86.46</gco:Decimal>
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
    <gml:GeodeticDatum gml:id="iso-datum-161">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/161</gml:identifier>
      <gml:name>North American Datum of 1983</gml:name>
      <gml:remarks>The 1986 adjustment includes connections to Greenland and Mexico but the system has not been adopted there. A set of numerical horizontal crustal motion models for California, Nevada, parts of Alaska and Hawaii were used to estimate horizontal velocities in order to convert geodetic observations from their original epoch to 1984.0. For other parts of the network, no datum realization epoch exists (datum is a mix of observations from different eras). Replaced NAD27 in Canada and U.S. Replaced by NAD 83 (HARN) in US and NAD83(CSRS96) v1 in Canada.</gml:remarks>
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
                <gco:Decimal>14.92</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>86.46</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>Original 1986 horizontal network adjusment. The origin, scale and orientation of the frame are nominally defined to be that for the BIH Terrestrial System 1984 (BTS84) with origin at the approximate geocentre. NAD83 Doppler stations in the Doppler reference frame NWL 9D were brought into alignment with BTS84 using an internationally adopted transformation.</gml:anchorDefinition>
      <gml:realizationEpoch>1986</gml:realizationEpoch>
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