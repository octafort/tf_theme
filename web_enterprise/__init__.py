# -*- coding: utf-8 -*-
# Part of Odoo, Cortex. See LICENSE file for full copyright and licensing details.

from . import controllers, models, version

CONFIG_PREFIX = "web_enterprise.login_"

def post_init_hook(env):
    users = env["res.users"].with_context(active_test=False).search([("share", "=", False)])
    for user in users:
        env["res.users.settings"].sudo()._find_or_create_for_user(user)

def uninstall_hook(env):
    env["ir.config_parameter"].sudo().search([("key", "=like", CONFIG_PREFIX + "%")]).unlink()
    env["ir.attachment"].sudo().search([("res_model", "=", "web_enterprise.theme.config")]).unlink()