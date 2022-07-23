#!/usr/bin/python
import os
import sys
import pgpy
from Crypto.Util.number import long_to_bytes

# This python script can parse the private keys out of OpenPGP keys (ed25519 or RSA). 
# Replace the passphrase with your OpenPGP passphrase.
print ("Entry rootkey passphrase")
rootkey_passphrase = sys.stdin.readline().strip()
# If you use a different passphrase for subkeys (such as rootless subkeys) replace 
# the passphrase below with your OpenPGP subkey passphrase
print ("Enter subkey passphrase (if you don't know it use your rootkey passphrase)")
subkey_passphrase = sys.stdin.readline().strip()
print ("Please enter your PGP Key (press enter and then control-d to end finish the user input)")
# Replace this with your ascii armored OpenPGP key
rootkey_ascii_armor = "".join(sys.stdin.readlines())
print (rootkey_ascii_armor)

(rootkey, _) = pgpy.PGPKey.from_blob(rootkey_ascii_armor)

# Or if you would prefer, import key as a file like this
# (rootkey, _) = pgpy.PGPKey.from_file('./testkey.asc')

# Run the script and raw keys will be displayed. Only run this on a 
# secure trusted system.

assert rootkey.is_protected
assert rootkey.is_unlocked is False

try:
    print('Load these raw key values to OnlyKey by using the OnlyKey App --> Advanced -> Add Private Key')
    with rootkey.unlock(rootkey_passphrase):
        # rootkey is now unlocked
        assert rootkey.is_unlocked
        print('rootkey is now unlocked')
        print('rootkey type %s', rootkey._key._pkalg)
        if 'RSA' in rootkey._key._pkalg._name_:
            print('rootkey value:')
            #Parse rsa pgp key
            primary_keyp = long_to_bytes(rootkey._key.keymaterial.p)
            primary_keyq = long_to_bytes(rootkey._key.keymaterial.q)
            print(("".join(["%02x" % c for c in primary_keyp])) + ("".join(["%02x" % c for c in primary_keyq])))
            print('rootkey size =', (len(primary_keyp)+len(primary_keyq))*8, 'bits')
            print('subkey values:')
            for subkey, value in rootkey._children.items():
                print('subkey id', subkey)
                sub_keyp = long_to_bytes(value._key.keymaterial.p)
                sub_keyq = long_to_bytes(value._key.keymaterial.q)
                print('subkey value')
                print(("".join(["%02x" % c for c in sub_keyp])) + ("".join(["%02x" % c for c in sub_keyq])))
                print('subkey size =', (len(primary_keyp)+len(primary_keyq))*8, 'bits')
        else:
            print('rootkey value:')
            #Parse ed25519 pgp key
            primary_key = long_to_bytes(rootkey._key.keymaterial.s)
            print("".join(["%02x" % c for c in primary_key]))
            print('subkey values:')
            for subkey, value in rootkey._children.items():
                print('subkey id', subkey)
                sub_key = long_to_bytes(value._key.keymaterial.s)
                print('subkey value')
                print("".join(["%02x" % c for c in sub_key]))
        
except:
    print('Unlocking root key failed, attempting rootless subkey unlock.')
    try:
        print('subkey key values:')
        for subkey, value in rootkey._children.items():
            assert value.is_protected
            assert value.is_unlocked is False
            with value.unlock(subkey_passphrase):
                # subkey is now unlocked
                assert value.is_unlocked
                print('subkey is now unlocked')
                print('subkey id', subkey)
                if 'RSA' in subkey._key._pkalg._name_:
                    sub_keyp = long_to_bytes(value._key.keymaterial.p)
                    sub_keyq = long_to_bytes(value._key.keymaterial.q)
                    print('subkey value')
                    print(("".join(["%02x" % c for c in sub_keyp])) + ("".join(["%02x" % c for c in sub_keyq])))
                else:
                    sub_key = long_to_bytes(value._key.keymaterial.s)
                    print('subkey value')
                    print("".join(["%02x" % c for c in sub_key]))
            # subkey is no longer unlocked
            assert value.is_unlocked is False
            
    except:
        print('Unlocking failed')

# rootkey is no longer unlocked
assert rootkey.is_unlocked is False

