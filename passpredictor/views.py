from django.shortcuts import render
from pandas.io import json
from .models.svm import Predictor
from .models.student_infos import StudentInfos
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from rest_framework.views import APIView, View
from django.core import serializers

class call_model(APIView):
    def post(self, request):
        predictor = Predictor()
        
        if request.method == 'POST':
            predictor = Predictor()
            provided = request.data
            evaluation= predictor.predict(data=provided)
            provided['G3']=evaluation[0]
            m = StudentInfos(**provided)
            m.save()
            return JsonResponse({'predict':  'passed' if provided['G3']==1 else 'failed'})
        else:
            return HttpResponseForbidden({'error': 'method not allowed'})

class get_predictions(View):
    def get(self, request):
        
        if request.method == 'GET':
            qs = StudentInfos.objects.all().__dict__()
            qs_json = serializers.serialize('json', qs)
            return HttpResponse(qs_json, content_type='application/json')
        else:
            return HttpResponseForbidden({'error': 'method not allowed'})
