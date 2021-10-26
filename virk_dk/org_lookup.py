# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contributor(s): Heini L. Ovason, Søren Howe Gersager
#
import json
import requests

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("virk_dk"),
    autoescape=select_autoescape()
)


def extract_org_info_from_virksomhed(org_dict):
    """
    Extract an org_info dict from Virk virksomhed JSON object.
    """
    virksomhed = org_dict.get("_source").get("Vrvirksomhed")
    cvr_no = virksomhed.get("cvrNummer", "")
    virk_meta = virksomhed.get("virksomhedMetadata")
    hoved_branche = virk_meta.get("nyesteHovedbranche")
    r_status = virk_meta.get("sammensatStatus")
    r_branchekode = hoved_branche.get("branchekode")
    r_branchetekst = hoved_branche.get("branchetekst")
    r_navn = virk_meta.get("nyesteNavn").get("navn", "")
    r_adresse = virk_meta.get("nyesteBeliggenhedsadresse")
    r_vejnavn = r_adresse.get("vejnavn", "")
    r_husnr = r_adresse.get("husnummerFra", "")
    r_postnr = r_adresse.get("postnummer", "")
    r_postdistrikt = r_adresse.get("postdistrikt", "")

    return {
        "cvr_no": cvr_no,
        "navn": r_navn,
        "vejnavn": r_vejnavn,
        "husnr": r_husnr,
        "postnr": r_postnr,
        "postdistrikt": r_postdistrikt,
        "branchekode": r_branchekode,
        "branchetekst": r_branchetekst,
        "status": r_status,
    }


def get_org_info_from_org_name_and_address(params_dict):
    """
    Return an org_info dict from an org_name and address info.

    Arguments:
    virk_usr - Virk user
    virk_pwd - Virk password
    virk_url - Virk endpoint URL
    org_name
    street_name
    house_no_from
    zipcode
    """
    template = env.get_template('get_org_info_from_org_name_and_address.j2')

    virk_usr = params_dict.get("virk_usr", None)
    virk_pwd = params_dict.get("virk_pwd", None)
    virk_url = params_dict.get("virk_url", None)

    if not virk_usr or not virk_pwd or not virk_url:
        return ("ERROR: Url and/or user credentials"
                " are missing in input dictionary.")

    org_name = params_dict.get("org_name", None)
    street_name = params_dict.get("street_name", None)
    house_no_from = params_dict.get("house_no_from", None)
    zipcode = params_dict.get("zipcode", None)

    # If logged in then these params are the mininimum requirements.
    if not org_name or not street_name or not house_no_from or not zipcode:
        return ("ERROR: Address info is missing in input dictionary.")

    navn = org_name.replace("/", "\\\\/")
    vejnavn = street_name
    # TODO: house letters need to be separate query param!
    hus_nr_fra = house_no_from
    postnr = zipcode

    populated_template = template.render(
        navn=navn,
        vejnavn=vejnavn,
        hus_nr_fra=hus_nr_fra,
        postnr=postnr
    )

    # json.decoder.JSONDecodeError does NOT LIKE the linebreaks in
    # the ElasticSearch query in the template.
    # Therefore we remove them before deserializing.
    payload = populated_template.replace('\n', '')

    resp = requests.post(
        virk_url,
        auth=(virk_usr, virk_pwd),
        json=json.loads(payload),
        headers={"Content-type": "application/json; charset=UTF-8"}
    )
    if not resp.status_code == 200:
        print(resp.status_code, resp.text)
        return

    hits = resp.json().get("hits").get("hits")

    orgs = []

    for org in hits:
        org_info = extract_org_info_from_virksomhed(org)
        orgs.append(org_info)
    return orgs


def get_org_info_from_cvr(params_dict):
    """
    Return an org_info dict from an *active* cvr_number.

    Arguments:
    virk_usr - Virk user
    virk_pwd - Virk password
    virk_url - Virk endpoint URL
    cvr_number - cvr_number
    """
    template = env.get_template('get_org_info_from_cvr.j2')

    virk_usr = params_dict.get("virk_usr", None)
    virk_pwd = params_dict.get("virk_pwd", None)
    virk_url = params_dict.get("virk_url", None)

    if not virk_usr or not virk_pwd or not virk_url:
        return ("ERROR: Url and/or user credentials"
                " are missing in input dictionary.")

    cvr_number = params_dict.get("cvr_number", None)
    if not cvr_number:
        return ("ERROR: CVR number is missing in input dictionary.")

    populated_template = template.render(
        cvr_number=cvr_number
    )

    resp = requests.post(
        virk_url,
        auth=(virk_usr, virk_pwd),
        json=json.loads(populated_template),
        headers={"Content-type": "application/json; charset=UTF-8"}
    )
    if not resp.status_code == 200:
        print(resp.status_code, resp.text)
        return

    hits = resp.json().get("hits").get("hits")

    orgs = []

    for org in hits:
        org_info = extract_org_info_from_virksomhed(org)
        orgs.append(org_info)
    return orgs


def get_org_info_from_cvr_p_number_or_name(params_dict):
    """
    Return an org_info dict from a general search on *active* CVR/P number/Name.

    Arguments:
    virk_usr - Virk user
    virk_pwd - Virk password
    virk_url - Virk endpoint URL
    search_term - term for searching
    """
    template = env.get_template('get_org_info_from_cvr_p_number_or_name.j2')

    virk_usr = params_dict.get("virk_usr", None)
    virk_pwd = params_dict.get("virk_pwd", None)
    virk_url = params_dict.get("virk_url", None)

    if not virk_usr or not virk_pwd or not virk_url:
        return ("ERROR: Url and/or user credentials"
                " are missing in input dictionary.")

    search_term = params_dict.get("search_term", None)
    if not search_term:
        return ("ERROR: Search term is missing in input dictionary.")

    populated_template = template.render(
        search_term=search_term
    )
    payload = json.loads(populated_template)
    resp = requests.post(
        virk_url,
        auth=(virk_usr, virk_pwd),
        json=payload,
    )
    if not resp.status_code == 200:
        print(resp.status_code, resp.text)
        return
    hits = resp.json().get("hits").get("hits")

    orgs = []

    for org in hits:
        org_info = extract_org_info_from_virksomhed(org)
        orgs.append(org_info)
    return orgs
