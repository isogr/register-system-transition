#!/usr/bin/python

import argparse
import csv
import datetime
import glob
import json
import pathlib
import re
import sys

import javaobj
import psycopg2
from yaml import dump

import config


extents = []
information_sources = []
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


def get_citations_by_item(uuid, identifier):
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

                # Used to output data for "information_sources.csv"
                info_source_data = {
                    "id": identifier,
                    **citation
                }
                information_sources.append(info_source_data)

    return result


def get_ci_citation_ci_responsibleparty(citation_uuid):
    cur.execute(
        """
        SELECT
            citedresponsibleparty_uuid
        FROM
            ci_citation_ci_responsibleparty
        WHERE
            ci_citation_uuid = %(uuid)s
    """,
        {"uuid": citation_uuid},
    )

    items = []

    for row in cur.fetchall():
        items.append(row[0])

    return items


def get_author_publisher_informationsource(uuid):
    cur.execute(
        """
        SELECT
            individualname, organisationname, role
        FROM
            ci_responsibleparty
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        if _row[2] == 'author':
            return {"author": _row[0]}
        elif _row[2] == 'publisher':
            return {"publisher": _row[1]}
    return None


def get_extra_information_source_data(uuid):
    cur.execute(
        """
        SELECT
            datetype_value, date_date
        FROM
            ci_citation_date
        WHERE
            ci_citation_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        if _row[0] == 'revision':
            return {"revisionDate": _row[1]}
        elif _row[0] == 'publication':
            return {"publicationDate": _row[1]}
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
            # year only:
            if len(edition_date) == 4:
                edition_date = "%s-01-01" % edition_date
            edition_date_dt = str_to_dt(edition_date)
        else:
            edition_date_dt = None

        output = {
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

        output.update(get_extra_information_source_data(row[_["uuid"]]))

        responsible_parties = get_ci_citation_ci_responsibleparty(uuid)
        for responsible_party in responsible_parties:
            output.update(**get_author_publisher_informationsource(responsible_party))
        return output


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


def get_baseCRS_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name,
            itemclass_uuid
        FROM
            engineeringcrs
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
                "classID": name_classes[get_class_by_uuid(_row[1])]
            }

        else:
            cur.execute(
                """
                SELECT
                    name,
                    itemclass_uuid
                FROM
                    projectedcrs
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
                        verticalcrs
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
        return {
            "value": convert_binary_into_human_readable_string(op_param_val[0].hex()),
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
                    "value": str(result[0]),
                    "unitOfMeasurement": result[1],
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
    file.write(dump(data, allow_unicode=True))
    file.close()


def save_items(items, class_id):
    for item in items:
        uuid = item.pop("uuid")
        date_accepted = item.pop("dateAccepted")
        status = item.pop("status")
        if status.lower() == "not_valid":
            status = "invalid"

        data = {
            "id": uuid,
            "dateAccepted": date_accepted,
            "status": status,
            "data": item,
        }
        if supersededby := item.pop("supersededBy", None):
            data["supersededBy"] = supersededby

        save_yaml(uuid, class_id, data)


def crs_compound_dump():
    print("Not Implemented\n")


def crs_projected_dump(uuid=None):
    query = """
        SELECT
            uuid,
            dateaccepted,
            itemidentifier,
            name,
            status,
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
            projectedcrs
    """

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        extent_data = get_extent_by_uuid(row[_["domainofvalidity_uuid"]])

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "name": row[_["name"]],
            "identifier": int(row[_["identifier"]]),
            "scope": row[_["crs_scope"]],
            "aliases": get_aliases(row[_["uuid"]]),
            "remarks": row[_["remarks"]],
            "extent": extent_data,
            "operation": get_operation_by_uuid(row[_["operation_uuid"]]),
            "datum": row[_["datum_uuid"]],
            "coordinateSystem": get_coord_sys_by_uuid(
                row[_["coordinatesystem_uuid"]]
            ),
            "baseCRS": get_baseCRS_by_uuid(
                row[_["basecrs_uuid"]]
            ),
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

        if extent_data:
            extents.append({
                "id": int(row[_["identifier"]]),
                **extent_data,
            })

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "crs--projected")


def crs_engineering_dump():
    print("Not Implemented\n")


def concat_operations_dump():
    print("Not Implemented\n")


def datums_engineering_dump():
    print("Not Implemented\n")


def get_conversion_accuracy(accuracy):
    if not accuracy:
        return {
            "unitOfMeasurement": None,
            "value": None
        }
    return accuracy


def concat_conversion_dump(uuid=None):
    query = """
            SELECT
                uuid,
                dateaccepted,
                dateamended,
                status,
                name,
                identifier,
                domainofvalidity_uuid,
                accuracy,
                remarks,
                definition,
                sourcecrs_uuid,
                targetcrs_uuid,
                method_uuid
            FROM
                conversionitem
        """

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)

    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        extent_data = get_extent_by_uuid(row[_["domainofvalidity_uuid"]])

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "dateAmended": row[_["dateamended"]],
            "status": row[_["status"]].lower(),
            "name": row[_["name"]],
            "identifier": int(row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
            "extent": extent_data,
            "accuracy": get_conversion_accuracy(int(row[_["accuracy"]]) if row[_["accuracy"]] else None),
            # "accuracy": get_coord_op_accuracy(row[_["uuid"]]),
            "scope": get_coord_op_scope(row[_["uuid"]]),
            "remarks": row[_["remarks"]],
            "parameters": get_conversion_params(row[_["uuid"]]),
            "definition": row[_["definition"]],
            "sourcecrs_uuid": row[_["sourcecrs_uuid"]],
            "targetcrs_uuid": row[_["targetcrs_uuid"]],
            "method_uuid": row[_["method_uuid"]],
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

        if extent_data:
            extents.append({
                "id": int(row[_["identifier"]]),
                **extent_data,
            })

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-ops--conversion")


def get_conversion_params(uuid):
    cur.execute(
        """
        SELECT 
            C.operationparametervalue_uuid,
            F.name,
            D.uuid,
            C.value
        FROM 
            conversionitem A,
            singleoperationitem_generalparametervalue B,
            operationparametervalue_parametervalue C,
            unitofmeasure D,
            generalparametervalue E,
            operationparameteritem F
        WHERE 
            A.uuid = %(uuid)s
            AND A.uuid = B.singleoperationitem_uuid
            AND B.parametervalue_uuid = C.operationparametervalue_uuid
            AND C.uom_uuid = D.uuid
            AND E.uuid = C.operationparametervalue_uuid
            AND F.uuid = E.parameter_uuid;
        """,
        {"uuid": uuid},
    )

    items = []

    for row in cur.fetchall():
        item = {
            "value": convert_binary_into_human_readable_string(row[3].hex()),
            "unitOfMeasurement": row[2]
        }

        param_val_uuid = row[0]
        _param_val = get_op_param_val(param_val_uuid)
        item["parameter"] = _param_val["uuid"]

        items.append(item)

    return items


def convert_binary_into_human_readable_string(binary_value):
    if binary_value:
        binary_data = bytes.fromhex(binary_value)
        deserialized_object = javaobj.loads(binary_data)
        return str(deserialized_object.value)
    return None


def cs_spherical_dump():
    print("Not Implemented\n")


def datums_geodetic_dump(uuid=None):
    query = """
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

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)

    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        extent_data = get_extent_by_uuid(row[_["domainofvalidity_uuid"]])

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "name": row[_["name"]],
            "identifier": int(row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
            "extent": extent_data,
            "remarks": row[_["remarks"]],
            "releaseDate": row[_["realization_epoch"]],
            "definition": row[_["definition"]],
            "originDescription": row[_["origin_description"]],
            "scope": row[_["datum_scope"]],
            "ellipsoid": row[_["ellipsoid_uuid"]],
            "primeMeridian": row[_["primemeridian_uuid"]],
            "coordinateReferenceEpoch": row[_["coordinatereferenceepoch"]],
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

        if extent_data:
            extents.append({
                "id": int(row[_["identifier"]]),
                **extent_data,
            })

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "datums--geodetic")


def datums_vertical_dump(uuid=None):
    query = """
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
        WHERE
            identifier > 0
    """

    if uuid:
        query += " AND uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        if int(row[_["identifier"]]) > 0:
            supersedingitem = get_supersededitem(row, _)
            extent_data = get_extent_by_uuid(row[_["domainofvalidity_uuid"]])

            data = {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
                "extent": extent_data,
                "remarks": row[_["remarks"]],
                "releaseDate": row[_["realization_epoch"]],
                "definition": row[_["definition"]],
                "originDescription": row[_["origin_description"]],
                "scope": row[_["datum_scope"]],
                "coordinateReferenceEpoch": row[_["coordinatereferenceepoch"]],
                "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
            }

            if supersedingitem:
                data["supersededBy"] = supersedingitem

            items.append(data)

            if extent_data:
                extents.append({
                    "id": int(row[_["identifier"]]),
                    **extent_data,
                })

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "datums--vertical")


