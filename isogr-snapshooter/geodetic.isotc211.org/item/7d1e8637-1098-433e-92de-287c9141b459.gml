<?xml version="1.0" encoding="UTF-8"?>
<gml:VerticalCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-438">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/438</gml:identifier>
  <gml:name>NZVD2009 - NOHt</gml:name>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>160.0</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>-170.0</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>-60.0</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>-25.0</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing.</gml:scope>
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
    <gml:VerticalDatum gml:id="iso-datum-170">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/170</gml:identifier>
      <gml:name>New Zealand Vertical Datum 2009</gml:name>
      <gml:remarks>Replaced by NZVD2016 from 2016-06-27. Normal orthometric heights.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>160.0</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>-170.0</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>-60.0</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>-25.0</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>New Zealand Quasigeoid 2009 which is defined by the application of the NZ quasigeoid 2009 grid to NZGD2000 ellipsoidal heights at epoch 2000.0.</gml:anchorDefinition>
      <gml:realizationEpoch>2009-09-14</gml:realizationEpoch>
    </gml:VerticalDatum>
  </gml:verticalDatum>
</gml:VerticalCRS>