# -*- coding: utf-8 -*-

from unittest.mock import Mock

import pytest
from urchintai_client.request_sender import RequestSender


@pytest.mark.asyncio
async def test_should_return_content_if_post_ok():
    '''
    Test sending HTTP request using POST without error
    '''

    # Arrange
    url = 'http://example.com'
    data = { 'content': 'dummy' }
    response_text = 'dummy response text'

    resp = MockResponse(response_text, 200)

    session = Mock()
    session.post.return_value = resp
    request_sender = RequestSender(session)

    # Act
    actual_response_text = await request_sender.post(url, data)

    # Assert
    assert actual_response_text == response_text

@pytest.mark.asyncio
async def test_should_throw_exception_if_post_not_ok():
    '''
    Test sending HTTP request using POST with error
    '''

    # Arrange
    url = 'http://example.com'
    data = { 'content': 'dummy' }
    response_error = 'Server error'

    resp = MockResponse(response_error, 500)

    session = Mock()
    session.post.return_value = resp
    request_sender = RequestSender(session)

    # Act
    with pytest.raises(ConnectionError) as e:
        await request_sender.post(url, data)

    # Assert
    assert str(e.value) == f'An error occurred while sending request to {url}: {response_error}'

@pytest.mark.asyncio
async def test_should_return_content_if_get_ok(mocker):
    '''
    Test sending HTTP request using GET without error
    '''

    # Arrange
    url = 'http://example.com'
    response_text = 'dummy response text'

    resp = MockResponse(response_text, 200)

    session = Mock()
    session.get.return_value = resp
    request_sender = RequestSender(session)

    # Act
    actual_response_text = await request_sender.get(url)

    # Assert
    assert actual_response_text == response_text

@pytest.mark.asyncio
async def test_should_throw_exception_if_get_not_ok(mocker):
    '''
    Test sending HTTP request using GET with error
    '''

    # Arrange
    url = 'http://example.com'
    response_error = 'Server error'

    resp = MockResponse(response_error, 500)

    session = Mock()
    session.get.return_value = resp
    request_sender = RequestSender(session)

    # Act
    with pytest.raises(ConnectionError) as e:
        await request_sender.get(url)

    # Assert
    assert str(e.value) == f'An error occurred while sending request to {url}: {response_error}'

class MockResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
