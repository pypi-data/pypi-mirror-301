#  Copyright (c) 2020 Data Spree UG (haftungsbeschraenkt) - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

import boto3

aws_access_key_id = None
aws_secret_access_key = None
region_name = None

execution_role_arn = "arn:aws:iam::785405927117:role/ecsTaskExecutionRole"
docker_image = "785405927117.dkr.ecr.eu-central-1.amazonaws.com/dataspree/dlds-training"
task_role_arn = "arn:aws:iam::785405927117:role/ecsTaskExecutionRole"

task_defintion = {
    # "ipcMode": None,
    "executionRoleArn": execution_role_arn,
    "containerDefinitions": [
        {
            # "dnsSearchDomains": None,
            # "logConfiguration": None,
            # "entryPoint": None,
            # "portMappings": [],
            "command": [],
            "linuxParameters": {
                "sharedMemorySize": 16384
            },
            "cpu": 0,
            "environment": [],
            "resourceRequirements": [
                {
                    "type": "GPU",
                    "value": "1"
                }
            ],
            # "ulimits": None,
            # "dnsServers": None,
            "mountPoints": [
                {
                    "containerPath": "/data",
                    "sourceVolume": "data"
                }
            ],
            # "workingDirectory": None,
            # "secrets": None,
            # "dockerSecurityOptions": None,
            "memory": 16384,
            # "memoryReservation": None,
            # "volumesFrom": [],
            # "stopTimeout": None,
            "image": docker_image,
            # "startTimeout": None,
            # "firelensConfiguration": None,
            # "dependsOn": None,
            # "disableNetworking": None,
            # "interactive": None,
            # "healthCheck": None,
            "essential": True,
            # "links": None,
            # "hostname": None,
            # "extraHosts": None,
            # "pseudoTerminal": None,
            # "user": None,
            # "readonlyRootFilesystem": None,
            # "dockerLabels": None,
            # "systemControls": None,
            # "privileged": None,
            "name": "dlds-training"
        }
    ],
    # "placementConstraints": [],
    # "memory": None,
    "taskRoleArn": task_role_arn,
    # "compatibilities": [
    #     "EC2"
    # ],
    # "taskDefinitionArn": "arn:aws:ecs:eu-central-1:785405927117:task-definition/dlds-training:1",
    "family": "dlds-training",
    # "requiresAttributes": [
    #     {
    #         "targetId": None,
    #         "targetType": None,
    #         "value": None,
    #         "name": "com.amazonaws.ecs.capability.ecr-auth"
    #     },
    #     {
    #         "targetId": None,
    #         "targetType": None,
    #         "value": None,
    #         "name": "com.amazonaws.ecs.capability.task-iam-role"
    #     },
    #     {
    #         "targetId": None,
    #         "targetType": None,
    #         "value": None,
    #         "name": "ecs.capability.execution-role-ecr-pull"
    #     }
    # ],
    # "pidMode": None,
    "requiresCompatibilities": [
        "EC2"
    ],
    # "networkMode": None,
    # "cpu": None,
    # "revision": 1,
    # "status": "ACTIVE",
    # "inferenceAccelerators": None,
    # "proxyConfiguration": None,
    "volumes": [
        {
            "name": "data",
            "host": {
                "sourcePath": "/data"
            },
        }
    ]
}

# initialize boto3 client (aws api)
boto_session = boto3.session.Session(aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     region_name=region_name)

ecs = boto_session.client('ecs')
ecs.register_task_definition(**task_defintion)
