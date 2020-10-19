#!/usr/bin/python

import datetime
import pathlib
import argparse

import json
import glob

import psycopg2
from yaml import load, dump

import config


def get_items_class_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name
        FROM
            re_itemclass
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0]
    else:
        return None


def get_crs_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name,
            itemclass_uuid
        FROM
            geodeticcrs
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return {
            "itemID": _row[1],
            "classID": crs_uuid_classes[_row[1]]
        }

    else:
        return None


def get_citations_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            informationsource_uuid
        FROM
            identifieditem_ci_citation
        WHERE
            identifieditem_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    rows = cur.fetchall()

    result = []
    
    if rows:
        for row in rows:
            citation = get_citation(row[0])
            if citation:
                result.append(citation)

        return result

    else:
        return None


def get_citation(uuid):
    cur.execute(
        """
        SELECT
            uuid,
            collectivetitle,
            edition,
            identifier_code,
            isbn,
            issn,
            othercitationdetails,
            title,
            authority_uuid,
            editiondate,
            series_name,
            series_issueidentification,
            series_page
        FROM
            ci_citation
    """,
        {"uuid": uuid},
    )

    row = cur.fetchone()
    cols = [desc[0] for desc in cur.description]

    items = []

    if row:
        return {
                "uuid": row[cols.index("uuid")],
                "title": row[cols.index("title")],
                "collectiveTitle": row[cols.index("collectivetitle")],
                "edition": row[cols.index("edition")],
                "editionDate": row[cols.index("editiondate")],
                "isbn": row[cols.index("isbn")],
                "issn": row[cols.index("issn")],
                "otherDetails": row[cols.index("othercitationdetails")],
                "seriesName": row[cols.index("series_name")],
                "seriesIssueId": row[cols.index("series_issueidentification")],
                "seriesPage": row[cols.index("series_page")],
        }

    else:
        return None



def get_geo_datum_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name
        FROM
            geodeticdatum
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0]
    else:
        return None


def get_vert_datum_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name
        FROM
            verticaldatum
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0]
    else:
        return None


def get_coord_sys_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name,
            itemclass_uuid
        FROM
            cartesiancs
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return {
            "name": _row[0],
            "uuid": uuid,
            "class": get_items_class_by_uuid(_row[1]),
        }

    else:
        cur.execute(
            """
            SELECT
                name,
                itemclass_uuid
            FROM
                ellipsoidalcs
            WHERE
                uuid = %(uuid)s
        """,
            {"uuid": uuid},
        )

        _row = cur.fetchone()

        if _row:
            return {
                "name": _row[0],
                "uuid": uuid,
                "class": get_items_class_by_uuid(_row[1]),
            }

        else:

            cur.execute(
                """
                SELECT
                    name,
                    itemclass_uuid
                FROM
                    sphericalcs
                WHERE
                    uuid = %(uuid)s
            """,
                {"uuid": uuid},
            )

            _row = cur.fetchone()

            if _row:
                return {
                    "name": _row[0],
                    "uuid": uuid,
                    "class": get_items_class_by_uuid(_row[1]),
                }

            else:

                cur.execute(
                    """
                    SELECT
                        name,
                        itemclass_uuid
                    FROM
                        verticalcs
                    WHERE
                        uuid = %(uuid)s
                """,
                    {"uuid": uuid},
                )

                _row = cur.fetchone()

                if _row:
                    return {
                        "name": _row[0],
                        "uuid": uuid,
                        "class": get_items_class_by_uuid(_row[1]),
                    }
                else:
                    return None


def get_op_method_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name
        FROM
            operationmethoditem
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0]
    else:
        return None


