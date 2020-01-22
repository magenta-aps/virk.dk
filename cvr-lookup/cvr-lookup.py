# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contributor(s): Heini L. Ovason
#

import json
import requests
import settings
from jinja2 import Template

success_file = open(settings.SUCCESS_FILE, "a")
success_file.write(f"CVRNR;NAVN;VEJNAVN;HUSNR;POSTNR;INPUT/SØGEPARAMETRE;\n")

failed_file = open(settings.FAILED_FILE, "a")

# input_file must be utf-8 encoded.
input_file = open(settings.INPUT_FILE, "r", encoding="utf-8")

for line in input_file:

    addr_line_array = line.split(";")

    navn = addr_line_array[0].replace("/", "\\\\/")
    vejnavn = addr_line_array[1].rsplit(" ", 1)[0]
    husnr = addr_line_array[1].rsplit(" ", 1)[1]
    postnr = addr_line_array[2].split(" ")[0]

    search_params = f"{navn}+{vejnavn}+{husnr}+{postnr}"

    with open(settings.QUERY_TEMPLATE, "r") as filestream:
        template_string = filestream.read()

    template_object = Template(template_string)

    populated_template = template_object.render(
        navn=navn,
        vejnavn=vejnavn,
        husnr=husnr,
        postnr=postnr
    )

    url = settings.VIRK_DK_ENDPOINT
    usr = settings.VIRK_DK_USERNAME
    pwd = settings.VIRK_DK_PASSWORD
    headers = {"Content-type": "application/json; charset=UTF-8"}
    payload = json.loads(populated_template)

    resp = requests.post(
        url,
        auth=(usr, pwd),
        json=payload,
        headers=headers
        )

    if resp.status_code is 200:
        try:
            resp_len = len(json.loads(resp.text).get("hits").get("hits"))
            if resp_len == 1:
                hits = json.loads(resp.text).get("hits").get("hits")
                virksomhed = hits[0].get("_source").get("Vrvirksomhed")
                cvr_no = virksomhed.get("cvrNummer", "NODATA")
                virk_meta = virksomhed.get("virksomhedMetadata")
                r_navn = virk_meta.get("nyesteNavn").get("navn", "NODATA")
                r_adresse = virk_meta.get("nyesteBeliggenhedsadresse")
                r_vejnavn = r_adresse.get("vejnavn", "NODATA")
                r_husnr = r_adresse.get("husnummerFra", "NODATA")
                r_postnr = r_adresse.get("postnummer", "NODATA")
                success_file.write(f"""{cvr_no};
                                    {r_navn};
                                    {r_vejnavn};
                                    {r_husnr};
                                    {r_postnr};
                                    {search_params};
                                    \n""")
            else:
                failed_file.write(f"Firma findes ikke -->{line}\n")
        except AttributeError as ae:
                failed_file.write(f"AttributeError -->{ae}\n")
                print(ae)

    else:
        failed_file.write(f"""HTTP Error -->{resp.status_code}\n
                        HTTP Response Body --> {resp.text}\n""")
        print(populated_template)

input_file.close()
success_file.close()
failed_file.close()