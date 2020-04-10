import boto3
import botocore
import os
import sys

# List all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
#print(regions)

for region in ec2_client.describe_regions()['Regions']:
    region_name = region['RegionName']
    ec2 = boto3.client("ec2", region_name=region_name)
    vpc = ec2.describe_vpcs()
    print(vpc)
    subnets = ec2.describe_subnets()
    print(subnets)
        #for subnet in vpc.subnets.all():
        #    print(vpc, "all:", subnet)
        #for az in ec2.meta.client.describe_availability_zones()["AvailabilityZones"]:
        #    for subnet in vpc.subnets.filter(Filters=[{"Name": "availabilityZone", "Values": [az["ZoneName"]]}]):
        #        print(vpc, "filter:", subnet)
