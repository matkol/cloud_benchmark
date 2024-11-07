#!/bin/bash

# create bucket
gcloud storage buckets create gs://download-test-data  --location=EUROPE-WEST10


create() {
    echo "creating $1" ;  dd if=/dev/zero  bs=1024 count=$2  | gcloud storage cp --gzip-in-flight-all - gs://download-test-data/$1
}

# create 1 x 100Mb file
fil=100mb; create $fil 102400

# create 10 x 10Mb files
for (( i=0 ; i<10; i++ )) ;  do fil=10mb-`printf "%03d" $i`;  create $fil 10240 ; done

# create 100 x 1Mb files
cd /tmp
mkdir upload
for (( i=0 ; i<100; i++ )) ; do fil=upload/1mb-`printf "%03d" $i` ; dd if=/dev/zero  bs=1024 count=1024 of=$fil; done

# create 1000 x 0.1Mb files
for (( i=0 ; i<1000; i++ )) ; do fil=upload/100kb-`printf "%03d" $i` ; dd if=/dev/zero  bs=1024 count=100 of=$fil; done

gcloud storage cp --gzip-in-flight-all upload/* gs://download-test-data/
rm -r upload

