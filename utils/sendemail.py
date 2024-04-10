from django.core.mail import EmailMultiAlternatives
from celebration import settings
from user.models import UserInfo


def send_email(identity):
    recipient = UserInfo.objects.filter(roles=2)
    recipient_list = [i.email for i in recipient if i.email]
    subject = f'校友回归小程序有新的{identity}认证啦'
    message = '爱特工作室'
    html_content = """
<div style="box-sizing: border-box; width: 98%; margin: 0 auto; max-width: 508px; background-color: #FFFFFF; border: 1px solid #f6f6f6; box-shadow: 0px 0 10px rgba(0, 0, 0, 0.08); border-radius: 8px;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="main-table_zZLU" style="width:100%;height:100%"></table>
    <table align="center" border="0" cellpadding="0" cellspacing="0" style="max-width: 508px; width: 100%; margin: 0 auto;">
        <tbody>
            <tr>
                <td>
                    <div style="text-align: center; width: 100%; overflow: hidden; height: 100%; border-top-left-radius: 8px; border-top-right-radius: 8px;">
                        <img style="max-width: 100%;" src="https://picture.daoxuan.cc/ouchelper/3c1ee96af66111eda22a005056c00008.png">
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0">
        <tbody>
            <tr>
                <td>
                    <div style="text-align: center; font-size: 18px; font-weight: bold; margin-top: 20px;">认证通知</div>
                </td>
            </tr>
        </tbody>
    </table>
    <table align="center" border="0" cellpadding="0" cellspacing="0">
        <tbody>
            <tr>
                <td>
                    <div style="text-align: center; font-size: 16px; margin-top: 20px;">有新的{}进行认证</div>
                    <div style="text-align: center; font-size: 16px; margin-top: 10px;">请您及时处理相关事宜。</div>
                </td>
            </tr>
        </tbody>
    </table>
    <p class="normal-font_oArV" style="margin:0 auto; overflow-wrap: break-word; word-break: break-word; text-align:left; width:90%; font-family:SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-size:14px; line-height:20px; font-weight:normal; color:#000000;"></p>
    <table align="center" border="0" cellpadding="0" cellspacing="0" class="logo-table_NOgq" style="width: 100%;">
        <tbody>
            <tr>
                <td style="text-align: center;">
                    <div style="max-width: 508px; margin: 0 auto; padding: 15px 24px 28px;">
                        <div style="font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-size: 12px; line-height: 17px; text-align: center; color: #7D7D7D;">
                            本小程序由爱特工作室开发<br> - 如果您怀疑自己收到了诈骗信息，请立即联系客服
                        </div>
                        <div style="margin: 14px auto 12px;">
                            <img src="https://static.coinall.ltd/cdn/oksupport/headImg/20221117/1668687253371.png" style="width: 14px; height: 14px; vertical-align: middle;">
                            <span style="font-size: 14px; font-family: SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; font-weight: 500; color: #000000; opacity: 0.8;">期待与您保持联系</span>
                        </div>
                        <div style="font-size: 11px; font-family: HarmonyOS Sans, SF Pro Text, SF Pro Icons, robot, Helvetica Neue, Helvetica, Arial, sans-serif; color: #7d7d7d; text-align: center; line-height: 17px;">
                            感谢您选择爱特工作室<br> 如果有任何问题，疑虑或建议，请联系爱特工作室客服
                        </div>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</div>""".format(identity)
    from_email = settings.EMAIL_HOST_USER
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list)
    if html_content:
        mail.attach_alternative(html_content, 'text/html')

    return mail.send()
