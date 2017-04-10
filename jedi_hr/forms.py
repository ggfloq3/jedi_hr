from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from jedi_hr.models import Jedi, Candidate


class CandidateQuizForm(forms.Form):
    def __init__(self, candidate, *args, **kwargs):
        super(CandidateQuizForm, self).__init__(*args, **kwargs)

        quiz = candidate.get_quiz()
        # создание полей формы(вопросов) на основе теста для этого кандидата
        for x in quiz.question_set.all():
            name = 'question_{}'.format(x.id)
            self.fields[name] = forms.BooleanField(label=x.text, required=False)


class JediCandidateForm(forms.ModelForm):
    def __init__(self, jedi_id, *args, **kwargs):
        super(JediCandidateForm, self).__init__(*args, **kwargs)
        self.jedi_id = jedi_id
        self.initial = {'jedi_master': jedi_id}
        self.fields['jedi_master'].widget.attrs['style'] = 'display:none'
        self.fields['jedi_master'].label = ''

    def clean(self):
        max_padawan = settings.JEDI_MAXIMUM_PADAWAN
        if Jedi.objects.get(id=self.jedi_id).candidate_set.all().count() >= max_padawan:
            raise ValidationError(
                'Слишком много учеников у этого джедая(максимум {})'.format(max_padawan))
        else:
            return super(JediCandidateForm, self).clean()

    class Meta:
        model = Candidate
        fields = ('jedi_master',)