def ellipsoid_dump(uuid=None):
    query = """
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

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)

        data = {
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
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }
        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "ellipsoid")


def co_method_dump(uuid=None):
    query = """
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
        WHERE
            identifier > 0
    """

    if uuid:
        query += " AND uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():

        supersedingitem = get_supersededitem(row, _)

        data = {
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
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-op-method")


def co_parameter_dump(uuid=None):
    query = """
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

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        if row[_["minimumoccurs"]]:
            minimum_occurs = int(row[_["minimumoccurs"]])
        else:
            minimum_occurs = None

        supersedingitem = get_supersededitem(row, _)

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "name": row[_["name"]],
            "identifier": int(row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
            "definition": row[_["definition"]],
            "remarks": row[_["remarks"]],
            "minimumOccurs": minimum_occurs,
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-op-parameter")


def prime_meridian_dump(uuid=None):
    """
    TODO: missing `unit`
    E.g.
    unit:
      name: degree
      uuid: 1d86d720-ff1a-47ef-819e-2fb3524c9ce9
    """
    query = """
        SELECT
            uuid,
            dateaccepted,
            description,
            definition,
            name,
            status,
            identifier,
            remarks,
            information_source,
            greenwichlongitude,
            greenwichlongitudeuom_uuid
        FROM
            primemeridian
    """

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "identifier": row[_["identifier"]],
            "name": row[_["name"]],
            "remarks": row[_["remarks"]],
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
            "longitudeFromGreenwich": row[_["greenwichlongitude"]],
            "longitudeFromGreenwichUoM": row[_["greenwichlongitudeuom_uuid"]]
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "prime-meridian")


