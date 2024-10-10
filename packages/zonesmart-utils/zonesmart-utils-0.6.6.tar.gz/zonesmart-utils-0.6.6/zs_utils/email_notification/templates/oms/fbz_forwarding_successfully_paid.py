from zs_utils.email_notification.templates.oms import base

icon = "payment_remind_icon.png"

title_ru = "Оплата прошла успешно"
title_en = "Payment was successful"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151;box-sizing:border-box;max-width: 420px;width:100%;font-size:13px;line-height:149%;padding:0 20px">
        <tbody>
        <tr>
            <td style="padding:0 0 10px">
                Оплата форвард-отправления №{number} (трек номер консолидации {tracking_number}).
            </td>
        </tr>
        </tbody>
    </table>
"""

body_en = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151;box-sizing:border-box;max-width: 420px;width:100%;font-size:13px;line-height:149%;padding:0 20px">
        <tbody>
        <tr>
            <td style="padding:0 0 10px">
                Payment for forwarding shipment #{number} (consolidation tracking number {tracking_number}).
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
