from django.contrib import admin
from django.urls import path, include
from .views import DebtPassInquiryAPIView, NewsList, NewsDetails, CreateNews, NotificationListAPIView, PassInquiryAPIView, PlateCreateApiView, PlateDeleteAPIView, PlateListAPIView, PlateListDetailApiView,PlateUpdateDetailsApiView, UpdateNews, NotificationCreateApiView, NotificationDetailAPIView,NotificationDeleteApiView,NotificationUpdateApiView
app_name = 'kmo_api'

urlpatterns = [
    path('news/', NewsList.as_view(), name="listnews"),
    path('news/<int:pk>/', NewsDetails.as_view(), name="detailnews"),
    path('news/create/', CreateNews.as_view(), name="createnews"),
    path('news/update/<int:pk>/', UpdateNews.as_view(), name="updatenews"),
    path('notifications/',NotificationListAPIView.as_view(), name="notif-list"),
    path('notifications/<int:pk>/', NotificationDetailAPIView.as_view(),name="notif-detail"),
    path('notifications/update/<int:pk>/',NotificationUpdateApiView.as_view(), name="notif-update"),
    path('notifications/create',NotificationCreateApiView.as_view(), name="notif-create"),
    path('notifications/delete/<int:pk>/',NotificationDeleteApiView.as_view(), name="notif-delete"),
    path('plates/',PlateListAPIView.as_view(), name="plates-list"),
    path('plates/<int:pk>/', PlateListDetailApiView.as_view(),name="plate-detail"),
    path('plates/update/<int:pk>/',PlateUpdateDetailsApiView.as_view(),name="plate-update"),
    path('plates/create',PlateCreateApiView.as_view(),name="plate-create"),
    path('plates/delete/<int:pk>/',PlateDeleteAPIView.as_view(), name="plate-delete"),
    path('passes/<str:plate>/',PassInquiryAPIView.as_view(),name='pass_inquiry'),
    path('debt/<str:plate>/',DebtPassInquiryAPIView.as_view(),name='debt_inquiry')
    # path('news/delete/<int:pk>/',DeleteNews.as_view(),name="deletenews"),
]
