<?xml version="1.0" encoding="UTF-8"?>
<gml:VerticalCRS xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gml="http://www.opengis.net/gml/3.2" gml:id="iso-crs-965">
  <gml:description/>
  <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/965</gml:identifier>
  <gml:name>CGVD2013(CGG2013a) epoch 1997 - OHt</gml:name>
  <gml:remarks>CGVD2013 heights at epoch 1997.0.</gml:remarks>
  <gml:domainOfValidity>
    <gmd:EX_Extent>
      <gmd:geographicElement>
        <gmd:EX_GeographicBoundingBox>
          <gmd:westBoundLongitude>
            <gco:Decimal>-141.01</gco:Decimal>
          </gmd:westBoundLongitude>
          <gmd:eastBoundLongitude>
            <gco:Decimal>-47.74</gco:Decimal>
          </gmd:eastBoundLongitude>
          <gmd:southBoundLatitude>
            <gco:Decimal>40.04</gco:Decimal>
          </gmd:southBoundLatitude>
          <gmd:northBoundLatitude>
            <gco:Decimal>90.0</gco:Decimal>
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
    <gml:VerticalDatum gml:id="iso-datum-963">
      <gml:description/>
      <gml:identifier codeSpace="urn:ietf:rfc:1738">geodetic.isotc211.org/register/geodetic/items/963</gml:identifier>
      <gml:name>Canadian Geodetic Vertical Datum of 2013 (Canadian Gravimetric Geoid of 2013a) Epoch 1997</gml:name>
      <gml:remarks>Heights are at epoch 1997.0.</gml:remarks>
      <gml:domainOfValidity>
        <gmd:EX_Extent>
          <gmd:geographicElement>
            <gmd:EX_GeographicBoundingBox>
              <gmd:westBoundLongitude>
                <gco:Decimal>-141.01</gco:Decimal>
              </gmd:westBoundLongitude>
              <gmd:eastBoundLongitude>
                <gco:Decimal>-47.74</gco:Decimal>
              </gmd:eastBoundLongitude>
              <gmd:southBoundLatitude>
                <gco:Decimal>40.04</gco:Decimal>
              </gmd:southBoundLatitude>
              <gmd:northBoundLatitude>
                <gco:Decimal>90.0</gco:Decimal>
              </gmd:northBoundLatitude>
            </gmd:EX_GeographicBoundingBox>
          </gmd:geographicElement>
        </gmd:EX_Extent>
      </gml:domainOfValidity>
      <gml:scope>Spatial referencing</gml:scope>
      <gml:anchorDefinition>CGVD2013(CGG2013a) is a gravimetric datum defined by the Canadian Gravimetric Geoid of 2013a (CGG2013a), referenced to the NAD83(CSRS) v6 geodetic datum. The geoid-based datum is defined by the equipotential surface Wo=62,636,856.0 m*m/s/s, representing by convention the coastal mean sea level for North America. The definition and geopotential value comes from an agreement between Canada and the USA. The Canadian Gravimetric Geoid of 2013a (CGG2013a) is the second realization of the CGVD2013 vertical datum and is considered static. It is available in both the NAD83(CSRS) and ITRF2008 geometric reference frames using the GRS80 ellipsoid, making it compatible with space-based positioning techniques. Heights in CGVD2013(CGG2013a) epoch 1997.0 are orthometric and can be obtained from NAD83(CSRS) v6 or ITRF2008 ellipsoidal heights at epoch 1997.0 by subtracting the CGG2013a geoid height in either NAD83(CSRS) v6 or ITRF2008, respectively. </gml:anchorDefinition>
      <gml:realizationEpoch>2015</gml:realizationEpoch>
    </gml:VerticalDatum>
  </gml:verticalDatum>
</gml:VerticalCRS>