def cs_cartesian_dump(uuid=None):
    query = """
            SELECT
                uuid,
                dateaccepted,
                description,
                definition,
                name,
                status,
                identifier,
                remarks,
                information_source
            FROM
                cartesiancs
        """

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "identifier": row[_["identifier"]],
            "coordinateSystemAxes": get_coordinate_sys_by_uuid(
                row[_["uuid"]]
            ),
            "name": row[_["name"]],
            "remarks": row[_["remarks"]],
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-sys--cartesian")


def cs_ellipsoidal_dump(single_uuid=None):
    query = """
                SELECT
                    uuid,
                    dateaccepted,
                    description,
                    definition,
                    name,
                    status,
                    identifier,
                    remarks,
                    information_source
                FROM
                    ellipsoidalcs
            """

    if single_uuid:
        query += " WHERE uuid = '%s'" % single_uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "identifier": row[_["identifier"]],
            "coordinateSystemAxes": get_coordinate_sys_by_uuid(
                row[_["uuid"]]
            ),
            "name": row[_["name"]],
            "remarks": row[_["remarks"]],
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
        }
        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if single_uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-sys--ellipsoidal")


def get_coordinate_sys_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            axes_uuid
        FROM
            coordinatesystem_axis
        WHERE
            coordinatesystem_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )
    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(row[0])

    return items


def cs_vertical_dump(uuid=None):
    query = """
        SELECT
            uuid,
            dateaccepted,
            description,
            definition,
            name,
            status,
            identifier,
            remarks,
            information_source
        FROM
            verticalcs
    """

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "identifier": row[_["identifier"]],
            "coordinateSystemAxes": get_coordinate_sys_by_uuid(
                row[_["uuid"]]
            ),
            "name": row[_["name"]],
            "remarks": row[_["remarks"]],
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-sys--vertical")


def cs_axis_dump(uuid=None):
    query = """
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

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        # min_value = str(psycopg2.Binary(row[_["minimumvalue"]]))
        # max_value = str(psycopg2.Binary(row[_["maximumvalue"]]))

        supersedingitem = get_supersededitem(row, _)

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "name": row[_["name"]],
            "remarks": row[_["remarks"]],
            "identifier": int(row[_["identifier"]]),
            "abbreviation": row[_["coord_axis_abbreviation"]],
            "orientation": row[_["coord_axis_orientation"]],
            "unitOfMeasurement": row[_["axisunit_uuid"]],
            "minValue": convert_binary_into_human_readable_string(row[_["minimumvalue"]]),
            "maxValue": convert_binary_into_human_readable_string(row[_["maximumvalue"]]),
            "rangeMeaning": row[_["rangemeaning"]],
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]]),
            "aliases": get_aliases(row[_["uuid"]]),
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-sys-axis")


def units_dump(uuid=None):
    query = """
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

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        data = {
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
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }
        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "unit-of-measurement")


