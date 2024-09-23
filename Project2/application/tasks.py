from celery import shared_task
from .models import Category, db, Order
from .mail_service import send_mail
from .models import User, Role
from jinja2 import Template
from .worker import celery_app
from celery.schedules import crontab
import csv


from weasyprint import HTML
def get_pdf(htmlContent, pdfFile):
    HTML(string=htmlContent).write_pdf(pdfFile)


@celery_app.task()
def export_data(categories, reciver_mail, name):
    file_name = f'{name}_details.csv'
    category_header = ['Name', 'Description']

    with open(file_name, 'w', newline='', encoding='utf8') as csvf: 
        cwriter = csv.writer(csvf) 
        cwriter.writerow(category_header) 
        cwriter.writerows(categories)
    send_mail(receiver=reciver_mail, subject="Details ", message= "Please find attached detail csv. Thankyou!", attachment=f'{name}_details.csv')
    return "CSV file exported!"

def get_product_report(template, data, username):
    with open(template) as file_template:
        template = Template(file_template.read())
        html_report = template.render(product_details=data, username=username)
        pdf_report = f"src/{username.split()[0]}.pdf"
        get_pdf(html_report, pdf_report)
        return pdf_report
    


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, daily_reminder.s(), name='DailyReminder')
     
    sender.add_periodic_task(10, shopping_report.s(), name='ShoppingReport')

    # Calls daily_reminder.s() daily.
    sender.add_periodic_task(
        crontab(minute=0, hour=20, day_of_month='*'),
        daily_reminder.s(),
        name = 'Daily reminder everyday @8PM via mail.'
    )
    # Calls shopping_report.s() on 1st day of the month.
    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        shopping_report.s(),
        name = 'Shopping  Report @1st of every month via mail.'
    )

@celery_app.task()
def daily_reminder():
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()
    for user in users:
        send_mail(user.email, subject="Daily Reminder", message="Hey! Visit the Shopping Mart and buy something for your kitchen.")
    return "OK"

    
@celery_app.task()
def shopping_report():
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()    
    for user in users:
        username = user.username
        usermail = user.email
        orders = Order.query.filter_by(user_id=user.id).all()
        order_details = [] 
        for order in orders:
            order_temp = []
            order_temp.append(order.name)
            order_temp.append(order.total)
            order_temp.append(order.quantity)
            order_details.append(order_temp)
            
        file = get_product_report("src/shopping_report.html", order_details, username)
        send_mail(usermail, subject="Shopping Report", message="view your shopping report", attachment=f'{file}')
    
    return "Shopping Report Sent!"


