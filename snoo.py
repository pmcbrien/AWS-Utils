import boto3
import botocore
import os
import sys

#Patrick McBrien
#THIS FINDS ALL REGIONS IN ORG AND LOOPS THROUGH ALL ACCOUNTS IN ORG AND DUMPS VPC/CIDR INFO

####################################################################################################
# Get AWS Credentials
def get_new_client(account_id, resource, region):
    """Return temp creds for each account"""

    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    try:
        response = DEFAULT_CLIENT.assume_role(
            RoleArn="arn:aws:iam::" + account_id + ":role/" + AWS_ROLE,
            RoleSessionName="AssumeRoleSession1"
            )

        session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                      aws_session_token=response['Credentials']['SessionToken'],
                      region_name=region)

        return session.client(resource)

    except botocore.exceptions.ClientError as e:
        logging.info("Error: %s", e)

        
####################################################################################################
# Get All Account Instances
def get_all_instances(ec2_client):
    """Return ALL Instances to Compare against SSM"""
    logging.info('Getting SSM Inventory')

    # Utilize SSM Paginator
    paginator = ec2_client.get_paginator('describe_instances')

    response_iterator = paginator.paginate(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values' :['running', 'stopped']
            }]
    )

    # Initialize Instance List
    ec2_instances = []

    ## Loop Through Inventory in each Account
    for reservations in response_iterator:
        for instances in reservations['Reservations']:
            ec2_instances.append(instances['Instances'][0])

    # Send back list of Instances
    return ec2_instances

def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result

# List all regions
#ec2_client = boto3.client('ec2')

# Get EC2 Client
ec2_client = get_new_client(account, 'ec2', region)

# Grab All Instances
all_instances = get_all_instances(ec2_client)


regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
#print(regions)
#
org_client = boto3.client('organizations')
for account in paginate(org_client.list_accounts):
    #print (" AccountId  " + str(account['Id']))
    #print (account['Id'], account['Name'], account['Arn'])
    #if account['Id'] != rootaccount:
    #print (account['Status'])
    #if account['Id'] != '134': #use if you want to leave out ROOT account.
    if account['Status'] == 'ACTIVE':
        for region in ec2_client.describe_regions()['Regions']:
            region_name = region['RegionName']

            sc_client=boto3.client('ec2', region_name=region_name)
            try:
                response = sc_client.describe_vpcs()
                resp = response['Vpcs']
                if resp:
                    for rp in resp:
                        #if rp['IsDefault']:

                        print('\n\n')
                        print ("AccountId " + str(account['Id']))
                        print ("Region " + region_name )
                        print("OwnerId " + rp['OwnerId'])
                        print("VPCId " + rp['VpcId'])
                        print (rp['CidrBlock'])
                        print(rp)
                else:
                    print('No vpcs found')
            except:
                print("Error getting")
                raise