def get_transformation_item_status_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            status
        FROM
            transformationitem
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0]


def transformations_dump(uuid=None):
    query = """

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
        WHERE identifier > 0
    """

    if uuid:
        query += " AND uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        extent_data = get_extent_by_uuid(row[_["domainofvalidity_uuid"]])

        data = {
                "uuid": row[_["uuid"]],
                "dateAccepted": row[_["dateaccepted"]],
                "status": row[_["status"]].lower(),
                "name": row[_["name"]],
                "identifier": int(row[_["identifier"]]),
                "description": row[_["description"]],
                "remarks": row[_["remarks"]],
                "operationVersion": row[_["operationversion"]],
                "extent": extent_data,
                "scope": get_coord_op_scope(row[_["uuid"]]),
                "accuracy": get_coord_op_accuracy(row[_["uuid"]]),
                "parameters": get_tf_params_by_tf_uuid(row[_["uuid"]]),
                "coordOperationMethod": row[_["method_uuid"]],
                "sourceCRS": get_crs_by_uuid(row[_["sourcecrs_uuid"]]),
                "targetCRS": get_crs_by_uuid(row[_["targetcrs_uuid"]]),
                "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]]),
                "aliases": get_aliases(row[_["uuid"]]),
            }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

        if extent_data:
            extents.append({
                "id": int(row[_["identifier"]]),
                **extent_data,
            })

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "coordinate-ops--transformation")


def get_supersededitem(row, _):
    supersedingitem_uuid = None
    supersedingitem = None

    item_uuids = get_proposals_management_uuids(row[_["uuid"]])
    for item_uuid in item_uuids:
        sp = get_simple_proposal_by_management_uuid(item_uuid)

        proposal = get_proposal_by_simple_proposal_uuid(sp['uuid'])

        proposal_type = get_proposal_type(sp["proposalmanagementinformation_uuid"])
        item_type = proposal_type["type"]

        if item_type == "amendment":

            if proposal_type["amendmentType"] == "supersession":
                supersedingitem_uuid = get_supersedingitems_uuid(proposal["parent_uuid"])
                class_slug = name_classes[sp["itemclassname"]]
                # Exclude supersededBy when superseding item is NOT VALID (identifier<0)
                supersedingitem = transformations_dump(supersedingitem_uuid)  # all supersedingitems are transformations

    if supersedingitem_uuid and supersedingitem:
        return [{
            "itemID": supersedingitem_uuid,
            "classID": class_slug
        }]
    return None


def get_operation_by_uuid(uuid):
    cur.execute(
        """
        SELECT
            name,
            itemclass_uuid
        FROM
            transformationitem
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
                conversionitem
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


def crs_geodetic_dump(uuid=None):
    query = """
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

    if uuid:
        query += " WHERE uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        extent_data = get_extent_by_uuid(row[_["domainofvalidity_uuid"]])

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "name": row[_["name"]],
            "identifier": int(row[_["identifier"]]),
            "scope": row[_["crs_scope"]],
            "aliases": get_aliases(row[_["uuid"]]),
            "remarks": row[_["remarks"]],
            "description": row[_["description"]],
            "extent": extent_data,
            "operation": get_operation_by_uuid(row[_["operation_uuid"]]),
            "datum": row[_["datum_uuid"]],
            "coordinateSystem": get_coord_sys_by_uuid(
                row[_["coordinatesystem_uuid"]]
            ),
            "baseCRS": get_baseCRS_by_uuid(
                row[_["basecrs_uuid"]]
            ),
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

        if extent_data:
            extents.append({
                "id": int(row[_["identifier"]]),
                **extent_data,
            })

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "crs--geodetic")


