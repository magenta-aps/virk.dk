[![](https://www.magenta.dk/wp-content/uploads/2019/03/cropped-magenta_logo-2.png)](https://magenta.dk)

# virk.dk (EARLY DEVELOPMENT STAGES)

Python REST integration with **distribution.virk.dk/cvr-permanent/virksomhed/_search**.

Initiated by MAGENTA ApS as a part of a *Proof Of Concept* for The Danish Environmental Protection Agency, a.k.a. Miljøstyrelsen.

### Prerequisite

The API requires a service account and token from The Danish Business Authority. They can be reached at: cvrselvbetjening@erst.dk

### License

Mozilla Public License Version 2.0

### Features

  - **get_org_info_from_org_name_and_address(credentials, company_name, streetname, house_no, zipcode)**
  *Retrieves company/organisation information from a company name and address information.*

  - **get_org_info_from_cvr(credentials, cvr_no)**
  *Retrieves company/organisation information from a CVR number.*

  - **get_org_info_from_cvr_p_number_or_name**
  *Retrieves company/organisation information from either CVR number, a P number or by name.*

### Upcoming features

  - **get_all_org_info(credentials, cvr_no)**
  *Retrieves all registered information about a given company/organisation.*

  - **Other suggestions?**

### Installation

virk.dk requires [Python](https://www.python.org/) v3.6+

```sh
$ virtualenv -p python3 test_package
$ cd test_package
$ . bin/activate
$ git clone git@github.com:magenta-aps/virk.dk.git 
$ cd virk.dk && python setup.py install
```

### Example of implementation

```python
from virk_dk import get_org_info_from_org_name_and_address

input_dict =	{
  "virk_usr": "<user>",
  "virk_pwd": "<token>",
  "virk_url": "http://distribution.virk.dk/cvr-permanent/virksomhed/_search",
  "org_name": "MAGENTA ApS",
  "street_name": "Pilestræde",
  "house_no_from": "43",
  "zipcode": "1112"
}
result = get_org_info_from_org_name_and_address(
    params_dict=input_dict
)
print(result)
```
```python
from virk_dk import get_org_info_from_cvr

input_dict =  {
  "virk_usr": "<user>",
  "virk_pwd": "<token>",
  "virk_url": "http://distribution.virk.dk/cvr-permanent/virksomhed/_search", # note that this could change at some point.
  "cvr_number": "25052943"
}

result = get_org_info_from_cvr(params_dict=input_dict)
print(result)
```
```python
from virk_dk import get_org_info_from_cvr_p_number_or_name

input_dict =  {
  "virk_usr": "<user>",
  "virk_pwd": "<token>",
  "virk_url": "http://distribution.virk.dk/cvr-permanent/virksomhed/_search", # note that this could change at some point.
  "search_term": "25553489" # could be either CVR number (25052943), P number (1019601052) or company name (Magenta Aps).
}
result = get_org_info_from_cvr_p_number_or_name(input_dict)
print(result)
```