from zs_utils.email_notification.templates.oms import base

icon = "payment_remind_icon.png"

title_ru = "Пользователь прикрепил платёжное поручение!"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                Пользователь {user_id} оплатил счет {payment_number} на сумму {amount} {currency}.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Подтвердить платеж нужно по ссылке https://app.zonesmart.ru/admin/billing/all в течение двух часов (пн-пт с 10.00-19.00)
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
