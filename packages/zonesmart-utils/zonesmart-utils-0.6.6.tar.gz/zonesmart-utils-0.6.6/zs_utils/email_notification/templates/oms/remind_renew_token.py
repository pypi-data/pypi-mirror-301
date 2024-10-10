from zs_utils.email_notification.templates.oms import base

icon = "token_renewal_icon.png"

title_ru = "Требуется обновление токена аккаунта"
title_en = "Account token update required"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, аккаунт <span style='color: #3BD0BC; font-weight: bold'>{marketplace_user_account}</span> маркетплейса <span style='color: #3BD0BC; font-weight: bold'>{marketplace}</span> был деактивирован из-за устаревшего токена.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Если у Вас возникли вопросы, ознакомьтесь с <a href='https://zonesmart.zendesk.com/hc/ru/articles/4403027869201' style='color: #3BD0BC; font-weight: bold'>инструкцией по обновлению токена (на примере eBay)</a>, или обратитесь в службу поддержки: <a style="color: #3BD0BC; font-weight: bold">support@zonesmart.ru</a>.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{token_renew_url}" class="button" style="color: #ffffff">
                    Обновить токен
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, account <span style='color: #3BD0BC; font-weight: bold'>{marketplace_user_account}</span> marketplace <span style='color: #3BD0BC; font-weight: bold'>{marketplace}</span> has been deactivated due to a deprecated token.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                For questions, please see <a href='https://zonesmart.zendesk.com/hc/en/articles/4403027869201' style='color: #3BD0BC; font-weight: bold'>instructions for refreshing the token (using eBay as an example)</a>, or contact support: <a style="color: #3BD0BC; font-weight: bold">support@zonesmart.ru</a>.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{token_renew_url}" class="button" style="color: #ffffff">
                    Refresh Token
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
