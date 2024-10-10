# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Manifest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'folder': 'str',
        'file_name': 'str',
        'manifest_source': 'str'
    }

    attribute_map = {
        'folder': 'folder',
        'file_name': 'file_name',
        'manifest_source': 'manifest_source'
    }

    def __init__(self, folder=None, file_name=None, manifest_source=None):  # noqa: E501
        """Manifest - a model defined in Swagger"""  # noqa: E501

        self._folder = None
        self._file_name = None
        self._manifest_source = None
        self.discriminator = None

        if folder is not None:
            self.folder = folder
        if file_name is not None:
            self.file_name = file_name
        if manifest_source is not None:
            self.manifest_source = manifest_source

    @property
    def folder(self):
        """Gets the folder of this Manifest.  # noqa: E501

        The folder that contains the files. Manifests can be placed in 'manifests' or 'openshift' directories.  # noqa: E501

        :return: The folder of this Manifest.  # noqa: E501
        :rtype: str
        """
        return self._folder

    @folder.setter
    def folder(self, folder):
        """Sets the folder of this Manifest.

        The folder that contains the files. Manifests can be placed in 'manifests' or 'openshift' directories.  # noqa: E501

        :param folder: The folder of this Manifest.  # noqa: E501
        :type: str
        """
        allowed_values = ["manifests", "openshift"]  # noqa: E501
        if folder not in allowed_values:
            raise ValueError(
                "Invalid value for `folder` ({0}), must be one of {1}"  # noqa: E501
                .format(folder, allowed_values)
            )

        self._folder = folder

    @property
    def file_name(self):
        """Gets the file_name of this Manifest.  # noqa: E501

        The file name prefaced by the folder that contains it.  # noqa: E501

        :return: The file_name of this Manifest.  # noqa: E501
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """Sets the file_name of this Manifest.

        The file name prefaced by the folder that contains it.  # noqa: E501

        :param file_name: The file_name of this Manifest.  # noqa: E501
        :type: str
        """

        self._file_name = file_name

    @property
    def manifest_source(self):
        """Gets the manifest_source of this Manifest.  # noqa: E501

        Describes whether manifest is sourced from a user or created by the system.  # noqa: E501

        :return: The manifest_source of this Manifest.  # noqa: E501
        :rtype: str
        """
        return self._manifest_source

    @manifest_source.setter
    def manifest_source(self, manifest_source):
        """Sets the manifest_source of this Manifest.

        Describes whether manifest is sourced from a user or created by the system.  # noqa: E501

        :param manifest_source: The manifest_source of this Manifest.  # noqa: E501
        :type: str
        """
        allowed_values = ["user", "system"]  # noqa: E501
        if manifest_source not in allowed_values:
            raise ValueError(
                "Invalid value for `manifest_source` ({0}), must be one of {1}"  # noqa: E501
                .format(manifest_source, allowed_values)
            )

        self._manifest_source = manifest_source

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Manifest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Manifest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
