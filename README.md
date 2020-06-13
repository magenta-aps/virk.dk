[![](https://www.magenta.dk/wp-content/uploads/2019/03/cropped-magenta_logo-2.png)](https://magenta.dk)

# virk.dk (EARLY DEVELOPMENT STAGES)

Python REST intergration with **distribution.virk.dk/cvr-permanent/virksomhed/_search**.

Initiated by MAGENTA ApS as a part of a *Proof Of Concept* for The Danish Environmental Protection Agency, a.k.a. Miljøstyrelsen.

### Prerequisite

The API is free of charge, but requires username and password from The Danish Business Authority (cvrselvbetjening@erst.dk)

### License

Mozilla Public License Version 2.0

### Features

  - **get_cvr_no(credentials, company_name, streetname, house_no, zipcode)**
  *Retrieves the CVR number (public unique identifier) of a given Danish company/organisation.*

  - **get_org_info(credentials, cvr_no)**
  *Retrieves name- and address information about a given company/organisation.*

### Upcoming features

  - **get_all_org_info(credentials, cvr_no)**
  *Retrieves all registered information about a given company/organisation.*

  - **Other suggestions?**

### Installation

virk.dk requires [Python](https://www.python.org/) v3.6+

```sh
$ virtualenv -p python3 test_package
$ cd test_package && mkdir src
$ . bin/activate
$ git clone git@github.com:magenta-aps/virk.dk.git 
$ cd virk.dk && python setup.py install
```

### Example of implementation

```python
from virk_dk import get_cvr_no

get_cvrnr_input_dict =	{
  "virk_usr": "<user>",
  "virk_pwd": "<token>",
  "virk_url": "http://distribution.virk.dk/cvr-permanent/virksomhed/_search",
  "org_name": "MAGENTA ApS",
  "street_name": "Pilestræde",
  "house_no_from": "43",
  "zipcode": "1112"
}
result = get_cvr_no(
    params_dict=get_cvrnr_input_dict
    )
print(result)
```
```python
from virk_dk import get_org_info

get_org_input_dict =	{
  "virk_usr": "<user>",
  "virk_pwd": "<token>",
  "virk_url": "http://distribution.virk.dk/cvr-permanent/virksomhed/_search",
  "cvr": "25052943"
}
result = get_org_info(
    params_dict=get_org_input_dict
    )
print(result)
```