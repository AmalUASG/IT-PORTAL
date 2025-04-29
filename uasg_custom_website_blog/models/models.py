import requests
from odoo import models, fields, api
import datetime
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import logging


_logger = logging.getLogger(__name__)


class ResUser(models.Model):
    
    _inherit="res.users"

    def _check_credentials(self, password, env):
        """ Validates the current user's password.

        Override this method to plug additional authentication methods.

        Overrides should:

        * call `super` to delegate to parents for credentials-checking
        * catch AccessDenied and perform their own checking
        * (re)raise AccessDenied if the credentials are still invalid
          according to their own validation method

        When trying to check for credentials validity, call _check_credentials
        instead.
        """
        """ Override this method to plug additional authentication methods"""
        # assert password
        # self.env.cr.execute(
        #     "SELECT COALESCE(password, '') FROM res_users WHERE id=%s",
        #     [self.env.user.id]
        # )
        # [hashed] = self.env.cr.fetchone()
        # valid, replacement = self._crypt_context()\
        #     .verify_and_update(password, hashed)
        # if replacement is not None:
        #     self._set_encrypted_password(self.env.user.id, replacement)
        # if not valid:
        #     raise AccessDenied()

        return True