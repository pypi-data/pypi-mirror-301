from zs_utils.email_notification.templates.oms import base

icon = "shipment_icon.png"

title_ru = "Создано отправление товаров"
title_en = "Order shipment was created"


body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, {created_date} было создано отправление товаров.
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
                        <td style="padding: 0 10px 10px; font-weight: 700" width="30%">
                            Товар
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Кол-во
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">
                            Штрих-код
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Склад
                        </td>
                    </tr>
                    {items}
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, {created_date} shipment has been created.
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
                        <td style="padding: 0 10px 10px; font-weight: 700" width="30%">
                            Product
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Quantity
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="20%">
                            Barcode
                        </td>
                        <td style="padding: 0 10px 10px; font-weight: 700" width="15%">
                            Warehouse
                        </td>
                    </tr>
                    {items}
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

items_ru = """
    <tr>
        <td style="padding: 0 10px 10px">
            <img src="{item_img_url}" alt="item_img_url" width="90px">
        </td>
        <td style="padding: 0 10px 10px">
            {title}
            <p style="color: #85868B; font-weight: 400; font-size: 12px; margin: 0; padding-top: 5px">SKU: {sku}</p>
        </td>
        <td style="padding: 0 10px 10px">
            {quantity} шт
        </td>
        <td style="padding: 0 10px 10px">
            {barcode}
        </td>
        <td style="padding: 0 10px 10px">
            {warehouse}
        </td>
    </tr>
"""
items_en = """
    <tr>
        <td style="padding: 0 10px 10px">
            <img src="{item_img_url}" alt="item_img_url" width="90px">
        </td>
        <td style="padding: 0 10px 10px">
            {title}
            <p style="color: #85868B; font-weight: 400; font-size: 12px; margin: 0; padding-top: 5px">SKU: {sku}</p>
        </td>
        <td style="padding: 0 10px 10px">
            {quantity} pcs
        </td>
        <td style="padding: 0 10px 10px">
            {barcode}
        </td>
        <td style="padding: 0 10px 10px">
            {warehouse}
        </td>
    </tr>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
