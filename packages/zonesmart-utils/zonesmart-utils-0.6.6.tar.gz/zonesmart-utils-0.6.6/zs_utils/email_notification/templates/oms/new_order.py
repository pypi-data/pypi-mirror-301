from zs_utils.email_notification.templates.oms import base

icon = "order_icon.png"

title_ru = "Новый заказ"
title_en = "New order"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, поступил новый заказ {created_date}.
            </td>
        </tr>
        </tbody>
    </table>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 34px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px; font-size: 18px">
                Источник: <span style="color: #3BD0BC; font-weight: bold">{channel}</span>
            </td>
        </tr>
        <tr>
            <td style="font-size: 13px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">

                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="45%">
                            Товар
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Кол-во
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">
                            Цена
                        </td>
                    </tr>
                    {items}
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td style="padding: 34px 0 34px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px; font-size: 18px; font-weight: 700">
                Покупатель:
            </td>
        </tr>
        <tr>
            <td style="font-size: 13px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td>
                            {buyer}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            {phone}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 10px;">
                            {email}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Адрес:</b> {first_line} {second_line}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Город:</b> {city}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Область:</b> {state}
                        </td>
                        <td align="right" style="color: #938C8C">
                            Цена товаров: {currency_code} {subtotal_price}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Страна:</b> {country}
                        </td>
                        <td align="right" style="color: #938C8C">
                            Доставка: {currency_code} {total_shipping_cost}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Индекс:</b> {zip_code}
                        </td>
                        <td align="right" style="color: #938C8C">
                            Итог: <span style="color: #3BD0BC; font-weight: bold">{currency_code} {total_price}</span>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 50px 0 40px">
                <a href="{order_url}" class="button" style="color: #ffffff">
                    Перейти к заказу
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, received a new order {created_date}.
            </td>
        </tr>
        </tbody>
    </table>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 34px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 40px; font-size: 18px">
                Source: <span style="color: #3BD0BC; font-weight: bold">{channel}</span>
            </td>
        </tr>
        <tr>
            <td style="font-size: 13px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">

                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="45%">
                            Product
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Quantity
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">
                            Price
                        </td>
                    </tr>
                    {items}
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td style="padding: 34px 0 34px">
                <hr color="#EAE7FF">
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px; font-size: 18px; font-weight: 700">
                Buyer:
            </td>
        </tr>
        <tr>
            <td style="font-size: 13px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="color: #515151; box-sizing:border-box;width:100%; font-size: 13px;line-height: 149%;">
                    <tbody>
                    <tr>
                        <td>
                            {buyer}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            {phone}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding-bottom: 10px;">
                            {email}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Address:</b> {first_line} {second_line}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>City:</b> {city}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Region:</b> {state}
                        </td>
                        <td align="right" style="color: #938C8C">
                            Products price: {currency_code} {subtotal_price}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Country:</b> {country}
                        </td>
                        <td align="right" style="color: #938C8C">
                            Delivery: {currency_code} {total_shipping_cost}
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <b>Index:</b> {zip_code}
                        </td>
                        <td align="right" style="color: #938C8C">
                            Total: <span style="color: #3BD0BC; font-weight: bold">{currency_code} {total_price}</span>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 50px 0 40px">
                <a href="{order_url}" class="button" style="color: #ffffff">
                    Go to order
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

items = """
    <tr>
        <td style="padding: 0 10px 10px">
            <img src="{item_img_url}" alt="item_img_url" width="90px">
        </td>
        <td style="padding: 0 10px 10px">
            {title}
            <p style="color: #85868B; font-weight: 400; font-size: 12px; margin: 0; padding-top: 5px">SKU: {sku}</p>
        </td>
        <td style="padding: 0 10px 10px">
            {quantity}
        </td>
        <td style="padding: 0 10px 10px">
            <span style="color: #3BD0BC; font-weight: bold">{currency} {subtotal_price}</span>
        </td>
    </tr>
"""


cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
