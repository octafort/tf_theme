import re
from cortex import api, fields, models
from cortex.exceptions import ValidationError

HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
MAX_BOOKMARKS = 100
MAX_FAVORITE_APPS = 60
BOOKMARK_TYPES = {"menu", "action", "record"}
BOOKMARK_KEYS = {
    "id": str, "type": str, "label": str, "menuId": int, "appId": int,
    "actionId": int, "resModel": str, "resId": int, "viewType": str, "createdAt": int,
}


class ResUsersSettings(models.Model):
    _inherit = "res.users.settings"

    # --- Enterprise ---
    homemenu_config = fields.Json(string="Home Menu Configuration", readonly=True)
    color_scheme = fields.Selection(
        [("system", "System"), ("light", "Light"), ("dark", "Dark")],
        default="system", required=True, string="Color Scheme",
    )

    # --- Theme (color_scheme removed: color_scheme replaces it) ---
    cbt_palette = fields.Selection(
        [("indigo", "Indigo"), ("blue", "Blue"), ("purple", "Purple"), ("green", "Green"),
         ("teal", "Teal"), ("orange", "Orange"), ("red", "Red"), ("slate", "Slate"),
         ("custom", "Custom")],
        string="Color Palette", default="indigo", required=True)
    o_brand_cortex = fields.Char(string="Custom Primary Color", default="#4f46e5")
    cbt_nav_mode = fields.Selection(
        [("vertical", "Vertical (sidebar)"), ("horizontal", "Horizontal (top bar)"),
         ("compact", "Compact (icon rail + top bar)"), ("drawer", "Home menu")],
        string="Navigation", default="vertical", required=True)
    cbt_sidebar_mode = fields.Selection(
        [("expanded", "Expanded"), ("mini", "Mini"), ("collapsed", "Collapsed")],
        string="Sidebar", default="expanded", required=True)
    cbt_sidebar_locked = fields.Boolean(string="Sidebar Locked", default=True)
    cbt_sidebar_position = fields.Selection(
        [("start", "Start"), ("end", "End")], string="Sidebar Position", default="start", required=True)
    cbt_sidebar_style = fields.Selection(
        [("light", "Light"), ("tinted", "Tinted"), ("ink", "Ink")],
        string="Sidebar Style", default="tinted", required=True)
    cbt_font_family = fields.Selection(
        [("system", "System UI"), ("roboto", "Roboto"), ("open_sans", "Open Sans"),
         ("montserrat", "Montserrat"), ("raleway", "Raleway"), ("tajawal", "Tajawal")],
        string="Font", default="system", required=True)
    cbt_font_size = fields.Selection(
        [("sm", "Small"), ("md", "Default"), ("lg", "Large"), ("xl", "Extra large")],
        string="Font Size", default="md", required=True)
    cbt_radius = fields.Selection(
        [("none", "Square"), ("sm", "Subtle"), ("md", "Rounded"), ("lg", "Soft")],
        string="Corner Radius", default="md", required=True)
    cbt_density = fields.Selection(
        [("compact", "Compact"), ("comfortable", "Comfortable"), ("spacious", "Spacious")],
        string="Density", default="comfortable", required=True)
    cbt_chatter_position = fields.Selection(
        [("auto", "Automatic"), ("side", "Side"), ("bottom", "Bottom")],
        string="Chatter Position", default="auto", required=True)
    cbt_drawer_style = fields.Selection(
        [("grid", "Grid"), ("categories", "Categories"), ("list", "List")],
        string="App Drawer Style", default="grid", required=True)
    cbt_icon_style = fields.Selection(
        [("original", "Original"), ("rounded", "Rounded tile"), ("circle", "Circle"), ("flat", "Flat")],
        string="App Icon Style", default="rounded", required=True)
    cbt_animation = fields.Selection(
        [("full", "Full"), ("reduced", "Reduced"), ("none", "None")],
        string="Animations", default="full", required=True)
    cbt_split_view = fields.Boolean(string="List/Form Split View", default=False)
    cbt_favorite_apps = fields.Json(string="Favorite Apps", default=lambda self: [])
    cbt_bookmarks = fields.Json(string="Bookmarks", default=lambda self: [])

    def write(self, vals):
        if not vals.get("color_scheme", "system"):
            vals.pop("color_scheme")
        return super().write(vals)

    # _check_o_brand_cortex / _check_cbt_favorite_apps / _check_cbt_bookmarks /
    # _cbt_is_valid_bookmark: copy verbatim from web_enterprise.
    @api.constrains("o_brand_cortex")
    def _check_o_brand_cortex(self):
        for settings in self:
            color = settings.o_brand_cortex
            if color and not HEX_COLOR.match(color):
                raise ValidationError(self.env._("The primary color must be a #RRGGBB hex value."))

    @api.constrains("cbt_favorite_apps")
    def _check_cbt_favorite_apps(self):
        for settings in self:
            value = settings.cbt_favorite_apps or []
            if not isinstance(value, list) or len(value) > MAX_FAVORITE_APPS or not all(
                isinstance(v, str) and len(v) <= 256 for v in value
            ):
                raise ValidationError(self.env._("Invalid favorite applications."))

    @api.constrains("cbt_bookmarks")
    def _check_cbt_bookmarks(self):
        for settings in self:
            value = settings.cbt_bookmarks or []
            if not isinstance(value, list) or len(value) > MAX_BOOKMARKS:
                raise ValidationError(self.env._("Invalid bookmarks."))
            for bookmark in value:
                if not self._cbt_is_valid_bookmark(bookmark):
                    raise ValidationError(self.env._("Invalid bookmark entry."))

    @api.model
    def _cbt_is_valid_bookmark(self, bookmark):
        if not isinstance(bookmark, dict) or bookmark.get("type") not in BOOKMARK_TYPES:
            return False
        if not isinstance(bookmark.get("id"), str) or not isinstance(bookmark.get("label"), str):
            return False
        for key, value in bookmark.items():
            expected = BOOKMARK_KEYS.get(key)
            if expected is None:
                return False
            if value is None or value is False:
                continue
            if expected is int and (not isinstance(value, int) or isinstance(value, bool)):
                return False
            if expected is str and (not isinstance(value, str) or len(value) > 512):
                return False
        return True
