from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import pagination
# from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, get_list_or_404
from .permissions import QuestionAuthorPermission
from .serializers import OWQuestionListSerializer, OWQuestionDetailSerializer, OWQuestionCreateUpdateSerializer
from .serializers import SCQuestionListSerializer, SCQuestionDetailSerializer, SCQuestionCreateUpdateSerializer
from .serializers import MCQuestionListSerializer, MCQuestionDetailSerializer, MCQuestionCreateUpdateSerializer
from rest_server.core.models import OneWordAnswerType, OneWordAnswerAnswer
from rest_server.core.models import SingleChoiceQuestion, SingleChoiceAnswer, SingleChoiceOptions
from rest_server.core.models import MultiChoiceQuestion, MultiChoiceOptions, MultiChoiceAnswers


class OWQuestion(APIView):
    permission_classes = [permissions.IsAuthenticated, QuestionAuthorPermission]
    pagination_class = pagination.PageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            data = get_list_or_404(OneWordAnswerType, author=request.user)
            paged_data = self.paginate_queryset(data)
            if paged_data is not None:
                serializer = OWQuestionListSerializer(paged_data, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)
            serializer = OWQuestionListSerializer(data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = get_object_or_404(OneWordAnswerType, author=request.user, q_slug=slug)
        self.check_object_permissions(request, data)
        serializer = OWQuestionDetailSerializer(data, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = OWQuestionCreateUpdateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            return Response({'message': 'Slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        que = get_object_or_404(OneWordAnswerType, q_slug=slug)
        self.check_object_permissions(request, que)
        serializer = OWQuestionCreateUpdateSerializer(que, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        print(serializer.errors)
        return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            return Response({'message': 'Slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(OneWordAnswerType, q_slug=slug)
        self.check_object_permissions(request, question)
        answer = get_object_or_404(OneWordAnswerAnswer, question=question)
        answer.delete()
        question.delete()
        return Response('Question Deleted', status=status.HTTP_200_OK)


class SCQuestion(APIView):
    permission_classes = [permissions.IsAuthenticated, QuestionAuthorPermission]
    pagination_class = pagination.PageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request, *args, **kwargs):
        print('HOST', request.get_host())
        slug = kwargs.get('slug', None)
        if not slug:
            data = get_list_or_404(SingleChoiceQuestion, author=request.user)
            paged_data = self.paginate_queryset(data)
            if paged_data is not None:
                serializer = SCQuestionListSerializer(paged_data, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)
            serializer = SCQuestionListSerializer(data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = get_object_or_404(SingleChoiceQuestion, author=request.user, q_slug=slug)
        self.check_object_permissions(request, data)
        serializer = SCQuestionDetailSerializer(data, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        print('View 1', data.get('question'), data.getlist('options'), data.get('answer'))
        p_data = {'question': data.get('question'),
                  'options': {option: option for option in data.getlist('options')},
                  'answer': data.get('answer')}
        print('View 2', p_data)
        serializer = SCQuestionCreateUpdateSerializer(data=p_data, context={'request': request})
        print('View 3', serializer.is_valid())
        if serializer.is_valid():
            print('View 4')
            serializer.save()
            print('View 5')
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            return Response({'message': 'Slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(SingleChoiceQuestion, q_slug=slug)
        self.check_object_permissions(request, question)
        data = request.data
        p_data = {'options': {option: option for option in data.getlist('options')},
                  'answer': data.get('answer')}
        serializer = SCQuestionCreateUpdateSerializer(question, data=p_data,  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            return Response({'message': 'Slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(SingleChoiceQuestion, q_slug=slug)
        self.check_object_permissions(request, question)
        answer = get_object_or_404(SingleChoiceAnswer, question=question)
        options = get_list_or_404(SingleChoiceOptions, question=question)
        answer.delete()
        for option in options:
            option.delete()
        question.delete()
        return Response(data={'status': 'Deleted'}, status=status.HTTP_200_OK)


class MCQuestion(APIView):
    permission_classes = [permissions.IsAuthenticated, QuestionAuthorPermission]
    pagination_class = pagination.PageNumberPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            data = get_list_or_404(MultiChoiceQuestion, author=request.user)
            paged_data = self.paginate_queryset(data)
            if paged_data is not None:
                serializer = MCQuestionListSerializer(paged_data, many=True, context={'request': request})
                return self.get_paginated_response(serializer.data)
            serializer = MCQuestionListSerializer(data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = get_object_or_404(MultiChoiceQuestion, author=request.user, q_slug=slug)
        self.check_object_permissions(request, data)
        serializer = MCQuestionDetailSerializer(data, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        print('View 1', data.get('question'), data.getlist('options'), data.get('answer'))
        p_data = {'question': data.get('question'),
                  'options': {option: option for option in data.getlist('options')},
                  'answers': {answer: answer for answer in data.getlist('answers')}}
        print('View 2', p_data)
        serializer = MCQuestionCreateUpdateSerializer(data=p_data, context={'request': request})
        print('View 3', serializer.is_valid())
        if serializer.is_valid():
            print('View 4')
            serializer.save()
            print('View 5')
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            return Response({'message': 'Slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(MultiChoiceQuestion, q_slug=slug)
        self.check_object_permissions(request, question)
        data = request.data
        p_data = {'options': {option: option for option in data.getlist('options')},
                  'answers': {answer: answer for answer in data.getlist('answers')}}
        serializer = MCQuestionCreateUpdateSerializer(question, data=p_data, partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            return Response({'message': 'Slug is required'}, status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(MultiChoiceQuestion, q_slug=slug)
        self.check_object_permissions(request, question)
        answers = get_list_or_404(MultiChoiceAnswers, question=question)
        options = get_list_or_404(MultiChoiceOptions, question=question)
        for answer in answers:
            answer.delete()
        for option in options:
            option.delete()
        question.delete()
        return Response(data={'status': 'Deleted'}, status=status.HTTP_200_OK)

