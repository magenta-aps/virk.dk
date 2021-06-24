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
    virksomhed = org_dict.get("_source").get("Vrvirksomhed")
    cvr_no = virksomhed.get("cvrNummer", "")
    virk_meta = virksomhed.get("virksomhedMetadata")
    hoved_branche = virk_meta.get("nyesteHovedbranche")
    r_status = virk_meta.get("sammensatStatus")
    r_branchekode = hoved_branche.get("branchekode")
    r_navn = virk_meta.get("nyesteNavn").get("navn", "")
    r_adresse = virk_meta.get("nyesteBeliggenhedsadresse")
    r_vejnavn = r_adresse.get("vejnavn", "")
    r_husnr = r_adresse.get("husnummerFra", "")
    r_postnr = r_adresse.get("postnummer", "")

    return {
        "cvr_no": cvr_no,
        "navn": r_navn,
        "vejnavn": r_vejnavn,
        "husnr": r_husnr,
        "postnr": r_postnr,
        "branchekode": r_branchekode,
        "status": r_status,
    }


def val_cred_and_url(params_dict):


    virk_usr = params_dict.get("virk_usr", None)
    virk_pwd = params_dict.get("virk_pwd", None)
    virk_url = params_dict.get("virk_url", None)

    if virk_usr and virk_pwd and virk_url:
        return True
    else:
        return False


def get_org_info(params_dict):
    """Explanation pending
    """

    if val_cred_and_url(params_dict):

        cvr = params_dict.get("cvr", None)

        # If logged in then these params are the mininimum requirements.
        if cvr:

            here = os.path.dirname(os.path.abspath(__file__))
            template = os.path.join(here, 'query.j2')
            with open(template, "r") as filestream:
                template_string = filestream.read()

            template_object = Template(template_string)

            populated_template = template_object.render(
                cvr=cvr
            )

            url = params_dict.get("virk_url", None)
            usr = params_dict.get("virk_usr", None)
            pwd = params_dict.get("virk_pwd", None)
            headers = {"Content-type": "application/json; charset=UTF-8"}

            # json.decoder.JSONDecodeError does NOT LIKE the linebreaks in
            # the ElasticSearch query in the template.
            # Therefore we remove them before deserializing.
            payload = json.loads(populated_template.replace('\n', ''))

            resp = requests.post(
                url,
                auth=(usr, pwd),
                json=payload,
                headers=headers
            )

            if resp.status_code is 200:

                try:

                    resp_len = len(json.loads(
                        resp.text).get("hits").get("hits")
                    )

                    if resp_len == 1:

                        return resp.text

                    else:

                        # TODO: log(input, err) - Remove return statement

                        return "No hit for -->{0}".format(navn)

                except AttributeError as ae:

                    # TODO: log(input, err) - Remove return statement

                    return "AttributeError --> {0}".format(ae)

            # if resp.status_code ...
            else:

                # TODO: log(input, err) - Remove return statement

                return "HTTP Error --> {0}\nHTTP Body --> {1}".format(
                    resp.status_code,
                    resp.text
                )

        # if org_name ....
        else:

            # TODO: log(input, err) - Remove return statement

            return "ERROR: CVR Number missing in input dictionary."

    # if virk_usr and ...
    else:

        # TODO: log(input, err) - Remove return statement

        return "ERROR: Url and/or user credentials" \
            " are missing in input dictionary."


def get_cvr_no(params_dict):
    """Explanation pending
    """
    template = env.get_template('get_cvr_no_query.j2')

    if val_cred_and_url(params_dict):

        cvr = params_dict.get("cvr", None)
        org_name = params_dict.get("org_name", None)
        street_name = params_dict.get("street_name", None)
        house_no_from = params_dict.get("house_no_from", None)
        zipcode = params_dict.get("zipcode", None)

        # If logged in then these params are the mininimum requirements.
        if org_name and street_name and house_no_from and zipcode:

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

            url = params_dict.get("virk_url", None)
            usr = params_dict.get("virk_usr", None)
            pwd = params_dict.get("virk_pwd", None)

            headers = {"Content-type": "application/json; charset=UTF-8"}

            # json.decoder.JSONDecodeError does NOT LIKE the linebreaks in
            # the ElasticSearch query in the template.
            # Therefore we remove them before deserializing.
            payload = json.loads(populated_template.replace('\n', ''))

            resp = requests.post(
                url,
                auth=(usr, pwd),
                json=payload,
                headers=headers
            )

            if resp.status_code == 200:

                try:
                    resp_len = len(resp.json().get("hits").get("hits"))
                    if resp_len == 1:
                        hits = resp.json().get("hits").get("hits")
                        org_info = extract_org_info_from_virksomhed(hits[0])
                        return org_info
                    else:

                        # TODO: log(input, err) - Remove return statement

                        return "No hit for -->{0}".format(navn)

                except AttributeError as ae:

                    # TODO: log(input, err) - Remove return statement

                    return "AttributeError --> {0}".format(ae)

            # if resp.status_code ...
            else:

                # TODO: log(input, err) - Remove return statement

                return "HTTP Error --> {0}\nHTTP Body --> {1}".format(
                    resp.status_code,
                    resp.text
                )

        # if org_name ....
        else:

            # TODO: log(input, err) - Remove return statement

            return "ERROR: Company name and/or address info" \
                " missing in input dictionary."

    # if virk_usr and ...
    else:

        # TODO: log(input, err) - Remove return statement

        return "ERROR: Url and/or user credentials" \
                " are missing in input dictionary."


def get_org_info_from_cvr(params_dict):
    """
    Return an org_info dict from a cvr_number.
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
    Return an org_info dict from a general search on CVR/P number/Name.
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
