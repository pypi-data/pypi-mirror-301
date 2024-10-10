from zs_utils.email_notification.templates.oms import base

icon = "new_message_icon.png"

subject_ru = "Обращение №{ticket_number} закрыто"
subject_en = "Ticket #{ticket_number} was closed"

title_ru = "Обращение №{ticket_number} закрыто"
title_en = "Ticket #{ticket_number} was closed"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Если у Вас возникнут дополнительные вопросы, просьба создать повторное обращение <span style='color: #3BD0BC; font-weight: bold'>с указанием номера</span> текущей заявки.
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
                If you have any additional questions, please create a second ticket <span style='color: #3BD0BC; font-weight: bold'>indicating the number</span> of the current application.
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
