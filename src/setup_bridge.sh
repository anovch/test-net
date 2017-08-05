#!/bin/bash

COUNTER=0
while [  $COUNTER -lt $1 ]; do
	command="ip link add br$COUNTER type bridge"
	$command
	command="ip link set br$COUNTER up"
	$command
	let COUNTER=COUNTER+1 
done
