#!/bin/bash
#
# Connect to AWS EC2 Instance from this IP,
#   checking to see if this IP is in the Instance's Security Group,
#   adding this IP to the Security Group if not present.
# Then ssh, using a private key file, finding the Instance's public IP.
#
# Leverages AWS CLI, which must be installed and configured, prior.
#
# Use this in a situation where your computer's IP changes and the
# EC2 VM's IP changes.

## Change the following readonly vars:

readonly EC2_INSTANCE=XXXXX
readonly SECURITY_GROUP=XXXXXXX
readonly KEY=~/.ssh/XXXXX.pem
readonly USER=ubuntu

### Functions ###

#################
# Sets MYIP to this machine's IP, using AWS's whatsmyip url
# arguments: None
# returns: none
function this_ip() {
  #echo "Checking IP"
  MYIP=$(ping -c1 host.com | sed -nE 's/^PING[^(]+\(([^)]+)\).*/\1/p')
  echo "  Found ${MYIP}"
}

#################
# Check to see if given secgroup contains an IP.
# arguments: secgroup, ip
# returns: 1|0
function secgroup_has_ip() {
  if [[ -z "${1}" || -z "${2}" ]]; then
        echo "Missing SECGROUP or IP in call to secgroup_has_ip."
        return
  fi
  local SECGROUP=$1
  local IP=$2
  local IPEXISTS=0
  #echo "Checking if security group ${SECGROUP} has IP ${IP}"
  local HASIP="aws ec2 describe-security-groups --group-ids=${SECGROUP}"
  #echo "  has ip cmd: '${HASIP}'"
  local SECGROUP_INFO=$(${HASIP})
  case "${SECGROUP_INFO}" in
    *"${IP}"*) IPEXISTS=1 ;;
    *) IPEXISTS=0 ;;
  esac
  #echo "  IPEXISTS: ${IPEXISTS}"
  return ${IPEXISTS}
}

#################
# Add a given IP to a given secgroup
# Arguments: secgroup, ip
# Returns nothing
function add_ip_to_secgroup() {
  if [[ -z "${1}" || -z "${2}" ]]; then
        echo "Missing SECGROUP or IP in call to add_ip_to_secgroup."
        return
  fi
  local SECGROUP=$1
  local IP=$2
  #echo "Adding IP to security group."
  local ADDIP="aws ec2 authorize-security-group-egress --group-id ${SECGROUP} --protocol tcp --port 443 --cidr ${IP}/32"
  #echo " add ip cmd: '${ADDIP}'"
  RESULT=$(${ADDIP})
  #echo "  ${RESULT}"
}

#################
# Remove a given IP from a given security group
# TODO not used/finished
# Arguments: secgroup, ip
# Returns: nothing
function remove_ip_from_secgroup() {
  if [[ -z "${1}" || -z "${2}" ]]; then
        echo "Missing SECGROUP or IP."
        return
  fi
  local SECGROUP=$1
  local IP=$2
  local REMOVEIP="aws ec2 revoke-security-group-egress --group-id ${SECGROUP} --protocol tcp --port 443 --cidr ${IP}/32"
  #echo ${REMOVEIP}
}

function main() {
  this_ip
  secgroup_has_ip "${SECURITY_GROUP}" "${MYIP}"
  local IPEXISTS=$?
  if [[ "${IPEXISTS}" = 0 ]]; then
        add_ip_to_secgroup "${SECURITY_GROUP}" "${MYIP}"
  fi
}

main "$@"
