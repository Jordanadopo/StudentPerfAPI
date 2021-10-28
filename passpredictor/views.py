from django.shortcuts import render
from pandas.io import json
from .models.svm import Predictor
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.views import APIView

class call_model(APIView):
    def post(self, request):
        predictor = Predictor()
        
        if request.method == 'POST':
            predictor = Predictor()
            
            evaluation= predictor.predict(request.data)
            
            return JsonResponse({'predict':  'passed' if evaluation[0]==1 else 'failed'})
        else:
            return HttpResponseForbidden({'error': 'method not allowed'})
