from django.test import TestCase
import datetime
from django.utils import timezone
from django.shortcuts import reverse

from app.views import IndexView
from .models import *
# Create your tests here.


class QuestionsModelTest(TestCase):
    def setUp(self):
        self.future_question = Question(
            question_text="¿cual es el mejore profe?")

    def test_was_published_recently_future_questions(self):
        """
        deber retornar false para cuando las preguntas se vean en el futuro
        """
        time = timezone.now() + datetime.timedelta(days=30)
        self.future_question.pub_date=time
        self.assertIs(self.future_question.was_published_recently(), False)

    def test_was_published_present_recently(self):
        """
        debe retornar false si es pasado o futuro dentro de las 23 horas
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        self.future_question.pub_date = time
        self.assertIs(self.future_question.present_published_recently(), True)

    def test_was_published_past_recently(self):
        """
        debe estar devolverl false si esta durante las 23  y 59 minutos y si es futuro es decir mas de 23 horas
        """
        time = timezone.now() - datetime.timedelta(days=1, minutes=1)
        self.future_question.pub_date = time
        self.assertIs(self.future_question.past_published_recently(), False)
        
def create_question(question_text="escribe pregunta",days=0,hours=0,minutes=0,seconds=0):
    time = timezone.now() + datetime.timedelta(days=days,hours=hours,minutes=minutes,seconds=seconds)
    return Question.objects.create(question_text=question_text, pub_date=time)
        
class QuestionIndexViews(TestCase):
    def test_no_question(self):
        response=self.client.get(reverse("app:index"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,"no hay preguntas")
        self.assertQuerysetEqual(response.context['question_list'],[])
       
    def test_future_question(self):
        """preguntas del futuro que no sera desplegadas
        """
        create_question("¿perro?",21,2,50,15)
        response=self.client.get(
            reverse('app:index')
        )
        self.assertContains(response,"no hay preguntas")
        self.assertQuerysetEqual(response.context['question_list'],[])
    def test_past_question(self):
        """
        que obtenga las preguntas del pasado
        """
        question=create_question("¿perro?",-10,2,50,15)
        response=self.client.get(
            reverse('app:index')
        )
   
        self.assertQuerysetEqual(response.context['question_list'],[question])
        
    def test_future_question_and_past_question(self):
        """
        si hay preguntas del futuro y pasadao, solamente debe desplegarse las preguntas del pasado
        """
        past_question=create_question("past_question",days=-10,hours=2,minutes=30,seconds=30)
        future_question=create_question("future_question",days=10,hours=3,minutes=20,seconds=20)
        response=self.client.get(reverse('app:index'))
        self.assertQuerysetEqual(response.context['question_list'],[past_question])
    def test_two_past_question(self):
        """
        si hay preguntas del futuro y pasadao, solamente debe desplegarse las preguntas del pasado
        """
        past_question1=create_question("past_question1",days=-10,hours=2,minutes=30,seconds=30)
        past_question2=create_question("past_question2",days=-30,hours=3,minutes=20,seconds=20)
        response=self.client.get(reverse('app:index'))
        self.assertQuerysetEqual(response.context['question_list'],[past_question1,past_question2])
    def test_two_future_question(self):
        """
        si hay preguntas del futuro y pasadao, solamente debe desplegarse las preguntas del pasado
        """
        future_question1=create_question("future_question1",days=20,hours=2,minutes=30,seconds=30)
        future_question2=create_question("future_question2",days=30,hours=3,minutes=20,seconds=20)
        response=self.client.get(reverse('app:index'))
        self.assertQuerysetEqual(response.context['question_list'],[])

class DetailTestView(TestCase):
    def test_future_question(self):
        """
        debe de retonar 404 si busca preguntas del futuro
        
        """
        future_question=create_question('¿veo el futuro?',30,1,1,20)
        response=self.client.get(reverse("app:detail",args=(future_question.id,)))
        self.assertEqual(response.status_code,404)
        
    def test_past_question(self):
        
        """
        debe mostrar las preguntas del pasado 
        """
        past_question=create_question('¿veo el pasado?',-30,6,1,20)
        response=self.client.get(reverse("app:detail",args=(past_question.id,)))
        self.assertContains(response,past_question.question_text)
        
class ResultViewTest(TestCase):
    def test_save(self):
        question=Question(question_text="pregunta",pub_date=timezone.now()) 
        with self.assertRaises(Exception):
            question.save()
            
        