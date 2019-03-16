#!/bin/bash

rm -f dummy.txt

for file in *.txt
do 
	mv "${file}" "${file//:}"
done
