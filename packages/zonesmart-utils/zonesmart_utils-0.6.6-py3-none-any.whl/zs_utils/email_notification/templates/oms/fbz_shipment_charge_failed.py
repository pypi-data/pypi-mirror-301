from zs_utils.email_notification.templates.oms import base

icon = "payment_remind_icon.png"

subject_ru = "Недостаточно средств на кошельке"
subject_en = "Insufficient funds in your wallet"

title_ru = "Не удалось оплатить отправку заказа"
title_en = "Failed to pay for order shipping"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Заказ №{order_id} от {date} не может быть отправлен. Пополните кошелек.
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
                Order №{order_id} dated {date} can't be shipped. Top up your wallet.
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
