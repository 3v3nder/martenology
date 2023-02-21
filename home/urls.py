from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("admin", views.admin, name="admin"),
    path("register", views.register, name="register"),
    path("receipt", views.receipt, name="receipt"),
    path("appointment_reg", views.appointment_reg, name="appointment_reg"),
    path("treatment", views.treatment, name="treatment"),
    path("appointment", views.appointment, name="appointment"),
    path("appointmentAdmin", views.appointmentAdmin, name="appointmentAdmin"),
    path("meetTest/<int:meetID>", views.meetTest, name="meetTest"),
    path("sales", views.sales, name="sales"),
    path("calling/", views.calling, name="calling"),
    path("sms", views.sms, name="sms"),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path("logout", views.logout, name="logout"),
    path("prediction", views.prediction, name="prediction"),
    path("invoice", views.invoice, name="invoice"),
    path("salesAdmin", views.salesAdmin, name="salesAdmin"),
]