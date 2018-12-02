from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField, Serializer
from rest_server.core.models import OneWordAnswerType, OneWordAnswerAnswer
from rest_server.core.models import SingleChoiceQuestion, SingleChoiceOptions, SingleChoiceAnswer
from rest_server.core.models import MultiChoiceQuestion, MultiChoiceOptions, MultiChoiceAnswers
from rest_framework import serializers


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
        a_obj = get_list_or_404(SingleChoiceAnswer, question=q_obj)
        return a_obj.answer.option

    def get_options(self, q_obj):
        op_obj = get_list_or_404(SingleChoiceOptions, question=q_obj)
        return [{'option', op.option} for op in op_obj]

    def get_url(self, q_obj):
        return reverse('author:SCQ_Author', args=[str(q_obj.q_slug)])  # + str(q_obj.q_slug)


class SCOptionSerializer(Serializer):
    option = CharField(max_length=50)


class SCQuestionCreateUpdateSerializer(ModelSerializer):
    options = SCOptionSerializer(many=True)
    answer = CharField(max_length=60, allow_blank=False)

    class Meta:
        model = SingleChoiceQuestion
        fields = ['question', 'options', 'answer']

    def create(self, validated_data):
        user = self.context['request'].user
        question = SingleChoiceQuestion(author=user, question=validated_data.get('question'))
        question.save(force_insert=True)
        option_dict_list = validated_data.get('options')
        option_list = [od['option'] for od in option_dict_list]
        op_model_list = []
        for option in option_list:
            sco = SingleChoiceOptions(question=question, option=option)
            sco.save(force_insert=True)
            op_model_list.append(sco)
        ans = validated_data.get('answer')
        ai = option_list.index(ans)
        answer = SingleChoiceAnswer(question=question, answer=op_model_list[ai])
        answer.save(force_insert=True)
        return question

    def update(self, instance, validated_data):
        del_option_list = get_list_or_404(SingleChoiceOptions, question=instance)
        del_ans = get_object_or_404(SingleChoiceAnswer, question=instance)
        del_ans.delete()
        for do in del_option_list:
            do.delete()
        option_dict_list = validated_data.get('options')
        option_list = [od['option'] for od in option_dict_list]
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
        option_dict_list = data.get('options')
        answer = data.get('answer')
        option_list = [od['option'] for od in option_dict_list]
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
        a_obj = get_list_or_404(SingleChoiceAnswer, question=q_obj)
        return a_obj.answer.option

    def get_options(self, q_obj):
        op_obj = get_list_or_404(SingleChoiceOptions, question=q_obj)
        return [{'option', op.option} for op in op_obj]

    def get_url(self, q_obj):
        return reverse('author:SCQ_Author', args=[str(q_obj.q_slug)])  # + str(q_obj.q_slug)


class MCOptionSerializer(Serializer):
    option = CharField(max_length=50)


class MCAnswerSerializer(Serializer):
    answer = CharField(max_length=50)


class MCQuestionCreateUpdateSerializer(ModelSerializer):
    options = MCOptionSerializer(many=True)
    answers = MCAnswerSerializer(many=True)

    class Meta:
        model = MultiChoiceQuestion
        fields = ['question', 'options', 'answers']

    def create(self, validated_data):
        user = self.context['request'].user
        question = MultiChoiceQuestion(author=user, question=validated_data.get('question'))
        question.save(force_insert=True)
        option_dict_list = validated_data.get('options')
        option_list = [od['option'] for od in option_dict_list]
        op_model_list = []
        for option in option_list:
            mco = MultiChoiceOptions(question=question, option=option)
            mco.save(force_insert=True)
            op_model_list.append(mco)
        ans_dict_list = validated_data.get('answers')
        answer_list = [ad['answer'] for ad in ans_dict_list]
        for ans in answer_list:
            ai = option_list.index(ans)
            answer = MultiChoiceAnswers(question=question, answer=op_model_list[ai])
            answer.save(force_insert=True)
        return question

    def update(self, instance, validated_data):
        del_option_list = get_list_or_404(MultiChoiceOptions, question=instance)
        del_ans = get_list_or_404(MultiChoiceAnswers, question=instance)
        for ans in del_ans:
            ans.delete()
        for do in del_option_list:
            do.delete()
        option_dict_list = validated_data.get('options')
        option_list = [od['option'] for od in option_dict_list]
        op_model_list = []
        for option in option_list:
            mco = MultiChoiceOptions(question=instance, option=option)
            mco.save(force_insert=True)
            op_model_list.append(mco)
        ans_dict_list = validated_data.get('answers')
        answer_list = [ad['answer'] for ad in ans_dict_list]
        for ans in answer_list:
            ai = option_list.index(ans)
            answer = MultiChoiceAnswers(question=instance, answer=op_model_list[ai])
            answer.save(force_insert=True)
        return instance

    def validate(self, data):
        option_dict_list = data.get('options')
        answer_dict_list = data.get('answers')
        option_list = [od['option'] for od in option_dict_list]
        answer_list = [od['answer'] for od in answer_dict_list]
        if len(option_list) != len(set(option_list)):
            raise serializers.ValidationError("Some Options are repeating")
        if len(answer_list) != len(set(answer_list)):
            raise serializers.ValidationError("Some Answers are repeating")
        if len(option_list) != len(set(option_list + answer_list)):
            raise serializers.ValidationError("All Answers should be part of the Options")
        return data

    # def validate_options(self, value):
    #     pass



