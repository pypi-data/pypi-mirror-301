# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from assisted_service_client.api_client import ApiClient


class ManifestsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def v2_create_cluster_manifest(self, cluster_id, create_manifest_params, **kwargs):  # noqa: E501
        """v2_create_cluster_manifest  # noqa: E501

        Creates a manifest for customizing cluster installation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_create_cluster_manifest(cluster_id, create_manifest_params, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster for which a new manifest should be created. (required)
        :param CreateManifestParams create_manifest_params: The new manifest to create. (required)
        :return: Manifest
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.v2_create_cluster_manifest_with_http_info(cluster_id, create_manifest_params, **kwargs)  # noqa: E501
        else:
            (data) = self.v2_create_cluster_manifest_with_http_info(cluster_id, create_manifest_params, **kwargs)  # noqa: E501
            return data

    def v2_create_cluster_manifest_with_http_info(self, cluster_id, create_manifest_params, **kwargs):  # noqa: E501
        """v2_create_cluster_manifest  # noqa: E501

        Creates a manifest for customizing cluster installation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_create_cluster_manifest_with_http_info(cluster_id, create_manifest_params, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster for which a new manifest should be created. (required)
        :param CreateManifestParams create_manifest_params: The new manifest to create. (required)
        :return: Manifest
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cluster_id', 'create_manifest_params']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v2_create_cluster_manifest" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if ('cluster_id' not in params or
                params['cluster_id'] is None):
            raise ValueError("Missing the required parameter `cluster_id` when calling `v2_create_cluster_manifest`")  # noqa: E501
        # verify the required parameter 'create_manifest_params' is set
        if ('create_manifest_params' not in params or
                params['create_manifest_params'] is None):
            raise ValueError("Missing the required parameter `create_manifest_params` when calling `v2_create_cluster_manifest`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cluster_id' in params:
            path_params['cluster_id'] = params['cluster_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'create_manifest_params' in params:
            body_params = params['create_manifest_params']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['userAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v2/clusters/{cluster_id}/manifests', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Manifest',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def v2_delete_cluster_manifest(self, cluster_id, file_name, **kwargs):  # noqa: E501
        """v2_delete_cluster_manifest  # noqa: E501

        Deletes a manifest from the cluster.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_delete_cluster_manifest(cluster_id, file_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster whose manifest should be deleted. (required)
        :param str file_name: The manifest file name to delete from the cluster. (required)
        :param str folder: The folder that contains the files. Manifests can be placed in 'manifests' or 'openshift' directories.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.v2_delete_cluster_manifest_with_http_info(cluster_id, file_name, **kwargs)  # noqa: E501
        else:
            (data) = self.v2_delete_cluster_manifest_with_http_info(cluster_id, file_name, **kwargs)  # noqa: E501
            return data

    def v2_delete_cluster_manifest_with_http_info(self, cluster_id, file_name, **kwargs):  # noqa: E501
        """v2_delete_cluster_manifest  # noqa: E501

        Deletes a manifest from the cluster.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_delete_cluster_manifest_with_http_info(cluster_id, file_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster whose manifest should be deleted. (required)
        :param str file_name: The manifest file name to delete from the cluster. (required)
        :param str folder: The folder that contains the files. Manifests can be placed in 'manifests' or 'openshift' directories.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cluster_id', 'file_name', 'folder']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v2_delete_cluster_manifest" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if ('cluster_id' not in params or
                params['cluster_id'] is None):
            raise ValueError("Missing the required parameter `cluster_id` when calling `v2_delete_cluster_manifest`")  # noqa: E501
        # verify the required parameter 'file_name' is set
        if ('file_name' not in params or
                params['file_name'] is None):
            raise ValueError("Missing the required parameter `file_name` when calling `v2_delete_cluster_manifest`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cluster_id' in params:
            path_params['cluster_id'] = params['cluster_id']  # noqa: E501

        query_params = []
        if 'folder' in params:
            query_params.append(('folder', params['folder']))  # noqa: E501
        if 'file_name' in params:
            query_params.append(('file_name', params['file_name']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['userAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v2/clusters/{cluster_id}/manifests', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def v2_download_cluster_manifest(self, cluster_id, file_name, **kwargs):  # noqa: E501
        """v2_download_cluster_manifest  # noqa: E501

        Downloads cluster manifest.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_download_cluster_manifest(cluster_id, file_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster whose manifest should be downloaded. (required)
        :param str file_name: The manifest file name to download. (required)
        :param str folder: The folder that contains the files. Manifests can be placed in 'manifests' or 'openshift' directories.
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.v2_download_cluster_manifest_with_http_info(cluster_id, file_name, **kwargs)  # noqa: E501
        else:
            (data) = self.v2_download_cluster_manifest_with_http_info(cluster_id, file_name, **kwargs)  # noqa: E501
            return data

    def v2_download_cluster_manifest_with_http_info(self, cluster_id, file_name, **kwargs):  # noqa: E501
        """v2_download_cluster_manifest  # noqa: E501

        Downloads cluster manifest.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_download_cluster_manifest_with_http_info(cluster_id, file_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster whose manifest should be downloaded. (required)
        :param str file_name: The manifest file name to download. (required)
        :param str folder: The folder that contains the files. Manifests can be placed in 'manifests' or 'openshift' directories.
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cluster_id', 'file_name', 'folder']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v2_download_cluster_manifest" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if ('cluster_id' not in params or
                params['cluster_id'] is None):
            raise ValueError("Missing the required parameter `cluster_id` when calling `v2_download_cluster_manifest`")  # noqa: E501
        # verify the required parameter 'file_name' is set
        if ('file_name' not in params or
                params['file_name'] is None):
            raise ValueError("Missing the required parameter `file_name` when calling `v2_download_cluster_manifest`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cluster_id' in params:
            path_params['cluster_id'] = params['cluster_id']  # noqa: E501

        query_params = []
        if 'folder' in params:
            query_params.append(('folder', params['folder']))  # noqa: E501
        if 'file_name' in params:
            query_params.append(('file_name', params['file_name']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['userAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v2/clusters/{cluster_id}/manifests/files', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def v2_list_cluster_manifests(self, cluster_id, **kwargs):  # noqa: E501
        """v2_list_cluster_manifests  # noqa: E501

        Lists manifests for customizing cluster installation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_list_cluster_manifests(cluster_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster for which the manifests should be listed. (required)
        :param bool include_system_generated: Include system generated manifests in results? Default is false.
        :return: ListManifests
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.v2_list_cluster_manifests_with_http_info(cluster_id, **kwargs)  # noqa: E501
        else:
            (data) = self.v2_list_cluster_manifests_with_http_info(cluster_id, **kwargs)  # noqa: E501
            return data

    def v2_list_cluster_manifests_with_http_info(self, cluster_id, **kwargs):  # noqa: E501
        """v2_list_cluster_manifests  # noqa: E501

        Lists manifests for customizing cluster installation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_list_cluster_manifests_with_http_info(cluster_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster for which the manifests should be listed. (required)
        :param bool include_system_generated: Include system generated manifests in results? Default is false.
        :return: ListManifests
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cluster_id', 'include_system_generated']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v2_list_cluster_manifests" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if ('cluster_id' not in params or
                params['cluster_id'] is None):
            raise ValueError("Missing the required parameter `cluster_id` when calling `v2_list_cluster_manifests`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cluster_id' in params:
            path_params['cluster_id'] = params['cluster_id']  # noqa: E501

        query_params = []
        if 'include_system_generated' in params:
            query_params.append(('include_system_generated', params['include_system_generated']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['userAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v2/clusters/{cluster_id}/manifests', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ListManifests',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def v2_update_cluster_manifest(self, cluster_id, update_manifest_params, **kwargs):  # noqa: E501
        """v2_update_cluster_manifest  # noqa: E501

        Updates a manifest for customizing cluster installation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_update_cluster_manifest(cluster_id, update_manifest_params, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster for which a new manifest should be updated. (required)
        :param UpdateManifestParams update_manifest_params: The manifest to be updated. (required)
        :return: Manifest
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.v2_update_cluster_manifest_with_http_info(cluster_id, update_manifest_params, **kwargs)  # noqa: E501
        else:
            (data) = self.v2_update_cluster_manifest_with_http_info(cluster_id, update_manifest_params, **kwargs)  # noqa: E501
            return data

    def v2_update_cluster_manifest_with_http_info(self, cluster_id, update_manifest_params, **kwargs):  # noqa: E501
        """v2_update_cluster_manifest  # noqa: E501

        Updates a manifest for customizing cluster installation.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.v2_update_cluster_manifest_with_http_info(cluster_id, update_manifest_params, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cluster_id: The cluster for which a new manifest should be updated. (required)
        :param UpdateManifestParams update_manifest_params: The manifest to be updated. (required)
        :return: Manifest
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cluster_id', 'update_manifest_params']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method v2_update_cluster_manifest" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if ('cluster_id' not in params or
                params['cluster_id'] is None):
            raise ValueError("Missing the required parameter `cluster_id` when calling `v2_update_cluster_manifest`")  # noqa: E501
        # verify the required parameter 'update_manifest_params' is set
        if ('update_manifest_params' not in params or
                params['update_manifest_params'] is None):
            raise ValueError("Missing the required parameter `update_manifest_params` when calling `v2_update_cluster_manifest`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cluster_id' in params:
            path_params['cluster_id'] = params['cluster_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'update_manifest_params' in params:
            body_params = params['update_manifest_params']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['userAuth']  # noqa: E501

        return self.api_client.call_api(
            '/v2/clusters/{cluster_id}/manifests', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Manifest',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
