#!/usr/bin/env bash

# dummy1
ip link add dev dummy1 type dummy
ip link set dummy1 up
ip addr add dev dummy1 2333::aa/128
