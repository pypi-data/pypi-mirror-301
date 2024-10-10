from zs_utils.email_notification.templates.oms import base

icon = "icon_pricing.png"

title_ru = "Оформление подписки"
title_en = "Subscription created"

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
                Вы успешно подключили тарифный план {tariff} ({period_in_days} дней за {currency} {price}) для доступа к системе ZoneSmart. Условия тарифа начнут применяться с {date_active_from}.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                В дальнейшем Вы можете управлять подключенным тарифным планом в настройках вашего профиля
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{tariff_url}" class="button" style="color: #ffffff">
                    Перейти в настройки
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, good afternoon!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                 You have successfully activated the tariff plan {tariff} ({period_in_days} days for {currency} {price}) to access the ZoneSmart system. Tariff conditions will start to apply from {date_active_from}.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                In the future, you can manage the connected tariff plan in your profile settings
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{tariff_url}" class="button" style="color: #ffffff">
                    Go to settings
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
