from zs_utils.email_notification.templates.oms import base

icon = "icon_email.png"

title_ru = "Изменение email"
title_en = "Email changing"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Здравствуйте, <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Для изменения адреса электронной почты вашего аккаунта <span style='color: #3BD0BC; font-weight: bold'>Zonesmart</span>, пожалуйста, нажмите на кнопку ниже.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{reset_email_url}" class="button" style="color: #ffffff">
                    Изменить email
                </a>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Мы желаем вам удачных продаж по всему миру.
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
                Hello, <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                To change your account email address <span style='color: #3BD0BC; font-weight: bold'>Zonesmart</span>, please click the button below.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{reset_email_url}" class="button" style="color: #ffffff">
                    Change email
                </a>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                We wish you successful sales all over the world.
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
