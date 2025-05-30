from django.db import models
from questionnaire.models import QuestionnaireItem, Questionnaire



class QuestionnaireResponse(models.Model):

    class Gender(models.TextChoices):
        MALE = 'L', 'Low'
        FEMALE = 'M', 'Medium'
        NO_BINARY = 'NB', 'No Binary'      
        NO_LISTED = 'NL', 'No Listed',
        UNKNOWN = 'U', 'Unknown'
       

    class Role(models.TextChoices): 
        DEV  = 'DEV', 'Developer'
        UX = 'UX', 'UX'
        LEADER = 'LEAD', 'Leader'

    class AgileExperience(models.TextChoices):
        NEVER = 'NEVER', 'Nunca trabaje con métodos ágiles'
        OCCASIONAL = 'OCCASIONAL', 'He trabajado ocasionalmente con métodos ágiles'
        USUAL = 'USUAL', 'Trabajo regularmente con métodos ágiles'

    class ProjectType(models.TextChoices):
        WEB = 'WEB', 'Aplicaciones web'
        MOBILE = 'MOBILE', 'Aplicaciones para móviles'
        OTHER = 'OTHER', 'Otra (indicar opción)'

    class SprintPlanningExperience(models.TextChoices):
        USUAL = 'USUAL', 'Habitualmente participo'
        SOMETIMES = 'SOMETIMES', 'Algunas veces he participado'
        ONLY_CRITICAL = 'ONLY_CRITICAL', 'Participo sólo cuando hay ítems críticos relacionados con mi rol'
        NEVER = 'NEVER', 'Nunca participo de esas actividades'

    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=2, choices=Gender.choices)
    role = models.CharField(max_length=4, choices=Role.choices)
    agile_experience = models.CharField(
        max_length=10,
        choices=AgileExperience.choices,
        default=AgileExperience.NEVER
    )
    project_type = models.CharField(
        max_length=10,
        choices=ProjectType.choices
    )
    project_type_other = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    sprint_planning_experience = models.CharField(
        max_length=15,
        choices=SprintPlanningExperience.choices
    )

    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questionnaire_responses', null=True)


class QuestionnaireResponseItem(models.Model):
    response = models.ForeignKey(QuestionnaireResponse, on_delete=models.CASCADE, related_name='response_items')
    questionnaire_item = models.ForeignKey(
        QuestionnaireItem,
        on_delete=models.CASCADE,
        related_name='response_items'
    )