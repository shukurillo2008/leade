from rest_framework import serializers
from main import models


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        exclude = ["is_active", "id"]




class StatusSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(slug_field="uuid", queryset=models.Board.objects.filter(is_active=True))
    board_name = serializers.CharField(source="board.name", read_only=True)

    class Meta:
        model = models.Status
        exclude = ["is_active", "id"]
    
    

        
class LeadTypeSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(slug_field="uuid", queryset=models.Status.objects.filter(is_active=True))
    status_name = serializers.SlugRelatedField(slug_field="name", read_only=True)
    
    class Meta:
        model = models.LeadType
        exclude = ["is_active", "id"]

        
class LeadSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field="uuid", queryset=models.LeadType.objects.filter(is_active=True))
    type_name = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = models.Lead
        exclude = ["is_active", "id"]
        

class LeadHistorySerializer(serializers.ModelSerializer):
    lead = serializers.SlugRelatedField(slug_field="uuid", queryset=models.Lead.objects.filter(is_active=True))
    lead_title = serializers.CharField(source="lead.title", read_only=True)
    status = serializers.SlugRelatedField(slug_field="uuid", queryset=models.Status.objects.filter(is_active=True))
    status_name = serializers.CharField(source="status.name", read_only=True)
    
    class Meta:
        model = models.LeadHistory
        exclude = ["is_active", "id"]

        



