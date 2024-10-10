import base64
import hashlib

from src import pmplicense as pmp


def create_test_license(order_id, pkg_name, license_type, license_term, quantity, expiration_date):
    meta = f"oid:{order_id};pkg:{pkg_name};lt:{license_type};trm:{license_term};qty:{quantity};exp:{expiration_date}"
    hash = hashlib.md5(meta.encode()).hexdigest()
    raw = f"{hash}|{meta}"
    return base64.b64encode(raw.encode()).decode()


def test_generate_edu_license_check_license_valid():
    license = create_test_license('1234', 'pmp-license', 'EDU', 'ANN', 1, '2025-12-31')
    assert pmp.check_license('pmp-license', license) == True

def test_generate_per_license_check_license_valid():
    license = create_test_license('1234', 'pmp-license', 'PER', 'ANN', 1, '2025-12-31')
    assert pmp.check_license('pmp-license', license) == True

def test_generate_com_license_check_license_valid():
    license = create_test_license('1234', 'pmp-license', 'COM', 'ANN', 1, '2025-12-31')
    assert pmp.check_license('pmp-license', license) == True

def test_generate_com_license_set_license_check_license_valid():
    license = create_test_license('1234', 'pmp-license', 'PER', 'ANN', 1, '2025-12-31')
    pmp.set_license('pmp-license', license)
    assert pmp.check_license('pmp-license') == True

def test_hard_code_invalid_license_check_license_invalid():
    license = 'INVALID_LICENSE'
    assert pmp.check_license('pmp-license', license) == False

def test_hard_code_invalid_license_set_license_check_license_invalid():
    license = 'INVALID_LICENSE'
    pmp.set_license('pmp-license', license)
    assert pmp.check_license('pmp-license') == False

def test_generate_license_with_invalid_pkg_name_set_license_check_license_invalid():
    license = create_test_license('1234', 'INVALID-NAME', 'COM', 'ANN', 1, '2025-12-31')
    pmp.set_license('pmp-license', license)
    assert pmp.check_license('pmp-license') == False

def test_generate_license_with_invalid_type_set_license_check_license_invalid():
    license = create_test_license('1234', 'pmp-license', 'BAD', 'ANN', 1, '2025-12-31')
    pmp.set_license('pmp-license', license)
    assert pmp.check_license('pmp-license') == False

def test_generate_invalid_type_license_check_license_invalid():
    license = create_test_license('1234', 'pmp-license', 'INVALID_TYPE', 'ANN', 1, '2025-12-31')
    assert pmp.check_license('pmp-license', license) == False

def test_generate_expired_license_check_license_invalid():
    license = create_test_license('1234', 'pmp-license', 'COM', 'ANN', 1, '2022-12-31')
    assert pmp.check_license('pmp-license', license) == False

def test_generate_license_alter_meta_check_license_invalid():
    license = create_test_license('1234', 'pmp-license', 'COM', 'ANN', 1, '2035-12-31')
    license_parts = base64.b64decode(license).decode().split('|')
    new_license = base64.b64encode(f"{license_parts[0]}|INVALID_META".encode()).decode()
    assert pmp.check_license('pmp-license', new_license) == False

def test_generate_license_alter_hash_check_license_invalid():
    license = create_test_license('1234', 'pmp-license', 'COM', 'ANN', 1, '2035-12-31')
    license_parts = base64.b64decode(license).decode().split('|')
    new_license = base64.b64encode(f"badhash|{license_parts[1]}".encode()).decode()
    assert pmp.check_license('pmp-license', new_license) == False