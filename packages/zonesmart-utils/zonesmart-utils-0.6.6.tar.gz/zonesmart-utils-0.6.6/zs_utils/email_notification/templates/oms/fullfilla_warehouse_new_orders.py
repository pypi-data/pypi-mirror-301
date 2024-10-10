from zs_utils.email_notification.templates.oms import base

icon = "new_message_icon.png"

subject_en = "You have ZoneSmart orders to ship today"

title_en = "You have ZoneSmart orders to ship today"

body_en = """
    <table border="0" cellpadding="0" cellspacing="0" width="100%" align="center" style="color: #515151; box-sizing:border-box;max-width: 420px;width:100%; font-size: 13px;line-height: 149%; padding: 0 20px">
        <tbody>
        <tr>
            <td style="padding: 0 0 10px">
                As for {current_time} there are some new orders to process, check them out here: https://app.zonesmart.com/admin/warehouse/shipments
            </td>
        </tr>
        </tbody>
    </table>
"""

cheers_en = base.cheers_team_email_en
