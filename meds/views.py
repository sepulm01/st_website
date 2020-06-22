from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from meds.models import Pais, Region, Prov, Comuna, Paciente, Contacto
from meds.forms import Paciente_f
from django.contrib import messages

# Create your views here.

def comunas():
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
    return p_dic

def paciente_new(request):
    p_dic=comunas()
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

def paciente_upd(request, id):
    p_dic=comunas()
    pac= get_object_or_404(Paciente, pk=id)
    form = Paciente_f(request.POST or None, instance=pac)
    if form.is_valid():
        instance = form.save(commit=False  )
        #print("instance",instance)
        instance.save()
        messages.success(request, "You successfully updated the post")
        context = {
        'paises': {"country":[p_dic]},
        'form' : form
        }
        return render(request, 'meds/meds.html', context)
    else:
        messages.success(request, "Error")
    context = {
    'paises': {"country":[p_dic]},
    'form' : form
    }
    return render(request, 'meds/meds.html', context)


def contactos(request, id):
    persona = Paciente.objects.get(pk=id)
    ContInlineFormSet = inlineformset_factory(Paciente, Contacto, fields=('nombre','fono','parentesco'), extra=1)
    if request.method == "POST":
        formset = ContInlineFormSet(request.POST, request.FILES, instance=persona)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect('/meds/paciente/%s/' % id)
    else:
        formset = ContInlineFormSet(instance=persona)
    return render(request, 'meds/meds_plus.html', {'formset': formset})

def lista_paci(request):
    if request.method == 'GET': 
        all_items = Paciente.objects.all()
        d = []
        for e in all_items:
            #print(type(e),e , "\n")
            d.append({
                "id":e.pk,
                "nombre":e.nombre,
                "apellido":e.apellido, 
                "rut":e.rut,  
                "edad":e.edad, 

                })
        print(d)   
        return render(request, "meds/lista.html", {'all_items':d} )