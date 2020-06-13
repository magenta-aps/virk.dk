# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contributor(s): Heini L. Ovason
#

import os
import json
import requests
from jinja2 import Template


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

            here = os.path.dirname(os.path.abspath(__file__))
            template = os.path.join(here, 'query.j2')
            with open(template, "r") as filestream:
                template_string = filestream.read()

            template_object = Template(template_string)

            populated_template = template_object.render(
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

            if resp.status_code is 200:

                try:

                    resp_len = len(json.loads(
                        resp.text).get("hits").get("hits")
                    )

                    if resp_len == 1:

                        hits = json.loads(resp.text).get("hits").get("hits")
                        virksomhed = hits[0].get("_source").get("Vrvirksomhed")
                        cvr_no = virksomhed.get("cvrNummer", "")
                        virk_meta = virksomhed.get("virksomhedMetadata")
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
                            "postnr": r_postnr
                        }

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
