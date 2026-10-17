# -*- coding: utf-8 -*-
# Part of Odoo, Cortex. See LICENSE file for full copyright and licensing details.

import cortex

# ----------------------------------------------------------
# Monkey patch release to set the edition as 'enterprise'
# ----------------------------------------------------------
cortex.release.version_info = cortex.release.version_info[:5] + ('e',)
if '+e' not in cortex.release.version:     # not already patched by packaging
    cortex.release.version = '{0}+e{1}{2}'.format(*cortex.release.version.partition('-'))

cortex.service.common.RPC_VERSION_1.update(
    server_version=cortex.release.version,
    server_version_info=cortex.release.version_info)
