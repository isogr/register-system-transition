<?xml version="1.0" encoding="UTF-8"?>
<gml:VerticalCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-771">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/771</gml:identifier>
  <gml:name>IGLD (1985) - DHt</gml:name>
  <gml:remarks>Dynamic heights. Equivalent to NAVD88 dynamic heights except that Hydraulic Correctors are applied to the heights of a lake's water levels, excluding rivers and interconnection channels, for the management and regulation of water levels and flows throughout the Great Lakes.</gml:remarks>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>-93.17</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>-54.75</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>40.99</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>52.22</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing, navigation and hydraulic &amp; hydrologic applications.</gml:scope>
  <gml:verticalCS>
    <gml:VerticalCS gml:id="iso-cs-41">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/41</gml:identifier>
      <gml:name>Vertical CS. Axis: height (H). Orientation: up. UoM: ftUS.</gml:name>
      <gml:remarks>Used in vertical coordinate reference systems.</gml:remarks>
      <gml:axis>
        <gml:CoordinateSystemAxis gml:id="iso-csaxis-32" uom="7">
          <gml:description/>
          <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/32</gml:identifier>
          <gml:name>Gravity-related height</gml:name>
          <gml:remarks>Used in a 1D vertical coordinate system.</gml:remarks>
          <gml:axisAbbrev>H</gml:axisAbbrev>
          <gml:axisDirection>up</gml:axisDirection>
        </gml:CoordinateSystemAxis>
      </gml:axis>
    </gml:VerticalCS>
  </gml:verticalCS>
  <gml:verticalDatum>
    <gml:VerticalDatum gml:id="iso-datum-769">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/769</gml:identifier>
      <gml:name>International Great Lakes Datum (1985)</gml:name>
      <gml:remarks>Dynamic heights. Equivalent to NAVD88 dynamic heights except that Hydraulic Correctors are applied to the heights of a lake's water levels, excluding rivers and interconnection channels, for the management and regulation of water levels and flows throughout the Great Lakes. Replaces IGLD (1955).</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>-93.17</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>-54.75</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>40.99</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>52.22</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing, navigation and hydraulic &amp; hydrologic applications.</gml:scope>
      <gml:anchorDefinition>Reference zero defined by the mean water level at tide gauges at Pointe-au-Pere (1970-1983) and Rimouski (1984-1988) with an elevation of 6.273 m at bench mark 1250-G. The datum is realized by that part of the NAVD88 first-order levelling network from Pointe-au-Pere to the head of the Great Lakes - St. Lawrence River system.</gml:anchorDefinition>
      <gml:realizationEpoch>1992</gml:realizationEpoch>
    </gml:VerticalDatum>
  </gml:verticalDatum>
</gml:VerticalCRS>