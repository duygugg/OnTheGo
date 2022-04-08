from rest_framework import generics
from core.models import News, Notification, Plate
from .serializers import NewsSerializer, NotificationSerializer, PlateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS, BasePermission, AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import Http404
from django.shortcuts import get_object_or_404
from kmo_api.permissions import IsStaffOrReadOnly
from zeep import Client
from django.http import HttpResponse, JsonResponse
from lxml import etree
import datetime
import json


class PassInquiryAPIView(APIView):
    def get(self, request, plate):
        client = Client(
            'https://gecisavrupa.kuzeymarmaraotoyolu.com:8443/WebService.asmx?wsdl')
        client_asya = Client(
            'https://gecisasya.kuzeymarmaraotoyolu.com/WebService.asmx?wsdl')

        current_date = datetime.date.today()
        start_date = datetime.date(
            current_date.year, current_date.month, current_date.day-2)

        results = client.service.aracaAitGecisSorgula(
            kullaniciAdi='kmoavrupauser', sifre='Kmo*?918273', ipAdresi='?',
            tcKimlikNo='?', plaka=plate, aracSahiplikBaslangicTarihi='2021-03-04',
            sorguBaslangicTarihi=str(start_date), sorguBitisTarihi=str(current_date)
        )

        results_asya = client_asya.service.aracaAitGecisSorgula(
            kullaniciAdi='kmoasyauser', sifre='Kmo*?918273', ipAdresi='?',
            tcKimlikNo='?', plaka=plate, aracSahiplikBaslangicTarihi='2021-03-04',
            sorguBaslangicTarihi=str(start_date), sorguBitisTarihi=str(current_date)
        )

        results = results['gecisListesi']['gecisBilgisi']
        results_asya = results_asya['gecisListesi']['gecisBilgisi']

        europe_results = [{'id': id, "plate_no":plate, 'entry_station': x.girisIstasyonu, 'exit_date': x.cikisZamani,
                           'exit_station': x.cikisIstasyonu, 'class': x.aracSinifi, 'pass_cost': x.gecisUcreti,} for id, x in enumerate(results)]

        asia_results = [{'id': id ,"plate_no":plate, 'entry_station': x.girisIstasyonu, 'exit_date': x.cikisZamani,
                         'exit_station': x.cikisIstasyonu, 'class': x.aracSinifi, 'pass_cost': x.gecisUcreti, } for id, x in enumerate(results_asya)]

        return Response([{"Avrupa": europe_results}, {"Asya": asia_results}])


class DebtPassInquiryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, plate):
        client = Client(
            'https://gecisavrupa.kuzeymarmaraotoyolu.com:8443/WebService.asmx?wsdl')
        client_asya = Client(
            'https://gecisasya.kuzeymarmaraotoyolu.com/WebService.asmx?wsdl')

        current_date = datetime.date.today()
        start_date = datetime.date(
            current_date.year-1, current_date.month, current_date.day)

        results = client.service.aracaAitIhlalSorgula(
            kullaniciAdi='kmoavrupauser', sifre='Kmo*?918273', ipAdresi='?',
            tcKimlikNo='?', plaka=plate, aracSahiplikBaslangicTarihi='2022-02-18',
        )

        results_asya = client_asya.service.aracaAitIhlalSorgula(
            kullaniciAdi='kmoasyauser', sifre='Kmo*?918273', ipAdresi='?',
            tcKimlikNo='?', plaka=plate, aracSahiplikBaslangicTarihi='2022-02-18',
        )

        results = results['ihlalListesi']['ihlalBilgisi']
        results_asya = results_asya['ihlalListesi']['ihlalBilgisi']

        europe_results = [{'id': id, 'plate_no': x.plaka, 'last_payment_date': x.cezasizSonOdemeTarihi, 'entry_station': x.girisIstasyonu, 'exit_date': x.cikisZamani,
                           'exit_station': x.cikisIstasyonu, 'class': x.aracSinifi, 'pass_cost': x.gecisUcreti, 'debt_fee': x.cezaTutari, 'total_cost': x.odenecekTutar} for id, x in enumerate(results)]

        asia_results = [{'id': id, 'plate_no': x.plaka, 'last_payment_date': x.cezasizSonOdemeTarihi, 'entry_station': x.girisIstasyonu, 'exit_date': x.cikisZamani,
                         'exit_station': x.cikisIstasyonu, 'class': x.aracSinifi, 'pass_cost': x.gecisUcreti, 'debt_fee': x.cezaTutari, 'total_cost': x.odenecekTutar} for id, x in enumerate(results_asya)]

        return Response([{"Avrupa": europe_results}, {"Asya": asia_results}])


class PlateListAPIView(generics.ListAPIView):

    serializer_class = PlateSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Plate.objects.all()
        if self.request.user.is_authenticated:
            print(self.request.user)
            queryset = Plate.objects.filter(user=self.request.user)

        return queryset


class PlateListDetailApiView(generics.RetrieveAPIView):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    permission_classes = [AllowAny]


class PlateCreateApiView(generics.ListCreateAPIView):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    permission_classes = [AllowAny]


class PlateUpdateDetailsApiView(generics.RetrieveUpdateAPIView):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    permission_classes = [AllowAny]


class PlateDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    permission_classes = [AllowAny]


class NotificationListAPIView(generics.ListAPIView):

    queryset = Notification.notifobjects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class NotificationCreateApiView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsStaffOrReadOnly]


class NotificationUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class NotificationDeleteApiView(generics.RetrieveDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]


class NotificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.notifobjects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsStaffOrReadOnly]


class NewsList(generics.ListAPIView):
    queryset = News.newsobjects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]


class NewsDetails(generics.RetrieveAPIView):
    queryset = News.newsobjects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]


class CreateNews(generics.ListCreateAPIView):
    permission_classes = [IsStaffOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class UpdateNews(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsStaffOrReadOnly]
