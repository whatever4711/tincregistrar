#!/usr/bin/env bash

NETWORKNAME="demo"

#CONFIG_SERVER="192.168.200.49:8000"
CONFIG_SERVER="172.19.0.2:8000"



HOSTNAME=${HOSTNAME//[\-\_\.\s]/}
TINC_PATH="/etc/tinc"
NODE_HOST_FILE="${TINC_PATH}/${NETWORKNAME}/hosts/${HOSTNAME}"
NODE_CONFIG_FILE="${TINC_PATH}/${NETWORKNAME}/tinc.conf"

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

function enable_autostart(){
  if [[ ($(grep -c "${NETWORKNAME}" "${TINC_PATH}/nets.boot") -eq 0) ]]; then
    echo "${NETWORKNAME}" >> "${TINC_PATH}/nets.boot"
  fi
}

function disable_autostart(){
  if [[ $(grep -c "${NETWORKNAME}" "${TINC_PATH}/nets.boot") -gt 0 ]]; then
    sed -i '' "s/${NETWORKNAME}\n//g" > ${TINC_PATH}/nets.boot
  fi
}

function prepare_tinc_config(){
mkdir -p "${TINC_PATH}/${NETWORKNAME}/hosts/"

cat << EOM > "${TINC_PATH}/${NETWORKNAME}/tinc-up"
#!/bin/sh
IP="\$(grep Subnet "${NODE_HOST_FILE}" |cut -d' ' -f3 | cut -d'/' -f1)"
ifconfig "\${INTERFACE}" "\${IP}" netmask 255.255.255.0
EOM
chmod a+x "${TINC_PATH}/${NETWORKNAME}/tinc-up"

cat << EOM > "${TINC_PATH}/${NETWORKNAME}/tinc-down"
#!/bin/sh
ifconfig "\${INTERFACE}" down
EOM
chmod a+x "${TINC_PATH}/${NETWORKNAME}/tinc-down"
}

function create_tinc_config(){
cat << EOM > "${NODE_CONFIG_FILE}"
Name = ${HOSTNAME}
AddressFamily = ipv4
Interface = tun0
EOM

IP="$(get_ip_of_interface eth0)"
if [[ -z "${IP}" ]]; then
  IP="$(get_ip_of_interface wlan0)"
fi

echo -e "# Hostname = ${HOSTNAME}\nAddress = ${IP}" > "${NODE_HOST_FILE}"
tincd -n ${NETWORKNAME} -K1024
}

function publish_config(){
  #send own config
  temp=$(curl --silent -X POST -T "${NODE_HOST_FILE}" "${CONFIG_SERVER}/regService/config")
  echo -e "$temp" > "${NODE_HOST_FILE}"
}
function get_configs(){
  #receive all other configs
  others="$(curl --silent "${CONFIG_SERVER}/regService/config")"

#others=$(cat temp)
  echo "${others}"
  echo -e "${others}" > temp

  regex="#\sHostname\s=\s([A-Za-z0-9]*)"
  OLD_IFS="$IFS"
  IFS="%"
  STR_ARRAY=( $others )
  for x in "${STR_ARRAY[@]}"
  do
    [[ "$x" =~ ${regex} ]]
    local name=${BASH_REMATCH[1]}

    if [[ ! -f "${TINC_PATH}/${NETWORKNAME}/hosts/$name" ]]; then
      echo $x > "${TINC_PATH}/${NETWORKNAME}/hosts/$name"
    fi

    if [[ "$HOSTNAME" != "$name" ]]; then
      if [[ ($(grep -c "ConnectTo = $name" "${NODE_CONFIG_FILE}") -eq 0) ]]; then
        echo "ConnectTo = $name" >> "${NODE_CONFIG_FILE}"
      fi
    fi
  done
  IFS="$OLD_IFS"
}

function delete_config(){
  curl --silent -X DELETE -T "${NODE_HOST_FILE}" "${CONFIG_SERVER}/regService/config"
}

function start(){
  echo "prepare"
  prepare_tinc_config

  echo "configure"
  create_tinc_config

  publish_config

  get_configs

#  echo "enable"
#  enable_autostart
  #systemctl start tinc.service
}

function stop(){
  systemctl stop tinc.service
  echo "disable"
  disable_autostart

  echo "remove network ${NETWORKNAME}"
  rm -rf "${TINC_PATH}/${NETWORKNAME}"

  delete_config
}


#start
#stop
