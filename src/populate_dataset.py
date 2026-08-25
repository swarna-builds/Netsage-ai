import csv
import os
from datetime import datetime

CSV_FILE = "data/cases.csv"

# 30 Pre-defined Cisco Packet Tracer / Lab Cases covering required topics
cases_data = [
    # VLAN Issues
    ("PC in VLAN 10 cannot ping PC in VLAN 10 on adjacent switch.", "Rule Engine (Fast Match)", "VLAN Trunking Error", "Layer 2", "High", "show interfaces trunk", "Set switchport mode trunk on interconnecting interfaces.", "ACCEPTED", "N/A"),
    ("Host on VLAN 20 cannot communicate with default gateway.", "Gemini AI", "Access Port Assigned to Wrong VLAN", "Layer 2", "High", "show switchport interface", "Reassign interface to VLAN 20 using switchport access vlan 20.", "ACCEPTED", "N/A"),
    ("Switch port error-disabled due to port-security violation.", "Gemini AI", "Port Security Violation", "Layer 2", "High", "show interface port-security", "Clear sticky MAC settings and issue shutdown / no shutdown on port.", "ACCEPTED", "N/A"),
    ("Trunk link down between Core and Access switches.", "Gemini AI", "Native VLAN Mismatch", "Layer 2", "Medium", "show cdp neighbors detail", "Align native VLAN IDs on both ends of trunk interface.", "ACCEPTED", "N/A"),

    # Gateway / Routing Issues
    ("PC gets IP but cannot reach server in VLAN 30; gateway ping works.", "Gemini AI", "Inter-VLAN Routing Failure / Missing Route", "Layer 3", "Medium", "show ip route", "Add ip route command or configure router-on-a-stick subinterfaces.", "ACCEPTED", "N/A"),
    ("R1 cannot reach subnet on R2 across serial link.", "Gemini AI", "Static Route Next-Hop Unreachable", "Layer 3", "High", "show ip route", "Correct destination next-hop IP in static route table.", "ACCEPTED", "N/A"),
    ("OSPF neighbor adjacencies failing to establish.", "Gemini AI", "OSPF Area / Hello Interval Mismatch", "Layer 3", "High", "show ip ospf neighbor", "Align OSPF area IDs and timer intervals across neighboring routers.", "ACCEPTED", "N/A"),
    ("High latency occurs when traffic passes across BGP peering link.", "Gemini AI", "BGP Path Selection Suboptimal", "Layer 3", "Low", "show ip bgp", "Adjust MED or Local Preference attributes for preferred routing.", "EDITED", "AI suggested resetting BGP peer; preferred adjusting Local Preference instead."),
    ("Router unable to forward packets to remote subnet 10.20.0.0/16.", "Gemini AI", "Missing Default Gateway / Default Route", "Layer 3", "High", "show ip route", "Configure ip route 0.0.0.0 0.0.0.0 pointing to ISP edge router.", "ACCEPTED", "N/A"),

    # DHCP Issues
    ("Host receives APIPA address (169.254.x.x) on startup.", "Rule Engine (Fast Match)", "IP Configuration Error / DHCP Scope Mismatch", "Layer 3", "High", "show ip interface brief", "Reconfigure static IP setting or issue release/renew on host.", "ACCEPTED", "N/A"),
    ("Branch PCs not receiving dynamic IP addresses from central server.", "Gemini AI", "Missing IP Helper Address on Router Subinterface", "Layer 3", "High", "show run interface", "Add ip helper-address <DHCP_SERVER_IP> to interface configuration.", "ACCEPTED", "N/A"),
    ("DHCP pool exhausted on router, new clients failing connection.", "Gemini AI", "DHCP Scope Exhaustion", "Layer 7", "High", "show ip dhcp pool", "Increase subnet pool scope size or lower DHCP lease timeouts.", "ACCEPTED", "N/A"),

    # DNS Issues
    ("PC can ping 8.8.8.8 but cannot browse websites by hostname.", "Gemini AI", "DNS Resolution Failure", "Layer 7", "High", "nslookup", "Reconfigure primary and secondary DNS server IPs on host network config.", "ACCEPTED", "N/A"),
    ("Internal clients failing to resolve local domain domain.local.", "Gemini AI", "Corrupted DNS Forward Lookup Zone", "Layer 7", "Medium", "ipconfig /displaydns", "Flush client DNS cache and restart DNS service on domain controller.", "EDITED", "AI recommended changing DNS server; issue was resolved by clearing stale client cache."),

    # ACL Issues
    ("Engineering workstation blocked from accessing FTP server.", "Gemini AI", "Implicit Deny All in ACL", "Layer 4", "High", "show access-lists", "Add explicit permit rule above deny rule in access list.", "ACCEPTED", "N/A"),
    ("Guest Wi-Fi users able to access internal subnet 192.168.1.0/24.", "Gemini AI", "Missing Inbound Access Control List", "Layer 4", "High", "show access-lists", "Apply inbound ACL restricting access to private RFC 1918 addresses.", "ACCEPTED", "N/A"),
    ("SSH access to router core-rtr-01 timing out from management PC.", "Gemini AI", "VTY Line ACL Blocking IP Subnet", "Layer 4", "Medium", "show running-config | section vty", "Update access-class on line vty 0 4 to include management IP.", "ACCEPTED", "N/A"),
    ("Telnet blocked but SSH connection succeeds.", "Gemini AI", "Explicit ACL Block on TCP Port 23", "Layer 4", "High", "show ip access-lists", "Normal security posture; no action required unless Telnet is explicitly needed.", "REJECTED", "AI suggested enabling Telnet; rejected to maintain zero-trust security compliance."),

    # NAT Issues
    ("Internal host 192.168.1.10 unreachable from internet.", "Gemini AI", "Missing Static Port Forwarding / NAT Entry", "Layer 3", "High", "show ip nat translations", "Configure ip nat inside source static tcp for inbound traffic.", "ACCEPTED", "N/A"),
    ("LAN hosts lose internet connectivity during peak usage hours.", "Gemini AI", "PAT/NAT Port Overload Exhaustion", "Layer 3", "Medium", "show ip nat statistics", "Add additional public IPs to NAT pool dynamic allocation.", "ACCEPTED", "N/A"),
    ("NAT interface overload failing to translate traffic.", "Gemini AI", "NAT Outside / Inside Interface Configuration Inverted", "Layer 3", "High", "show ip nat translations", "Verify ip nat inside and ip nat outside directives on router interfaces.", "EDITED", "AI suggested restarting NAT service; corrected interface assignment tags."),

    # Wireless Issues
    ("Laptop cannot connect to enterprise Wi-Fi network SSID Corp-Wifi.", "Gemini AI", "WPA2 Enterprise / 802.1X Authentication Failure", "Layer 2", "Medium", "show wlan summary", "Verify RADIUS server shared secret key and user credentials.", "ACCEPTED", "N/A"),
    ("Wireless clients disconnecting periodically in conference room.", "Gemini AI", "RF Co-Channel Interference / High Noise Floor", "Layer 1", "Low", "show ap auto-rf", "Adjust AP channel power assignment and switch to non-overlapping channels.", "ACCEPTED", "N/A"),
    ("IoT devices failing to connect to 5GHz wireless access point.", "Gemini AI", "Band Mismatch (Device supports 2.4GHz only)", "Layer 1", "High", "show wlan wlan_id", "Enable 2.4GHz radio band broadcast on designated SSID.", "ACCEPTED", "N/A"),

    # Physical / Miscellaneous Issues
    ("Port speed mismatch detected between Core Switch and Server 01.", "Rule Engine (Fast Match)", "Physical / Data Link Layer Mismatch", "Layer 2", "High", "show interface status", "Set speed/duplex to auto-negotiate or configure matching parameters.", "ACCEPTED", "N/A"),
    ("Interface FastEthernet0/1 goes up and down constantly (flapping).", "Gemini AI", "Faulty Cabling / Damaged SFP Transceiver", "Layer 1", "High", "show interface status", "Replace Ethernet patch cable or optic SFP module.", "ACCEPTED", "N/A"),
    ("Switch port stuck in err-disabled state after loop detected.", "Gemini AI", "BPDU Guard Triggered by Unmanaged Switch", "Layer 2", "High", "show interface status err-disabled", "Remove unauthorized device and re-enable port with shutdown/no shutdown.", "ACCEPTED", "N/A"),
    ("High CPU utilization on core switch (over 98%).", "Gemini AI", "Broadcast Storm / Spanning Tree Protocol Loop", "Layer 2", "Medium", "show processes cpu sorted", "Verify STP topologies and configure PortFast / BPDU Filter correctly.", "REJECTED", "AI suggested rebooting core switch; resolved STP loop manually to avoid downtime."),
    ("Router interface line protocol is down, signal state is up.", "Gemini AI", "Layer 2 Framing / Keepalive Mismatch", "Layer 2", "High", "show interface", "Verify serial encapsulation type (HDLC/PPP) on both endpoints.", "ACCEPTED", "N/A"),
    ("VPN tunnel between site A and site B failing Phase 2 negotiation.", "Gemini AI", "IPsec Transform Set / Traffic Selector Mismatch", "Layer 3", "Medium", "show crypto ipsec sa", "Align Phase 2 IPsec transform sets and crypto map ACLs.", "EDITED", "AI recommended rebuilding tunnel from scratch; resolved by updating ACL matching rules.")
]

def populate():
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp", "Problem", "Source", "Root Cause", "OSI Layer", 
            "Confidence", "Next Command", "Proposed Fix", "Status", "Correction Reason"
        ])
        
        for case in cases_data:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                case[0], case[1], case[2], case[3], case[4], case[5], case[6], case[7], case[8]
            ])
            
    print(f"[SUCCESS] {len(cases_data)} cases successfully written to {CSV_FILE}!")

if __name__ == "__main__":
    populate()