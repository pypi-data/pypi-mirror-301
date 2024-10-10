from zs_utils.email_notification.templates.oms import base

icon = "late_payment_icon.png"

title_ru = "Просрочен платеж"
title_en = "Payment overdue"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, платеж в сумме <span style='color: #3BD0BC; font-weight: bold'>{currency} {amount}</span> не был списан в дату <span style='color: #3BD0BC; font-weight: bold'>{date}</span> из-за ошибки.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                Вы можете обновить метод оплаты, чтобы избежать принудительного перехода на бесплатный тариф.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Все основные возможности системы, включая обновление остатков и обработку заказов, будут недоступны.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{payment_method_url}" class="button" style="color: #ffffff">
                    Обновить метод оплаты
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, payment in amount <span style='color: #3BD0BC; font-weight: bold'>{currency} {amount}</span> was not debited on date <span style='color: #3BD0BC; font-weight: bold'>{date}</span> due to a bug.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                You can update your payment method to avoid being forced to upgrade to a free plan.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                All the main features of the system, including updating balances and processing orders, will be unavailable.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{payment_method_url}" class="button" style="color: #ffffff">
                    Update payment method
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
