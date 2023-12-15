#!/usr/bin/env python3
"""
    Script to Generate IOM/Adapter commands when multiple chassis's in use and append to ucsm_data.yml file.
    Part of workflow to gather stats from UCSM domains for troubleshooting.
    Script filenames:
        get_ucsm_stats.py
        gen_cmds.py
        ucsm_cmds.yml
"""
import yaml

if __name__ == '__main__':
    data_file = "ucsm_data.yml"
    server_count = 8   # In a chassis
    chassis_count = 2  # In a UCSM Domain
    cmds = []
    for chassis in range(chassis_count):
        cmds.append(f"attach fex {chassis+1}")
        cmds.append(f"show platform software woodside sts")
        for n in range(8):
            cmds.append(f"show platform software woodside rmon 0 ni{n}")
        for h in range(0,32,1):
            cmds.append(f"show platform software woodside rmon 0 hi{h}")
        cmds.append("exit")
        if chassis+1 == chassis_count:
            cmds.append("exit")

    for chassis in range(chassis_count):
        for server in range(server_count):
            cmds.append(f"connect adapter {chassis+1}/{server+1}/1")
            cmds.append("connect")
            cmds.append("attach-mcp")
            cmds.append("vnic")
            cmds.append("lifstats x")
            cmds.append("lifstats y")
            cmds.append("exit")
            cmds.append("exit")
            cmds.append("exit")
        if chassis+1 == chassis_count:
            cmds.append("exit")
    print(cmds)

    with open(data_file, 'r') as f:
        data = yaml.safe_load(f)

    data["commands"].extend(cmds)

    with open(data_file, 'w') as f:
        yaml.dump(data, f)
