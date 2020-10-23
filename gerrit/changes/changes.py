#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.changes.change import GerritChange
from gerrit.utils.common import check


class GerritChanges:
    def __init__(self, gerrit):
        self.gerrit = gerrit

    def search(self, query: str) -> list:
        """
        Queries changes visible to the caller.

        :return:
        """
        endpoint = "/changes/?%s" % query
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritChange.parse_list(result, gerrit=self.gerrit)

    def get(self, id_: str) -> GerritChange:
        """
        Retrieves a change.

        :param id_: change id
        :return:
        """
        endpoint = "/changes/%s" % id_
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return GerritChange.parse(result, gerrit=self.gerrit)

    @check
    def create(self, input_: dict) -> GerritChange:
        """
        create a change

        .. code-block:: python

            input_ = {
                "project": "myProject",
                "subject": "Let's support 100% Gerrit workflow direct in browser",
                "branch": "stable",
                "topic": "create-change-in-browser",
                "status": "NEW"
            }
            result = gerrit.changes.create(input_)

        :param input_: the ChangeInput entity,
          https://gerrit-review.googlesource.com/Documentation/rest-api-changes.html#change-input
        :return:
        """
        endpoint = "/changes/"
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.post(
            base_url, json=input_, headers=self.gerrit.default_headers
        )
        result = self.gerrit.decode_response(response)
        return GerritChange.parse(result, gerrit=self.gerrit)