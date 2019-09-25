.PHONY: build-detector build-producer run-mysql

build-detector:
	cd detector && docker build -t coopernurse/object-detector .

build-detector-darknet:
	cd detector-darknet && docker build -t coopernurse/object-detector-darknet .

build-producer:
	cd producer && docker build -t coopernurse/object-producer .

run-mysql:
	docker run -d --name mysql-detector -p 3306:3306 -e MYSQL_ROOT_PASSWORD=test mysql:5.7.24

create-cfn:
	aws cloudformation create-stack --stack-name object-detector --capabilities CAPABILITY_NAMED_IAM --template-body file://create-cluster-cfn.yml --parameters file://params.json

update-cfn:
	aws cloudformation update-stack --stack-name object-detector --capabilities CAPABILITY_NAMED_IAM --template-body file://create-cluster-cfn.yml --parameters file://params.json
