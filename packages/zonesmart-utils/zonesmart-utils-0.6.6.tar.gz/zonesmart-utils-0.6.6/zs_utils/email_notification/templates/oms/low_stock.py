from zs_utils.email_notification.templates.oms import base

icon = "stock_icon.png"

title_ru = "У Вас низкий остаток по товару"
title_en = "You have a low stock for the product"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, количество товара опустилось ниже пользовательского значения.
            </td>
        </tr>
        </tbody>
    </table>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td style="font-size: 13px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">

                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="50%">
                            Товар
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Sku
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Кол-во
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 10px 10px">
                            <img src="{item_img_url}" alt="item_img_url" width="90px">
                        </td>
                        <td style="padding: 0 10px 10px">
                            <span style="color: #3BD0BC; font-weight: bold">{title}</span>
                        </td>
                        <td style="padding: 0 10px 10px">
                            <span style="color: #3BD0BC; font-weight: bold">{sku}</span>
                        </td>
                        <td style="padding: 0 10px 10px">
                            <span style="color: #3BD0BC; font-weight: bold">{quantity} шт</span>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 50px 0 40px">
                <a href="{update_stocks_url}" class="button" style="color: #ffffff">
                    Редактировать остатки
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
            <td style="padding: 0 0 40px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, the item's quantity has dropped below the custom value.
            </td>
        </tr>
        </tbody>
    </table>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td style="font-size: 13px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">

                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="50%">
                            Product
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Sku
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Quantity
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 0 10px 10px">
                            <img src="{item_img_url}" alt="item_img_url" width="90px">
                        </td>
                        <td style="padding: 0 10px 10px">
                            <span style="color: #3BD0BC; font-weight: bold">{title}</span>
                        </td>
                        <td style="padding: 0 10px 10px">
                            <span style="color: #3BD0BC; font-weight: bold">{sku}</span>
                        </td>
                        <td style="padding: 0 10px 10px">
                            <span style="color: #3BD0BC; font-weight: bold">{quantity} pcs</span>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 50px 0 40px">
                <a href="{update_stocks_url}" class="button" style="color: #ffffff">
                    Edit stocks
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
