from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, View

from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm, TestForm
from ..models import Quiz, Student, TakenQuiz, User
from ..views import compilepython
import math,re

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
})

default_py_code ="""import sys
import os
if __name__ == "__main__":
    print ("Hello Python World!!")
"""

class Test(View):
    template_name   =   'classroom/students/test_code.html'
    form_class      =   TestForm

    def get(self,request):
        form=self.form_class(None)
        return render(request,'classroom/students/test_code.html',{'form':form})

    def post(self,request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
            code=request.POST['code']
            run=compilepython.RunPyCode(code)
            rescompil, resrun=run.run_py_code()
            resrun  =resrun
            rescomp =rescompil
            if not resrun:
                resrun = 'No result!'
            return render (request,'classroom/students/test_code.html', {'code':code,'resrun':resrun,'rescomp':rescomp})
        else:
            code = default_py_code
            resrun = 'No result!'
            rescompil = "No compilation for Python"
            return render (request,'classroom/students/test_code.html')


def cosineSimilarity(request):
    universalSetOfUniqueWords = []
    matchPercentage = 0

    ####################################################################################################

    inputQuery = request.GET['code']
    lowercaseQuery = inputQuery.lower()

    queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()  # Replace punctuation by space and split
    queryWordList = map(str, queryWordList)

    for word in queryWordList:
        if word not in universalSetOfUniqueWords:
            universalSetOfUniqueWords.append(word)

    ####################################################################################################

    fd = open("database1.txt", "r")
    database1 = fd.read().lower()

    databaseWordList = re.sub("[^\w]", " ", database1).split()  # Replace punctuation by space and split
    databaseWordList = map(str, databaseWordList)

    for word in databaseWordList:
        if word not in universalSetOfUniqueWords:
            universalSetOfUniqueWords.append(word)

    ####################################################################################################

    queryTF = []
    databaseTF = []

    for word in universalSetOfUniqueWords:
        queryTfCounter = 0
        databaseTfCounter = 0

        for word2 in queryWordList:
            if word == word2:
                queryTfCounter += 1
        queryTF.append(queryTfCounter)

        for word2 in databaseWordList:
            if word == word2:
                databaseTfCounter += 1
        databaseTF.append(databaseTfCounter)

    dotProduct = 0
    for i in range(len(queryTF)):
        dotProduct += queryTF[i] * databaseTF[i]

    queryVectorMagnitude = 0
    for i in range(len(queryTF)):
        queryVectorMagnitude += queryTF[i] ** 2
    queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

    databaseVectorMagnitude = 0
    for i in range(len(databaseTF)):
        databaseVectorMagnitude += databaseTF[i] ** 2
    databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)

    matchPercentage = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

    '''
    print queryWordList
    print
    print databaseWordList


    print queryTF
    print
    print databaseTF
    '''

    output = "Your code matches %0.02f%% with code write by ..." % matchPercentage

    return render(request,'classroom/students/test_code.html', code=inputQuery, output=output)