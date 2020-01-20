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

credentials = {
    'endpoint': settings.VIRK_DK_ENDPOINT,
    'username': settings.VIRK_DK_USERNAME,
    'password': settings.VIRK_DK_PASSWORD,
}

# input_file must be utf-8 encoded.
input_file = open(settings.INPUT_FILE, "r")

for line in input_file:

    addr_line_array = line.split(";")

    navn = addr_line_array[0]
    vejnavn = addr_line_array[1].rsplit(" ", 1)[0]
    husnr = addr_line_array[1].rsplit(" ", 1)[1]
    postnr = addr_line_array[2].split(" ")[0]

    print("{0} - {1} - {2} - {3}".format(navn, vejnavn, husnr, postnr))

    # TODO
    # Create function to build JSON query

input_file.close()