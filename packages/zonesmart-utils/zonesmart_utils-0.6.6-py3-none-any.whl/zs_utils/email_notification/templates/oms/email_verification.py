from zs_utils.email_notification.templates.oms import base

icon = "icon_email.png"

title_ru = "Подтверждение email"
title_en = "Email verification"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, добрый день.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                 Для подтверждения адреса электронной почты Вашего аккаунта <span style='color: #3BD0BC; font-weight: bold'>ZoneSmart</span>, пожалуйста, нажмите на кнопку ниже.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0px 0 40px">
                <a href="{accept_email_url}" class="button" style="color: #ffffff">
                    Подтвердить email
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
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, good afternoon.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                  To confirm the email address of your account <span style='color: #3BD0BC; font-weight: bold'>ZoneSmart</span>, please click the button below.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0px 0 40px">
                <a href="{accept_email_url}" class="button" style="color: #ffffff">
                    Confirm email
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
