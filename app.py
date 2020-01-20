# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import json
import requests
import settings

credentials = {
    'endpoint': settings.VIRK_DK_ENDPOINT,
    'username': settings.VIRK_DK_USERNAME,
    'password': settings.VIRK_DK_PASSWORD,
}

print(json.dumps(credentials))