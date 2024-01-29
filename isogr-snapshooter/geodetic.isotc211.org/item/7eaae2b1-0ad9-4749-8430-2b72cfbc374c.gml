<?xml version="1.0" encoding="UTF-8"?>
<gml:VerticalCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-780">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/780</gml:identifier>
  <gml:name>KSA-VRF14 - OHt</gml:name>
  <gml:remarks>Orthometric height</gml:remarks>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>34.51</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>55.67</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>16.37</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>32.16</gco:Decimal>
          </gmd:northBoundLatitude>
        </gmd:EX_GeographicBoundingBox>
      </gmd:geographicElement>
    </gmd:EX_Extent>
  </gml:domainOfValidity>
  <gml:scope>Spatial referencing.</gml:scope>
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
    <gml:VerticalDatum gml:id="iso-datum-776">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/776</gml:identifier>
      <gml:name>Kingdom of Saudi Arabia Vertical Reference Frame Jeddah 2014</gml:name>
      <gml:remarks>Helmert-orthometric heights realized by the National Vertical Network (NVN). KSA-VRF14 replaces all previous vertical datums including KSA-JED69, KSA-SVD71 and KSA-SVD78.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>34.51</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>55.67</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>16.37</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>32.16</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>Mean sea level at Jeddah tide gauge represented by an orthometric height of 1.7446 m at bench mark TGBM-B in a tide free system at epoch 2014.75.</gml:anchorDefinition>
      <gml:realizationEpoch>2014-01-10T00:00:00.000Z</gml:realizationEpoch>
    </gml:VerticalDatum>
  </gml:verticalDatum>
</gml:VerticalCRS>