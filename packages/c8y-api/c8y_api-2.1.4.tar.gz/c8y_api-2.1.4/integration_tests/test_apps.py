# Copyright (c) 2020 Software AG,
# Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA,
# and/or its subsidiaries and/or its affiliates and/or their licensors.
# Use, reproduction, transfer, publication or disclosure is prohibited except
# as specifically provided for in your License Agreement with Software AG.

import pytest
import requests

from c8y_api import CumulocityRestApi, HTTPBearerAuth
from c8y_api.app import SimpleCumulocityApp
from c8y_api.model import ManagedObject


@pytest.fixture(name='token_app')
def fix_token_app(test_environment):
    """Provide a token-based REST API instance."""
    # First, create an instance for basic auth
    c8y = SimpleCumulocityApp()
    # Submit auth request
    form_data = {
            'grant_type': 'PASSWORD',
            'username': c8y.auth.username,
            'password': c8y.auth.password
        }
    r = requests.post(url=c8y.base_url + '/tenant/oauth', data=form_data, timeout=60.0)
    # Obtain token from response
    assert r.status_code == 200
    cookie = r.headers['Set-Cookie']
    # split by ; to separate parts, then map a=b items to dictionary
    cookie_parts = {x[0]:x[1] for x in [c.split('=') for c in cookie.split(';')] if len(x) == 2}
    auth_token = cookie_parts['authorization']
    assert auth_token
    # build token-based app
    return CumulocityRestApi(
        base_url=c8y.base_url,
        tenant_id=c8y.tenant_id,
        auth=HTTPBearerAuth(auth_token)
    )


def test_token_based_app_headers(token_app):
    """Verify that a token-based app only features a 'Bearer' auth header."""
    response = token_app.session.get("https://httpbin.org/headers")
    auth_header = response.json()['headers']['Authorization']
    assert auth_header.startswith('Bearer')


def test_token_based_app(token_app):
    """Verify that a token-based app can be used for all kind of requests."""
    mo = ManagedObject(token_app, name='test-object', type='test-object-type').create()
    mo['new_Fragment'] = {}
    mo.update()
    mo.delete()
