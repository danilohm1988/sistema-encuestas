import graphene
from surveys.schema import Query as SurveysQuery, Mutation as SurveysMutation

class Query(SurveysQuery, graphene.ObjectType):
    # En el futuro puedes combinar más Query de otras apps
    pass

class Mutation(SurveysMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
