# Copyright © 2024-2025 Pavel Rabaev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
logger = logging.getLogger(__name__)

from petaly.utils.file_handler import FileHandler
from petaly.core.f_loader import FLoader
from petaly.connectors.aws.s3.s3_connector import S3Connector


class S3Loader(FLoader):
    def __init__(self, pipeline):
        self.s3_connector = S3Connector(pipeline.target_attr, aws_session=None)
        self.f_handler = FileHandler()

        super().__init__(pipeline)
        self.cloud_bucket_name = self.pipeline.target_attr.get('aws_bucket_name')
        self.cloud_bucket_path = self.s3_connector.bucket_prefix + self.cloud_bucket_name + '/'

    def load_data(self):
        super().load_data(file_to_gzip=True)

    def load_from(self, loader_obj_conf):
        """ Load files to bucket
        """
        self.s3_connector.delete_object_in_bucket(self.cloud_bucket_name, loader_obj_conf.get('blob_prefix'))
        self.s3_connector.upload_files_to_bucket(self.cloud_bucket_name, loader_obj_conf.get('blob_prefix'), loader_obj_conf.get('file_list'))
