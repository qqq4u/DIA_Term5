from django.urls import path

from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/parkings/search/', search_parking),  # GET
    path('api/parkings/<int:parking_id>/', get_parking_by_id),  # GET
    path('api/parkings/<int:parking_id>/update/', update_parking),  # PUT
    path('api/parkings/<int:parking_id>/delete/', delete_parking),  # DELETE
    path('api/parkings/create/', create_parking),  # POST
    path('api/parkings/<int:parking_id>/add_to_ticket/', add_parking_to_ticket),  # POST
    path('api/parkings/<int:parking_id>/image/', get_parking_image),  # GET
    path('api/parkings/<int:parking_id>/update_image/', update_parking_image),  # PUT

    # Набор методов для заявок
    path('api/tickets/', get_tickets),  # GET
    path('api/tickets/<int:ticket_id>/', get_ticket_by_id),  # GET
    path('api/tickets/<int:ticket_id>/update/', update_ticket),  # PUT
    path('api/tickets/<int:ticket_id>/update_status_user/', update_status_user),  # PUT
    path('api/tickets/<int:ticket_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/tickets/<int:ticket_id>/delete/', delete_ticket),  # DELETE
    path('api/tickets/<int:ticket_id>/delete_parking/<int:parking_id>/', delete_parking_from_ticket),  # DELETE
]