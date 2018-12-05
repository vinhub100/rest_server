from collections import OrderedDict
from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, Serializer, ListField, DictField
from rest_server.core.models import OneWordAnswerType, OneWordAnswerAnswer
from rest_server.core.models import SingleChoiceQuestion, SingleChoiceOptions, SingleChoiceAnswer
from rest_server.core.models import MultiChoiceQuestion, MultiChoiceOptions, MultiChoiceAnswers
from rest_framework import serializers
import logging


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
        a_obj = get_object_or_404(SingleChoiceAnswer, question=q_obj)
        return a_obj.answer.option

    def get_options(self, q_obj):
        op_obj = get_list_or_404(SingleChoiceOptions, question=q_obj)
        return [{'option': op.option} for op in op_obj]

    def get_url(self, q_obj):
        return reverse('author:SCQ_Author', args=[str(q_obj.q_slug)])  # + str(q_obj.q_slug)


class SCOptionField(DictField):
    option = CharField(max_length=50)


class SCQuestionCreateUpdateSerializer(ModelSerializer):
    question = CharField(max_length=255, allow_blank=False)
    options = SCOptionField()
    answer = CharField(max_length=60, allow_blank=False)

    class Meta:
        model = SingleChoiceQuestion
        fields = ['question', 'options', 'answer']

    def to_representation(self, instance):
        a_obj = get_object_or_404(SingleChoiceAnswer, question=instance)
        answer = a_obj.answer.option
        op_obj = get_list_or_404(SingleChoiceOptions, question=instance)
        options = [{'option': op.option} for op in op_obj]
        da = OrderedDict()
        da['question'] = instance.question
        da['options'] = options
        da['answer'] = answer
        da['slug'] = instance.q_slug
        return da

    def create(self, validated_data):
        user = self.context['request'].user
        print('VV->')
        print('VVV DDD', validated_data)
        print('Create 1', validated_data.get('question'))
        question = SingleChoiceQuestion(author=user, question=validated_data.get('question'))
        question.save()
        print('Create 2')
        option_dict_list = validated_data.get('options')
        option_list = [od for od in option_dict_list]
        print('create 2.5', option_list)
        op_model_list = []
        print('Create 3')
        for option in option_list:
            sco = SingleChoiceOptions(question=question, option=option)
            sco.save(force_insert=True)
            op_model_list.append(sco)
        ans = validated_data.get('answer')
        ai = option_list.index(ans)
        answer = SingleChoiceAnswer(question=question, answer=op_model_list[ai])
        answer.save(force_insert=True)
        print('Create 4', type(question))
        return question

    def update(self, instance, validated_data):
        del_option_list = get_list_or_404(SingleChoiceOptions, question=instance)
        del_ans = get_object_or_404(SingleChoiceAnswer, question=instance)
        del_ans.delete()
        for do in del_option_list:
            do.delete()
        option_dict_list = validated_data.get('options')
        option_list = [od for od in option_dict_list]
        op_model_list = []
        for option in option_list:
            sco = SingleChoiceOptions(question=instance, option=option)
            sco.save(force_insert=True)
            op_model_list.append(sco)
        ans = validated_data.get('answer')
        ai = option_list.index(ans)
        answer = SingleChoiceAnswer(question=instance, answer=op_model_list[ai])
        answer.save(force_insert=True)
        return instance

    def validate(self, data):
        print('Val', data)
        option_dict_list = data.get('options')
        answer = data.get('answer')
        print('Val 1', option_dict_list)
        option_list = [od for od in option_dict_list]
        print('Val 2', option_list)
        if len(option_list) != len(set(option_list)):
            raise serializers.ValidationError("Some Options are repeating")
        if answer not in option_list:
            raise serializers.ValidationError("Answer should be one of the options")
        return data

    # def validate_options(self, value):
    #     pass
    #
    #

#  MULTI CHOICE QUESTION


class MCQuestionListSerializer(ModelSerializer):
    url = SerializerMethodField()

    class Meta:
        model = MultiChoiceQuestion
        fields = ['question', 'q_slug', 'url']

    def get_url(self, q_obj):
        return reverse('author:SCQ_Author', args=[str(q_obj.q_slug)])  # + str(q_obj.q_slug)


class MCQuestionDetailSerializer(ModelSerializer):
    options = SerializerMethodField()
    answers = SerializerMethodField()
    url = SerializerMethodField()
