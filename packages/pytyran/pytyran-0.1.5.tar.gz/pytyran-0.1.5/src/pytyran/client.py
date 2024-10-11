# MIT License
#
# Copyright (c) 2024 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests


class Client:

    def __init__(self, base_url, api_key):
        self._base_url = base_url
        self._api_key = api_key

    def create_document(self, content, metadata):
        url = f"{self._base_url}/api/v1/document"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self._api_key,
        }

        data = {"content": content, "metadata": metadata}

        return requests.post(url, json=data, headers=headers)

    def delete_document(self, uuid):
        url = f"{self._base_url}/api/v1/document/{uuid}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self._api_key,
        }

        return requests.delete(url, headers=headers)

    def search_documents(self, text, metadata, limit):
        url = f"{self._base_url}/api/v1/document/search"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self._api_key,
        }

        data = {"text": text, "limit": limit, "metadata": metadata}

        return requests.post(url, json=data, headers=headers)
