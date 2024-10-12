# Deep Learning DS - AWS Scheduler

The AWS Scheduler is intended to run training and evaluation jobs using AWS ECS containers and set the desired number
of instances of a configured autoscaling group.



## Create docker container
```
docker build -t dataspree/dlds-aws-scheduler .
docker run -d -v config_dir:/etc/dldsaws --name dlds-aws-scheduler dataspree/dlds-aws-scheduler
````
