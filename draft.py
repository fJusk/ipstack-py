from ipstackpy.api import IpStackClient


ips = ['192.165.0.0', '192.282.1.1']

client = IpStackClient(access_key='ca260c650d36be38f719c5ff938b8f15')
client.bulk_lookup(ips)