def crs_vertical_dump(uuid=None):
    query = """
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
        WHERE
            identifier > 0
    """

    if uuid:
        query += " AND uuid = '%s'" % uuid

    cur.execute(query)
    _ = get_cols_dict()

    items = []

    for row in cur.fetchall():
        supersedingitem = get_supersededitem(row, _)
        extent_data = get_extent_by_uuid(row[_["domainofvalidity_uuid"]])

        data = {
            "uuid": row[_["uuid"]],
            "dateAccepted": row[_["dateaccepted"]],
            "status": row[_["status"]].lower(),
            "name": row[_["name"]],
            "identifier": int(row[_["identifier"]]),
            "scope": row[_["crs_scope"]],
            "aliases": get_aliases(row[_["uuid"]]),
            "remarks": row[_["remarks"]],
            "description": row[_["description"]],
            "extent": extent_data,
            "operation": get_operation_by_uuid(row[_["operation_uuid"]]),
            "datum": row[_["datum_uuid"]],
            "coordinateSystem": get_coord_sys_by_uuid(
                row[_["coordinatesystem_uuid"]]
            ),
            "baseCRS": get_baseCRS_by_uuid(
                row[_["basecrs_uuid"]]
            ),
            # get_base_crs_by_uuid(row[_["basecrs_uuid"]]),
            "informationSources": get_citations_by_item(row[_["uuid"]], row[_["identifier"]])
        }

        if supersedingitem:
            data["supersededBy"] = supersedingitem

        items.append(data)

        if extent_data:
            extents.append({
                "id": int(row[_["identifier"]]),
                **extent_data,
            })

    if uuid:
        if items:
            return items[0]
        else:
            return None
    else:
        save_items(items, "crs--vertical")


