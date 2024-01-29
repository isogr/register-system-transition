<?xml version="1.0" encoding="UTF-8"?>
<gml:VerticalCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-765">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/765</gml:identifier>
  <gml:name>EVRF2019 - NHt</gml:name>
  <gml:remarks>European Vertical Reference  Frame 2019 in zero tide system. See EVRF2019mean-NHt for mean-tide realization of EVRF2019. Replaces EVRF2007-NHt.</gml:remarks>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>-9.56</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>69.16</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>35.95</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>77.07</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing </gml:scope>
  <gml:verticalCS>
    <gml:VerticalCS gml:id="iso-cs-42">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/42</gml:identifier>
      <gml:name>Vertical CS. Axis: height (H). Orientation: up. UoM: m.</gml:name>
      <gml:remarks>Used in vertical coordinate reference systems.</gml:remarks>
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-35" uom="3">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/35</gml:identifier>
          <gml:name>Gravity-related height</gml:name>
          <gml:remarks>Used in a 1D vertical coordinate system.</gml:remarks>
          <gml:axisAbbrev>H</gml:axisAbbrev>
          <gml:axisDirection>up</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
    </gml:VerticalCS>
  </gml:verticalCS>
  <gml:verticalDatum>
    <gml:VerticalDatum gml:id="iso-datum-763">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/763</gml:identifier>
      <gml:name>European Vertical Reference Frame 2019</gml:name>
      <gml:remarks>EVRF2019 is realized by an adjustment of geopotential numbers of the Unified European Levelling Network in the zero-tide system, followed by computation of Normal heights, referenced to the GRS80 ellipsoid. Measurements of BY, CH, DK, EE, FI, LT, LV, NO, RU, SE were reduced to epoch 2000 using the vertical velocity model NKG2016LU for Nordic countries and a set of velocities for Switzerland, provided by Swisstopo. See EVRF2019mean for the mean-tide realization of EVRF2019. Replaces EVRF2007.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>-9.56</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>69.16</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>35.95</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>77.07</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>Height at Normal Amsterdams Peil (NAP) is zero, realised by least squares fit to 12 datum points of EVRF2007 solution.</gml:anchorDefinition>
      <gml:realizationEpoch>2020-01-09T00:00:00.000Z</gml:realizationEpoch>
    </gml:VerticalDatum>
  </gml:verticalDatum>
</gml:VerticalCRS>