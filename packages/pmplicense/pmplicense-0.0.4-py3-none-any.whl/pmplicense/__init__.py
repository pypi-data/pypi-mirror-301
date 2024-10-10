import base64
import datetime
import hashlib
import logging

from . import constants


LICENSES = {}

def set_license(pkgName, license):
    LICENSES[pkgName] = license


def unpack(b64raw):
    raw = base64.b64decode(b64raw).decode('utf-8')
    return {
        'raw': raw,
        'hash': raw.split('|')[0],
        'meta': raw.split('|')[1],
    }


def validate_license(unpacked):
    # format is base64('${hash}|${raw}')
    lHash = hashlib.md5(unpacked['meta'].encode()).hexdigest()
    return unpacked['hash'] == lHash


def decode_license(meta):
    # Meta format is 'on:${orderNo};pk:${packageName};lt:${licenseType};ex:${expirationDate}'
    parts = meta.split(';')
    decoded = {}
    for p in parts:
        k, v = p.split(':')
        decoded[k] = v
    return decoded


def order_number_valid(orderNo):
    # TODO
    return True


def is_expired(expirationDate):
    exp_date = datetime.datetime.strptime(expirationDate, '%Y-%m-%d')
    return exp_date < datetime.datetime.now()


def check_license(pkgName, license=None):
    # Check if license is valid for the given pkgName
    try:
        unpacked = unpack(license or LICENSES[pkgName])

        if not unpacked or not validate_license(unpacked):
            logging.error(constants.INVALID_LICENSE_ERROR)
            return False

        decoded = decode_license(unpacked["meta"])

        if not order_number_valid(decoded['oid']):
            logging.error(constants.INVALID_LICENSE_ERROR)
            return False

        if pkgName != decoded['pkg']:
            logging.error(constants.MISMATCHED_PACKAGE_ERROR)
            return False

        if decoded['lt'] == constants.LICENSE_TYPES["EDUCATIONAL"]:
            logging.warning(constants.EDUCATIONAL_LICENSE_WARN)
        elif decoded['lt'] == constants.LICENSE_TYPES["PERSONAL"]:
            logging.warning(constants.PERSONAL_LICENSE_WARN)
        elif decoded['lt'] == constants.LICENSE_TYPES["COMMERCIAL"]:
            logging.info(constants.COMMERCIAL_LICENSE_INFO)
        else:
            logging.error(constants.INVALID_LICENSE_ERROR)
            return False

        if is_expired(decoded['exp']):
            logging.error(constants.EXPIRED_LICENSE_ERROR)
            return False

        return True
    except Exception as error:
        logging.error(constants.INVALID_LICENSE_ERROR)
        return False