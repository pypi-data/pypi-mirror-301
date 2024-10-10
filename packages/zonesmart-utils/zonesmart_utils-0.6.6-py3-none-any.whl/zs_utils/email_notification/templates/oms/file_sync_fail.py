from zs_utils.email_notification.templates.oms import base

icon = "file_sync_fail_icon.png"

title_ru = "Проблема с синхронизацией данных из файла"
title_en = "Problem synchronizing data from the file"

body_ru = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 40px">
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, сообщаем о возникновении критической ошибки при обработке файла с данными, ранее импортированного в систему.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{source_log_url}" class="button" style="color: #ffffff">
                    Просмотр ошибок
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
                <span style="color: #3BD0BC; font-weight: bold">{first_name}</span>, we report a critical error while processing a data file that was previously imported into the system.
            </td>
        </tr>
        <tr>
            <td align="center" style="padding: 0 0 40px">
                <a href="{source_log_url}" class="button" style="color: #ffffff">
                    View errors
                </a>
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_ru = base.cheers_team_email_ru
cheers_en = base.cheers_team_email_en
