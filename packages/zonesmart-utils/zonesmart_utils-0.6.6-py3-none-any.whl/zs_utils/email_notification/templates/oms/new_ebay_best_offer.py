from zs_utils.email_notification.templates.oms import base

icon = "best_offer_icon.png"

title_ru = "Новое предложение от покупателя на eBay"
title_en = "New eBay offer from buyer"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, добрый день!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px">
                Вам поступило ценное предложение от потенциального покупателя <span style='color: #3BD0BC; font-weight: bold'>{buyer}</span> на eBay.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{best_offer_url}" class="button" style="color: #ffffff">
                    Рассмотреть предложение
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
            <td style="padding: 0 0 40px">
                You have received a valuable offer from a potential buyer <span style='color: #3BD0BC; font-weight: bold'>{buyer}</span> on eBay.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{best_offer_url}" class="button" style="color: #ffffff">
                    Consider the proposal
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
