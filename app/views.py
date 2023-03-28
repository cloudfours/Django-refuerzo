from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,reverse
from django.views.generic import * 
from app.models import Question,Choices
from django.utils import timezone
# Create your views here.


# def index(request) :
#     question_list=Question.objects.all()
#     # data={
#     #     'question_list': question_list,
#     # }
   
#     return render(request,'app/index.html', {
#         'question_list': question_list,
#     })


# def detail(request, id: int):
#     """
#     funcion dar a detalle lo que se espera o lo que se retorna

#     Args:
#         request (_type_): espera la peticion
#         id (int): busca por su di
#     """
#     question = get_object_or_404(Question, pk=id)
#     return render(request, 'app/detail.html',{'question':question})


# def results(request, id: int):
#     question=get_object_or_404(Question, pk=id)
    
#     """
#     retorna los resultados de la pregunt numero uno

#     Args:
#         request (_type_): espera una peticion
#         id (int): busca por id
#     """
#     return render(request,'app/results.html',{'question':question})

class IndexView(ListView):
    template_name="app/index.html"
    context_object_name="question_list"
    def get_queryset(self):
        """
        retorna las ultimas preguntas
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
class DetailView(DetailView):
    model=Question
    template_name = "app/detail.html"
    def get_queryset(self):
        """
        no perimitira que se muestras las preguntas del futuro

        Returns:
            solo debe retornar las de hoy
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultView(DetailView):
    model=Question
    template_name = "app/results.html"
    

def vote(request, id: int):
    question =  get_object_or_404(Question, pk=id)
    """espera los votos

    Args:
        request (_type_): peticion
        id (int): busca por id
    """ 
    try:
       select_choice = question.question_choice.get(pk=request.POST['choice'])
    except (KeyError,Choices.DoesNotExist):
        return render(request,'app/detail.html',{'question':question, 'error_message':'no elegiste una respuesta'}
                      )
    else:
        select_choice.votes+=1
        select_choice.save()
        return HttpResponseRedirect(reverse('app:results',args=(question.id,)))