def get_supersedingitems_uuid(uuid):
    cur.execute(
        """
        SELECT
            supersedingitems_uuid
        FROM
            supersession_supersedingitems
        WHERE
            supersessionid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0]


def proposals_dump():
    cur.execute(
        """
        SELECT
            uuid,
            parent_uuid,
            sponsor_uuid,
            title,
            datesubmitted,
            isconcluded,
            status
        FROM
            proposal
    """)

    proposals = []
    group_proposals_uuid = set()
    _ = get_cols_dict()

    for row in cur.fetchall():

        if row[_["status"]].lower() == "not_submitted":
            # Exclude proposals that have not been submitted
            continue

        if row[_["parent_uuid"]] in group_proposals_uuid:
            # Avoid duplicating proposals
            continue

        sp = get_simple_proposal(row[_["uuid"]])

        if sp:
            # Some proposals can be both parents of a ProposalGroup
            # and single Proposals. In this case, a SimpleProposal
            # is associated with this uuid, thus this is a Proposal
            if is_proposal_group(row[_["parent_uuid"]]):
                # 1) Proposal group: process all proposals_items associated with parent_uuid
                if row[_["parent_uuid"]] in group_proposals_uuid:
                    # Avoid duplicating proposals
                    continue
                group_proposals_uuid.add(row[_["parent_uuid"]])
                items_uuid_list = get_proposals_uuid_by_parent(row[_["parent_uuid"]])
            else:
                # 2) Single proposal
                items_uuid_list = [row[_["uuid"]]]
            proposal_items = {}
            disposition = ""

            for gp_uuid in items_uuid_list:

                _sp = get_simple_proposal(gp_uuid)

                mgnt_info = get_proposals_management(_sp["proposalmanagementinformation_uuid"])

                if mgnt_info['disposition']:
                    disposition = mgnt_info['disposition'].lower()
                else:
                    disposition = ""

                item_uuid = mgnt_info['item_uuid']
                item_class = name_classes[_sp['itemclassname']]

                item_body = objects_dumpers[item_class](item_uuid)

                if not item_body:
                    continue
                item_filename = "/%s/%s.yaml" % (item_class, item_body.get('uuid'))

                proposal_type = get_proposal_type(_sp["proposalmanagementinformation_uuid"])
                item_type = proposal_type["type"]

                proposal_items[item_filename] = {
                    "item_uuid": item_uuid,
                    "item_body": item_body,
                    "item_class": item_class,
                    # "disposition": disposition,
                    "type": item_type
                }
                if item_type == "amendment":
                    proposal_items[item_filename]["amendmentType"] = proposal_type["amendmentType"]
                    if proposal_type["amendmentType"] == "supersession":
                        if supersedingitems_uuid := get_supersedingitems_uuid(row[_["parent_uuid"]]):
                            proposal_items[item_filename]["supersedingItemIDs"] = [supersedingitems_uuid]
                        else:
                            proposal_items[item_filename]["supersedingItemIDs"] = []

            mgnt_info = get_proposals_management(sp["proposalmanagementinformation_uuid"])
            responsible_parties = transform_responsible_parties(mgnt_info['responsible_party'])
            role = responsible_parties.pop('role')

            dateproposed = mgnt_info['dateproposed']
            datedisposed = mgnt_info['datedisposed']

            data = {
                "submittingStakeholderGitServerUsername": "984851E6-82C6-4CE6-AB58-EF09D3FE412B",
                "controlBodyDecisionEvent": mgnt_info['controlbody_decision_event'],
                "controlBodyNotes": mgnt_info['controlbody_notes'],
                "registerManagerNotes": mgnt_info['register_manager_notes'],
                "justification": mgnt_info['justification'],
                "state": disposition,
                # "sponsor": {
                #     "gitServerUsername": "",
                #     "name": mgnt_info['responsible_party'][0]['name'],
                #     "role": role,
                #     "parties": [responsible_parties]
                # },

                "timeProposed": dateproposed,
                "timeDisposed": datedisposed,

                "items": proposal_items,

                "id": row[_["uuid"]],
                "title": row[_["title"]],
                "isConcluded": row[_["isconcluded"]],
                "notes": get_proposals_notes(row[_["uuid"]]),
            }

            data["pastTransitions"] = []
            if dateproposed:
                data["pastTransitions"].append({
                    "label": "Propose",
                    "timestamp": str(dateproposed),
                    # "fromState": "draft",
                    # "toState": "proposed",
                    "stakeholder": {
                        "name": mgnt_info['responsible_party'][0]['name'],
                        "role": role
                    },
                    "input": {
                        "justification": mgnt_info['justification']
                    }
                })

            if datedisposed:
                data["pastTransitions"].append({
                    "label": "Accept",
                    "timestamp": str(datedisposed),
                    # "fromState": "pending-control-body-review",
                    # "toState": "accepted",
                    "stakeholder": {
                        "name": mgnt_info['responsible_party'][0]['name'],
                        "role": role
                    },
                    "input": {
                        "controlBodyNotes": mgnt_info['controlbody_notes']
                    }
                })

            proposals.append(data)
        # else:
        #     print(f"No simple proposal found for {row[_['uuid']]}")

    for proposal in proposals:
        uuid = proposal.get("id")

        for proposal_item in proposal['items']:
            _item_uuid = proposal['items'][proposal_item].pop('item_uuid')
            _item_class = proposal['items'][proposal_item].pop('item_class')
            _body = proposal['items'][proposal_item].pop('item_body')
            _uuid = _body.get('uuid')
            _body = prepare_single_proposal_item(_body)

            _dirname = "proposals/%s/items/%s" % (uuid, _item_class)

            save_yaml(_uuid, _dirname, _body)

        save_yaml("main", "proposals/%s" % uuid, proposal)


def is_proposal_group(uuid):
    cur.execute(
        """
        SELECT
            count(uuid)
        FROM
            proposal
        WHERE
            parent_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    return cur.fetchone()[0] > 0


def get_proposals_uuid_by_parent(parent_uuid):
    cur.execute(
        """
        SELECT
            uuid
        FROM
            proposal
        WHERE
            parent_uuid = %(parent_uuid)s
    """,
        {"parent_uuid": parent_uuid},
    )

    items = []

    for row in cur.fetchall():
        items.append(row[0])

    return items


def get_clarification(uuid):
    cur.execute(
        """
        SELECT
            proposedchange
        FROM
            re_clarificationinformation
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0]


def is_addition(uuid):
    cur.execute(
        """
        SELECT
            uuid
        FROM
            re_additioninformation
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0].lower()


def get_amendment_type(uuid):
    cur.execute(
        """
        SELECT
            amendmenttype
        FROM
            re_amendmentinformation
        WHERE
            uuid = %(uuid)s

    """,
        {"uuid": uuid},
    )

    _row = cur.fetchone()

    if _row:
        return _row[0].lower()


def get_proposal_type(uuid):
    if is_addition(uuid):
        return {
            'type': 'addition'
        }
    elif amendment := get_amendment_type(uuid):
        return {
            'type': 'amendment',
            'amendmentType': amendment
        }
    elif clarification := get_clarification(uuid):
        return {
            'type': 'clarification',
            'proposedChange': clarification
        }
    else:
        print('failed to detect proposal type: %s' % uuid)


def prepare_single_proposal_item(item):
    uuid = item.pop("uuid")
    date_accepted = item.pop("dateAccepted")
    status = item.pop("status")
    if status.lower() == "not_valid":
        status = "invalid"

    data = {
        "id": uuid,
        "dateAccepted": date_accepted,
        "status": status,
        "data": item,
    }

    return data


def transform_responsible_parties(data):
    output = {
        "contacts": []
    }

    role = ''
    for item in data:
        name = item.get('name')

        output['contacts'].append({"name": name})

        for party in item['parties']:
            role = item.get('role')
            output['contacts'].append({
                "label": "name",
                "value": party.get("individual_name")
            })

    output['role'] = role
    return output


def get_proposals_notes(uuid):
    cur.execute(
        """
        SELECT
            uuid,
            note,
            author_uuid
        FROM
            proposalnote
        WHERE
            proposal_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "note": row[_["note"]],
                "author_uuid": row[_["author_uuid"]]
            }
        )

    return items


def get_proposals_management(uuid):
    cur.execute(
        """
        SELECT
            uuid,
            controlbodydecisionevent,
            controlbodynotes,
            datedisposed,
            dateproposed,
            disposition,
            justification,
            registermanagernotes,
            status,
            item_uuid,
            sponsor_uuid
        FROM
            re_proposalmanagementinformation
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "controlbody_decision_event": row[_["controlbodydecisionevent"]],
                "controlbody_notes": row[_["controlbodynotes"]],
                "datedisposed": row[_["datedisposed"]],
                "dateproposed": row[_["dateproposed"]],
                "disposition": row[_["disposition"]],
                "justification": row[_["justification"]],
                "register_manager_notes": row[_["registermanagernotes"]],
                "status": row[_["status"]],
                "item_uuid": row[_["item_uuid"]],
                "sponsor_uuid": row[_["sponsor_uuid"]],
                "responsible_party": get_proposals_organization(row[_["sponsor_uuid"]])
            }
        )

    # uuid in re_proposalmanagementinformation is uniq (pk)
    return items[0]


