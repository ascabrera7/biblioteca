from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.base.forms import BeneficiarioForm
from core.base.models import Beneficiario



class BeneficiarioView(TemplateView):
    model = Beneficiario
    template_name = 'beneficiario/listado.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Beneficiario.objects.all():
                    data.append(i.toJSON())
                
            elif action == 'add':
                ben = Beneficiario()
                ben.nombres = request.POST['nombres']
                ben.apellidos = request.POST['apellidos']
                ben.cedula = request.POST['cedula']
                ben.cumpleaños = request.POST['cumpleaños']
                ben.direccion = request.POST['direccion']
                ben.sexo = request.POST['sexo']
                ben.save()
            elif action == 'edit':
                ben = Beneficiario.objects.get(pk=request.POST['id'])
                ben.nombres = request.POST['nombres']
                ben.apellidos = request.POST['apellidos']
                ben.cedula = request.POST['cedula']
                ben.cumpleaños = request.POST['cumpleaños']
                ben.direccion = request.POST['direccion']
                ben.sexo = request.POST['sexo']
                ben.save()
            elif action == 'delete':
                ben = Beneficiario.objects.get(pk=request.POST['id'])
                ben.delete()


            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Beneficiario'
        context['list_url'] = reverse_lazy('base:beneficiario')
        context['entity'] = 'Beneficiario'
        context['form'] = BeneficiarioForm()
        context['entidad'] = 'Beneficiario'
        return context