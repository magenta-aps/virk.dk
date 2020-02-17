![](https://www.magenta.dk/wp-content/uploads/2019/03/cropped-magenta_logo-2.png | height=35)

# Virk.dk 

# WARNING: DUE TO EARLY DEVELOPMENT STAGES USE WITH CAUTION. COMPREHENSIVE CHANGES TO E.G. API MIGHT OCCUR

Python intergration with **distribution.virk.dk/cvr-permanent/virksomhed/_search**.

*Developed by MAGENTA ApS as a part of project for The Danish Environmental Protection Agency.*

### Prerequisite

virk.dk's API is free of charge, but requires username and password from The Danish Business Authority (cvrselvbetjening@erst.dk)

### License

Mozilla Public License Version 2.0

### Features

  - **get_cvr_no(credentials, company_name, streetname, house_no, zipcode)**
  *Retrieves the unique identifier of a given company/organisation.*

### Upcoming feature(s)

  - **get_org_info(credentials, cvr_no)**
  *Retrieves the all registered information about a given company/organisation.*

### Installation ()

CVR Lookup requires [Python](https://www.python.org/) v3.6.+ to run.

Download, and go to project folder, and run:

```sh
$ python setup.py install
```

### Example of implementation

```
from virk_dk import get_cvr_no

input_dict =	{
  "virk_usr": "USERNAME",
  "virk_pwd": "PASSWORD",
  "virk_url": "http://distribution.virk.dk/cvr-permanent/virksomhed/_search", # note that this could change at some point.
  "org_name": "MAGENTA ApS",
  "street_name": "Pilestræde",
  "house_no_from": "43",
  "zipcode": "1112"
}

result = get_cvr_no(params_dict=input_dict)

print(result)
```

