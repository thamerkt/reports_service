from rest_framework import serializers
from .models import Rapport, RapportData
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class RapportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapportData
        fields = '__all__'
    
    def validate_metric_value(self, value):
        """Ensure metric_value is a valid number"""
        if not isinstance(value, (int, float)):
            raise serializers.ValidationError("Metric value must be a number")
        return value
    
    def validate(self, data):
        """Additional validation for the entire RapportData"""
        errors = {}
        
        # Validate rapport exists
        if 'rapport' not in data:
            errors['rapport'] = "This field is required"
        elif not Rapport.objects.filter(id=data['rapport'].id).exists():
            errors['rapport'] = "Invalid rapport ID"
            
        # Validate required fields
        if 'metric_name' not in data or not data['metric_name']:
            errors['metric_name'] = "This field is required"
            
        if 'metric_value' not in data:
            errors['metric_value'] = "This field is required"
            
        if errors:
            raise serializers.ValidationError(errors)
            
        return data

class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = '__all__'
    
    def validate_date_created(self, value):
        """Ensure date_created is not in the future"""
        if value > timezone.now():
            raise serializers.ValidationError("Date created cannot be in the future")
        return value
    
    def validate_start_date(self, value):
        """Basic start date validation"""
        if not value:
            raise serializers.ValidationError("Start date is required")
        return value
    
    def validate_end_date(self, value):
        """Basic end date validation"""
        if not value:
            raise serializers.ValidationError("End date is required")
        return value
    
    def validate(self, data):
        """Cross-field validation for Rapport"""
        errors = {}
        
        # Validate date sequence
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                errors['end_date'] = "End date must be after start date"
                
        # Validate required fields
        required_fields = ['type', 'title', 'user', 'is_scheduled']
        for field in required_fields:
            if field not in data or not data[field]:
                errors[field] = "This field is required"
                
        # Validate schedule_frequency if is_scheduled is True
        if data.get('is_scheduled') and not data.get('schedule_frequency'):
            errors['schedule_frequency'] = "This field is required when is_scheduled is True"
            
        if errors:
            raise serializers.ValidationError(errors)
            
        return data