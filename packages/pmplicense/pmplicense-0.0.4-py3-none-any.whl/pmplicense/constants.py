
INVALID_LICENSE_ERROR = """
======= PMP License Check =======
ERROR: Invalid License

You are using an unlicensed version of this software. Please purchase a valid license.
Commercial uses of this software under this license is prohibited and will be prosecuted. 
=================================
"""
EDUCATIONAL_LICENSE_WARN = """
======= PMP License Check =======
INFO: Educational License

You are using an educational license of this software. This license is valid for educational use only.
Commercial uses of this software under this license is prohibited and will be prosecuted. 
=================================
"""
PERSONAL_LICENSE_WARN = """
======= PMP License Check =======
INFO: Personal License

You are using a personal license of this software. This license is valid for personal, non-commercial use only.
Commercial uses of this software under this license is prohibited and will be prosecuted. 
=================================
"""

COMMERCIAL_LICENSE_INFO = """
======= PMP License Check =======
INFO: Commercial License

Thank you for purchasing a license. Enjoy!
=================================
"""

MISMATCHED_PACKAGE_ERROR = """
======= PMP License Check =======
ERROR: Mismatched Package

The license you are using is not for this package. Verify the package name and try again.
===============================
"""

EXPIRED_LICENSE_ERROR = """
======= PMP License Check =======
ERROR: License is expired.

The license you are using has expired. Please purchase a new one at https://pimpmypackage.com
===============================
"""


LICENSE_TYPES = {
    "EDUCATIONAL": 'EDU',
    "PERSONAL": 'PER',
    "COMMERCIAL": 'COM',
}
