from .base_form import *
from ..models.tournament import Tournament
from ..enums.AjaxActions import AjaxAction
from django import forms
from django.core import serializers
from ..serializers.clan_user_roles_serializer import ClanUserRolesSerializer,ClanUserRoles


class RequestTournamentsForm(BaseForm):
    def __init__(self,*args, **kwargs):
        super(RequestTournamentsForm, self).__init__(AjaxAction.GETTOURNAMENTS, *args, **kwargs)


    def handle(self,request):
        try:
            tours=serializers.serialize('json',Tournament.objects.all())
        except:
            return self.response(False,'Something went wrong')#TODO better exception
        else:
            return self.response(True,{'data':tours})


    class Meta:
        model=Tournament
        fields=()



class CreateTournamentForm(BaseForm):
    def __init__(self,*args, **kwargs):
        super(CreateTournamentForm, self).__init__(AjaxAction.CREATETOURNAMENT, *args, **kwargs)


    def handle(self,request):
        try:
            tour=self.save()
        except:
            return self.response(False,'Something went wrong')#TODO better exception
        else:
            return self.response(True,{'data':{'name':tour.name,'description':tour.description}})


    class Meta:
        model=Tournament
        fields=('name','description')


class EditTournamentForm(BaseForm):
    pk_id=forms.IntegerField(min_value=0,widget=forms.HiddenInput(),required=True)

    def __init__(self,*args, **kwargs):
        super(EditTournamentForm, self).__init__(AjaxAction.EDITTOURNAMENT, *args, **kwargs)

    def handle(self, request):
        try:
            tour = Tournament.objects.get(pk=int(self.cleaned_data['pk_id']))
            tour.name=self.cleaned_data['name']
            tour.description=self.cleaned_data['description']
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception

        else:

            return self.response(True, {'data': {'name': tour.name,'description':tour.description, 'action': 'deleted'}})

    class Meta:
        model=Tournament
        fields=('pk_id','name','description')


class DeleteTournamentForm(BaseForm):
    pk_id=forms.IntegerField(min_value=0,widget=forms.HiddenInput(),required=True)

    
    def __init__(self,*args, **kwargs):
        super(DeleteTournamentForm, self).__init__(AjaxAction.DELETETOURNAMENT, *args, **kwargs)


    def handle(self,request):
        try:
            tour=Tournament.objects.get(pk=int(self.cleaned_data['pk_id']))
            tour.delete()
        except BaseException as e:
            return self.response(False, 'Something went wrong: '+str(e))  # TODO better exception
        
        else:
            
            return self.response(True,{'data':{'name':tour.name,'action':'deleted'}})

    class Meta:
        model=Tournament
        fields=('pk_id',)