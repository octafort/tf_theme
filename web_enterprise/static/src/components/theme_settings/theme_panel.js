import { Component } from "@cortex/owl";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";
import { useService } from "@web/core/utils/hooks";
import { usePanel } from "../../core/use_panel";
import { ThemeSettings } from "./theme_settings";

/** Quick settings sheet opened from the systray / sidebar. */
export class ThemePanel extends Component {
    static template = "web_enterprise.ThemePanel";
    static components = { ThemeSettings };
    static props = {};

    setup() {
        this.themeService = useService("cbt_theme");
        this.action = useService("action");
        this.rootRef = usePanel("root", () => this.close());
        this.isSystem = user.isSystem;
    }

    close() {
        this.themeService.closePanel("settings");
    }

    async openFullPage() {
        this.close();
        await this.action.doAction("web_enterprise.action_theme_settings");
    }

    get labels() {
        return {
            title: _t("Theme settings"),
            close: _t("Close"),
            more: _t("Login page & full settings"),
        };
    }
}
