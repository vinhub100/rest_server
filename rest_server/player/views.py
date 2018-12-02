import random
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import permissions
from .permissions import PlayerRoleOnly
from .models import PlayerScore
from rest_server.core.models import SingleChoiceQuestion, SingleChoiceOptions, SingleChoiceAnswer
from rest_server.core.models import OneWordAnswerType, OneWordAnswerAnswer
from rest_server.core.models import MultiChoiceQuestion, MultiChoiceOptions, MultiChoiceAnswers


class Quiz(APIView):
    permission_classes = [permissions.IsAuthenticated, PlayerRoleOnly]

    def single_choice_question(self, request):
        question = SingleChoiceQuestion.objects.random()
        options = SingleChoiceOptions.objects.filter(question=question)
        data = {'type': 'SC',
                'slug': question.q_slug,
                'question': question.question,
                'options': [opt.option for opt in options]
                }
        return Response(data=data, status=status.HTTP_200_OK)

    def multi_choice_question(self, request):
        question = MultiChoiceQuestion.objects.random()
        options = MultiChoiceOptions.objects.filter(question=question)
        data = {'type': 'MC',
                'slug': question.q_slug,
                'question': question.question,
                'options': [opt.option for opt in options]}
        return Response(data=data, status=status.HTTP_200_OK)

    def one_word_question(self, request):
        question = OneWordAnswerType.objects.random()
        data = {'type': 'OW',
                'slug': question.q_slug,
                'question': question.question,
                'hint': question.hint}
        return Response(data=data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        option = ['SC', 'MC', 'Word']
        q_type = random.choice(option)
        if q_type == 'SC':
            return self.single_choice_question(request)
        elif q_type == 'MC':
            return self.multi_choice_question(request)
        else:
            return self.one_word_question(request)

    def one_word_answer(self, request):
        qes_slug = request.data.get('slug')
        try:
            question = OneWordAnswerType.objects.get(q_slug=qes_slug)
        except (ObjectDoesNotExist, Exception):
            return Response(data={'error': 'Please send proper slug'}, status=status.HTTP_204_NO_CONTENT)
        try:
            answer = OneWordAnswerAnswer.objects.get(question=question)
        except (ObjectDoesNotExist, Exception):
            return Response(data={'error': 'Unable to find answer'}, status=status.HTTP_204_NO_CONTENT)
        submitted_ans = request.data.get('answer')
        ans = str(answer.answers)
        if submitted_ans.lower() == ans.lower():
            player = PlayerScore.objects.get(user=request.user)
            player.score += 5
            player.save()
            answer_state = 'Right'
        else:
            answer_state = 'Wrong'
        data = {'question': question,
                'submitted_answer': submitted_ans,
                'right_answer': ans,
                'result': answer_state}
        return Response(data=data, status=status.HTTP_200_OK)

    def single_choice_answer(self, request):
        slug = request.data.get('slug')
        try:
            question = SingleChoiceQuestion.objects.get(q_slug=slug)
        except (ObjectDoesNotExist, Exception):
            return Response(data={'error': 'Please send proper slug'}, status=status.HTTP_204_NO_CONTENT)
        try:
            answer = SingleChoiceAnswer.objects.get(question=question)
        except (ObjectDoesNotExist, Exception):
            return Response(data={'error': 'Unable to find answer'}, status=status.HTTP_204_NO_CONTENT)
        submitted_ans = request.data.get('answer')
        ans = str(answer.answer)
        if submitted_ans == ans:
            player = PlayerScore.objects.get(user=request.user)
            player.score += 5
            player.save()
            answer_state = 'Right'
        else:
            answer_state = 'Wrong'
        data = {'question': question,
                'submitted_answer': submitted_ans,
                'right_answer': ans,
                'result': answer_state}
        return Response(data=data, status=status.HTTP_200_OK)

    def multi_choice_answer(self, request):
        slug = request.data.get('slug')
        try:
            question = MultiChoiceQuestion.objects.get(q_slug=slug)
        except (ObjectDoesNotExist, Exception):
            return Response(data={'error': 'Please send proper slug'}, status=status.HTTP_204_NO_CONTENT)
        try:
            answers = MultiChoiceAnswers.objects.filter(question=question)
            options = MultiChoiceOptions.objects.filter(question=question)
        except (ObjectDoesNotExist, Exception):
            return Response(data={'error': 'Unable to find answer or options'}, status=status.HTTP_204_NO_CONTENT)
        submitted_ans = request.data.getlist('answers')
        ans = [str(answer.answers.option) for answer in answers ]
        pass_ans = False
        fail_ans = False
        wrong_ans = [str(option.option) for option in options]
        for answer in ans:
            wrong_ans.remove(answer)

        for sub_ans in submitted_ans:
            if sub_ans in ans:
                pass_ans = True
            else:
                fail_ans = True

        for sub_ans in submitted_ans:
            if sub_ans in wrong_ans:
                fail_ans = True
            else:
                pass_ans = True

        if len(submitted_ans) == len(ans):
            pass_ans = True
        else:
            fail_ans = True

        if pass_ans is True and fail_ans is False:
            player = PlayerScore.objects.get(user=request.user)
            player.score += 5
            player.save()
            answer_state = 'Right'
        else:
            answer_state = 'Wrong'
        data = {'question': question,
                'result': answer_state,
                'submitted_answer': submitted_ans,
                'right_answer': ans}
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if request.data.get('type') == 'MC':
            return self.multi_choice_answer(request)
        elif request.data.get('type') == 'SC':
            return self.single_choice_answer(request)
        elif request.data.get('type') == 'OW':
            return self.one_word_answer(request)
        else:
            return Response(data={'error': 'Unable to identify the question type'}, status=status.HTTP_204_NO_CONTENT)


class GetScore(APIView):
    permission_classes = [permissions.IsAuthenticated, PlayerRoleOnly]

    def get(self, request, *args, **kwargs):
        score_obj = get_object_or_404(PlayerScore, user=request.user)
        data = {'score': score_obj.score}
        return Response(data=data, status=status.HTTP_200_OK)

