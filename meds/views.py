from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from robot.models import Persona, Descriptor, Compras
from django.contrib.auth.decorators import login_required
from meds.models import Pais, Region, Prov, Comuna
from meds.forms import Paciente_f
# Create your views here.



def comunas(request):
    pais = Pais.objects.all()
    for p in pais:
        p_dic = {}
        p_dic['name']= p.pais_name
        p_dic['id']= p.pk
        regiones = []
        for r in Region.objects.filter(reg_pais=p).order_by('reg_name'):
            r_dic = {}
            r_dic['name']= r.reg_name
            r_dic['id']= r.pk
            provincias = []
            for pr in Prov.objects.filter(prov_reg=r).order_by('prov_name'):
                pr_dic = {}
                pr_dic['name'] = pr.prov_name
                pr_dic['id'] = pr.pk
                comuna = []
                for c in Comuna.objects.filter(prov_reg=pr).order_by('com_name'):
                    com_dic = {}
                    com_dic['name']=c.com_name
                    com_dic['id']=c.pk
                    comuna.append(com_dic)
                pr_dic['comunas'] = comuna
                provincias.append(pr_dic)
            r_dic['cities']=provincias
            regiones.append(r_dic)
        p_dic['states']=regiones

    if request.method == 'POST':
        form = Paciente_f(request.POST)
        if form.is_valid():
            instance = form.save(commit=False  )
            #print("instance",instance)
            instance.save()
            # process the data in form.cleaned_data as required
            return HttpResponseRedirect('/')
    else:
        form = Paciente_f()
    context = {
    'paises': {"country":[p_dic]},
    'form' : form
    }
    return render(request, 'meds/meds.html', context)


