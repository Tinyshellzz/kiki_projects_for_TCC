from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from kiki_app.services import myMcstatus


# Create your views here.
def home(request):
    return render(request, "base.html")

def mcstatus(request):
    system_status = myMcstatus.get_system_status()
    mc_status = myMcstatus.get_mc_status()
    tps = myMcstatus.get_tps()
    all_status = {**mc_status, 'tps': tps, **system_status}
    return JsonResponse(all_status)

def mcstatusOnline(request):
    online = myMcstatus.get_online_players()
    return JsonResponse(online)

def mcstatusTps(request):
    tps = myMcstatus.get_tps()
    return HttpResponse(tps)

def mcstatusSystem(request):
    system_status = myMcstatus.get_system_status()
    return JsonResponse(system_status)