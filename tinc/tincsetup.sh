#!/usr/bin/env bash

CONFIG_SERVER=${CONFIG_SERVER:-"tinc.ktr.wiai.uni-bamberg.de"}
AUTH_TOKEN=${AUTH_TOKEN:-"changeme"}
TINC_NETWORKNAME=${TINC_NETWORKNAME:-"demo"}

EXPECTED_NODES=3
POLL_TIMEOUT=300
INTERFACE="eth0"

TINC_KEYLENGTH="512"
TINC_INTERFACE="tun0"

#######################
# generated parameter #
#######################
HOSTNAME=${HOSTNAME//[\-\_\.]/}
TINC_PATH="/etc/tinc"
NODE_HOST_FILES="${TINC_PATH}/${TINC_NETWORKNAME}/hosts"
NODE_CONFIG_FILE="${TINC_PATH}/${TINC_NETWORKNAME}/tinc.conf"

#######################

function get_ip_of_interface(){
  local interface="${1}"
  local all_ip_addresses=$(hostname -I)
  local interface_ip=$(ip a s "$interface" 2>/dev/null)
  for ip_address in $all_ip_addresses; do
    if [[ "$interface_ip" == *"$ip_address"* ]]; then
      echo "$ip_address"
    fi
  done
}

function evaluate_result(){
  local returnvalue="${1}"
  local message="${2}"
  if [ "$returnvalue" -eq 0 ]; then
    echo -e "\e[32m  [PASS] ${message}\e[0m"
  else
    echo -e "\e[31m  [FAIL] ${message}\e[0m"
  fi
}

function enable_autostart(){
  if [[ ($(grep -c "${TINC_NETWORKNAME}" "${TINC_PATH}/nets.boot") -eq 0) ]]; then
    echo "${TINC_NETWORKNAME}" >> "${TINC_PATH}/nets.boot"
  fi
}

function disable_autostart(){
  if [[ $(grep -c "${TINC_NETWORKNAME}" "${TINC_PATH}/nets.boot") -gt 0 ]]; then
    sed -i -e "s/${TINC_NETWORKNAME}\n//g" "${TINC_PATH}/nets.boot"
  fi
}

function delete_config(){
  local response="$(curl --silent -H "Authorization: ${AUTH_TOKEN}" -X DELETE "${CONFIG_SERVER}/regService/config")"
  echo "${response}"
  if [[ "${response}" == "DELETED"* ]]; then
    echo "${response}"
  else
    echo "Something went wrong"
  fi
}

function post_config(){
  #send own config
  temp=$(curl --silent -H "Authorization: ${AUTH_TOKEN}" -X POST -T "${NODE_HOST_FILES}/${HOSTNAME}" "${CONFIG_SERVER}/regService/config")
  echo -e "$temp" > "${NODE_HOST_FILES}/${HOSTNAME}"
}

function get_configs(){

  local cmd="curl --silent -H \"Authorization: ${AUTH_TOKEN}\" -X GET \"${CONFIG_SERVER}/regService/config\""
  local ALL_CONFIGS="$(eval "${cmd}")"
  echo "${cmd}"

  sed -i -e '/ConnectTo.*/d' "${NODE_CONFIG_FILE}"
  rm -rf "${NODE_HOST_FILES}/*"

  local regex="#\sHostname\s*=\s*([A-Za-z0-9]*)"
  local OLD_IFS="$IFS"
  IFS="%"
  local CONFIG_ARRAY=( $ALL_CONFIGS )
  for ONE_CONFIG in "${CONFIG_ARRAY[@]}"
  do
    [[ "$ONE_CONFIG" =~ ${regex} ]]
    local NODE_NAME=${BASH_REMATCH[1]}

    echo $ONE_CONFIG > "${NODE_HOST_FILES}/${NODE_NAME}"

    if [[ "$HOSTNAME" != "$NODE_NAME" ]]; then
      if [[ ($(grep -c "ConnectTo = $NODE_NAME" "${NODE_CONFIG_FILE}") -eq 0) ]]; then
        echo "ConnectTo = $NODE_NAME" >> "${NODE_CONFIG_FILE}"
      fi
    fi
  done
  IFS="$OLD_IFS"
}

function poll_configs(){
  while true; do
    get_configs
    if [[ $(ls "${NODE_HOST_FILES}/" | wc -w) -gt ${EXPECTED_NODES} ]]; then
      return 0
    fi
    sleep 5
  done
}

function create_tinc_config(){
mkdir -p "${NODE_HOST_FILES}/"

cat << EOM > "${TINC_PATH}/${TINC_NETWORKNAME}/tinc-up"
#!/bin/sh

IP="\$(grep Subnet "/etc/tinc/\${NETNAME}/hosts/\${NAME}" |cut -d' ' -f3 | cut -d'/' -f1)"
ifconfig "\${INTERFACE}" "\${IP}" netmask 255.255.255.0
EOM
chmod a+x "${TINC_PATH}/${TINC_NETWORKNAME}/tinc-up"

cat << EOM > "${TINC_PATH}/${TINC_NETWORKNAME}/tinc-down"
#!/bin/sh
ifconfig "\${INTERFACE}" down
EOM
chmod a+x "${TINC_PATH}/${TINC_NETWORKNAME}/tinc-down"

cat << EOM > "${NODE_CONFIG_FILE}"
Name = ${HOSTNAME}
AddressFamily = ipv4
Interface = ${TINC_INTERFACE}
EOM

if [[ -n "${INTERFACE}" ]]; then
  IP="$(get_ip_of_interface ${INTERFACE})"
  echo -e "# Hostname = ${HOSTNAME}\n# NetworkName = ${TINC_NETWORKNAME}\nAddress = ${IP}" > "${NODE_HOST_FILES}/${HOSTNAME}"
else
  echo -e "# Hostname = ${HOSTNAME}\n# NetworkName = ${TINC_NETWORKNAME}" > "${NODE_HOST_FILES}/${HOSTNAME}"
fi
tincd -n ${TINC_NETWORKNAME} -K${TINC_KEYLENGTH}
}

function test(){
  for ONE_FILE in ${NODE_HOST_FILES}/* ; do
    local NODE_NAME="$(basename "${ONE_FILE}")"
    local NODE_IP="$(grep Subnet "${ONE_FILE}" |cut -d' ' -f3 | cut -d'/' -f1)"
    ping -W 1 -c 2 ${NODE_IP} > /dev/null 2>&1
    evaluate_result $? "  ${NODE_NAME} is pingable with IP ${NODE_IP}"
  done
}

function create(){
  echo "configure"
  create_tinc_config
  echo "post config to tincregistrar"
  post_config
  echo "get all configs"
#  timeout ${POLL_TIMEOUT} cat <( poll_configs )
}

function remove(){
  stop
  echo "delete config from tincregistrar"
  delete_config
  echo "remove network ${TINC_NETWORKNAME}"
  rm -rf "${TINC_PATH}/${TINC_NETWORKNAME}"
}

function start(){
  echo "enable"
  enable_autostart
  systemctl start tinc.service
}

function stop(){
  systemctl stop tinc.service
  echo "disable"
  disable_autostart
}

usage () {
cat << EOM
usage:

  tincsetup start           Start Tinc

  tincsetup stop            Stop Tinc.

  tincsetup create          Create new tinc configuration.

  tincsetup remove          Remove tinc configuration.

  tincsetup pullconfig      Get all configs from tincregistrar.

  tincsetup test            Ping all existing nodes.

EOM
}

if [[ $DEBUG == "true" ]]; then
  eval "$@"
elif [ $# -eq 1 ]; then
  case "$1" in
    "start" )
      start
      ;;
    "stop" )
      stop
      ;;
    "create" )
      create
      ;;
    "remove" )
      remove
      ;;
    "pullconfig" )
      get_configs
      ;;
    "test" )
      test
      ;;
    * )
      usage
      ;;
  esac
else
  usage
fi
