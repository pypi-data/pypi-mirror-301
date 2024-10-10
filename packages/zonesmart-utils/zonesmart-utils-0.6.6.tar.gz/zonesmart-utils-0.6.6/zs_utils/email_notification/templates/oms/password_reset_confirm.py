from zs_utils.email_notification.templates.oms import base

icon = "key-icon.png"

title_ru = "Ваш пароль был изменен"
title_en = "Password was changed"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                Пароль для  вашей учетной записи <span style='color: #3BD0BC; font-weight: bold'>Zonesmart</span> недавно был изменен. Теперь вы можете войти в систему, используя свой новый пароль.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{dashboard_url}" class="button" style="color: #ffffff">
                    Перейти в Zonesmart
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""
body_en = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                Password for your account <span style='color: #3BD0BC; font-weight: bold'>Zonesmart</span> has been changed recently. You can now log in with your new password.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{dashboard_url}" class="button" style="color: #ffffff">
                    Go to Zonesmart
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
