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

import json
import logging
import os

import numpy as np
from copy import copy, deepcopy
from enum import Enum
from time import sleep
from typing import Optional, Dict, List, Tuple

from tqdm import tqdm

from dataspree.platform_sdk.client import Client
from dataspree.platform_sdk.decoder.base_decoder import BaseDecoder
from dataspree.platform_sdk.decoder.pcd_decoder import PcdDecoder
from dataspree.platform_sdk.decoder.opencv_decoder import OpencvDecoder

logger = logging.getLogger(__name__)


class LoadMode(Enum):
    PRELOAD = 0
    ADHOC = 1
    ADHOC_CACHED = 2
    ADHOC_CACHED_BINARY = 3


class DataLoader:
    """Data loader for data from the Data Spree AI Platform"""

    def __init__(self, client: Client, network_model: Dict, dataset_directory: str,
                 mode: LoadMode = LoadMode.ADHOC_CACHED_BINARY,
                 allowed_status=('annotated', 'reviewed'), decoders: Optional[List[BaseDecoder]] = None,
                 distinct_items_per_category: bool = True):
        self._client = client
        self._network_model = network_model
        self._dataset_directory = dataset_directory
        self._mode = mode
        self._allowed_status = allowed_status
        self._decoders = []
        self._distinct_items_per_category = distinct_items_per_category
        self._max_retries = 10

        if self._dataset_directory == '':
            logger.info('Switching to adhoc mode because no dataset directory is provided.')
            self._mode = LoadMode.ADHOC

        if decoders is None:
            decoders = [PcdDecoder(), OpencvDecoder()]
            # decoders=[PcdDecoder(), OpencvDecoder(), PlyDecoder()] # TODO: Test Me

        for decoder in decoders:
            self.add_decoder(decoder)

        self._items = {}
        self._decoded_items = {}

        # load class label ids and names that are used within this model
        self._model_class_labels: List[Dict] = client.get_model_class_labels(network_model['id'])
        self._mapped_class_labels: Dict[int, List[int]] = dict()
        self._target_class_labels: List[Dict] = []
        target_class_label_ids = []
        for c in self._model_class_labels:
            target_class_label = c['target_class_label']
            if target_class_label is None:
                # old class labels have no target (they are the target/there is no remapping)
                target_class_label = c['class_label']
            if target_class_label['id'] not in target_class_label_ids:
                target_class_label_ids.append(target_class_label['id'])
                self._target_class_labels.append(target_class_label)
            class_label = c['class_label']
            mapped_labels = self._mapped_class_labels.setdefault(class_label['id'], [])
            if target_class_label['id'] not in mapped_labels:
                mapped_labels.append(target_class_label['id'])

        # get all categories and aggregate the respective subset IDs
        self._subsets_ids_by_category = {}
        for entry in network_model['data_subsets']:
            if entry['category'] not in self._subsets_ids_by_category.keys():
                self._subsets_ids_by_category[entry['category']] = []
            if entry['data_subset']['id'] not in self._subsets_ids_by_category[entry['category']]:
                self._subsets_ids_by_category[entry['category']].append(entry['data_subset']['id'])

        # get all subset IDs
        subset_ids = []
        condensed_subset_ids = [self._subsets_ids_by_category[cat] for cat in self._subsets_ids_by_category.keys()]
        for subset_id in [item for sublist in condensed_subset_ids for item in sublist]:
            subset_ids.append(subset_id)

        # get all item IDs
        self._item_ids = set()
        self._item_ids_by_subset = {}
        for subset_id in subset_ids:
            if subset_id not in self._item_ids_by_subset:
                self._item_ids_by_subset[subset_id] = []

            ## FIXME: only get items that have the reqested class IDs.
            # TODO: figure out the most efficient way to get those items.
            # SUGGESTIONS A: client.get_dataset_items with specified class_id for all IDs. Probably slow when a lot of labels are required
            # SUGGESTIONS B: client.get_dataset_items with specified class_id in filter query (?, this is also limited in DLDS isn't it?)
            subset_item_details = self._client.get_dataset_items(subset_id=subset_id, status=self._allowed_status)
            for item in subset_item_details:
                # del item['name']
                # del item['updated_date']
                if item['status'] in self._allowed_status:
                    item['exists'] = False
                    self._items[item['id']] = item
                    self._item_ids_by_subset[subset_id].append(item['id'])
                    self._item_ids.add(item['id'])

        self._item_ids = list(self._item_ids)
        if not len(self._item_ids):
            raise ValueError('No items loaded for training. Exit. Maybe you did not update the item\'s status?')

        self._item_ids_by_category = {}
        for category in self._subsets_ids_by_category.keys():
            for subset_id in self._subsets_ids_by_category[category]:
                if category not in self._item_ids_by_category:
                    if distinct_items_per_category:
                        self._item_ids_by_category[category] = set()
                    else:
                        self._item_ids_by_category[category] = list()

                if distinct_items_per_category:
                    self._item_ids_by_category[category].update(self._item_ids_by_subset[subset_id])
                else:
                    self._item_ids_by_category[category].extend(self._item_ids_by_subset[subset_id])

            if distinct_items_per_category:
                self._item_ids_by_category[category] = list(self._item_ids_by_category[category])

        if self._mode == LoadMode.PRELOAD:
            for item_id in tqdm(self._item_ids):
                image_directory = os.path.join(self._dataset_directory, str(self._items[item_id]['dataset']), 'images')
                metainformation_directory = os.path.join(self._dataset_directory, str(self._items[item_id]['dataset']),
                                                         'metainformation')

                item = self._items[item_id]
                dataset_id = item['dataset']
                item_name = item['name'].split('/')[-1]
                image_file_name = f'{dataset_id}_{item_id}_{item_name}'
                metainformation_file_name = image_file_name.split('.')[0] + '.json'
                image_path = os.path.join(image_directory, image_file_name)
                metainformation_path = os.path.join(metainformation_directory, metainformation_file_name)
                if os.path.exists(image_path) and os.path.exists(metainformation_path):
                    item['exists'] = True
                else:
                    self._client.download_dataset_item(item_id, image_dir=image_directory,
                                                       metainformation_directory=metainformation_directory,
                                                       accepted_status=self._allowed_status,
                                                       return_item=False)

    def __reduce__(self):
        return (DataLoader, (self._client,
                             self._network_model,
                             self._dataset_directory,
                             self._mode,
                             self._allowed_status,
                             self._decoders,
                             self._distinct_items_per_category,))

    def add_decoder(self, decoder):
        self._decoders.append(decoder)

    def get_class_labels(self) -> List[Dict]:
        """Get the list of class labels that are selected for the loaded model.

        :return: List containing the class labels with ID and name.
        """
        return copy(self._target_class_labels)

    def get_categories(self) -> List[str]:
        """List containing the names of all categories.

        :return: List of category names.
        """
        return list(self._item_ids_by_category.keys())

    def get_subset_ids_by_category(self, category) -> List[str]:
        """List containing the ids of all subsets in that categories.

        :return: List of subset ids.
        """
        return self._subsets_ids_by_category.get(category, [])

    def get_subset_ids(self, category=None) -> List[int]:
        """List containing the IDs of the subsets of the specified category or all subsets.

        :param category: Category to filter the subset IDs.
        :return: List of subset IDs.
        """

        if category is None:
            return list(self._item_ids_by_subset.keys())
        else:
            return list(self._subsets_ids_by_category[category])

    def get_item_ids(self) -> List[int]:
        """List containing the IDs of all items.

        This list contains unique item IDs, e.g. an item that belongs to multiple subsets is only listed once.

        :return: List of item IDs.
        """
        return copy(list(set(self._item_ids)))

    def get_item_ids_by_category(self, category) -> List[int]:
        """Get the IDs of all items that belong to the specified category.

        :param category: Category to filter the item IDs.
        :return: List of item IDs.
        """
        return copy(self._item_ids_by_category.get(category, []))

    def apply_label_remapping(self, annotations):
        """Remap dataset labels to model target labels.

        :param annotations: Dataset item annotations.
        :return: Updated annotations.
        """
        mcl = self._mapped_class_labels

        # update all image class labels
        classes = annotations.get('classes')
        new_classes = []
        if classes is not None:
            for label in classes:
                new_labels = mcl.get(label, [label])
                new_classes.extend(new_labels)
            annotations['classes'] = new_classes

        # update all object class labels
        new_objects = []
        objects = annotations.get('objects')
        if objects is not None:
            for obj in objects:
                label = obj['label']
                new_labels = mcl.get(label, [label])
                # update the label of the existing object
                new_label = new_labels[0]
                obj['label'] = new_label

                # add new objects with mapped labels if needed
                for l in new_labels[1:]:
                    new_obj = copy(obj)
                    new_obj['label'] = l
                    new_objects.append(new_obj)
            objects.extend(new_objects)
        return annotations

    def get_item_ids_by_subset(self, subset_id):
        """Get the IDs of all items that belong to the specified subset.

        :param subset_id: ID of a subset.
        :return: List of item IDs.
        """
        return copy(self._item_ids_by_subset.get(subset_id, []))

    def get_item_adhoc(self, item_id: int) -> Optional[Dict]:
        item_serialized = self._client.download_dataset_item(item_id, image_dir=None, metainformation_directory=None,
                                                             accepted_status=self._allowed_status, return_item=True)
        if item_serialized is None:
            return None

        item_file_extension = os.path.splitext(item_serialized['name'])[1].lower().replace('.', '') or 'jpg'
        item_serialized['image'] = self.decode_image(item_serialized['image'], file_extension=item_file_extension)
        return item_serialized

    def get_item_cached(self, item_id: int, cache_binary: bool = False) -> Optional[Dict]:
        cached_item = self._items.get(item_id) or self._client.get_dataset_item(item_id)
        if cached_item is None:
            return None

        item_serialized: Dict = deepcopy(cached_item)
        dataset_id: int = item_serialized['dataset']
        item_name: str = item_serialized['name'].split('/')[-1]
        item_file_extension = os.path.splitext(item_serialized['name'])[1].lower().replace('.', '') or 'jpg'

        image_directory: str = os.path.join(self._dataset_directory, str(dataset_id), 'images')
        metainformation_directory: str = os.path.join(self._dataset_directory, str(dataset_id), 'metainformation')

        image_file_name: str = f'{dataset_id}_{item_id}_{item_name}'
        metainformation_file_name = os.path.splitext(image_file_name)[0] + '.json'

        image_path: str = os.path.join(image_directory, image_file_name)
        item_serialized['image_path'] = image_path

        decoded_image_path: Optional[str] = os.path.join(image_directory,
                                                         f'{image_file_name}.bin') if cache_binary else None
        item_serialized['decoded_image_path'] = decoded_image_path

        metainformation_path: str = os.path.join(metainformation_directory, metainformation_file_name)
        item_serialized['metainformation_path'] = metainformation_path

        # Check if metainformation is up-to-date
        requires_download = True
        if os.path.exists(metainformation_path):
            with open(metainformation_path, 'r') as f:
                try:
                    loaded = json.load(f)

                    str_changed_date_json: Optional[str] = loaded.get('updated_date')
                    str_changed_date_item: Optional[str] = item_serialized.get('updated_date')
                    changed_date_json = Client.parse_dataset_item_date(str_changed_date_json)
                    changed_date_item = Client.parse_dataset_item_date(str_changed_date_item)

                    if changed_date_json is None:
                        logger.warning(f'Could not extract modified date from cached item: '
                                       f'"{str_changed_date_json}" decodes to None.')

                    if changed_date_item is None:
                        logger.warning(f'Could not extract modified date from item: '
                                       f'"{str_changed_date_json}" decodes to None.')

                    if changed_date_json is not None and changed_date_item is not None \
                            and changed_date_json > changed_date_item:
                        logger.warning('The item\'s cached metainformation are newer than those from the '
                                       'platform. Removing cached item!')

                    requires_download = changed_date_item != changed_date_json or changed_date_item is None

                    if not requires_download:
                        item_serialized['annotations'] = loaded['annotations']
                    else:
                        logger.debug('Will download because metainformation changed')

                except json.JSONDecodeError as e:
                    logger.warning(f'Could not load metainformation for item {item_id}: {e}.')

                if requires_download:
                    os.remove(metainformation_path)
        else:
            logger.debug('Will download (metainformation do not exist yet).')

        # Use cached image
        decoded_image_loaded = False
        if not requires_download:
            try:
                if decoded_image_path is not None and os.path.exists(decoded_image_path):
                    with open(decoded_image_path, 'rb') as f:
                        item_serialized['image'] = np.load(f)
                    decoded_image_loaded = True
            except Exception as e:
                logger.warning(f'Could not decode image from {decoded_image_path}: {e}.')
                os.remove(decoded_image_path)

            try:
                if item_serialized.get('image') is None and os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        blob = f.read()
                    try:
                        item_serialized['image'] = self.decode_image(blob, file_extension=item_file_extension)
                    except Exception as e:
                        raise Exception(f'Could not decode image for item {item_id}: {type(e)}: {e}')

            except Exception as e:
                logger.warning(f'Could not read image from {image_path}: {e}.')
                os.remove(image_path)

            requires_download = item_serialized.get('image') is None
            if requires_download:
                logger.debug('Will download (image does not exist yet).')

        # Attempt to load metainformation (if image is not None, otherwise we don't have to bother).
        if requires_download:
            logger.debug('Downloading item from platform.')
            item_serialized = self._client.download_dataset_item(
                item_id, image_dir=image_directory, metainformation_directory=metainformation_directory,
                accepted_status=self._allowed_status, return_item=True)

            if item_serialized is not None:
                try:
                    item_serialized['image'] = self.decode_image(item_serialized['image'],
                                                                 file_extension=item_file_extension)
                except Exception as e:
                    logger.warning(f'Could not decode image for item {item_id}: {type(e)}: {e}')
                    return None

        if item_serialized is None or item_serialized.get('image') is None:
            return None

        if decoded_image_path is not None and not decoded_image_loaded:
            with open(decoded_image_path, 'wb') as f:
                np.save(f, item_serialized['image'])

        if not requires_download:
            logger.debug('Using cached item.')

        return item_serialized

    def decode_image(self, blob, file_extension) -> Optional[np.ndarray]:
        for decoder in self._decoders or []:
            if file_extension in decoder.get_file_extensions():
                return decoder(blob)[0]
        logger.error(f'No decoder found for file extension: {file_extension}')

    def get_item(self, item_id) -> Optional[Dict]:
        """Get dataset item given its ID.

        :param item_id: ID of the item.
        :return: Dictionary containing the image and meta data or None if the item does not exist.
        >>> {
        >>> 'id': int,
        >>> 'image': [],
        >>> 'annotations': Dict
        >>> }
        """
        logger.debug(f'get item {item_id}')
        try:
            for retry_count in range(self._max_retries):
                sleep(min(2.0, 1e-3 * 2 ** retry_count))
                if self._mode == LoadMode.ADHOC:
                    item_serialized = self.get_item_adhoc(item_id)
                else:
                    item_serialized = self.get_item_cached(item_id, cache_binary=True)

                if item_serialized is None:
                    continue

                image = item_serialized['image']
                annotations = item_serialized['annotations']
                # update annotations based on the label remapping
                annotations = self.apply_label_remapping(annotations)
                return {
                    'id': item_id,
                    'image': image,
                    'annotations': annotations
                }
        except Exception as e:
            logger.error(f'An unexpected error occurred while loading the item: {e}')

        return None
