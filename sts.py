import boto
from boto.s3.connection import S3Connection
from boto.sts import STSConnection
import getopt, sys

if (len(sys.argv) <> 6):
    print 'Usage ' + sys.argv[0] + ' access_key secret_key mfa_serial_number mfa_token duration'
    exit(1)

access_key = sys.argv[1]
secret_key = sys.argv[2]
mfa_serial_number = sys.argv[3]
mfa_token = sys.argv[4]
duration = sys.argv[5]

sts = boto.connect_sts(access_key, secret_key)

token = sts.get_session_token(duration = 3600, force_new = True, mfa_serial_number = mfa_serial_number, mfa_token = mfa_token)
print('export AWS_ACCESS_KEY_ID=' + token.access_key )
print('export AWS_SECRET_ACCESS_KEY=' + token.secret_key )
print('export AWS_SECURITY_TOKEN=' + token.session_token )
