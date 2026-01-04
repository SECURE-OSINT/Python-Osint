import dns.resolver

def domain_has_mx(domain):
    try:
        dns.resolver.resolve(domain, "MX")
        return True
    except:
        return False
