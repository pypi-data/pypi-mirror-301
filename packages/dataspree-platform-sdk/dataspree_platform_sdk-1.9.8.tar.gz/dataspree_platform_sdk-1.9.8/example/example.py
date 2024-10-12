#  Copyright (c) 2020 Data Spree UG (haftungsbeschraenkt) - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited.
#  Proprietary and confidential.

import logging
import time
from typing import Dict

import click
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from dlds import DLDSModel, DLDSClient, DLDSWorker

logger = logging.getLogger(__name__)

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)
sentry_sdk.init("https://4954c11570d8489bbf776fa3697d8efe@sentry.io/1895117", integrations=[sentry_logging])


class ExampleModel(DLDSModel):

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.running = True
        self.start_iteration = 0
        self.current_iteration = 0

    def run(self) -> Dict:
        logger.info(f'Run example model. Going to train {self.iterations} iterations.')

        # simulate a trainings loop
        for i in range(self.iterations):
            self.current_iteration = i
            if not self.running:
                break

            # simulate some work
            time.sleep(0.1)

            logger.info(f'Iteration {i} for model {self.platform_model.get("id")}')

            # The iteration callback should be called after each iteration. In case of a high volume of iterations per
            # second, you can call the the iteration callback every N iterations to improve performance.
            if i % 10 == 0:
                self.iteration_callback(i)

        logger.info('Example model finished.')
        return {
            'start_iteration': self.start_iteration,
            'last_iteration': self.current_iteration
        }

    def stop(self) -> None:
        logger.info('Stopping the model...')
        self.running = False


@click.command()
@click.option('--dlds_token', required=True, help='Token for authenticating at Deep Learning DS.')
@click.option('--worker_id', required=True, help='ID of this worker.')
@click.option('--model_id', type=int, default=None, help='ID of this worker.')
def main(dlds_token, worker_id, model_id) -> None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)-6s %(message)s')

    try:
        dlds_client = DLDSClient(auth_token=dlds_token)
        dlds_worker = DLDSWorker(dlds_client, worker_id, model_id)
        dlds_worker.register_model([4, 5, 6], ExampleModel)
        dlds_worker.run()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