def get_extent_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            description
        FROM
            ex_extent
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()
    name = None

    if _row:
        name = _row[0]
    else:
        return None

    cur.execute(
        """
        SELECT
            geographicelement_uuid
        FROM
            ex_extent_ex_geographicextent
        WHERE
            ex_extent_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    geo_uuid = None

    if _row:
        geo_uuid = _row[0]
    else:
        return None

    cur.execute(
        """
        SELECT
            eastboundlongitude,
            northboundlatitude,
            southboundlatitude,
            westboundlongitude
         FROM
            ex_geographicboundingbox
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": geo_uuid},
    )

    _row = cur.fetchone()

    if _row:
        return {
            "name": name,
            "e": _row[0],
            "n": _row[1],
            "s": _row[2],
            "w": _row[3],
        }
    else:
        return None


def get_accuracy_by_uuid(uuid):
    pass


def crs_compound_dump():
    print("Not Implemented")


def crs_projected_dump():
    print("Not Implemented")


def crs_engineering_dump():
    print("Not Implemented")


def concat_operations_dump():
    print("Not Implemented")


def datums_engineering_dump():
    print("Not Implemented")


def concat_conversion_dump():
    print("Not Implemented")


def cs_spherical_dump():
    print("Not Implemented")


def read_json(fname):
    with open(fname, "r") as _f:
        result = json.load(_f)
        return result


def read_json_dir(alias):
    result = []
    json_dir = "%s/%s" % (config.data_dir, alias)
    files = glob.glob("%s/*.json" % json_dir)
    for fname in files:
        data = read_json(fname)
        result.append(data)

    return result


def save_yaml(uuid, dname, data):
    file_path = "%s/%s" % (config.output_dir, dname)
    pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)
    f = open("%s/%s.yaml" % (file_path, uuid), "w")
    f.write(dump(data))
    f.close()


def datums_geodetic_dump():

    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            dateamended,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            specificationlineage_uuid,
            specificationsource_uuid,
            data_source,
            identifier,
            information_source,
            remarks,
            origin_description,
            realization_epoch,
            datum_scope,
            domainofvalidity_uuid,
            ellipsoid_uuid,
            primemeridian_uuid,
            coordinatereferenceepoch
        FROM
            geodeticdatum
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "name": row[cols.index("name")],
                "identifier": int(row[cols.index("identifier")]),
                "aliases": get_aliases(row[cols.index("uuid")]),
                "extent": get_extent_by_uuid(row[cols.index("domainofvalidity_uuid")]),
                "remarks": row[cols.index("remarks")],
                "releaseDate": row[cols.index("realization_epoch")],
                "definition": row[cols.index("definition")],
                "originDescription": row[cols.index("origin_description")],
                "scope": row[cols.index("datum_scope")],
                "ellipsoid": {"itemID": row[cols.index("ellipsoid_uuid")]},
                "primeMeridian": {"itemID": row[cols.index("primemeridian_uuid")]},
                "coordinateReferenceEpoch": row[cols.index("coordinatereferenceepoch")],
                "informationSources": get_citations_by_uuid(row[cols.index("uuid")])
            }
        )

    for item in items:
        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            "dateAccepted": row[cols.index("dateaccepted")],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "datums--geodetic", data)


def datums_vertical_dump():
    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            dateamended,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            specificationlineage_uuid,
            specificationsource_uuid,
            data_source,
            identifier,
            information_source,
            remarks,
            origin_description,
            realization_epoch,
            datum_scope,
            domainofvalidity_uuid,
            coordinatereferenceepoch
        FROM
            verticaldatum
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "name": row[cols.index("name")],
                "identifier": int(row[cols.index("identifier")]),
                "aliases": get_aliases(row[cols.index("uuid")]),
                "extent": get_extent_by_uuid(row[cols.index("domainofvalidity_uuid")]),
                "remarks": row[cols.index("remarks")],
                "releaseDate": row[cols.index("realization_epoch")],
                "definition": row[cols.index("definition")],
                "originDescription": row[cols.index("origin_description")],
                "scope": row[cols.index("datum_scope")],
                "coordinateReferenceEpoch": row[cols.index("coordinatereferenceepoch")],
                "informationSources": get_citations_by_uuid(row[cols.index("uuid")])
            }
        )

    for item in items:

        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            "dateAccepted": row[cols.index("dateaccepted")],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "datums--vertical", data)