def get_proposals_management_uuids(item_uuid):
    cur.execute(
        """
        SELECT
            uuid
        FROM
            re_proposalmanagementinformation
        WHERE
            item_uuid = %(item_uuid)s
    """,
        {"item_uuid": item_uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(row[_["uuid"]])

    return items


def get_proposals_organization(uuid):\

    cur.execute(
        """
        SELECT
            uuid,
            name,
            contact_uuid

        FROM
            re_submittingorganization
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "name": row[_["name"]],
                "contact_uuid": row[_["contact_uuid"]],
                "parties": get_responsible_party(row[_["contact_uuid"]])
            }
        )

    return items


def get_responsible_party(uuid):
    cur.execute(
        """
        SELECT
            uuid,
            individualname,
            organisationname,
            positionname,
            codespace,
            role,
            contactinfo_uuid,
            role_codelist,
            role_codelistvalue,
            role_qname

        FROM
            ci_responsibleparty
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "individual_name": row[_["individualname"]],
                "organisation_name": row[_["organisationname"]],
                "position_name": row[_["positionname"]],
                "codespace": row[_["codespace"]],
                "role": row[_["role"]],
                "contactinfo_uuid": row[_["contactinfo_uuid"]],
                "role_codelist": row[_["role_codelist"]],
                "role_codelistvalue": row[_["role_codelistvalue"]],
                "role_qname": row[_["role_qname"]]
            }
        )

    return items


def get_simple_proposal(uuid):
    cur.execute(
        """
        SELECT
            uuid,
            proposalmanagementinformation_uuid,
            itemclassname,
            targetregister_uuid
        FROM
            simpleproposal
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                # "management_information": mg_data,
                "proposalmanagementinformation_uuid": row[_["proposalmanagementinformation_uuid"]],
                "itemclassname": row[_["itemclassname"]],
                "targetregister_uuid": row[_["targetregister_uuid"]]
            }
        )

    # uuid is PK
    if items:
        return items[0]
    else:
        return None


def get_simple_proposal_by_management_uuid(uuid):
    cur.execute(
        """
        SELECT
            uuid,
            proposalmanagementinformation_uuid,
            itemclassname
            
        FROM
            simpleproposal
        WHERE
            proposalmanagementinformation_uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "uuid": row[_["uuid"]],
                "proposalmanagementinformation_uuid": row[_["proposalmanagementinformation_uuid"]],
                "itemclassname": row[_["itemclassname"]]
            }
        )

    # uuid is PK
    if items:
        return items[0]
    else:
        return None


def get_proposal_by_simple_proposal_uuid(uuid):
    cur.execute(
        """
        SELECT
            parent_uuid
        FROM
            proposal
        WHERE
            uuid = %(uuid)s
    """,
        {"uuid": uuid},
    )

    items = []
    _ = get_cols_dict()

    for row in cur.fetchall():
        items.append(
            {
                "parent_uuid": row[_["parent_uuid"]],
            }
        )

    # uuid is PK
    if items:
        return items[0]
    else:
        return None


