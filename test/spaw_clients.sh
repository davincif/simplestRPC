COUNTER=0

while [ $COUNTER -lt 1000 ]; do
	python client.py
	let COUNTER=COUNTER+1
done