def ellipsoid_dump():

    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            dateamended,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            specificationlineage_uuid,
            specificationsource_uuid,
            data_source,
            identifier,
            information_source,
            remarks,
            inverseflattening,
            issphere,
            semimajoraxis,
            semiminoraxis,
            inverseflatteninguom_uuid,
            semimajoraxisuom_uuid,
            semiminoraxisuom_uuid
        FROM
            ellipsoid
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "name": row[cols.index("name")],
                "identifier": int(row[cols.index("identifier")]),
                "aliases": get_aliases(row[cols.index("uuid")]),
                "description": row[cols.index("description")],
                "remarks": row[cols.index("remarks")],
                "isSphere": row[cols.index("issphere")],
                "semiMajorAxis": row[cols.index("semimajoraxis")],
                "semiMajorAxisUoM": {
                    "itemID": row[cols.index("semimajoraxisuom_uuid")]
                },
                "semiMinorAxis": row[cols.index("semiminoraxis")],
                "semiMinorAxisUoM": {
                    "itemID": row[cols.index("semiminoraxisuom_uuid")]
                },
                "inverseFlattening": row[cols.index("inverseflattening")],
                "inverseFlatteningUoM": {
                    "itemID": row[cols.index("inverseflatteninguom_uuid")]
                },
                "informationSources": get_citations_by_uuid(row[cols.index("uuid")])
            }
        )

    for item in items:

        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            "dateAccepted": row[cols.index("dateaccepted")],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "ellipsoid", data)


def co_method_dump():

    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            dateamended,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            specificationlineage_uuid,
            specificationsource_uuid,
            data_source,
            identifier,
            information_source,
            remarks,
            formula,
            reversible,
            sourcedimensions,
            targetdimensions,
            formulacitation_uuid
        FROM
            operationmethoditem
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "name": row[cols.index("name")],
                "identifier": int(row[cols.index("identifier")]),
                "parameters": get_parameters(row[cols.index("uuid")]),
                "remarks": row[cols.index("remarks")],
                "formula": row[cols.index("formula")],
                "specification": {},
                "reversible": row[cols.index("reversible")],
                "definition": row[cols.index("definition")],
                "description": row[cols.index("description")],
                "informationSources": get_citations_by_uuid(row[cols.index("uuid")])
            }
        )

    for item in items:

        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            "dateAccepted": row[cols.index("dateaccepted")],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "coordinate-op-method", data)


def prime_meridian_dump():
    data = read_json_dir("prime-meridian")

    for item in data:
        uuid = item["uuid"]
        del item["uuid"]

        del item["information_source"]

        item["longitudeFromFreenwich"] = item["longitude_from_greenwich"]
        del item["longitude_from_greenwich"]

        item["informationSources"] = get_citations_by_uuid(uuid)

        data = {"id": uuid, "dateAccepted": "", "status": item["status"], "data": item}

        del data["data"]["status"]

        save_yaml(uuid, "prime-meridian", data)


def cs_axis_dump():
    data = read_json_dir("axes")

    for item in data:
        uuid = item["uuid"]
        del item["uuid"]

        del item["information_source"]

        item["unit"] = {
            "itemID": item["axis_unit"]["uuid"],
            "classID": "unit-of-measurement",
        }
        del item["axis_unit"]

        item["abbreviation"] = item["axis_abbreviation"]
        del item["axis_abbreviation"]

        item["direction"] = item["axis_direction"]
        del item["axis_direction"]

        item["minValue"] = item["minimum_value"]
        del item["minimum_value"]

        item["maxValue"] = item["maximum_value"]
        del item["maximum_value"]

        item["rangeMeaning"] = item["range_meaning"]
        del item["range_meaning"]

        item["informationSources"] = get_citations_by_uuid(uuid)

        data = {"id": uuid, "status": item["status"], "data": item}
        del data["data"]["status"]

        save_yaml(uuid, "coordinate-sys-axis", data)


