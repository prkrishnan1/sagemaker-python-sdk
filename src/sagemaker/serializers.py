# Copyright 2017-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Implements methods for serializing data for an inference endpoint."""
from __future__ import absolute_import

import abc
import json

import numpy as np


class BaseSerializer(abc.ABC):
    """Abstract base class for creation of new serializers.

    Provides a skeleton for customization requiring the overriding of the method
    serialize and the class attribute CONTENT_TYPE.
    """

    @abc.abstractmethod
    def serialize(self, data):
        """Serialize data into the media type specified by CONTENT_TYPE.

        Args:
            data (object): Data to be serialized.

        Returns:
            object: Serialized data used for a request.
        """

    @property
    @abc.abstractmethod
    def CONTENT_TYPE(self):
        """The MIME type of the data sent to the inference endpoint."""


class JSONSerializer(BaseSerializer):
    """Serialize data to a JSON formatted string."""

    CONTENT_TYPE = "application/json"

    def serialize(self, data):
        """Serialize data of various formats to a JSON formatted string.

        Args:
            data (object): Data to be serialized.

        Returns:
            str: The data serialized as a JSON string.
        """
        if isinstance(data, dict):
            return json.dumps(
                {
                    key: value.tolist() if isinstance(value, np.ndarray) else value
                    for key, value in data.items()
                }
            )

        if hasattr(data, "read"):
            return data.read()

        if isinstance(data, np.ndarray):
            return json.dumps(data.tolist())

        return json.dumps(data)
