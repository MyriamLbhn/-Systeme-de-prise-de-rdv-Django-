from django.urls import path 
from . import views

urlpatterns = [
    path('booking/', views.booking, name='booking'),
    path('booking-submit/', views.booking_submit, name='booking_submit'),
    path('user-panel/', views.user_appointment, name='user_appointment'),
    path('client-history/', views.client_history, name='client_history'),
    path('user-update/<int:id>/', views.user_update_appointment, name='user_update_appointment'),
    path('user-update-submit/<int:id>/', views.user_update_submit_appointment, name='user_update_submit_appointment'),
    path('staff-appointment/', views.staff_appointment, name='staff_appointment'),
    path('user-infos/', views.user_infos, name='user_infos'),
    path('historique-staff/', views.staff_history, name='staff_history'),
    path("cancel/<int:appointment_id>/", views.cancel_appointment, name="cancel_appointment"),
    path("cancel-user/<int:appointment_id>/", views.cancel_user_appointment, name="cancel_user_appointment"),
    path('appointments/<int:appointment_id>/notes/', views.appointment_notes, name='appointment_notes'),
    path('appointments/<int:appointment_id>/detail/', views.appointment_detail, name='appointment_detail'),
    path('delete-note/<int:appointment_id>/', views.delete_note, name="delete_note"),
]