def cs_cartesian_dump():
    data = read_json_dir("cartesian")

    for item in data:
        uuid = item["uuid"]
        del item["uuid"]

        coordinate_system_axes = item["coordinate_system_axes"]
        del item["coordinate_system_axes"]

        information_source = item["information_source"]
        del item["information_source"]

        _coordinate_system_axes = []

        for elm in coordinate_system_axes:
            _coordinate_system_axes.append(
                {"itemID": elm["uuid"], "classID": "coordinate-sys-axis"}
            )

        item["coordinateSystemAxes"] = _coordinate_system_axes
        item["informationSources"] = get_citations_by_uuid(uuid)

        data = {"id": uuid, "dateAccepted": "", "status": item["status"], "data": item}

        del data["data"]["status"]

        save_yaml(uuid, "coordinate-sys--сartesian", data)


def cs_ellipsoidal_dump():
    data = read_json_dir("ellipsoidal")

    for item in data:
        uuid = item["uuid"]
        del item["uuid"]

        coordinate_system_axes = item["coordinate_system_axes"]
        del item["coordinate_system_axes"]

        information_source = item["information_source"]
        del item["information_source"]

        _coordinate_system_axes = []

        for elm in coordinate_system_axes:
            _coordinate_system_axes.append(
                {"itemID": elm["uuid"], "classID": "coordinate-sys-axis"}
            )

        item["coordinateSystemAxes"] = _coordinate_system_axes
        item["informationSources"] = get_citations_by_uuid(uuid)

        data = {"id": uuid, "dateAccepted": "", "status": item["status"], "data": item}

        del data["data"]["status"]

        save_yaml(uuid, "coordinate-sys--ellipsoidal", data)


def cs_vertical_dump():
    data = read_json_dir("vertical")

    for item in data:
        uuid = item["uuid"]
        del item["uuid"]

        coordinate_system_axes = item["coordinate_system_axes"]
        del item["coordinate_system_axes"]

        information_source = item["information_source"]
        del item["information_source"]

        _coordinate_system_axes = []

        for elm in coordinate_system_axes:
            _coordinate_system_axes.append(
                {"itemID": elm["uuid"], "classID": "coordinate-sys-axis"}
            )

        item["coordinateSystemAxes"] = _coordinate_system_axes
        item["informationSources"] = get_citations_by_uuid(uuid)

        data = {"id": uuid, "dateAccepted": "", "status": item["status"], "data": item}

        del data["data"]["status"]

        save_yaml(uuid, "coordinate-sys--vertical", data)


