from zs_utils.email_notification.templates.oms import base

icon = "icon_password.png"

subject_ru = "Сброс пароля"
subject_en = "Password reset"

title_ru = "Забыли Ваш пароль?"
title_en = "Forgot Your password?"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Похоже, вы хотите сбросить пароль для учетной записи <span style="color: #3BD0BC; font-weight: bold">Zonesmart</span>.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Не волнуйтесь, вы можете создать новый, нажав кнопку ниже.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 30px">
                <a href="{reset_password_url}" class="button" style="color: #ffffff">
                    Сброс пароля.
                </a>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px; letter-spacing: 0.5px; color: #736E6E; font-size: 12px">
                Если вы не просили нас сбросить пароль, то просто проигнорируйте\nэто письмо. Ваша учетная запись в безопасности.
            </td>
        </tr>
        </tbody>
    </table>
"""
body_en = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                It looks like you want to reset your account password <span style="color: #3BD0BC; font-weight: bold">Zonesmart</span>.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Don't worry, you can create a new one by clicking the button below.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 30px">
                <a href="{reset_password_url}" class="button" style="color: #ffffff">
                    Password reset.
                </a>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px; letter-spacing: 0.5px; color: #736E6E; font-size: 12px">
                If you didn't ask us to reset your password, please just ignore\nthis email. Your account is safe.
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en

footer_ru = """
    Это письмо было отправлено, потому что вы попросили сбросить пароль на <a href="https://app.zonesmart.com" style="color: #3BD0BC; text-decoration: none">Zonesmart</a>
"""
footer_en = """
    This email was sent because you asked to reset your password on <a href="https://app.zonesmart.com" style="color: #3BD0BC; text-decoration: none">Zonesmart</a>
"""
