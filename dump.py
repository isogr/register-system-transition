#!/usr/bin/python

import datetime
import pathlib
import argparse

import json
import glob

from yaml import dump
import psycopg2

import config


def get_cols_dict():
    i = 0
    result = {}
    for name in [desc[0] for desc in cur.description]:
        result[name] = i
        i += 1

    return result


def get_class_by_uuid(uuid):
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
            "itemID": uuid,
            "classID": item_classes.get(_row[1])
        }


def get_citations_by_item(uuid):
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
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    row = cur.fetchone()
    _ = get_cols_dict()

    if row:
        other_details = row[_["othercitationdetails"]]
        if other_details and not other_details.strip():
            other_details = None

        edition_date = row[_["editiondate"]]

        # some fields has a garbage:
        if edition_date and edition_date.replace('-', '').isnumeric():
            edition_date_dt = str_to_dt(edition_date)
        else:
            edition_date_dt = None

        return {
            "uuid": row[_["uuid"]],
            "title": row[_["title"]],
            "edition": row[_["edition"]],
            "editionDate": edition_date_dt,
            "isbn": row[_["isbn"]],
            "issn": row[_["issn"]],
            "otherDetails": other_details,
            "seriesName": row[_["series_name"]],
            "seriesIssueID": row[_["series_issueidentification"]],
            "seriesPage": row[_["series_page"]],
        }


def get_geo_datum_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name,
            itemclass_uuid
        FROM
            geodeticdatum
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return {
            "uuid": uuid,
            "name": _row[0],
            "class_uuid": _row[1]
        }


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
            "itemID": uuid,
            "classID": name_classes[get_class_by_uuid(_row[1])]
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
                "itemID": uuid,
                "classID": name_classes[get_class_by_uuid(_row[1])]
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
                    "itemID": uuid,
                    "classID": name_classes[get_class_by_uuid(_row[1])]
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
                        "itemID": uuid,
                        "classID": name_classes[get_class_by_uuid(_row[1])]
                    }


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


def get_op_params_by_method_uuid(uuid):
    cur.execute(
        """
        SELECT
            parameter_uuid,
            parameter_index
        FROM
            operationmethoditem_generaloperationparameteritem
        WHERE
            operationmethoditem_uuid = %(uuid)s
        ORDER BY
            parameter_index
    """,
        {"uuid": uuid},
    )

    items = []

    for row in cur.fetchall():
        items.append(row[0])

    return items


