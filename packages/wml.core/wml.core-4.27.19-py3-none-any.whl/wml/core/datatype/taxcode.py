import re


def valid_taxcode(taxcode: str) -> bool:
    if not isinstance(taxcode, str) or len(taxcode) < 5:
        return False
    if re.search("[^A-Z0-9\#\.\$/]", taxcode) is not None:
        return False
    if re.match("(A0)|(A1)|(WROOT)|(W0)|(V)|(FK)", taxcode):
        return True
