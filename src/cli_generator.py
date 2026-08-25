def generate_cisco_cli(fix_description: str, osi_layer: str) -> str:
    """
    Translates high-level diagnoses into structured Cisco CLI configuration blocks.
    """
    text = fix_description.lower()
    
    if "trunk" in text or "vlan" in text:
        return (
            "```cisco\n"
            "configure terminal\n"
            "interface GigabitEthernet0/1\n"
            " switchport mode trunk\n"
            " switchport trunk native vlan 1\n"
            " no shutdown\n"
            "end\n"
            "write memory\n"
            "```"
        )
    elif "ip address" in text or "reconfigure static ip" in text or "layer 3" in osi_layer.lower():
        return (
            "```cisco\n"
            "configure terminal\n"
            "interface GigabitEthernet0/0\n"
            " ip address 192.168.1.1 255.255.255.0\n"
            " no shutdown\n"
            "end\n"
            "write memory\n"
            "```"
        )
    elif "dhcp" in text or "helper" in text:
        return (
            "```cisco\n"
            "configure terminal\n"
            "interface GigabitEthernet0/0.10\n"
            " ip helper-address 10.0.0.100\n"
            "end\n"
            "write memory\n"
            "```"
        )
    else:
        return f"! Manual verification required.\n! Reference guidance: {fix_description}"