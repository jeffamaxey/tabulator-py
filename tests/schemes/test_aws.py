# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import six
import sys
import boto3
import pytest
import string
import random
import subprocess
from moto import mock_s3
from tabulator import Stream, exceptions

# Setup

S3_ENDPOINT_URL = os.environ['S3_ENDPOINT_URL'] = 'http://localhost:5000'


# Read

# https://github.com/frictionlessdata/tabulator-py/issues/271
@pytest.mark.skip
def test_stream_s3(s3_client, bucket):

    # Upload a file
    s3_client.put_object(
        ACL='private',
        Body=open('data/table.csv', 'rb'),
        Bucket=bucket,
        ContentType='text/csv',
        Key='table.csv')

    # Check the file
    with Stream(f's3://{bucket}/table.csv') as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# https://github.com/frictionlessdata/tabulator-py/issues/271
@pytest.mark.skip
def test_stream_s3_endpoint_url(s3_client, bucket):

    # Upload a file
    s3_client.put_object(
        ACL='private',
        Body=open('data/table.csv', 'rb'),
        Bucket=bucket,
        ContentType='text/csv',
        Key='table.csv')

    # Check the file
    with Stream(f's3://{bucket}/table.csv', s3_endpoint_url=S3_ENDPOINT_URL) as stream:
        assert stream.read() == [['id', 'name'], ['1', 'english'], ['2', '中国人']]


# https://github.com/frictionlessdata/tabulator-py/issues/271
@pytest.mark.skip
def test_stream_s3_non_existent_file(s3_client, bucket):
    with pytest.raises(exceptions.IOError):
        Stream(f's3://{bucket}/table.csv').open()


# Fixtures

@pytest.fixture(scope='module')
def s3_client():
    subprocess.Popen('moto_server', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    yield boto3.client('s3', endpoint_url=S3_ENDPOINT_URL)
    os.system('pkill moto_server')


@pytest.fixture
def bucket(s3_client):
    bucket = f"bucket_{''.join(random.choice(string.digits) for _ in range(16))}"
    s3_client.create_bucket(Bucket=bucket, ACL='public-read')
    return bucket
