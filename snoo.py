import boto3
import botocore
import os
import sys
import json

# List all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
#print(regions)

for region in ec2_client.describe_regions()['Regions']:
    region_name = region['RegionName']
    print ('REGION ' + region_name)

    #vpc
    ec2 = boto3.client("ec2", region_name=region_name)
    vpc = ec2.describe_vpcs()
    print(json.dumps(vpc))

    #subnets
    subnets = ec2.describe_subnets()
    print(json.dumps(subnets))
