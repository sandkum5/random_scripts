# random_scripts

`create_tf_var_files.py` : Create Terraform variables.tf and terraform.tfvars file using variable names specified in *.tf files. 
                           Create *.tf files with references to variables. E.g. Name = var.ntp_name 
                           The script will add a "ntp_name" variable definition in variables.tf file and will add a variable in terraform.tfvars file.

`findCIMC.ps1` : Get UCS CIMC Product,Vendor Info using Redfish API without Auth

```
Sample Run:

> ./findCIMC.ps1
Please enter the subnet id in format x.y.z: [198.19.216]: 198.19.216
Please enter the start IP last octet: [163]: 163
Please enter the end IP last octet: [167]: 167
Checking Target: 198.19.216.163
-------------------------------
 
@{Product=UCSC-C220-M5SX; Vendor=Cisco Systems Inc.}
 
Checking Target: 198.19.216.164
-------------------------------
 
@{Product=UCSC-C220-M5SX; Vendor=Cisco Systems Inc.}
 
Checking Target: 198.19.216.165
-------------------------------
 
@{Product=UCSC-C220-M5SX; Vendor=Cisco Systems Inc.}
 
Checking Target: 198.19.216.166
-------------------------------
 
@{Product=UCSC-C220-M5SX; Vendor=Cisco Systems Inc.}
 
Checking Target: 198.19.216.167
-------------------------------
 
Invoke-RestMethod: /path/to/script/findCIMC.ps1:12:17
Line |
  12 |  … $response = Invoke-RestMethod -SkipCertificateCheck -Method 'GET' -Ur …
     |                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     | The request was canceled due to the configured HttpClient.Timeout of 2 seconds elapsing.

```
