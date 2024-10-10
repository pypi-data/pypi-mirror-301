from zs_utils.email_notification.templates.oms import base

icon = "payment_remind_icon.png"

title_ru = "Напоминаем Вам о предстоящем платеже"
title_en = "Remind you about the upcoming payment"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, добрый день!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                Напоминаем, что платеж за подписку <span style='color: #3BD0BC; font-weight: bold'>{tariff}</span> в <span style='color: #3BD0BC; font-weight: bold'>{currency} {amount}</span> будет списан через <span style='color: #3BD0BC; font-weight: bold'>{days_before_payment} дня</span> c активной карты.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Если Вы хотите поменять способ оплаты подписки перейдите по ссылке: <a href="{payment_method_url}" style="color: #3BD0BC; font-weight: bold">{payment_method_url}</a>
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, good afternoon!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                We remind you that the payment for the subscription <span style='color: #3BD0BC; font-weight: bold'>{tariff}</span> in <span style='color: #3BD0BC; font-weight: bold'>{currency} {amount}</span> will be deducted via <span style='color: #3BD0BC; font-weight: bold'>{days_before_payment} of the day</span> from the active card.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                If you want to change the subscription payment method, follow the link: <a href="{payment_method_url}" style="color: #3BD0BC; font-weight: bold">{payment_method_url}</a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
