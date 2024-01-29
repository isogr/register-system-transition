<?xml version="1.0" encoding="UTF-8"?>
<gml:GeodeticCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-802">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/802</gml:identifier>
  <gml:name>ITRF2020 - XYZ</gml:name>
  <gml:remarks>Replaces ITRF2014 - XYZ.</gml:remarks>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>-180.0</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>180.0</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>-90.0</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>90.0</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing</gml:scope>
  <gml:cartesianCS>
    <gml:CartesianCS gml:id="iso-cs-45">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/45</gml:identifier>
      <gml:name>Geocentric 3D right-handed Cartesian CS. Axes: Geocentric X,Y,Z. Orientation: Z to North Pole, [X and Y in the equatorial plane, X at Prime Meridian | X in the equatorial plane at the Prime Meridian]. UoM: m.</gml:name>
      <gml:remarks>Used in geocentric coordinate reference systems.</gml:remarks>
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-33" uom="3">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/33</gml:identifier>
          <gml:name>Geocentric X</gml:name>
          <gml:axisAbbrev>X</gml:axisAbbrev>
          <gml:axisDirection>Geocentre &amp;gt; equator/0°E</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-37" uom="3">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/37</gml:identifier>
          <gml:name>Geocentric Y</gml:name>
          <gml:axisAbbrev>Y</gml:axisAbbrev>
          <gml:axisDirection>Geocentre &amp;gt; equator/90°E</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-39" uom="3">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/39</gml:identifier>
          <gml:name>Geocentric Z</gml:name>
          <gml:axisAbbrev>Z</gml:axisAbbrev>
          <gml:axisDirection>Geocentre &amp;gt; north pole</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
    </gml:CartesianCS>
  </gml:cartesianCS>
  <gml:geodeticDatum>
    <gml:GeodeticDatum gml:id="iso-datum-801">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/801</gml:identifier>
      <gml:name>International Terrestrial Reference Frame 2020</gml:name>
      <gml:remarks>Replaces ITRF2014. This is a purely Cartesian reference frame with no ellipsoid defined. GRS80 is the ellipsoid recommended by the IAG and IERS.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>-180.0</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>180.0</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>-90.0</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>90.0</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial positioning</gml:scope>
      <gml:anchorDefinition>Realisation of the IERS Terrestrial Reference System (ITRS) at reference epoch 2015.0. Origin of the long-term frame is defined using the concept of internal constraints such that there are zero translation parameters at epoch 2015.0 and zero translation rates between the ITRF2020 and the ILRS SLR long-term frame over the time-span 1993.0-2021.0. Scale of the long-term frame is defined using the concept of internal constraints such that there are zero scale and scale rate between ITRF2020 and the scale and scale rate averages of VLBI selected sessions up to 2013.75 and SLR weekly solutions covering the time-span 1997.7-2021.0. Orientation is defined such that there are zero rotation parameters at epoch 2015.0 and zero rotation rates between the ITRF2020 and ITRF2014.  The datum is defined by a set of 3 dimensional Cartesian station coordinates, velocities, annual and semi-annual seasonal terms, and post-seismic deformation models given by the citations.</gml:anchorDefinition>
      <gml:realizationEpoch>2022-04-15</gml:realizationEpoch>
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