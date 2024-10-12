#  Copyright 2022 Data Spree GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import logging
from typing import Optional

import click
from time import time
import cv2

import numpy as np


class DifferenceTrigger:
    def __init__(self, threshold=10) -> None:
        super().__init__()
        self.threshold: int = threshold
        self.last_frame: Optional[np.ndarray] = None

    def __call__(self, current_frame):
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_RGB2GRAY)

        trigger = True
        if self.last_frame is not None:
            diff = cv2.absdiff(self.last_frame, current_frame)
            _, diff = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)
            diff = cv2.erode(diff, np.ones((3, 3), np.uint8), iterations=2)

            trigger = diff.any()

        self.last_frame = current_frame

        return trigger


@click.command(name='upload_video')
@click.option('--dataset_id', type=int, required=True, help='ID of the dataset to which new items should be uploaded')
@click.option('--video', 'video', required=True, type=click.Path(exists=True, file_okay=True, dir_okay=True),
              help='Video file')
@click.option('--skip_frames', type=int, default=0, help='Number of frames to skip.')
@click.option('--skip_offset', type=int, default=0, help='Number of frames to skip at the beginning of each video.')
@click.option('--class_id', 'class_ids', type=int, default=None, multiple=True,
              help='Class ID that will be assigned for the images as classification annotation.')
@click.option('--http_retries', required=False, default=10, help='Number of HTTP retries.', show_default=True, type=int)
@click.option('--parallel_requests', required=False, default=16, help='Number of parallel requests.', show_default=True,
              type=int)
@click.option('--username', prompt='Username', help='Username for data spree vision platform.')
@click.option('--password', prompt='Password', hide_input=True, help='Password for data spree vision platform.')
@click.option('--url', 'api_url', default='https://api.vision.data-spree.com/api',
              help='URL to the API of the platform.')
def upload_video_command(dataset_id, video, skip_frames, skip_offset, class_ids, http_retries, parallel_requests,
                         username, password,
                         api_url):
    client = dataspree.platform_sdk.client.Client(username, password, None, http_retries, parallel_requests, api_url)
    logging.info('Upload video {}'.format(video))

    videos = []
    if os.path.isdir(video):
        for f in os.listdir(video):
            videos.append(os.path.join(video, f))
    else:
        videos = [video]

    if len(videos) == 0:
        return

    trigger = DifferenceTrigger(threshold=30)

    output_dir = 'frames'
    os.makedirs(output_dir, exist_ok=True)

    for v in videos:
        cap = cv2.VideoCapture(v)

        running = True

        for _ in range(skip_offset):
            success, frame = cap.read()
            if not success:
                running = False
                break

        frame_i = 0
        while running:
            success, frame = cap.read()

            if success and trigger(frame):

                frame = frame[::2, :, :]
                frame = cv2.resize(frame, (frame.shape[1], frame.shape[0] * 2))

                cv2.imshow('frame', frame)
                key = cv2.waitKey(0)
                if key & 0xFF == ord('q'):
                    break

                frame_i += 1
                frame_file_name = os.path.join(output_dir, 'frame_{}.png'.format(int(time() * 1000)))

                print(v, frame_i)
                cv2.imwrite(frame_file_name, frame)

                annotations = {}
                status = 'uploaded'
                # if class_ids is not None and len(class_ids) > 0:
                #     status = 'reviewed'
                #     annotations = {
                #         'classes': class_ids
                #     }

                # client.create_dataset_item(frame_file_name, dataset_id, annotations=annotations, status=status)

                for _ in range(skip_frames):
                    success, frame = cap.read()
                    if not success:
                        running = False
                        break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)-6s %(message)s')
    upload_video_command()