def get_tf_params_by_tf_uuid(uuid):
    cur.execute(
        """
        SELECT
            parametervalue_uuid
        FROM
            singleoperationitem_generalparametervalue
        WHERE
            singleoperationitem_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _d = []

    for row in cur.fetchall():
        item = {}

        param_val_uuid = row[0]
        op_param_val = get_op_simple_param_val(param_val_uuid)
        _param_val = get_op_param_val(param_val_uuid)
        param_uuid = _param_val["uuid"]

        if op_param_val:
            # item["parameter"] = {
                # "classID": "coordinate-op-parameter",
                # "parameter": _param_val["uuid"],
                # "type": "measure (w/ UoM)",
                # "name": None,
                # "id": None
            # }

            # param = get_op_parameter_by_uuid(_param_val["uuid"])
            # if param:
                # item["parameter"]["name"] = param["name"]
                # item["parameter"]["id"] = param["id"]
                # item["name"] = param["name"]
            # else:
                # item["name"] = None

            item["parameter"] = _param_val["uuid"]
            item["type"] = "measure (w/ UoM)"
            item["value"] = op_param_val.pop("value")
            item["unitOfMeasurement"] = op_param_val["uuid"]
            item["fileCitation"] = get_citation(_param_val["citation_uuid"])

            items.append(item)

        else:
            cur.execute(
                """
                SELECT
                    parametervaluesimple
                FROM
                    operationparametervalue_parametervaluesimple
                WHERE
                    operationparametervalue_uuid = %(uuid)s
            """,
                {"uuid": param_val_uuid},
            )
            _val = cur.fetchone()

            if _val and _param_val:

                # param = get_op_parameter_by_uuid(param_uuid)
                # if param:
                    # item["parameter"] = {
                        # "classID": "coordinate-op-parameter",
                        # "parameter": param_uuid,
                        # "type": paramType.get(_param_val["type"]),
                        # "name": param["name"],
                        # "id": param["id"]
                    # }

                item["parameter"] = param_uuid
                item["type"] = paramType.get(_param_val["type"])
                item["value"] = _val[0]
                item["unitOfMeasurement"] = None
                item["fileCitation"] = get_citation(_param_val["citation_uuid"])

            items.append(item)

    return items


def get_op_param_val(uuid):
    cur.execute(
        """
        SELECT
            dtype,
            parametertype,
            parameter_uuid,
            referencefilecitation_uuid
        FROM
            generalparametervalue
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    param = cur.fetchone()
    if param:
        return {
            "dtype": param[0],
            "type": param[1],
            "uuid": param[2],
            "citation_uuid": param[3]
        }


def get_op_simple_param_val(uuid):
    cur.execute(
        """
        SELECT
            value,
            uom_uuid
        FROM
            operationparametervalue_parametervalue
        WHERE
            operationparametervalue_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    op_param_val = cur.fetchone()

    if op_param_val:
        val_str = str(psycopg2.Binary(op_param_val[0]))
        val_str = val_str.replace("::bytea", "").strip("'")

        val_str = val_str.replace('\\254\\355\\000\\005sr\\000\\020java.lang.Double\\200\\263\\302J)k\\373\\004\\002\\000\\001D\\000\\005valuexr\\000\\020java.lang.Number\\206\\254\\225\\035\\013\\224\\340\\213\\002\\000\\000xp', '')

        if not val_str.replace('\\000', ''):
            value = float(0.0)
        else:
            value = None

        return {
            "value": value,
            "classID": "unit-of-measurement",
            "uuid": op_param_val[1]
        }


def get_op_parameter_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name,
            identifier,
            itemclass_uuid
        FROM
            operationparameteritem
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return {
            "id": _row[1],
            "name": _row[0],
            "classID": name_classes.get(get_class_by_uuid(_row[2]))
        }


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

    items = []

    for row in cur.fetchall():
        items.append(row[0])

    return items


def get_coord_op_scope(uuid):
    cur.execute(
        """
        SELECT
            scope
        FROM
            coordinateoperationitem_scope
        WHERE
            coordinateoperationitem_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []

    for row in cur.fetchall():
        items.append(row[0])

    return items


def get_coord_op_accuracy(uuid):
    cur.execute(
        """
        SELECT
            coordinateoperationaccuracy_uuid
        FROM
            coordinateoperationitem_dq_positionalaccuracy
        WHERE
            coordinateoperationitem_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []

    for row in cur.fetchall():
        accuracy_uuid = row[0]

        cur.execute(
            """
            SELECT
                result_uuid
            FROM
                dq_absoluteexternalpositionalaccuracy
            WHERE
                uuid = %(uuid)s
        """,
            {"uuid": accuracy_uuid},
        )

        for row2 in cur.fetchall():
            result_uuid = row2[0]

            cur.execute(
                """
                SELECT
                    dtype,
                    accuracy,
                    accuracyunit_uuid
                FROM
                    result
                WHERE
                    uuid = %(uuid)s
            """,
                {"uuid": result_uuid},
            )

            result = cur.fetchone()

            items.append(
                {
                    "dtype": result[0],
                    "value": result[1],
                    "unitOfMeasurement": result[2],
                }
            )

    if items:
        return items[0]


def str_to_dt(date_str):
    return datetime.datetime.strptime(
        date_str, "%Y-%m-%d"
    ).date()


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
    file = open("%s/%s.yaml" % (file_path, uuid), "w")
    file.write(dump(data))
    file.close()


def save_items(items, class_id):
    for item in items:
        uuid = item.pop("uuid")
        date_accepted = item.pop("dateAccepted")
        status = item.pop("status")

        data = {
            "id": uuid,
            "dateAccepted": date_accepted,
            "status": status,
            "data": item,
        }

        save_yaml(uuid, class_id, data)


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
                "extent": get_extent_by_uuid(row[_["domainofvalidity_uuid"]]),
                "remarks": row[_["remarks"]],
                "releaseDate": row[_["realization_epoch"]],
                "definition": row[_["definition"]],
                "originDescription": row[_["origin_description"]],
                "scope": row[_["datum_scope"]],
                "ellipsoid": row[_["ellipsoid_uuid"]],
                "primeMeridian": row[_["primemeridian_uuid"]],
                "coordinateReferenceEpoch": row[_["coordinatereferenceepoch"]],
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "datums--geodetic")


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
                "extent": get_extent_by_uuid(row[_["domainofvalidity_uuid"]]),
                "remarks": row[_["remarks"]],
                "releaseDate": row[_["realization_epoch"]],
                "definition": row[_["definition"]],
                "originDescription": row[_["origin_description"]],
                "scope": row[_["datum_scope"]],
                "coordinateReferenceEpoch": row[_["coordinatereferenceepoch"]],
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "datums--vertical")


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
                "description": row[_["description"]],
                "remarks": row[_["remarks"]],
                "isSphere": row[_["issphere"]],
                "semiMajorAxis": row[_["semimajoraxis"]],
                "semiMajorAxisUoM": row[_["semimajoraxisuom_uuid"]],
                "semiMinorAxis": row[_["semiminoraxis"]],
                "semiMinorAxisUoM": row[_["semiminoraxisuom_uuid"]],
                "inverseFlattening": row[_["inverseflattening"]],
                "inverseFlatteningUoM": row[_["inverseflatteninguom_uuid"]],
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "ellipsoid")


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
                "definition": row[_["definition"]],
                "description": row[_["description"]],
                "parameters": get_op_params_by_method_uuid(row[_["uuid"]]),
                "remarks": row[_["remarks"]],
                "formula": row[_["formula"]],
                "formulaCitation": get_citation((row[_["formulacitation_uuid"]])),
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "coordinate-op-method")


def co_parameter_dump():
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
            minimumoccurs
        FROM
            operationparameteritem
    """
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        if row[_["minimumoccurs"]]:
            minimum_occurs = int(row[_["minimumoccurs"]])
        else:
            minimum_occurs = None

        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
                "definition": row[_["definition"]],
                "remarks": row[_["remarks"]],
                "minimumOccurs": minimum_occurs,
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "coordinate-op-parameter")


def prime_meridian_dump():
    data = read_json_dir("prime-meridian")

    for item in data:
        uuid = item.pop("uuid")
        status = item.pop("status")
        date_accepted = str_to_dt(item.pop("date_accepted"))
        item["longitudeFromGreenwich"] = item.pop("longitude_from_greenwich")
        item["longitudeFromGreenwichUoM"] = item.pop("longitude_from_greenwich_uom")
        item["informationSources"] = get_citations_by_item(uuid)

        del item["information_source"]

        data = {
            "id": uuid,
            "dateAccepted": date_accepted,
            "status": status,
            "data": item
        }

        save_yaml(uuid, "prime-meridian", data)


def cs_cartesian_dump():
    data = read_json_dir("cartesian")

    for item in data:
        uuid = item.pop("uuid")
        status = item.pop("status")
        date_accepted = str_to_dt(item.pop("date_accepted"))

        coordinate_system_axes = item.pop("coordinate_system_axes")

        _coordinate_system_axes = []

        for elm in coordinate_system_axes:
            _coordinate_system_axes.append(elm["uuid"])

        item["coordinateSystemAxes"] = _coordinate_system_axes
        item["informationSources"] = get_citations_by_item(uuid)

        del item["information_source"]

        data = {
            "id": uuid,
            "dateAccepted": date_accepted,
            "status": status,
            "data": item
        }

        save_yaml(uuid, "coordinate-sys--cartesian", data)


def cs_ellipsoidal_dump():
    data = read_json_dir("ellipsoidal")

    for item in data:
        uuid = item.pop("uuid")
        status = item.pop("status")
        date_accepted = str_to_dt(item.pop("date_accepted"))

        coordinate_system_axes = item.pop("coordinate_system_axes")

        _coordinate_system_axes = []

        for elm in coordinate_system_axes:
            _coordinate_system_axes.append(elm["uuid"])

        item["coordinateSystemAxes"] = _coordinate_system_axes
        item["informationSources"] = get_citations_by_item(uuid)

        del item["information_source"]

        data = {
            "id": uuid,
            "dateAccepted": date_accepted,
            "status": status,
            "data": item
        }

        save_yaml(uuid, "coordinate-sys--ellipsoidal", data)


def cs_vertical_dump():
    data = read_json_dir("vertical")

    for item in data:
        uuid = item.pop("uuid")
        status = item.pop("status")
        date_accepted = str_to_dt(item.pop("date_accepted"))

        coordinate_system_axes = item.pop("coordinate_system_axes")

        # information_source = item.pop("information_source")

        _coordinate_system_axes = []

        for elm in coordinate_system_axes:
            _coordinate_system_axes.append(elm["uuid"])

        item["coordinateSystemAxes"] = _coordinate_system_axes
        item["informationSources"] = get_citations_by_item(uuid)

        data = {
            "id": uuid,
            "dateAccepted": date_accepted,
            "status": status,
            "data": item
        }

        save_yaml(uuid, "coordinate-sys--vertical", data)


def cs_axis_dump():
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
            coord_axis_abbreviation,
            coord_axis_orientation,
            coord_axis_orientation_codespace,
            maximumvalue,
            minimumvalue,
            rangemeaning,
            axisunit_uuid
        FROM
            axis
    """
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        # min_value = str(psycopg2.Binary(row[_["minimumvalue"]]))
        # max_value = str(psycopg2.Binary(row[_["maximumvalue"]]))
        max_value = None
        min_value = None

        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "abbreviation": row[_["coord_axis_abbreviation"]],
                "orientation": row[_["coord_axis_orientation"]],
                "unitOfMeasurement": row[_["axisunit_uuid"]],
                "minValue": min_value,
                "maxValue": max_value,
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "coordinate-sys-axis")


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
                "remarks": row[_["remarks"]],
                "measureType": row[_["measuretype"]],
                "symbol": row[_["symbol"]],
                "numerator": row[_["scaletostandardunitnumerator"]],
                "denominator": row[_["scaletostandardunitdenominator"]],
                "standardUnit": row[_["standardunit_uuid"]],
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )
    save_items(items, "unit-of-measurement")


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "description": row[_["description"]],
                "remarks": row[_["remarks"]],
                "operationVersion": row[_["operationversion"]],
                "extent": get_extent_by_uuid(row[_["domainofvalidity_uuid"]]),
                "scope": get_coord_op_scope(row[_["uuid"]]),
                "accuracy": get_coord_op_accuracy(row[_["uuid"]]),
                "parameters": get_tf_params_by_tf_uuid(row[_["uuid"]]),
                "coordOperationMethod": row[_["method_uuid"]],
                "sourceCRS": get_crs_by_uuid(row[_["sourcecrs_uuid"]]),
                "targetCRS": get_crs_by_uuid(row[_["targetcrs_uuid"]]),
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "coordinate-ops--transformation")


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "scope": row[_["crs_scope"]],
                "aliases": get_aliases(row[_["uuid"]]),
                "remarks": row[_["remarks"]],
                "description": row[_["description"]],
                "extent": get_extent_by_uuid(row[_["domainofvalidity_uuid"]]),
                "operation": row[_["operation_uuid"]],
                "datum": row[_["datum_uuid"]],
                "coordinateSystem": get_coord_sys_by_uuid(
                    row[_["coordinatesystem_uuid"]]
                ),
                "baseCRS": row[_["basecrs_uuid"]],
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "crs--geodetic")


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

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "scope": row[_["crs_scope"]],
                "aliases": get_aliases(row[_["uuid"]]),
                "remarks": row[_["remarks"]],
                "description": row[_["description"]],
                "extent": get_extent_by_uuid(row[_["domainofvalidity_uuid"]]),
                "operation": row[_["operation_uuid"]],
                "datum": row[_["datum_uuid"]],
                "coordinateSystem": get_coord_sys_by_uuid(
                    row[_["coordinatesystem_uuid"]]
                ),
                "baseCRS": row[_["basecrs_uuid"]],
                "informationSources": get_citations_by_item(row[_["uuid"]])
            }
        )

    save_items(items, "crs--vertical")


if __name__ == "__main__":

    con = psycopg2.connect(
        database=config.db_name,
        user=config.db_user,
        password=config.db_password,
        host=config.db_host,
        port=config.db_port,
    )
    cur = con.cursor()

    paramType = {
        6: "parameter file name"
    }

    name_classes = {
        "GeodeticCRS": "crs--geodetic",
        "EngineeringCRS": "crs--engineering",
        "CompoundCRS": "crs--compound",
        "ProjectedCRS": "crs--projected",
        "VerticalCRS": "crs--vertical",
        "Transformation": "coordinate-ops--transformation",
        "Conversion": "coordinate-ops--conversion",
        "ConcatenatedOperation": "coordinate-ops--concatenated-operation",
        "EngineeringDatum": "datums--engineering",
        "GeodeticDatum": "datums--geodetic",
        "VerticalDatum": "datums--vertical",
        "CartesianCS": "coordinate-sys--cartesian",
        "EllipsoidalCS": "coordinate-sys--ellipsoidal",
        "VerticalCS": "coordinate-sys--vertical",
        "SphericalCS": "coordinate-sys--spherical",
        "Ellipsoid": "ellipsoid",
        "CoordinateSystemAxis": "coordinate-sys-axis",
        "OperationMethod": "coordinate-op-method",
        "OperationParameter": "coordinate-op-parameter",
        "PrimeMeridian": "prime-meridian",
        "UnitOfMeasure": "unit-of-measurement"
    }

    item_classes = {
        "69c0beba-4120-4e58-ae36-d294cb2e8623": "crs--geodetic",
        "7be258b1-ffcd-4493-aad4-58f913d08825": "crs--engineering",
        "9aabc0d2-039f-4202-aac0-3188ff71fce5": "crs--compound",
        "b8a1d920-61bb-4a2e-a111-b49df172719c": "crs--projected",
        "fb381dcb-f58e-41ec-994d-168734d6e029": "crs--vertical",
        "546b4647-1d3a-4b9b-9640-862ab3fd9867": "coordinate-ops--transformation",
        "a0b5683b-7cc7-4551-8bbb-f3b9870cb5d4": "coordinate-ops--conversion",
        "7b6cfab6-07d0-4f28-b425-29a9176597a7": "coordinate-ops--concatenated-operation",
        "bc0c8369-34c2-44e7-9498-b35c9d8438f4": "datums--engineering",
        "4d6353fc-ecd5-4024-bd76-fff10d0ac970": "datums--geodetic",
        "307dd049-e74b-4856-96e1-8108d69bf68d": "datums--vertical",
        "3582ebd6-57bb-4673-b32b-a5a555111013": "coordinate-sys--cartesian",
        "4299ce1c-9bd4-4b14-a168-0f9bcdcdb20b": "coordinate-sys--ellipsoidal",
        "9bccbe77-35b0-4078-813d-0e7d332990f7": "coordinate-sys--vertical",
        "c7eaf787-578d-4fb3-80bd-dbeb14ddc1ca": "coordinate-sys--spherical",
        "aada3089-bca3-4bc2-8ccb-23570def7d23": "ellipsoid",
        "6eb0564e-a4f7-4764-8e19-f62422bb562e": "coordinate-sys-axis",
        "4149b8f8-7cae-4f26-8396-6d7a9cc203eb": "coordinate-op-method",
        "d27ca5ec-65f7-4e72-be5a-9e1cac4afc63": "coordinate-op-parameter",
        "c176f626-dad9-4821-893b-ded32f175675": "prime-meridian",
        "c40172d7-9615-4d62-b512-a0b8d54a8fd0": "unit-of-measurement"
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
        "coordinate-sys--cartesian": cs_cartesian_dump,
        "coordinate-sys--ellipsoidal": cs_ellipsoidal_dump,
        "coordinate-sys--vertical": cs_vertical_dump,
        "coordinate-sys--spherical": cs_spherical_dump,
        "ellipsoid": ellipsoid_dump,
        "coordinate-sys-axis": cs_axis_dump,
        "coordinate-op-method": co_method_dump,
        "coordinate-op-parameter": co_parameter_dump,
        "prime-meridian": prime_meridian_dump,
        "unit-of-measurement": units_dump
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

    if " " in args.objects[0][0]:
        arg_objects = args.objects[0][0].split(" ")
    else:
        arg_objects = [args.objects[0][0]]

    for obj in arg_objects:
        if objects_dumpers.get(obj, None):
            print("Dumping %s" % obj.replace("_dump", ""))
            objects_dumpers[obj]()
        else:
            if obj:
                print("Unknown object type: %s" % obj)
            else:
                print("Not specified object(s) to dump.")
