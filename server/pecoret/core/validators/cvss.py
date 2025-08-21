import re
from rest_framework.exceptions import ValidationError


CVSS_40_REGEX = (r'CVSS:4\.0\/AV:[N|A|L|P]\/AC:[L|H]\/AT:[N|P]\/PR:[N|L|H]\/UI:[N|P|A]\/VC:[H|L|N]\/'
                 r'VI:[H|L|N]\/VA:[H|L|N]\/SC:[H|L|N]\/SI:[H|L|N]\/SA:[H|L|N]')

CVSS_31_REGEX = r'CVSS:3\.1/AV:[N|A|L|P]/AC:[L|H]/PR:[N|L|H]/UI:[N|R]/S:[C|U]/C:[N|L|H]/I:[N|L|H]/A:[N|L|H]'


def cvss_regex_validator(value):
    # a validator to check if a CharField is a valid v3 or v4 CVSS Field
    p1 = re.compile(CVSS_40_REGEX)
    p2 = re.compile(CVSS_31_REGEX)
    if not (p1.match(value) or p2.match(value)):
        raise ValidationError('value does not match CVSS standard')
