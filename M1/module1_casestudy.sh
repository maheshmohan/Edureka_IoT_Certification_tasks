#!/bin/bash

echo "Module1 case study"

while getopts ":v:i:t:" opt;
do
 case $opt in 
 t)
   time=$OPTARG
   ;;
 v)
   omxplayer $OPTARG | at now + $time minutes
   ;;
 i)
   fbi $OPTARG | at now + $time minutes
   ;;
 *)
   echo "usage ./module1_casestudy.sh -t 10 [-v] [-i]"
   echo "options:"
   echo " -t     scheduled start time from now in minutes"
   echo " -v     path to video file"
   echo " -i     path to image file"
   ;;
 esac
done

