#!/usr/bin/env python
import re, json, os
from func_tools import Args, Composable, composable , Id, fmap, Log

link_re = r"\d+:\s+(?P<dev>\S+)\:\s+<\S+>\s+mtu\s+(?P<mtu>\d+)\.*"
rule_re = r"^\d+\:\s+(?P<rule>.*)\s+lookup\s+(?P<table_id>\w+)"
route_re = r"^((local|broadcast)\s+)?(?P<dst>\S+)\s+(via\s+(?P<gw>\S+)\s+)?dev\s+(?P<dev_name>\S+)(\s+table\s+(?P<table_id>\S+))?(\s+proto\s+(?P<proto>\S+))?(\s+scope\s+(?P<scope>\S+))?(\s+src\s+(?P<src>\S+))?(\s+metric\s+(?P<metric>\d+))?.*"
ip_addr_re = r"\d+:\s+(?P<dev>\S+)\s+inet(6)?\s+(?P<ip_addr_cidr>(?P<ip_addr>\S+)\/(?P<prefix>\d+))(\s+brd\s+\S+)?\s+scope\s+(?P<scope>\S+).*"

def ddd(cmd):
    print('dddd'+cmd)
    return os.popen(cmd).readlines()

cli_run_fnc = Composable(lambda cmd: os.popen(cmd).readlines())
#cli_run_fnc = Composable(ddd)
show_links      = cli_run_fnc << 'ip -o l'
#show_bonds      = cli_run_fnc << ('ip -o l show type bond')
#show_vlans      = cli_run_fnc << ('ip -o l show type vlan')
#show_macvlans    = cli_run_fnc << ('ip -o l show type macvlan')
#show_ipvlans     = cli_run_fnc << ('ip -o l show type ipvlan')
#show_ip_addrs    = cli_run_fnc << ('ip -o a')
#show_ip_routes   = cli_run_fnc << ('ip -o ro sh ta all')
#show_ip_rules_v4 = cli_run_fnc << ('ip ru sh')
#show_ip_rules_v6 = cli_run_fnc << ('ip -6 ru sh')
re_search_args = Args(Id, Id, 0)
link_search_args = Args(link_re, Id, 0)

show_slaves_of_port = cli_run_fnc << 'ip -o l show master {}'.format

parse_link_line = (re.search << link_search_args).groupdict
#
#show_slaves      = fmap << (show_slaves_of_port << log << parse_link_line, Id) << show_links
#print(show_links())

#print(show_slaves())
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



