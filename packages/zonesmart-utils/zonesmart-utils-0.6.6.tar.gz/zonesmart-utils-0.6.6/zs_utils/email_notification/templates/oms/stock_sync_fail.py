from zs_utils.email_notification.templates.oms import base

icon = "stock_sync_fail_icon.png"

title_ru = "Неудачная синхронизация остатков на канале продаж"
title_en = "Synchronization of stocks on the channel was failed"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, остаток товара не был обновлен на канале продаж <span style='color: #3BD0BC; font-weight: bold'>{channel}</span> из-за возникшей ошибки.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                 Если у Вас возникли вопросы, обратитесь в службу поддержки: <a style="color: #3BD0BC; font-weight: bold">support@zonesmart.ru</a>.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{notification_url}" class="button" style="color: #ffffff">
                    Подробности
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>the rest of the product was not updated on the sales channel <span style='color: #3BD0BC; font-weight: bold'>{channel}</span> due to a bug.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                 If you have any questions, please contact support: <a style="color: #3BD0BC; font-weight: bold">support@zonesmart.ru</a>.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{notification_url}" class="button" style="color: #ffffff">
                    Details
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
