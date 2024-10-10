from zs_utils.email_notification.templates.oms import base

icon = "icon_pricing.png"

title_ru = "Спасибо за регистрацию в ZoneSmart"
title_en = "Thank you for registration in ZoneSmart"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 520px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 15px">
                <span style="color: #3BD0BC; font-weight: bold">{user_first_name}</span>, приветствую Вас!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Меня зовут <span style='color: #3BD0BC; font-weight: bold'>{manager_first_name}</span>, и я менеджер пробного периода в компании <span style='color: #3BD0BC; font-weight: bold'>ZoneSmart</span>, рад знакомству!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Предполагаю, что регистрация в платформе для мульти-канальных продаж - уже не первое Ваше успешное решение за сегодняшний день.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Для того, чтобы в этом убедиться за время бесплатного пробного периода (который, кстати, длится целых 14 дней), я буду рад помогать Вам в процессе освоения нашего сервиса. Периодически я буду присылать рекомендации по работе на почту – они помогут сделать наше взаимодействие эффективнее.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                Перед тем, как Вы <a href='https://zonesmart.zendesk.com/hc/ru/categories/4407691046033' style='color: #3BD0BC; font-weight: bold'>подключите первый аккаунт на маркетплейсе</a> к единому личному кабинету и начнете покорять новые каналы продаж, я бы посоветовал определить сценарий использования сервиса (их может быть <a href='https://zonesmart.zendesk.com/hc/ru/articles/4410033986577' style='color: #3BD0BC; font-weight: bold'>несколько одновременно</a>):
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                1. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4410033986577" style="color: #3BD0BC; font-weight: bold">Интеграция маркетплейса(-ов) с сайтом или системой товароучета.</a>
                <p style="margin: 0px">
                    Позволит массово адаптировать и разместить каталог товаров с сайта на одном или нескольких маркетплейсах. Товарные остатки синхронизируются автоматически, а заказы со всех каналов продаж – выгружаются в Вашу систему.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                2. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4410491540113" style="color: #3BD0BC; font-weight: bold">Интеграция аккаунтов на нескольких маркетплейсах между собой.</a>
                <p style="margin: 0px">
                    Подойдет для быстрой синхронизации каталога между маркетплейсами и автономного обновления информации об остатках.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                3. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4411155259537" style="color: #3BD0BC; font-weight: bold">Система управления заказами (OMS) для FBS / DBS / RFBS моделей.</a>
                <p style="margin: 0px">
                    Заказы со всех подключенных каналов продаж собираются в одном окне, а встроенные интеграции с популярными курьерскими службами не заставят тратить лишнее время на покупку почтового лейбла на стороннем ресурсе.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                4. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4411546464785" style="color: #3BD0BC; font-weight: bold">Система управления клиентской базой (CRM).</a>
                <p style="margin: 0px">
                    Платформа осуществляет сбор данных о покупателях со всех маркетплейсов в едином личном кабинете, упрощая анализ клиентской базы и статистики продаж.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                В процессе работы, пожалуйста, не забывайте обращаться к нам по любым возникающим вопросам, а также получать удовольствие.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                Желаю успехов!
            </td>
        </tr>
        </tbody>
    </table>
"""

body_en = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 520px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 15px">
                <span style="color: #3BD0BC; font-weight: bold">{user_first_name}</span>, greetings!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                My name is <span style='color: #3BD0BC; font-weight: bold'>{manager_first_name}</span> and I'm a trial manager at <span style='color: #3BD0BC; font-weight: bold'>ZoneSmart</span>, nice to meet you!
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                I assume that registration in the platform for multi-channel sales is not your first successful decision to date.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                In order to make sure of this during the free trial period (which, by the way, lasts for 14 days), I will be happy to help you in the process of mastering our service. From time to time I will send recommendations on work by email - they will help make our interaction more efficient.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                Before You <a href='https://zonesmart.zendesk.com/hc/ru/categories/4407691046033' style='color: #3BD0BC; font-weight: bold'>connect the first account on the marketplace</a> to a single personal account and start conquering new sales channels, I would advise you to determine the use case for the service (they can be <a href='https://zonesmart.zendesk .com/hc/en/articles/4410033986577' style='color: #3BD0BC; font-weight: bold'>several at the same time</a>):
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                1. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4410033986577" style="color: #3BD0BC; font-weight: bold">Integration of the marketplace(s) with the website or inventory system.</a>
                <p style="margin: 0px">
                    It will allow you to massively adapt and place a catalog of products from the site on one or more marketplaces. Product stocks are synchronized automatically, and orders from all sales channels are uploaded to your system.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                2. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4410491540113" style="color: #3BD0BC; font-weight: bold">Integration of accounts on several marketplaces among themselves.</a>
                <p style="margin: 0px">
                    Suitable for quick synchronization of the catalog between marketplaces and offline updating of information about the stocks.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                3. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4411155259537" style="color: #3BD0BC; font-weight: bold">Order Management System (OMS) for FBS / DBS / RFBS models.</a>
                <p style="margin: 0px">
                    Orders from all connected sales channels are collected in one window, and built-in integrations with popular courier services will not make you spend extra time buying a mail label on a third-party resource.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 10px">
                4. <a href="https://zonesmart.zendesk.com/hc/ru/articles/4411546464785" style="color: #3BD0BC; font-weight: bold">Customer base management system (CRM).</a>
                <p style="margin: 0px">
                    The platform collects customer data from all marketplaces in a single personal account, simplifying the analysis of the customer base and sales statistics.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                In the process of work, please do not forget to contact us for any questions that arise, and also have fun.
            </td>
        </tr>
        <tr>
            <td style="padding: 0 0 15px">
                I wish you success!
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_manager_email_ru
cheers_en = base.cheers_manager_email_en
