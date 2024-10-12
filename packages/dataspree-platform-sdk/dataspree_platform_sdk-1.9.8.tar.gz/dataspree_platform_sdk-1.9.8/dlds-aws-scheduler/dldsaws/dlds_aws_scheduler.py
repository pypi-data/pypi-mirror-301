#  Copyright (c) 2022 Data Spree GmbH - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

import copy
import sys
import logging
import time
from typing import Dict, List, Optional

from dldsaws.aws_task import AWSTask

import click
import boto3
import yaml

from dlds import DLDSClient

logger = logging.getLogger(__name__)


class DLDSAWSScheduler:

    def __init__(self, dlds_client: DLDSClient, config: Dict, update_interval: float = 60.0,
                 task_lifetime: float = 15 * 60.0) -> None:
        super().__init__()
        self.dlds_client = dlds_client
        self.dlds_config = config.get('dlds')
        self.worker_id = self.dlds_config.get('worker_id')
        self.update_interval = update_interval
        self.task_lifetime = task_lifetime

        self.aws_config = config.get('aws')

        logger.info(f'Found the following configuration: {config}')

        self.aws_task_definitions = {}
        self.default_aws_task_definition = None
        for task_definition_name, task_definition in self.aws_config.get('task_definitions').items():
            model_config_ids = task_definition.get('dlds_model_config_ids')
            if model_config_ids is None:
                if self.default_aws_task_definition is None:
                    logger.info(f'Taking "{task_definition_name}" as default AWS task definition.')
                    self.default_aws_task_definition = task_definition_name
                else:
                    logger.warning(f'Only one task definition can be the default. Please specify '
                                   f'"dlds_model_config_ids" for "{task_definition_name}".')
            else:
                for cfg_id in model_config_ids:
                    self.aws_task_definitions[cfg_id] = task_definition_name

        # model_id -> aws task
        self.aws_tasks: Dict[int, AWSTask] = {}

        # initialize boto3 client (aws api)
        self.boto_session = boto3.session.Session(aws_access_key_id=self.aws_config.get('access_key_id'),
                                                  aws_secret_access_key=self.aws_config.get('secret_access_key'),
                                                  region_name=self.aws_config.get('region_name'))

        self.ecs = self.boto_session.client('ecs')
        self.autoscaling = self.boto_session.client('autoscaling')

        self.last_desired_instances = -1
        self.last_desired_instances_change = 0

        # scale in/out intervals in seconds
        self.interval_between_scale_ins = 300
        self.interval_between_scale_outs = 600 if (getattr(sys, "gettrace", lambda: None)()) is not None else 60

        self.running = True

    def create_aws_task(self, model_id, task_definition, container_name, container_command, cpus=1, memory=8192,
                        gpus=1):

        cluster = self.aws_config.get('cluster')
        group_name = f'deep-learning-ds-training-{model_id}'
        started_by = f'deep-learning-ds-training-{self.worker_id}'

        container_override = {
            'name': container_name,
            'command': container_command,
            'cpu': cpus,
            'resourceRequirements': [],
            'memory': memory,
        }

        if gpus > 0:
            container_override['resourceRequirements'].append({
                'type': 'GPU',
                'value': str(gpus)
            })

        try:
            response = self.ecs.run_task(
                cluster=cluster,
                count=1,
                group=group_name,
                overrides={
                    'containerOverrides': [container_override],
                },
                taskDefinition=task_definition,
                startedBy=started_by,
                tags=[
                    {
                        'key': 'dlds_model_id',
                        'value': str(model_id)
                    },
                    {
                        'key': 'dlds_worker_id',
                        'value': str(self.worker_id)
                    }
                ]
            )

            tasks = response.get('tasks')

            if tasks is None or len(tasks) == 0:
                return None

            new_task = tasks[0]
            aws_task = AWSTask(new_task.get('taskArn'), new_task, self.task_lifetime)
            aws_task.update_time = time.time()
            return aws_task
        except Exception as e:
            logger.warning(e)
            return None

    def get_aws_tasks(self):
        cluster = self.aws_config.get('cluster')
        started_by = f'deep-learning-ds-training-{self.worker_id}'
        response = self.ecs.list_tasks(cluster=cluster, startedBy=started_by)
        return response.get('taskArns')

    def get_aws_task_details(self, task_arns: List[str]):
        response = self.ecs.describe_tasks(cluster=self.aws_config.get('cluster'),
                                           tasks=task_arns,
                                           include=['TAGS'])
        tasks = response.get('tasks')
        if len(tasks) > 0:
            return tasks

        return None

    def stop_aws_task(self, task_arn):
        cluster = self.aws_config.get('cluster')
        self.ecs.stop_task(cluster=cluster, task=task_arn)

    def add_aws_task(self, aws_task, task_model_id) -> AWSTask:
        t = AWSTask(aws_task.get('taskArn'), aws_task, self.task_lifetime)
        t.update_time = time.time()
        self.aws_tasks[task_model_id] = t
        return t

    def create_task(self, model_id, job) -> Optional[AWSTask]:
        model = self.dlds_client.get_model(model_id)
        if model is None:
            logger.error('Could not get model information.')
            return None

        model_config_id = model.get('network_config_option')

        task_definition = self.aws_task_definitions.get(model_config_id)
        if task_definition is None:
            task_definition = self.default_aws_task_definition

        new_aws_task = None
        if task_definition is None:
            # cannot start a task for this model
            logger.error('Cannot start a task for this model config type.')
        else:
            task_definition_details = copy.deepcopy(self.aws_config['task_definitions'].get(task_definition))
            container_name = task_definition_details.get('container_name')
            container_command = task_definition_details.get('container_command')

            for i in range(len(container_command)):
                cmd = container_command[i]
                if cmd == '%WORKER_ID%':
                    container_command[i] = str(self.worker_id)
                if cmd == '%MODEL_ID%':
                    container_command[i] = str(model_id)

            cpus = task_definition_details.get('cpus', 1)
            memory = task_definition_details.get('memory', 8192)
            gpus = task_definition_details.get('gpus', 1)

            new_aws_task = self.create_aws_task(model_id, task_definition, container_name, container_command, cpus,
                                                memory, gpus)
            if new_aws_task is not None:
                logger.info(f'New AWS task created for model {model_id}. AWS task ARN: {new_aws_task.arn}.')
                self.aws_tasks[model_id] = new_aws_task
            else:
                logger.error(
                    f'Could not create new task for model {model_id} using: '
                    f'task_definition: {task_definition} container_name: {container_name}')

        # if new_aws_task is None:
        #     self.dlds_client.update_job({'id': job['id'], 'status': 'exception'})

        return new_aws_task

    def set_desired_instances(self, desired_instances):
        auto_scaling_group_name = self.aws_config.get('auto_scaling_group_name')
        if auto_scaling_group_name is not None:
            scale_in = self.last_desired_instances - desired_instances > 0
            scale_out = self.last_desired_instances - desired_instances < 0
            no_scaling = self.last_desired_instances == desired_instances

            if no_scaling:
                return

            now = time.time()
            # skip setting the desired instances if the time between scale outs is not passed yet
            if scale_in and now - self.last_desired_instances_change < self.interval_between_scale_ins:
                return

            # skip setting the desired instances if the time between scale outs is not passed yet
            if scale_out and now - self.last_desired_instances_change < self.interval_between_scale_outs:
                return

            logger.info(f'Set number of instances to {desired_instances}')
            response = self.autoscaling.set_desired_capacity(AutoScalingGroupName=auto_scaling_group_name,
                                                             DesiredCapacity=desired_instances,
                                                             HonorCooldown=True)
            self.last_desired_instances = desired_instances
            self.last_desired_instances_change = time.time()

            return response
        else:
            return None

    def run(self) -> None:
        logger.info('AWS Scheduler started.')

        while self.running:
            jobs = self.dlds_client.get_jobs(self.worker_id)

            model_ids = set()
            if jobs is not None:
                for job in jobs:
                    if job['status'] not in ['stopped', 'exception']:
                        model_id = job.get('model')
                        model_ids.add(model_id)
            model_ids = list(model_ids)

            # check all aws tasks
            logger.info('Checking AWS tasks...')
            aws_task_arns = self.get_aws_tasks()
            if aws_task_arns is not None and len(aws_task_arns) > 0:

                aws_tasks = self.get_aws_task_details(aws_task_arns)

                if aws_tasks is not None:
                    logger.info(f'Got list containing {len(aws_tasks)} AWS tasks.')

                    for aws_task in aws_tasks:
                        task_arn = aws_task['taskArn']
                        logger.info(f'Checking AWS task with ARN {task_arn}.')

                        # check if a job exists for the aws task
                        task_model_id = None
                        task_worker_id = None
                        for tag in aws_task['tags']:
                            if tag['key'] == 'dlds_model_id':
                                task_model_id = int(tag['value'])
                            if tag['key'] == 'dlds_worker_id':
                                task_worker_id = int(tag['value'])

                        if self.worker_id == task_worker_id:
                            aws_task_state = aws_task['lastStatus']

                            logger.info(
                                f'AWS task with ARN {task_arn} belongs to this worker. Task state: {aws_task_state}')

                            task = self.aws_tasks.get(task_model_id)
                            if task is None:
                                if aws_task_state != 'STOPPED':
                                    logger.warning(f'Could not find task in scheduler (model_id: {task_model_id}). '
                                                   f'Adding it.')
                                    task = self.add_aws_task(aws_task, task_model_id)

                            if jobs is not None:
                                if task_model_id in model_ids:
                                    # reset remaining task lifetime
                                    task.update_time = time.time()
                                else:
                                    # reduce the remaining lifetime of the task
                                    if task.update_time + task.lifetime < time.time():
                                        logger.info(f'Task lifetime exceeded.')
                                        logger.info(f'Stopping task {task_arn}')
                                        self.stop_aws_task(task_arn)

                else:
                    logger.info(f'Empty AWS task list.')

            # check all jobs
            logger.info('Checking jobs...')
            if jobs is not None:

                # set the desired auto scaling group size
                desired_instances = min(len(model_ids), self.aws_config.get('max_instances', 10))

                try:
                    self.set_desired_instances(desired_instances)
                except Exception as e:
                    logger.warning(e)

                for job in jobs:
                    model_id = job.get('model')

                    if job['status'] == 'stopped':
                        logger.error(f'Job {job["id"]} is stopped but is not finished.')
                        continue

                    aws_task = self.aws_tasks.get(model_id)
                    if aws_task is None:
                        # there is no aws task running to process the job
                        if self.create_task(model_id, job) is None:
                            continue
                    else:
                        # there should be an aws task available for the job
                        logger.info(f'Checking job: {job}')

                        # check the state of the task
                        aws_task_details = self.get_aws_task_details([aws_task.arn])

                        create_new_task = False
                        if aws_task_details is not None:
                            aws_task_state = aws_task_details[0]['lastStatus']
                            logger.info(f'Found AWS task for job: {job}, ARN: {aws_task.arn}, state: {aws_task_state}')
                            aws_task.details = aws_task_details[0]

                            new_status = job['status']
                            if aws_task_state == 'PROVISIONING':
                                new_status = 'provisioning'
                            elif aws_task_state == 'PENDING':
                                new_status = 'pending'
                            elif aws_task_state == 'STOPPED':
                                new_status = 'stopped'

                            if new_status != job['status']:
                                self.dlds_client.update_job({'id': job['id'], 'status': new_status})

                            if aws_task_state == 'STOPPED':
                                create_new_task = True
                        else:
                            # the aws task doesn't exist
                            logger.info(f'Could not find AWS task for job: {job}, ARN: {aws_task.arn}.')
                            create_new_task = True

                        if create_new_task:
                            logger.info(f'Removing the AWS task and trying to create new one.')
                            # remove it from the task dict
                            self.aws_tasks.pop(model_id, None)

                            # try to create a new one
                            if self.create_task(model_id, job) is None:
                                continue
            else:
                logger.warning('Could not get job list.')

            if self.update_interval > 1:
                time.sleep(self.update_interval)
            else:
                sleep_seconds = int(self.update_interval)
                for _ in range(sleep_seconds):
                    if not self.running:
                        break
                    time.sleep(1)

        logger.info('AWS Scheduler stopped.')


@click.command()
@click.option('-c', '--config', 'config_file', default='config.yml', help='Configuration file.')
def main(config_file) -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)-6s %(message)s')
    logger.setLevel(logging.DEBUG)

    dlds_aws_scheduler = None
    try:
        config = None
        with open(config_file) as f:
            config = yaml.safe_load(f)

        if config is None:
            logger.error('Could not load configuration.')
            return

        sentry_dsn = config.get('sentry', dict()).get('dsn')
        if sentry_dsn is not None:
            try:
                import sentry_sdk
                from sentry_sdk.integrations.logging import LoggingIntegration
                sentry_logging = LoggingIntegration(
                    level=logging.INFO,
                    event_level=logging.ERROR
                )

                sentry_sdk.init(sentry_dsn, integrations=[sentry_logging])
            except ModuleNotFoundError:
                logger.error('Could not initialize sentry: sentry_sdk not found.')

        dlds_client = DLDSClient(auth_token=config.get('dlds').get('token'))
        dlds_aws_scheduler = DLDSAWSScheduler(dlds_client, config)
        dlds_aws_scheduler.run()
    except KeyboardInterrupt:
        if dlds_aws_scheduler is not None:
            dlds_aws_scheduler.running = False
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
