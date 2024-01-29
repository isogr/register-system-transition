<?xml version="1.0" encoding="UTF-8"?>
<gml:VerticalCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-323">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/323</gml:identifier>
  <gml:name>CGVD28 - NOHt</gml:name>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>-141.01</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>-59.73</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>41.67</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>69.8</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing</gml:scope>
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
    <gml:VerticalDatum gml:id="iso-datum-102">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/102</gml:identifier>
      <gml:name>Canadian Geodetic Vertical Datum of 1928</gml:name>
      <gml:remarks>Adopted by Federal Order in Council in 1935. Replaced by CGVD2013 November 2013. Normal orthometric heights.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>-141.01</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>-59.73</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>41.67</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>69.8</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>CGVD28 is a levelling-based vertical datum based on mean sea level determined at five tidal gauges in Yarmouth and Halifax on the Atlantic Ocean, Pointe-au-Père on the St-Lawrence River, and Vancouver and Prince-Rupert on the Pacific Ocean. The definition also includes an elevation at a bench mark in Rouses Point, NY (next to Lake Champlain), accepted as fixed by the United States and Canada in 1925. The datum was propagated inland from the tide gauges using geodetic levelling measurements. The vertical datum is accessible through some 94,000 bench marks anchored to the ground and stable structures. Heights in  CGVD28 are normal-orthometric based on normal gravity.</gml:anchorDefinition>
      <gml:realizationEpoch>1928</gml:realizationEpoch>
    </gml:VerticalDatum>
  </gml:verticalDatum>
</gml:VerticalCRS>