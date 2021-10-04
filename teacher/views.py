from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.utils import timezone
from .models import WorkTable, Dictonary, LearningModel
from .forms import TranslateForm2, TranslateForm1
import random
from .forms import TrainingForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        users_words = WorkTable.objects.filter(user__pk=request.user.pk)
        words_quantity = len(users_words)
        long_memory_words = len(users_words.filter(current_step=6))
        context = {'words_quantity': words_quantity,
                   'long_memory_words': long_memory_words}
    else:
        context = {}
    return render(request, 'teacher/index.html', context)

class TrainingView(LoginRequiredMixin, View):

    def __init__(self, *args, **kwargs):
        super(TrainingView, self).__init__(*args, **kwargs)
        self.word_number = 0


    def get_test_set(self):
        # Получаем тренировочный сет пользователя на текущую дату и его размер
        user = self.request.user

        training_set = user.dictonary_set.filter(worktable__training_date__lte=timezone.now())

        train_quantity = len(training_set)

        # Список переводов для формирования тестового списка
        training_words = []
        if train_quantity > 0:
            for line in training_set:
                training_words.append(line.translated_word)
        else:
            fool_test_set = ['', '', '', '']
            wright_word = ''
            wright_translate = ''
            return fool_test_set, train_quantity, wright_word, wright_translate

        if train_quantity < 4:
            add_quantity = 4-train_quantity
            k = 0
            while k < add_quantity:
                add_pk = random.randint(1, 10)
                add_word = Dictonary.objects.get(pk=add_pk).translated_word
                training_words.append(add_word)
                k +=1

        # количество вариантов ответа помимо правильного
        test_quantity = 3
        # Случайно установим номер тестируемого слова в списке ответов
        wright_number = random.randint(0, test_quantity)
        # Определим исходное значение и перевод тренируемого слова
        wright_word = training_set[self.word_number].original_word
        wright_translate = training_set[self.word_number].translated_word
        # Сформируем случайным образом ответы для включения в тест
        test_numbers = []
        test_set = []
        while len(test_numbers) < test_quantity:
            number = random.randint(0, len(training_words) - 1)
            if (number not in test_numbers) and (number != self.word_number):
                test_numbers.append(number)
                test_set.append(training_words[number])

        # Сформируем полный случайный список ответов, включая правильный
        n = 0
        fool_test_set = []
        for i in range(test_quantity + 1):
            if i == wright_number:
                fool_test_set.append(wright_translate)
            else:
                fool_test_set.append(test_set[n])
                n += 1

        return fool_test_set, train_quantity, wright_word, wright_translate


    def get(self, request):

        fool_test_set, train_quantity, wright_word, wright_translate = self.get_test_set()

        form = TrainingForm(fool_test_set)

        word_number = self.word_number #+1

        context = {'train_quantity': train_quantity,
                   'test_word': wright_word,
                   'word_number': word_number,
                   'wright_translate': wright_translate,
                   'form': form}

        return render(request, 'teacher/training_form.html', context)

    def post(self, request):

        user = request.user

        answer = request.POST.get('Ответ')
        """if request.POST.get('word_number'):
            self.word_number = int(request.POST.get('word_number'))"""
        reference = request.POST.get('wright_translate')

        """if self.word_number == 1:
            record_word = training_set[self.word_number - 1]
            test_word = training_set[self.word_number-1].translated_word
        else:
            record_word = training_set[self.word_number]
            test_word = reference"""

        test_word = reference
        record_word = user.dictonary_set.get(translated_word=reference)

        record = WorkTable.objects.get(user=request.user, word=record_word)

        if answer == test_word:
            verdict = f'{answer} - верный ответ'
            if record.current_step < 6:
                record.current_step += 1
                record.save()

            delta = LearningModel.objects.get(pk=record.current_step).training_interval
            record.training_date = timezone.now()+datetime.timedelta(days=delta)
            record.save()
            leading = f'Повторите слово через {delta} дней.'

        else:
            verdict = f'{answer} - неверный перевод, правильный перевод {test_word}.'
            if record.current_step > 1:
                record.current_step -= 1
                record.save()

            delta = LearningModel.objects.get(pk=record.current_step).training_interval
            record.training_date = timezone.now()+datetime.timedelta(days=delta)
            record.save()
            leading = f'Повторите слово через {delta} дней.'

        test_message = f'Изменен статус слова {record.word.original_word}'

        fool_test_set, train_quantity, wright_word, wright_translate = self.get_test_set()

        form = TrainingForm(fool_test_set)

        word_number = 0

        context = {'train_quantity': train_quantity,
                   'test_word': wright_word,
                   'wright_translate': wright_translate,
                   'verdict': verdict,
                   'leading': leading,
                   'word_number': word_number,
                   'form': form,
                   'test_message': test_message}

        return render(request, 'teacher/training_form.html', context)


class TranslateView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'teacher/translate_form.html', {})

    def post(self, request):
        requested_word = request.POST.get('original_word')
        returned_word = request.POST.get('translated_word')
        user = self.request.user

        try:
            users_word = Dictonary.objects.get(original_word=requested_word)
            translated_word = users_word.translated_word
            users = users_word.users.all()
            if not user in users:
                new_word = Dictonary.objects.get(translated_word=translated_word)
                training_date = timezone.now() + datetime.timedelta(days=1)
                WorkTable.objects.create(user=user, word=new_word, training_date=training_date)
                context = {'add_message': 'В ваш словарь добавлено слово: ',
                           'translated_word': translated_word,
                           'original_word': requested_word}
                return render(request, 'teacher/translate_form.html', context)


        except (KeyError, Dictonary.DoesNotExist):
            if returned_word:
                Dictonary.objects.create(original_word=requested_word, translated_word=returned_word)
                new_word = Dictonary.objects.get(translated_word=returned_word)
                training_date = timezone.now()+datetime.timedelta(days=1)
                WorkTable.objects.create(user=user, word=new_word, training_date=training_date)
                context = {'add_message': 'В ваш словарь добавлено слово: ',
                           'translated_word': returned_word,
                           'original_word': requested_word}

                return render(request, 'teacher/translate_form.html', context)

            context = {'error_message': 'Слова нет в словаре. Введите слово и перевод.',
                       'default_word': requested_word}
            return render(request, 'teacher/translate_form.html', context)
        else:
            context = {'translated_word': translated_word}
            return render(request, 'teacher/translate_form.html', context)















