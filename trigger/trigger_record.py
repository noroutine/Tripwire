from ipaddress import ip_address
import logging
from bloom_filter2 import BloomFilter

RECORD_FILE = "/var/www/html/record.txt"

bloom = BloomFilter(max_elements=10000000, error_rate=0.1)

logging.info("Loading addresses from " + RECORD_FILE)

address_count = 0
with open(RECORD_FILE, "r") as record_file:
    for line in record_file:
        ip_addr = line.rstrip()
        logging.debug("Loaded " + ip_addr)
        if ip_addr not in bloom:
            address_count += 1            
            bloom.add(ip_addr)

logging.info(f"Loaded {address_count} addresses from {RECORD_FILE}")

def icmp_trigger(eth, iph, icmph):
    pass

def tcp_trigger(eth, iph, tcph):
    pass

def udp_trigger(eth, iph, udph):
    pass

def trigger(eth, iph):
    if str(iph.src_addr) not in bloom:
        with open(RECORD_FILE, "a") as record_file:
            record_file.write(iph.src_addr + "\n")
        logging.info(f"action=recorded addr={str(iph.src_addr)}")
        bloom.add(str(iph.src_addr))
    else:
        logging.info(f"action=known-ignore addr={str(iph.src_addr)}")