def export_extents_to_csv(extents):
    extents_data = {}
    for extent in extents:

        east = extent.get("e")
        north = extent.get("n")
        west = extent.get("w")
        south = extent.get("s")

        extent_description = extent.get("name")
        punctuation = re.compile(r'^(.*?)([.,!?;:\'"()-]*)$')
        cleaned_text = punctuation.sub(r"\1", extent_description)

        # remove trailing whitespaces
        cleaned_text = cleaned_text.strip()
        # remove duplicate whitespaces
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        if extent_data := extents_data.get(cleaned_text):
            if extent_data.get("e") == east and \
                    extent_data.get("n") == north and \
                    extent_data.get("w") == west and \
                    extent_data.get("s") == south:
                extents_data[cleaned_text]["ids"].append(extent["id"])
            else:
                extents_data[cleaned_text + "  ***POSSIBLE DUPLICATE***"] = {
                    "ids": [extent["id"]],
                    "e": east,
                    "n": north,
                    "w": west,
                    "s": south,
                    "name": None
                }
        else:
            extents_data[cleaned_text] = {
                "ids": [extent["id"]],
                "e": east,
                "n": north,
                "w": west,
                "s": south,
                "name": None
            }

    fields = ['description', 'ids', 'e', 'n', 'w', 's', 'name']
    with open("extents.csv", "w") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for key, val in sorted(extents_data.items()):
            row = {"description": key}
            row.update(val)
            w.writerow(row)


def export_information_sources_to_csv(information_sources):
    information_sources_data = {}
    for information_source in information_sources:
        description = information_source.get("title")
        seriesName = information_source.get("seriesName")
        seriesIssueId = information_source.get("seriesIssueID")

        author = information_source.get("author")
        publisher = information_source.get("publisher")
        publicationDate = information_source.get("publicationDate")
        editionDate = information_source.get("editionDate")
        otherDetails = information_source.get("otherDetails")

        source_citation_online_resource = None
        if otherDetails:
            urls = re.findall(r'(https?://\S+)', otherDetails)
            if len(urls) > 0:
                source_citation_online_resource = urls[0]

        punctuation = re.compile(r'^(.*?)([.,!?;:\'"()-]*)$')
        cleaned_text = punctuation.sub(r"\1", description)

        if seriesName:
            seriesName = punctuation.sub(r"\1", seriesName)
        if seriesName == '':
            seriesName = None

        if seriesIssueId:
            seriesIssueId = punctuation.sub(r"\1", seriesIssueId)
        if seriesIssueId == '':
            seriesIssueId = None

        # remove trailing whitespaces
        cleaned_text = cleaned_text.strip()
        # remove duplicate whitespaces
        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        if information_source_data := information_sources_data.get(cleaned_text):
            if information_source_data.get("seriesName") == seriesName and \
                    information_source_data.get("seriesIssueID") == seriesIssueId and \
                    information_source_data.get("author") == author and \
                    information_source_data.get("publisher") == publisher and \
                    information_source_data.get("publicationDate") == publicationDate and \
                    information_source_data.get("editionDate") == editionDate and \
                    information_source_data.get("otherDetails") == otherDetails:
                information_sources_data[cleaned_text]["ids"].append(information_source["id"])
            else:
                information_sources_data[cleaned_text + "  ***POSSIBLE DUPLICATE***"] = {
                    "ids": [information_source["id"]],
                    "name": "",
                    "seriesName": seriesName,
                    "seriesIssueID": seriesIssueId,
                    "author": author,
                    "publisher": publisher,
                    "publicationDate": publicationDate,
                    "editionDate": editionDate,
                    "otherDetails": otherDetails,
                    "source_citation_online_resource": source_citation_online_resource
                }
        else:
            information_sources_data[cleaned_text] = {
                "ids": [information_source["id"]],
                "name": "",
                "seriesName": seriesName,
                "seriesIssueID": seriesIssueId,
                "author": author,
                "publisher": publisher,
                "publicationDate": publicationDate,
                "editionDate": editionDate,
                "otherDetails": otherDetails,
                "source_citation_online_resource": source_citation_online_resource
            }

    fields = [
        'title', 'ids', 'seriesName', 'seriesIssueID', 'name', 'author',
        'publisher', 'publicationDate', 'editionDate', 'otherDetails',
        'source_citation_online_resource'
    ]
    with open("information_sources.csv", "w") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for key, val in sorted(information_sources_data.items()):
            row = {"title": key}
            row.update(val)
            w.writerow(row)


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
        "unit-of-measurement": units_dump,
        "proposals": proposals_dump
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

    export_extents_to_csv(extents)
    export_information_sources_to_csv(information_sources)