#    url = HyperlinkedIdentityField(view_name='author:OWQ_Author', lookup_field='q_slug', read_only=True)

    class Meta:
        model = MultiChoiceQuestion
        fields = ['question', 'options', 'answers', 'q_slug', 'url']

    def get_answers(self, q_obj):
        a_obj = get_list_or_404(MultiChoiceAnswers, question=q_obj)
        return [{'answer': al.answers.option} for al in a_obj]

    def get_options(self, q_obj):
        op_obj = get_list_or_404(MultiChoiceOptions, question=q_obj)
        return [{'option': op.option} for op in op_obj]

    def get_url(self, q_obj):
        return reverse('author:SCQ_Author', args=[str(q_obj.q_slug)])  # + str(q_obj.q_slug)


class MCOptionField(DictField):
    option = CharField(max_length=50)


class MCAnswerField(DictField):
    answer = CharField(max_length=50)


class MCQuestionCreateUpdateSerializer(ModelSerializer):
    options = MCOptionField()
    answers = MCAnswerField()

    class Meta:
        model = MultiChoiceQuestion
        fields = ['question', 'options', 'answers']

    def to_representation(self, instance):
        a_obj = get_list_or_404(MultiChoiceAnswers, question=instance)
        answer = [{'answer': an.answers.option} for an in a_obj]
        op_obj = get_list_or_404(MultiChoiceOptions, question=instance)
        options = [{'option': op.option} for op in op_obj]
        da = OrderedDict()
        da['question'] = instance.question
        da['options'] = options
        da['answers'] = answer
        da['slug'] = instance.q_slug
        return da

    def create(self, validated_data):
        user = self.context['request'].user
        print('VV->')
        print('VVV DDD', validated_data)
        print('Create 1', validated_data.get('question'))
        question = MultiChoiceQuestion(author=user, question=validated_data.get('question'))
        question.save()
        print('Create 2')
        option_dict_list = validated_data.get('options')
        option_list = [od for od in option_dict_list]
        print('create 2.5', option_list)
        op_model_list = []
        print('Create 3')
        for option in option_list:
            sco = MultiChoiceOptions(question=question, option=option)
            sco.save(force_insert=True)
            op_model_list.append(sco)
        ans_dict_list = validated_data.get('answers')
        answer_list = [an for an in ans_dict_list]
        print('create 3', answer_list)
        for ans in answer_list:
            ai = option_list.index(ans)
            answer = MultiChoiceAnswers(question=question, answers=op_model_list[ai])
            answer.save(force_insert=True)
        return question

    def update(self, instance, validated_data):
        print('VV->')
        print('VVV DDD', validated_data)
        print('Create 1', validated_data.get('question'))
        del_option_list = get_list_or_404(MultiChoiceOptions, question=instance)
        del_ans_list = get_list_or_404(MultiChoiceAnswers, question=instance)
        for da in del_ans_list:
            da.delete()
        for do in del_option_list:
            do.delete()
        option_dict_list = validated_data.get('options')
        option_list = [od for od in option_dict_list]
        print('Update 2.5', option_list)
        op_model_list = []
        print('Update 3')
        for option in option_list:
            sco = MultiChoiceOptions(question=instance, option=option)
            sco.save(force_insert=True)
            op_model_list.append(sco)
        ans_dict_list = validated_data.get('answers')
        answer_list = [an for an in ans_dict_list]
        print('Update 3', answer_list)
        for ans in answer_list:
            ai = option_list.index(ans)
            answer = MultiChoiceAnswers(question=instance, answers=op_model_list[ai])
            answer.save(force_insert=True)
        return instance

    def validate(self, data):
        print('Val', data)
        option_dict_list = data.get('options')
        answer_dict_list = data.get('answers')
        print('Val 1', option_dict_list)
        print('Val 1.5', answer_dict_list)
        option_list = [od for od in option_dict_list]
        answer_list = [an for an in answer_dict_list]
        print('Val 2', option_list)
        print('Val 2.5', answer_list)
        if len(option_list) != len(set(option_list)):
            raise serializers.ValidationError("Some Options are repeating")
        if len(option_list) != len(set(option_list + answer_list)):
            raise serializers.ValidationError("Answer should be one of the options")
        return data

    # def validate_options(self, value):
    #     pass