def get_aliases(uuid):
    cur.execute(
        """
        SELECT
            aliases
        FROM
            identifieditem_aliases
        WHERE
            identifieditem_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(row[0])

    return items


def units_dump():

    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            dateamended,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            specificationlineage_uuid,
            specificationsource_uuid,
            data_source,
            identifier,
            information_source,
            remarks,
            measuretype,
            offsettostandardunit,
            scaletostandardunitdenominator,
            scaletostandardunitnumerator,
            symbol,
            standardunit_uuid
        FROM
            unitofmeasure
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "name": row[cols.index("name")],
                "identifier": int(row[cols.index("identifier")]),
                "aliases": get_aliases(row[cols.index("uuid")]),
                "remarks": row[cols.index("remarks")],
                "measureType": row[cols.index("measuretype")],
                "symbol": row[cols.index("symbol")],
                "numerator": row[cols.index("scaletostandardunitnumerator")],
                "denominator": row[cols.index("scaletostandardunitdenominator")],
                "standardUnit": row[cols.index("standardunit_uuid")],
                "informationSources": [],
            }
        )

    for item in items:

        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            "dateAccepted": row[cols.index("dateaccepted")],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "unit-of-measurement", data)


def transformations_dump():

    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            data_source,
            identifier,
            remarks,
            operationversion,
            domainofvalidity_uuid,
            sourcecrs_uuid,
            targetcrs_uuid,
            method_uuid

        FROM
            transformationitem
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "identifier": int(row[cols.index("identifier")]),
                "name": row[cols.index("name")],
                "description": row[cols.index("description")],
                # 'accepted': row[cols.index('dateaccepted')],
                "remarks": row[cols.index("remarks")],
                "operationVersion": row[cols.index("operationversion")],
                "extent": get_extent_by_uuid(row[cols.index("domainofvalidity_uuid")]),
                "scope": [],
                "parameters": [],
                "informationSources": [],
                # 'coordOperationMethod': {
                #   'uuid': row[cols.index('method_uuid')],
                #   'name': get_op_method_by_uuid(row[cols.index('method_uuid')])
                # },
                "coordOperationMethod": row[cols.index("method_uuid")],
                "sourceCRS": get_crs_by_uuid(row[cols.index("sourcecrs_uuid")]),
                "targetCRS": get_crs_by_uuid(row[cols.index("targetcrs_uuid")]),
                "informationSources": get_citations_by_uuid(row[cols.index("uuid")])                
            }
        )

    for item in items:
        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            # 'timestamp': datetime.datetime.now(),
            "dateAccepted": row[cols.index("dateaccepted")],
            # 'parents': [],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "coordinate-ops--transformation", data)


def crs_geodetic_dump():

    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            dateamended,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            specificationlineage_uuid,
            specificationsource_uuid,
            data_source,
            identifier,
            information_source,
            remarks,
            domainofvalidity_uuid,
            crs_scope,
            basecrs_uuid,
            operation_uuid,
            coordinatesystem_uuid,
            datum_uuid
        FROM
            geodeticcrs
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "name": row[cols.index("name")],
                "identifier": int(row[cols.index("identifier")]),
                "scope": row[cols.index("crs_scope")],
                "alias": [],
                "remarks": row[cols.index("remarks")],
                "description": row[cols.index("description")],
                "extent": get_extent_by_uuid(row[cols.index("domainofvalidity_uuid")]),
                "operation": row[cols.index("operation_uuid")],
                "datum": {
                    "uuid": row[cols.index("datum_uuid")],
                    "name": get_geo_datum_by_uuid(row[cols.index("datum_uuid")]),
                },
                "coordinateSystem": get_coord_sys_by_uuid(
                    row[cols.index("coordinatesystem_uuid")]
                ),
                "baseCRS": row[cols.index("basecrs_uuid")],
                "informationSources": get_citations_by_uuid(row[cols.index("uuid")])
            }
        )

    for item in items:
        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            "dateAccepted": row[cols.index("dateaccepted")],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "crs--geodetic", data)


def crs_vertical_dump():
    cur.execute(
        """
        SELECT
            uuid,
            dateaccepted,
            dateamended,
            definition,
            description,
            itemidentifier,
            name,
            status,
            itemclass_uuid,
            register_uuid,
            specificationlineage_uuid,
            specificationsource_uuid,
            data_source,
            identifier,
            information_source,
            remarks,
            domainofvalidity_uuid,
            crs_scope,
            basecrs_uuid,
            operation_uuid,
            coordinatesystem_uuid,
            datum_uuid
        FROM
            verticalcrs
    """
    )

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]

    items = []

    for row in rows:
        items.append(
            {
                "uuid": row[cols.index("uuid")],
                "name": row[cols.index("name")],
                "identifier": int(row[cols.index("identifier")]),
                "scope": row[cols.index("crs_scope")],
                "alias": [],
                "remarks": row[cols.index("remarks")],
                "description": row[cols.index("description")],
                "extent": get_extent_by_uuid(row[cols.index("domainofvalidity_uuid")]),
                "operation": row[cols.index("operation_uuid")],
                "datum": {
                    "uuid": row[cols.index("datum_uuid")],
                    "name": get_vert_datum_by_uuid(row[cols.index("datum_uuid")]),
                },
                "coordinateSystem": get_coord_sys_by_uuid(
                    row[cols.index("coordinatesystem_uuid")]
                ),
                "baseCRS": row[cols.index("basecrs_uuid")],
                "informationSources": get_citations_by_uuid(row[cols.index("uuid")])
            }
        )

    for item in items:

        uuid = item["uuid"]
        del item["uuid"]

        data = {
            "id": uuid,
            "dateAccepted": row[cols.index("dateaccepted")],
            "status": row[cols.index("status")].lower(),
            "data": item,
        }

        save_yaml(uuid, "crs--vertical", data)


if __name__ == "__main__":

    con = psycopg2.connect(
        database=config.db_name,
        user=config.db_user,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port,
    )
    cur = con.cursor()

    crs_name_classes = {
        "Compound CRS": "crs--compound",
        "Engineering CRS": "crs--engineering",
        "Geodetic CRS": "crs--geodetic",
        "Projected CRS": "crs--projected",
        "Vertical CRS": "crs--vertical",
    }

    crs_uuid_classes = {
        "69c0beba-4120-4e58-ae36-d294cb2e8623": "crs--geodetic",
        "7be258b1-ffcd-4493-aad4-58f913d08825": "crs--engineering",
        "9aabc0d2-039f-4202-aac0-3188ff71fce5": "crs--compound",
        "b8a1d920-61bb-4a2e-a111-b49df172719c": "crs--projected",
        "fb381dcb-f58e-41ec-994d-168734d6e029": "crs--vertical",
    }

    objects_dumpers = {
        "crs--geodetic": crs_geodetic_dump,
        "crs--vertical": crs_vertical_dump,
        "crs--compound": crs_compound_dump,
        "crs--projected": crs_projected_dump,
        "crs--engineering": crs_engineering_dump,
        "coordinate-ops--transformation": transformations_dump,
        "coordinate-ops--conversion": concat_conversion_dump,
        "coordinate-ops--concatenated-operation": concat_operations_dump,
        "datums--engineering": datums_engineering_dump,
        "datums--geodetic": datums_geodetic_dump,
        "datums--vertical": datums_vertical_dump,
        "coordinate-sys--сartesian": cs_cartesian_dump,
        "coordinate-sys--ellipsoidal": cs_ellipsoidal_dump,
        "coordinate-sys--vertical": cs_vertical_dump,
        "coordinate-sys--spherical": cs_spherical_dump,
        "ellipsoid": ellipsoid_dump,
        "coordinate-sys-axis": cs_axis_dump,
        # "coordinate-op-method": co_method_dump, # not ready
        # "coordinate-op-parameter": co_parameter_dump, #23 objects id db
        "prime-meridian": prime_meridian_dump,
        "unit-of-measurement": units_dump,
    }

    parser = argparse.ArgumentParser(
        description="Dump data from Geodetic Registry postgres db to yaml."
    )
    parser.add_argument(
        "-o",
        "--objects",
        action="append",
        help="<Required> list of objects to dump",
        required=True,
        nargs="+",
        type=str,
    )
    args = parser.parse_args()

    if ' ' in args.objects[0][0]:
        arg_objects = args.objects[0][0].split(' ')
    else:
        arg_objects = [args.objects[0][0]]

    for obj in arg_objects:
        if objects_dumpers.get(obj, None):
            print('Dumping %s' % obj.replace('_dump', ''))
            objects_dumpers[obj]()
        else:
            if obj:
                print('Unknown object type: %s' % obj)
            else:
                print('Not specified object(s) to dump.')
