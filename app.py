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

# input_file must be utf-8 encoded.
input_file = open(settings.INPUT_FILE, "r")

for line in input_file:

    addr_line_array = line.split(";")

    navn = addr_line_array[0]
    vejnavn = addr_line_array[1].rsplit(" ", 1)[0]
    husnr = addr_line_array[1].rsplit(" ", 1)[1]
    postnr = addr_line_array[2].split(" ")[0]

    with open(settings.QUERY_TEMPLATE, "r") as filestream:
        template_string = filestream.read()

    template_object = Template(template_string)

    populate_template = template_object.render(
        navn=navn,
        vejnavn=vejnavn,
        husnr=husnr,
        postnr=postnr
    )

    url = settings.VIRK_DK_ENDPOINT
    usr = settings.VIRK_DK_USERNAME
    pwd = settings.VIRK_DK_PASSWORD
    headers = {'Content-type': 'application/json'}
    
    r = requests.post(
        url, 
        auth=(usr, pwd),
        data=populate_template,
        headers=headers
        )

    response_body = print(r.text)

    break 
    # TODO
    # Create function to build JSON query

input_file.close()

