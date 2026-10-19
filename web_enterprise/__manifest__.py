# -*- coding: utf-8 -*-
# Part of Odoo, Cortex. See LICENSE file for full copyright and licensing details.

{
    'name': 'Web Enterprise',
    'category': 'Hidden',
    'summary': 'Enterprise web client with the DevsCodespace backend theme integrated',
    'version': '1.0',
    'description': """
Cortex Enterprise Web Client with an integrated, configurable backend theme:
    sidebar, app drawer, global search, bookmarks, palettes, split view,
    chatter position and branded login pages. Home Menu and dark mode are kept.
    """,
    'depends': ['web','mail', 'base_setup'],
    'auto_install': ['web'],
    'data': [
        'views/webclient_templates.xml',
        'views/res_users_views.xml',
        'views/login_templates.xml',
        'data/theme_actions.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'web/static/src/scss/primary_variables.scss', 'web_enterprise/static/src/**/*.variables.scss'),
            ('before', 'web/static/src/scss/primary_variables.scss', 'web_enterprise/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'web/static/src/scss/secondary_variables.scss', 'web_enterprise/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'web_enterprise/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            #'web_enterprise/static/src/webclient/home_menu/home_menu_background.scss', # used by login page
            'web_enterprise/static/src/theme/login/login.scss',
            'web_enterprise/static/src/webclient/navbar/navbar.scss',
        ],
        'web.assets_backend': [
            'web_enterprise/static/src/webclient/**/*.scss',
            'web_enterprise/static/src/views/**/*.scss',

            'web_enterprise/static/src/core/**/*',
            'web_enterprise/static/src/webclient/**/*.js',
            ('after', 'web/static/src/views/list/list_renderer.xml', 'web_enterprise/static/src/views/list/list_renderer_desktop.xml'),
            'web_enterprise/static/src/webclient/**/*.xml',
            'web_enterprise/static/src/views/**/*.js',
            'web_enterprise/static/src/views/**/*.xml',
            ('remove', 'web_enterprise/static/src/views/pivot/**'),
            
            # --- theme (after Enterprise SCSS so equal-specificity rules win) ---
            'web_enterprise/static/src/scss/fonts.scss',
            'web_enterprise/static/src/scss/tokens.scss',
            'web_enterprise/static/src/scss/ui/*.scss',
            'web_enterprise/static/src/components/**/*',
            'web_enterprise/static/src/patches/**/*',

            # Don't include dark mode files in light mode
            ('remove', 'web_enterprise/static/src/**/*.dark.scss'),
        ],
        'web.assets_backend_lazy': [
            'web_enterprise/static/src/views/pivot/**',
        ],
        'web.assets_backend_lazy_dark': [
            ('include', 'web.dark_mode_variables'),
            # web._assets_backend_helpers
            ('before', 'web_enterprise/static/src/scss/bootstrap_overridden.scss', 'web_enterprise/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'web_enterprise/static/src/scss/bs_functions_overridden.dark.scss'),
        ],
        'web.assets_web': [
            ('replace', 'web/static/src/main.js', 'web_enterprise/static/src/main.js'),
        ],
        # ========= Dark Mode =========
        "web.dark_mode_variables": [
            # web._assets_primary_variables
            ('before', 'web_enterprise/static/src/scss/primary_variables.scss', 'web_enterprise/static/src/scss/primary_variables.dark.scss'),
            ('before', 'web_enterprise/static/src/**/*.variables.scss', 'web_enterprise/static/src/**/*.variables.dark.scss'),
            # web._assets_secondary_variables
            ('before', 'web_enterprise/static/src/scss/secondary_variables.scss', 'web_enterprise/static/src/scss/secondary_variables.dark.scss'),
        ],
        "web.assets_web_dark": [
            ('include', 'web.dark_mode_variables'),
            # web._assets_backend_helpers
            ('before', 'web_enterprise/static/src/scss/bootstrap_overridden.scss', 'web_enterprise/static/src/scss/bootstrap_overridden.dark.scss'),
            ('after', 'web/static/lib/bootstrap/scss/_functions.scss', 'web_enterprise/static/src/scss/bs_functions_overridden.dark.scss'),
            # assets_backend
            'web_enterprise/static/src/**/*.dark.scss',
        ],
        'web.tests_assets': [
            'web_enterprise/static/tests/*.js',
        ],
        "web.assets_tests": [
            "web_enterprise/static/tests/tours/**/*.js",
        ],
        # Unit test files
        'web.assets_unit_tests': [
            'web_enterprise/static/tests/**/*.test.js',
        ],
        'web.qunit_suite_tests': [
            'web_enterprise/static/tests/views/**/*.js',
            'web_enterprise/static/tests/webclient/**/*.js',
            ('remove', 'web_enterprise/static/tests/**/*.test.js'),
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'author': 'Cortex S.A.',
    'license': 'OEEL-1',
}
