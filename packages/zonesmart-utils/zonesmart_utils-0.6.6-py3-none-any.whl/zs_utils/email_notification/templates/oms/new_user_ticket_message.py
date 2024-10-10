from zs_utils.email_notification.templates.oms import base

icon = "new_message_icon.png"

title_ru = "Новое сообщение от пользователя Zonesmart"
title_en = "New user message from ZoneSmart"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 30px">
                Вам поступило новое сообщение от пользователя <span style="color: #3BD0BC; font-weight: bold">Zonesmart OMS</span>.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 20px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td style="padding: 0 10px 20px">
                            <img src="{user_img_url}" alt="user_img_url" width="90px">
                        </td>
                        <td style="padding: 0 10px 20px">
                            <span style="font-weight: 700">{first_name}</span>
                            <p>{message_text}</p>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{ticket_url}" class="button" style="color: #ffffff">
                    Перейти в чат
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
            <td style="padding: 0 0 30px">
                You received a new message from a user <span style="color: #3BD0BC; font-weight: bold">Zonesmart OMS</span>.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 20px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td>
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td style="padding: 0 10px 20px">
                            <img src="{user_img_url}" alt="user_img_url" width="90px">
                        </td>
                        <td style="padding: 0 10px 20px">
                            <span style="font-weight: 700">{first_name}</span>
                            <p>{message_text}</p>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{ticket_url}" class="button" style="color: #ffffff">
                    Go to chat
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
