from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from core.forms import GameForm, QuestionForm
from core.models import Game
from django.shortcuts import get_object_or_404
from django.db.models import Count, Case, When, IntegerField


class NewGameView(FormView):
    template_name = 'game-form.html'
    form_class = GameForm

    def form_valid(self, form):
        game = form.create_game()
        return HttpResponseRedirect(reverse('question', args=(game.pk, 1)))


class QuestionView(FormView):
    template_name = 'question-form.html'
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs['game'])
        context = super(QuestionView, self).get_context_data(**kwargs)
        question = game.get_question_by_index(self.kwargs['question'])
        context['question'] = question
        mappings = dict(A=0, B=1, C=2, D=3)
        reverse_mappings = dict(enumerate(['A','B','C','D']))
        answers = [a.content for a in question.fake_tweets.all()]
        index = mappings[question.correct_answer]
        answers.insert(index, question.real_tweet.content)
        answers = [dict(option=reverse_mappings[i], text=x) for i, x in enumerate(answers)]
        context['answers'] = answers
        context['number'] = self.kwargs['question']
        return context

    def form_valid(self, form):
        game = Game.objects.get(pk=self.kwargs['game'])
        question = game.get_question_by_index(self.kwargs['question'])
        answer = form.return_choice()

        if not question.answer:
            question.answer = 'REAL' if answer == question.correct_answer else 'FAKE'
            question.selected_answer = answer
            question.save()
        return HttpResponseRedirect(
            reverse('answer', args=(self.kwargs['game'], self.kwargs['question']))
        )


class AnswerView(TemplateView):
    template_name = 'answer-view.html'

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data(**kwargs)
        game = get_object_or_404(Game, pk=self.kwargs['game'])
        question = game.get_question_by_index(self.kwargs['question'])
        context['question'] = question
        mappings = dict(A=0, B=1, C=2, D=3)
        reverse_mappings = dict(enumerate(['A', 'B', 'C', 'D']))
        answers = [a.content for a in question.fake_tweets.all()]
        index = mappings[question.correct_answer]
        answers.insert(index, question.real_tweet.content)
        answers = [dict(option=reverse_mappings[i], text=x, correct=question.real_tweet.content == x, selected=question.selected_answer == reverse_mappings[i]) for i, x in enumerate(answers)]
        context['answers'] = answers

        if self.kwargs['question'] >= game.questions.count():
            context['next'] = reverse('results', args=(self.kwargs['game'],))
            context['last'] = True
        else:
            context['next'] = reverse(
                'question', args=(self.kwargs['game'], self.kwargs['question'] + 1)
            )
        return context


class ResultView(TemplateView):
    template_name = 'results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultView, self).get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, pk=self.kwargs['game'])
        return context


class HighScores(TemplateView):
    template_name = 'high-scores.html'

    def get_context_data(self, **kwargs):
        context = super(HighScores, self).get_context_data(**kwargs)

        high_scores = (
            Game.objects.filter(questions__answer__isnull=False)
            .annotate(
                total_score=Count(
                    Case(
                        When(questions__answer='REAL', then=1),
                        output_field=IntegerField(),
                    )
                ),
                answered_questions=Count(
                    Case(
                        When(questions__answer__in=['REAL', 'FAKE'], then=1),
                        output_field=IntegerField(),
                    )
                ),
            )
            .filter(answered_questions=20)
            .order_by('-total_score')[:50]
        )
        context['high_scores'] = high_scores
        return context
