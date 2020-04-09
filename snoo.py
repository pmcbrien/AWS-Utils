import boto3
import botocore
import os
import sys

#Patrick McBrien

def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result

# List all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
print(regions)

for region in ec2_client.describe_regions()['Regions']:
    region_name = region['RegionName']
    print ("Listing VPC and subnet info on all accounts in org in region" + region_name)
    org_client = boto3.client('organizations')
    for account in paginate(org_client.list_accounts):
        #print "result  " + str(account['Id'])

        print (account['Id'], account['Name'], account['Arn'])
        ###     #if account['Id'] != rootaccount:
        if account['Id'] != '1234':

            #client_sess = getsession(account)
            #clientcf=client_sess.client('cloudformation')
            sc_client=boto3.client('ec2', region_name=region_name)
            try:
                response = sc_client.describe_vpcs()
                resp = response['Vpcs']
                if resp:
                    for rp in resp:
                        if rp['IsDefault']:
                            print(rp)
                            #return rp['VpcId']
                            #print(rp['CidrBlock']) + " VPC ID " + rp['VpcId'] + " Is Default " + str(rp['IsDefault']) + " Tag " + str(rp.get('Tags',"NA"))
                else:
                    print('No vpcs found')
            except:
                print("Error getting")
                raise




