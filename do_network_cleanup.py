#!/usr/bin/env python
import re, json, os
from func_tools import Args, Composable, composable , Id, fmap, Log, call

link_re = r"\d+:\s+(?P<dev>\S+)\:\s+<\S+>\s+mtu\s+(?P<mtu>\d+)\.*"
rule_re = r"^\d+\:\s+(?P<rule>.*)\s+lookup\s+(?P<table_id>\w+)"
route_re = r"^((local|broadcast)\s+)?(?P<dst>\S+)\s+(via\s+(?P<gw>\S+)\s+)?dev\s+(?P<dev_name>\S+)(\s+table\s+(?P<table_id>\S+))?(\s+proto\s+(?P<proto>\S+))?(\s+scope\s+(?P<scope>\S+))?(\s+src\s+(?P<src>\S+))?(\s+metric\s+(?P<metric>\d+))?.*"
ip_addr_re = r"\d+:\s+(?P<dev>\S+)\s+inet(6)?\s+(?P<ip_addr_cidr>(?P<ip_addr>\S+)\/(?P<prefix>\d+))(\s+brd\s+\S+)?\s+scope\s+(?P<scope>\S+).*"

cli_run_fnc         = composable(lambda cmd: os.popen(cmd).readlines())
ip_cli              = cli_run_fnc << 'ip -o {}'.format
ip_cli_v6           = ip_cli << '-6 {}'.format
show_links          = ip_cli << 'link show'
show_slaves_of_link = ip_cli << 'link show master {}'.format
show_links_by_type  = ip_cli << 'link show type {}'.format
show_bonds          = show_links_by_type << "bond"
show_vlans          = show_links_by_type << "vlan"
show_bonds          = show_links_by_type << "macvlan"
show_bonds          = show_links_by_type << "ipvlan"
show_ip_addrs       = ip_cli << 'all'
show_ip_routes      = ip_cli << 'route show table all'
show_ip_rules_v4    = ip_cli << 'rule show'
show_ip_rules_v6    = ip_cli_v6 << 'rule show'

re_search           = re.search << Args(Id, Id, 0)
parse_link_line     = ((link_re, Id) >> re_search).groupdict >> call()['dev']
show_slaves         = fmap << (show_slaves_of_link << parse_link_line, Id) << show_links
print(show_links())

print(show_slaves())
'''
parse         = lambda _re, lines: [m.groupdict() for m in (re.search(_re, line, 0) for line in lines) if m]
parse_links   = lambda li: parse(link_re, li)
parse_address = lambda ad: parse(ip_addr_re, ad)
parse_rules   = lambda ru: parse(rule_re, ru)
parse_routes  = lambda ro: parse(route_re, ro)
find = lambda l, **kw: (i for i in l if all((i[k] == v for k,v in kw.items())))



links       = map(setattr, parse_links(show_links()))
bonds       = map(setattr, parse_links(show_bonds()))
vlans       = parse_links(show_vlans())
macvlans    = parse_links(show_macvlans())
ipvlans     = parse_links(show_ipvlans())
ip_addrs    = parse_address(show_ip_addrs())
routes      = parse_routes(show_ip_routes())
rules_v4    = parse_routes(show_ip_rules_v4())
rules_v6    = parse_routes(show_ip_rules_v6())
[bond.update({'slaves': parse_links(show_slaves(bond['dev']))}) for bond in bonds]

show_in_json = Composable(json.dumps) << Args(Id, indent=2)


def print_in_json(header, val):
    json_show = lambda val: json.dumps(val, indent=2)
    print("***** {} *****".format(header.upper()))
    print(json_show(val))
    print("")

links = {dev['dev']: dev for dev in links}
bonds = {dev['dev']: dev for dev in bonds}
links.update(bonds)

print_in_json('links', links)
print_in_json('bonds', bonds)
print_in_json('vlans', vlans)
print_in_json('macvlans', macvlans)
print_in_json('ipvlans', ipvlans)
print_in_json('ip_addrs', ip_addrs)
print_in_json('rules_v4', rules_v4)
print_in_json('rules_v6', rules_v6)
print_in_json('routes', routes)
'''



