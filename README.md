# random_scripts

`create_tf_var_files.py` : Create Terraform variables.tf and terraform.tfvars file using variable names specified in *.tf files. 
                           Create *.tf files with references to variables. E.g. Name = var.ntp_name 
                           The script will add a "ntp_name" variable definition in variables.tf file and will add a variable in terraform.tfvars file.
