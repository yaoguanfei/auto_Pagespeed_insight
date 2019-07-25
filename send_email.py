from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

# MTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件


if __name__ == '__main__':
    # 格式化一个邮件地址
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


    # # 使用SMTP 发送文件
    # # 输入Email地址和口令:
    # from_addr = input('From: ')
    # password = input('Password: ')
    # # 输入收件人地址:
    # to_addr = input('To: ')
    # # 输入SMTP服务器地址:
    # # 发送邮件服务器：smtp.exmail.qq.com (端口 25)
    # smtp_server = input('SMTP server: ')
    #

    # 固定便于测试
    from_addr = "yaoguanfei@youmi.net"
    password = "Kxmyt970205"
    to_addr = "zhangchuzhao@youmi.net"
    smtp_server = "smtp.exmail.qq.com"

    # 使用emai-MIMEtext 构建邮件正文
    #  邮件主题、如何显示发件人、收件人等信息并不是通过SMTP协议发给MTA，而是包含在发给MTA的文本中的，所以，我们必须把From、To和Subject添加到MIMEText中
    # 构造MIMEText对象时，第一个参数就是邮件正文，第二个参数是MIME的subtype，传入'plain'表示纯文本，最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性。
    # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    # 邮件对象:
    msg = MIMEMultipart()
    msg['From'] = _format_addr(from_addr)
    msg['To'] = _format_addr(to_addr)
    msg['Subject'] = Header('有米Web产品加载性能排行榜', 'utf-8').encode()

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open('/home/youmi/图片/insight_result.png',
              'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('image', 'png', filename='test.png')
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename='test.png')
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

        # 读取html文件内容
        with open("email_text.html") as f:
            s = f.read()
        # 构造html:
        html_file = s

msg.attach(MIMEText(html_file, 'html', 'utf-8'))

server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
