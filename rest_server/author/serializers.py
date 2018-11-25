from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, CharField,\
    HyperlinkedRelatedField, HyperlinkedModelSerializer
from rest_server.core.models import OneWordAnswerType, OneWordAnswerAnswer
from rest_server.core.models import SingleChoiceQuestion, SingleChoiceOptions, SingleChoiceAnswer
from rest_server.core.models import MultiChoiceQuestion, MultiChoiceOptions, MultiChoiceAnswers


from django.shortcuts import get_object_or_404, reverse, get_list_or_404


# ONE WORD QUESTION


class OWQuestionListSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = OneWordAnswerType
        fields = ['question', 'q_slug', 'url']

    def get_url(self, q_obj):
        return reverse('author:OWQ_Author', args=[str(q_obj.q_slug)]) # + str(q_obj.q_slug)


class OWQuestionDetailSerializer(ModelSerializer):
    answer = SerializerMethodField()
    url = SerializerMethodField()
#    url = HyperlinkedIdentityField(view_name='author:OWQ_Author', lookup_field='q_slug', read_only=True)

    class Meta:
        model = OneWordAnswerType
        fields = ['question', 'hint', 'answer', 'q_slug', 'url']

    def get_answer(self, q_obj):
        a_obj = get_object_or_404(OneWordAnswerAnswer, question=q_obj)
        return a_obj.answers

    def get_url(self, q_obj):
        return reverse('author:OWQ_Author', args=[str(q_obj.q_slug)]) # + str(q_obj.q_slug)

#
# class OWAnswerSerializer(ModelSerializer):
#     class Meta:
#         model = OneWordAnswerAnswer
#         fields = ['answers']


class OWQuestionCreateUpdateSerializer(ModelSerializer):
    answer = CharField(max_length=60, allow_blank=False)

    class Meta:
        model = OneWordAnswerType
        fields = ['question', 'hint', 'answer']

    def create(self, validated_data):
        user = self.context['request'].user
        question = OneWordAnswerType(author=user, question=validated_data.get('question'),
                                     hint=validated_data.get('hint'))
        question.save(force_insert=True)
        answer = OneWordAnswerAnswer(question=question, answers=validated_data.get('answer'))
        answer.save(force_insert=True)
        return question

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question')
        instance.hint = validated_data.get('hint')
        instance.save()
        a_obj = get_object_or_404(OneWordAnswerAnswer, question=instance)
        a_obj.answers = validated_data.get('answer')
        a_obj.save()
        return instance


#  SINGLE CHOICE QUESTION

class SCQuestionListSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = SingleChoiceQuestion
        fields = ['question', 'q_slug', 'url']

    def get_url(self, q_obj):
        return reverse('author:SCQ_Author', args=[str(q_obj.q_slug)])  # + str(q_obj.q_slug)


class SCQuestionDetailSerializer(ModelSerializer):
    options = SerializerMethodField()
    answers = SerializerMethodField()
    url = SerializerMethodField()
#    url = HyperlinkedIdentityField(view_name='author:OWQ_Author', lookup_field='q_slug', read_only=True)

    class Meta:
        model = SingleChoiceQuestion
        fields = ['question', 'options', 'answers', 'q_slug', 'url']

    def get_answers(self, q_obj):
        a_obj = get_list_or_404(SingleChoiceAnswer, question=q_obj)
        return a_obj.answer.option

    def get_options(self, q_obj):
        op_obj = get_list_or_404(SingleChoiceOptions, question=q_obj)
        return [{'option', op.option} for op in op_obj]

    def get_url(self, q_obj):
        return reverse('author:SCQ_Author', args=[str(q_obj.q_slug)])  # + str(q_obj.q_slug)


class SCQuestionCreateUpdateSerializer(ModelSerializer):
    answer = CharField(max_length=60, allow_blank=False)

    class Meta:
        model = SingleChoiceQuestion
        fields = ['question', 'options', 'answer']

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     question = OneWordAnswerType(author=user, question=validated_data.get('question'),
    #                                  hint=validated_data.get('hint'))
    #     question.save(force_insert=True)
    #     answer = OneWordAnswerAnswer(question=question, answers=validated_data.get('answer'))
    #     answer.save(force_insert=True)
    #     return question
    #
    # def update(self, instance, validated_data):
    #     instance.question = validated_data.get('question')
    #     instance.hint = validated_data.get('hint')
    #     instance.save()
    #     a_obj = get_object_or_404(OneWordAnswerAnswer, question=instance)
    #     a_obj.answers = validated_data.get('answer')
    #     a_obj.save()
    #     return instance
    #
    # def validate(self, data):
    #     pass

