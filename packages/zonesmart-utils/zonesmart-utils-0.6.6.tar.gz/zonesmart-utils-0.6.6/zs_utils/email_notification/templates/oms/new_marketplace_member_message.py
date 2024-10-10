from zs_utils.email_notification.templates.oms import base

icon = "new_message_icon.png"

subject_ru = "Новое сообщение от покупателя на {marketplace_name}"
subject_en = "New message from {marketplace_name} buyer"

title_ru = "Новое сообщение от покупателя на {marketplace_name}"
title_en = "New message from {marketplace_name} buyer"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 30px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, вам поступило новое сообщение от потенциального покупателя <span style='color: #3BD0BC; font-weight: bold'>{sender}</span> на <b>{marketplace_name}</b>!
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
                            <span style="font-weight: 700">{sender}</span>
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
                <a href="{chat_url}" class="button" style="color: #ffffff">
                    Перейти к сообщению
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, you have received a new message from a potential buyer <span style='color: #3BD0BC; font-weight: bold'>{sender}</span> on <b>{marketplace_name}</b>!
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
                            <span style="font-weight: 700">{sender}</span>
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
                <a href="{chat_url}" class="button" style="color: #ffffff">
                    Go to message
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
