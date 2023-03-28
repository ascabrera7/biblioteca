from django.views.generic import TemplateView, ListView, DeleteView
from django.shortcuts import render, redirect
from core.base.models import Eventos, Libro
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.

class IndexView(TemplateView):
    
    template_name = 'index.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True)
        return queryset
    
# class BibliotecaView(ListView):

#     model = Libro
#     paginate_by = 6
#     template_name = 'biblioteca.html'

#     def get_queryset(self):
#         queryset = self.model.objects.filter(estado = True,cantidad__gte = 1)
#         return queryset
    
    
#     def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             return context
    
# def search(request):
#         template_name = "biblioteca.html"
#         buscar = request.GET["buscar"]
#         queryset = Libro.objects.filter(titulo__icontains=buscar)
#         context = {'queryset':queryset}
#         return render(request, template_name, context)

class DetalleLibro(DeleteView):
    model = Libro
    template_name = 'librosDetalle.html'

    def get(self,request,*args,**kwargs):
        if self.get_object().cantidad > 0:
            return render(request,self.template_name,{'object':self.get_object()})
        return redirect('principal:biblioteca')
    
class EventosView(ListView):

    model = Eventos
    paginate_by = 3
    template_name = 'eventos.html'
    
    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True)
        return queryset
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            return context

class HistoriaView(TemplateView):

    template_name = 'historia.html'


def libros(request):
    queryset = request.GET.get("buscar")
    Libros = Libro.objects.filter(estado = True)
    if queryset:
        Libros = Libro.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset)
        ).distinct()

    paginator = Paginator(Libros,9)
    page = request.GET.get('page')
    Libros = paginator.get_page(page)
    return render(request, 'biblioteca.html',{'Libros':Libros})



