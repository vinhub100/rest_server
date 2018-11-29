from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, get_list_or_404
from .permissions import QuestionAuthorPermission
from .serializers import OWQuestionListSerializer, OWQuestionDetailSerializer, OWQuestionCreateUpdateSerializer
from rest_server.core.models import OneWordAnswerType, OneWordAnswerAnswer


class OWQuestion(APIView):
    permission_classes = [permissions.IsAuthenticated, QuestionAuthorPermission]

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            data = get_list_or_404(OneWordAnswerType, author=request.user)
            paginator = PageNumberPagination()
            paged_data = paginator.paginate_queryset(data, request)
            serializer = OWQuestionListSerializer(paged_data, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = get_object_or_404(OneWordAnswerType, author=request.user, q_slug=slug)
        serializer = OWQuestionDetailSerializer(data, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = OWQuestionCreateUpdateSerializer(data=data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not slug:
            return Response("Slug is required", status=status.HTTP_400_BAD_REQUEST)
        question = get_object_or_404(OneWordAnswerType, q_slug=slug)
        serializer = OWQuestionCreateUpdateSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        question = get_object_or_404(OneWordAnswerType, q_slug=slug)
        answer = get_object_or_404(OneWordAnswerAnswer, question=question)
        answer.delete()
        question.delete()
        return Response('Question Deleted', status=status.HTTP_200_OK)


class SCQuestion(APIView):
    permission_classes = [permissions.IsAuthenticated, QuestionAuthorPermission]

    def get(self, request, *args, **kwargs):
        # slug = kwargs.get('slug', None)
        # if not slug:
        #     data = get_list_or_404(OneWordAnswerType, author=request.user)
        #     paginator = PageNumberPagination()
        #     paged_data = paginator.paginate_queryset(data, request)
        #     serializer = OWQuestionListSerializer(paged_data, many=True, context={'request': request})
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # data = get_object_or_404(OneWordAnswerType, author=request.user, q_slug=slug)
        # serializer = OWQuestionDetailSerializer(data, context={'request': request})
        # return Response(serializer.data, status=status.HTTP_200_OK)
        pass

    def post(self, request, *args, **kwargs):
        # data = request.data
        # serializer = OWQuestionCreateUpdateSerializer(data=data, context={'request':request})
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        pass

    def put(self, request, *args, **kwargs):
        # slug = kwargs.get('slug', None)
        # if not slug:
        #     return Response("Slug is required", status=status.HTTP_400_BAD_REQUEST)
        # question = get_object_or_404(OneWordAnswerType, q_slug=slug)
        # serializer = OWQuestionCreateUpdateSerializer(question, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_202_ACCEPTED)
        # return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)
        pass

    def delete(self, request, *args, **kwargs):
        # slug = kwargs.get('slug', None)
        # question = get_object_or_404(OneWordAnswerType, q_slug=slug)
        # answer = get_object_or_404(OneWordAnswerAnswer, question=question)
        # answer.delete()
        # question.delete()
        # return Response('Question Deleted', status=status.HTTP_200_OK)
        pass


class MCQuestion(APIView):
    permission_classes = [permissions.IsAuthenticated, QuestionAuthorPermission]

    def get(self, request, *args, **kwargs):
        # slug = kwargs.get('slug', None)
        # if not slug:
        #     data = get_list_or_404(OneWordAnswerType, author=request.user)
        #     paginator = PageNumberPagination()
        #     paged_data = paginator.paginate_queryset(data, request)
        #     serializer = OWQuestionListSerializer(paged_data, many=True, context={'request': request})
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # data = get_object_or_404(OneWordAnswerType, author=request.user, q_slug=slug)
        # serializer = OWQuestionDetailSerializer(data, context={'request': request})
        # return Response(serializer.data, status=status.HTTP_200_OK)
        pass

    def post(self, request, *args, **kwargs):
        # data = request.data
        # serializer = OWQuestionCreateUpdateSerializer(data=data, context={'request':request})
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        pass

    def put(self, request, *args, **kwargs):
        # slug = kwargs.get('slug', None)
        # if not slug:
        #     return Response("Slug is required", status=status.HTTP_400_BAD_REQUEST)
        # question = get_object_or_404(OneWordAnswerType, q_slug=slug)
        # serializer = OWQuestionCreateUpdateSerializer(question, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_202_ACCEPTED)
        # return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)
        pass

    def delete(self, request, *args, **kwargs):
        # slug = kwargs.get('slug', None)
        # question = get_object_or_404(OneWordAnswerType, q_slug=slug)
        # answer = get_object_or_404(OneWordAnswerAnswer, question=question)
        # answer.delete()
        # question.delete()
        # return Response('Question Deleted', status=status.HTTP_200_OK)
        pass

