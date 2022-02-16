# random_scripts

`create_tf_var_files.py` : Create Terraform variables.tf and terraform.tfvars file using variable names specified in *.tf files. 
                           Create *.tf files with references to variables. E.g. Name = var.ntp_name 
                           The script will add a "ntp_name" variable definition in variables.tf file and will add a variable in terraform.tfvars file.

`findCIMC.ps1` : Get UCS CIMC Product,Vendor Info using Redfish API without Auth

```
Sample Run:

> ./findCIMC.ps1
Please enter the subnet id in format [198.19.216]: 198.19.216 
Please enter the start IP last octet [163]: 150
Please enter the end IP last octet [167]: 165
Target: 198.19.216.150, Not Reachable
Target: 198.19.216.151, Not a Cisco UCS Server: Status Code: 404
Target: 198.19.216.152, Not a Cisco UCS Server: Status Code: 404
Target: 198.19.216.153, Not a Cisco UCS Server: Status Code: 404
Target: 198.19.216.154, Not a Cisco UCS Server: Status Code: 500
Target: 198.19.216.155, Not a Cisco UCS Server: Status Code: 500
Target: 198.19.216.156, Not a Cisco UCS Server: Status Code: 500
Target: 198.19.216.157, Not a Cisco UCS Server: Status Code: 500
Target: 198.19.216.158, Not Reachable
Target: 198.19.216.159, Not Reachable
Target: 198.19.216.160, Not Reachable
Target: 198.19.216.161, Not Reachable
Target: 198.19.216.162, Product Id: UCSC-C220-M5SX, Company: Cisco Systems Inc.                                         
Target: 198.19.216.163, Product Id: UCSC-C220-M5SX, Company: Cisco Systems Inc.                                         
Target: 198.19.216.164, Product Id: UCSC-C220-M5SX, Company: Cisco Systems Inc.                                         
Target: 198.19.216.165, Product Id: UCSC-C220-M5SX, Company: Cisco Systems Inc.   
```
