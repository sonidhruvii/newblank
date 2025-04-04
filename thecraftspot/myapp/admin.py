from django.contrib import admin
from . models import login,Category,product,cartable,contact_us,order
from django.http import HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.core.mail import send_mail


def export_to_pdf(modeladmin, request, queryset):

# Create a new PDF

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment;filename="report.pdf"'
        # Generate the report using ReportLab
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        # Define the style for the table
        style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ])
        # Create the table headers
        # headers = ['LOGIN_ID','FINALTOTAL','PAY_MODE','NAME','ADDRESS','TIMESTAMP']
        # headers = ['LOGIN_ID','FINALTOTAL','PAY_MODE','ADDRESS','TIMESTAMP']
        headers = ['NAME','FINALTOTAL','PAY_MODE','ADDRESS','TIMESTAMP']
        # Create the table data
        data = []
        for obj in queryset:
                # data.append([obj.LOGIN_ID, obj.FINALTOTAL,obj.PAY_MODE,obj.NAME,obj.ADDRESS,obj.TIMESTAMP])
                # data.append([obj.LOGIN_ID, obj.FINALTOTAL,obj.PAY_MODE,obj.ADDRESS,obj.TIMESTAMP])
                data.append([obj.NAME, obj.FINALTOTAL,obj.PAY_MODE,obj.ADDRESS,obj.TIMESTAMP])
        # Create the table
                t = Table([headers] + data, style=style)
        # Add the table to the elements array
                elements.append(t)
        # Build the PDF document
                doc.build(elements)

        return response

export_to_pdf.short_description = "Export to PDF"





@admin.action(description="Mark selected orders as Delivered and Notify User")
def mark_as_delivered(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = "Delivered"
        obj.save()

        try:
            email = obj.LOGIN_ID.EMAIL_ID  # Make sure this field exists in your related model

            send_mail(
                subject=f"Your order #{obj.id} has been delivered",
                message="Thank you for shopping with The Craft Spot! Your order has been delivered.",
                from_email="krushanuinfolabz@gmail.com",  # Must match your EMAIL_HOST_USER
                recipient_list=[email],
                fail_silently=False
            )

            modeladmin.message_user(request, f"Order #{obj.id} marked as delivered and email sent.")

        except Exception as e:
            modeladmin.message_user(request, f"Failed to send email for Order #{obj.id}: {e}", level="error")



# Register your models here.
class showlogin(admin.ModelAdmin):
    list_display =['U_NAME','EMAIL_ID','PHONE_NO','PASSWORD','U_ADDRESS','U_GENDER','STATUS']
# ,'ROLE_TYPE'
admin.site.register(login,showlogin)


class showcategory(admin.ModelAdmin):
    list_display =['CAT_NAME','category_photo']
# ,'CAT_DESC'
admin.site.register(Category,showcategory)

class showproduct(admin.ModelAdmin):
    list_display =['id','ITEM_NAME','ITEM_PRICE','ITEM_DESC','product_photo']
# 'CAT_ID',,'STATUS'
admin.site.register(product,showproduct)


class showcart(admin.ModelAdmin):
    list_display =['LOGIN_ID','PROD_ID','QUANTITY','Totalamount','Cart_STATUS','ORDER_ID','SHIPPING_CHARGE']

admin.site.register(cartable,showcart)


class showcontact_us(admin.ModelAdmin):
    list_display =['Subject','U_NAME','Email_ID','Phone_NO','MESSAGE','TIMESTAMP']

admin.site.register(contact_us,showcontact_us)

class ShowOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'LOGIN_ID', 'FINALTOTAL', 'PAY_MODE', 'NAME', 'ADDRESS', 'TIMESTAMP']
    list_filter = ['TIMESTAMP']
    actions = [export_to_pdf,mark_as_delivered]
    


admin.site.register(order, ShowOrderAdmin)