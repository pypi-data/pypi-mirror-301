from zs_utils.email_notification.templates.oms import base

icon = "payment_remind_icon.png"

subject_ru = "Платеж для аккаунта {email} обработан"
subject_en = "Payment for account {email} processed"

title_ru = "Платеж обработан"
title_en = "Payment processed"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                Спасибо за ваш заказ.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 20px">
                Пожалуйста, проверьте сумму платежа ниже, мы также приложили PDF с подробным описанием вашего заказа и условий подписки.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 5px">
                Аккаунт Zonesmart: {email}
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 5px">
                Метод оплаты: Credit Card
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 5px">
                Дата платежа: {date}
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 20px">
                Сумма: {currency} {amount}
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 30px">
                В случае любых вопросов, пожалуйста, свяжитесь с нами через почту support@zonesmart.ru
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
                Thank you for your order.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 20px">
                Please check the payment amount below, we have also attached a PDF detailing your order and subscription terms.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 5px">
                Zonesmart account: {email}
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 5px">
                Payment method: Credit Card
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 5px">
                Payment date: {date}
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 20px">
                Amount: {currency} {amount}
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 30px">
                For any questions, please contact us via mail support@zonesmart.ru
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
