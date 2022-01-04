#!/usr/bin/env python3
"""
The intention of creating this script is to easy the creation of variables.tf and terraform.tfvars files. 
Start by creating *.tf resource files with references to the variables. 
E.g. 
resource "demo_xyz" "demo_name" {
  Name = var.ntp_name
}
The script reads the *.tf resource files and creates variables.tf and terraform.tfvars files with below content.
Result:
Filename: variables.tf
variable "ntp_name" {
  type = 
  description = ""
  default = ""
}

Filename: terraform.tfvars
ntp_name = ""

The code does the following:
    - Read *.tf files in the current dir.
    - Check each line for var.xxx.
    - If we have a variable defined, create variables.tf file with the variable definition.
    - Create terraform.tfvars file with the variable.
    - Append variable template to the file with the variable name.
    - Skip lines starting with "#" or "  #". Modify line 24 for further filtering.
"""
import os
import re
import glob
from string import Template


def get_variable_names(tf_file):
    """
    Read .tf file, search for variable reference and add to a list.
    Return a list of unqiue variables defined in *.tf files
    """
    var_list = []
    with open(tf_file, 'r') as f:
        for line in f:
            if not re.search("^#|^  #", line):
                if re.findall(" var\.", line):
                    line_list = line.split()
                    for var in line_list:
                        if re.search('var\.', var):
                            var_list.append(var)
    # Create a list with variable names
    var_list2 = []
    for var in var_list:
        var_list2.append(re.split("\.", var)[1])
    # Create final list with unique variables
    tfvar_list = list(set(var_list2))
    return tfvar_list


def create_file_variables(tfvar_list):
    """
    Write template for each variable to variables.tf file
    """
    template = Template(
        'variable "$var_name" {\n  type = string\n  description = ""\n  default = ""\n}\n\n')
    for var in tfvar_list:
        with open("variables.tf", 'a') as f:
            f.write(template.substitute(var_name=var))
    print("variables.tf file created Successfully!")


def create_file_tfvars(tfvar_list):
    """
    Create terraform.tfvars file with all the variables.
    """
    for var in tfvar_list:
        with open("terraform.tfvars", "a") as f:
            data = f'{var} = ""\n'
            f.write(data)
    print("terraform.tfvars file created Successfully!")


def main():
    pwd = os.getcwd()
    path = f"{pwd}/*.tf"
    file_list = []
    for file in glob.glob(path):
        if file != "variables.tf":
            file_list.append(file)

    all_vars = []
    for file in file_list:
        tfvar_list = get_variable_names(file)
        for var in tfvar_list:
            all_vars.append(var)
    create_file_variables(all_vars)
    create_file_tfvars(all_vars)


if __name__ == '__main__':
    main()
