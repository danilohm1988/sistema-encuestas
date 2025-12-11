import graphene
from graphene_django.types import DjangoObjectType
from .models import Survey, Question, Option, Answer


# ============================
#   TYPES (Objetos GraphQL)
# ============================

class SurveyType(DjangoObjectType):
    class Meta:
        model = Survey
        fields = ("id", "title", "description", "created_at", "questions")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "text", "survey", "options")


class OptionType(DjangoObjectType):
    class Meta:
        model = Option
        fields = ("id", "text", "question")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("id", "survey", "question", "option", "created_at")


# ===================================================
#   QUERIES (Listar encuestas + Detalle + Resultados)
# ===================================================

# ---------- Resultados por opción ----------
class ResultType(graphene.ObjectType):
    option_id = graphene.Int()
    option_text = graphene.String()
    votos = graphene.Int()


# ---------- Resultados por pregunta ----------
class ResultadoPreguntaType(graphene.ObjectType):
    question_id = graphene.Int()
    question_text = graphene.String()
    resultados = graphene.List(ResultType)


# ---------- Resultados de toda la encuesta ----------
class ResultadosEncuestaType(graphene.ObjectType):
    survey_id = graphene.Int()
    titulo = graphene.String()
    preguntas = graphene.List(ResultadoPreguntaType)


class Query(graphene.ObjectType):
    all_surveys = graphene.List(SurveyType)
    survey = graphene.Field(SurveyType, id=graphene.Int(required=True))

    resultados_encuesta = graphene.Field(ResultadosEncuestaType, id=graphene.Int(required=True))

    def resolve_all_surveys(root, info):
        return Survey.objects.all()

    def resolve_survey(root, info, id):
        return Survey.objects.get(pk=id)

    # ============= RESULTADOS =============
    def resolve_resultados_encuesta(root, info, id):
        survey = Survey.objects.get(pk=id)
        preguntas_resultado = []

        for pregunta in survey.questions.all():
            opciones_resultado = []

            for opcion in pregunta.options.all():
                votos = Answer.objects.filter(option=opcion).count()

                opciones_resultado.append(
                    ResultType(
                        option_id=opcion.id,
                        option_text=opcion.text,
                        votos=votos
                    )
                )

            preguntas_resultado.append(
                ResultadoPreguntaType(
                    question_id=pregunta.id,
                    question_text=pregunta.text,
                    resultados=opciones_resultado
                )
            )

        return ResultadosEncuestaType(
            survey_id=survey.id,
            titulo=survey.title,
            preguntas=preguntas_resultado
        )


# =======================
#   MUTATIONS (CRUD)
# =======================

class CreateSurvey(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()

    survey = graphene.Field(SurveyType)

    @classmethod
    def mutate(cls, root, info, title, description=None):
        survey = Survey.objects.create(
            title=title,
            description=description or ""
        )
        return CreateSurvey(survey=survey)


class CreateQuestion(graphene.Mutation):
    class Arguments:
        survey_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    question = graphene.Field(QuestionType)

    @classmethod
    def mutate(cls, root, info, survey_id, text):
        survey = Survey.objects.get(pk=survey_id)
        question = Question.objects.create(survey=survey, text=text)
        return CreateQuestion(question=question)


class CreateOption(graphene.Mutation):
    class Arguments:
        question_id = graphene.ID(required=True)
        text = graphene.String(required=True)

    option = graphene.Field(OptionType)

    @classmethod
    def mutate(cls, root, info, question_id, text):
        question = Question.objects.get(pk=question_id)
        option = Option.objects.create(question=question, text=text)
        return CreateOption(option=option)


class CreateAnswer(graphene.Mutation):
    class Arguments:
        survey_id = graphene.Int(required=True)
        question_id = graphene.Int(required=True)
        option_id = graphene.Int(required=True)

    answer = graphene.Field(AnswerType)

    @classmethod
    def mutate(cls, root, info, survey_id, question_id, option_id):
        survey = Survey.objects.get(pk=survey_id)
        question = Question.objects.get(pk=question_id)
        option = Option.objects.get(pk=option_id)

        answer = Answer.objects.create(
            survey=survey,
            question=question,
            option=option
        )
        return CreateAnswer(answer=answer)


class Mutation(graphene.ObjectType):
    create_survey = CreateSurvey.Field()
    create_question = CreateQuestion.Field()
    create_option = CreateOption.Field()
    create_answer = CreateAnswer.Field()


# ---------- SCHEMA GLOBAL ----------
schema = graphene.Schema(query=Query, mutation=Mutation)
