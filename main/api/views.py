from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from main import models
from . import serializers as my_serializers
from rest_framework import serializers as rest_serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter,inline_serializer
from main.api.utils import CustomPagination

######################################
# Status
######################################

class StatusApiView(APIView):

    @extend_schema(
        request=my_serializers.StatusSerializer,
        responses={200: my_serializers.StatusSerializer(many=True)},
        summary="Get all statuses",
        parameters=[
            OpenApiParameter(
                name="company_uuid",
                description="Company UUID",
                required=False,
                type=str
            ),
        ],
        description="Get all statuses",
        tags=["Status"],
    )
    def get(self, request):
        """
        Get all statuses
        """
        statuses = models.Status.objects.filter(is_active=True)
        if request.query_params.get("company_uuid"):
            statuses = statuses.filter(company_uuid=request.query_params.get("company_uuid"))
        serializer = my_serializers.StatusSerializer(statuses, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=my_serializers.StatusSerializer,
        responses={200: my_serializers.StatusSerializer},
        summary="Create a new status",
        description="Create a new status",
        tags=["Status"],
    )
    def post(self, request):
        """
        Create a new status
        """

        serializer = my_serializers.StatusSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        responses={200: {"message": "Status deleted successfully"}},
        summary="Delete a status",
        description="Delete a status",
        tags=["Status"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Status UUID",
                required=True,
                type=str
            ),
        ],
    )
    def delete(self, request):
        """
        Delete a status
        """
        status = models.Status.objects.get(uuid=request.query_params.get("uuid"))
        status.is_active = False
        status.save()
        return Response({"message": "Status deleted successfully"})
    
    @extend_schema(
        request=inline_serializer(
            name="UpdateStatusSerializer",
            fields={
                "name": rest_serializers.CharField(required=False),
                "description": rest_serializers.CharField(required=False),
                "company_uuid": rest_serializers.UUIDField(required=False),
            },
        ),
        responses={200: my_serializers.StatusSerializer},
        summary="Update a status",
        description="Update a status",
        tags=["Status"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Status UUID",
                required=True,
                type=str
            ),
        ],
    )
    def patch(self, request):
        """
        Update a status
        """
        status = models.Status.objects.get(uuid=request.query_params.get("uuid"))
        serializer = my_serializers.StatusSerializer(status, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

######################################
# LeadType
######################################

class LeadTypeApiView(APIView):

    @extend_schema(
        request=my_serializers.LeadTypeSerializer,
        responses={200: my_serializers.LeadTypeSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="company_uuid",
                description="Company UUID",
                required=False,
                type=str
            ),
        ],
        summary="Get all lead types",
        description="Get all lead types",
        tags=["LeadType"],
    )
    def get(self, request):
        """
        Get all lead types
        """
        lead_types = models.LeadType.objects.filter(is_active=True)
        if request.query_params.get("company_uuid"):
            lead_types = lead_types.filter(company_uuid=request.query_params.get("company_uuid"))
        serializer = my_serializers.LeadTypeSerializer(lead_types, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=my_serializers.LeadTypeSerializer,
        responses={200: my_serializers.LeadTypeSerializer},
        summary="Create a new lead type",
        description="Create a new lead type",
        tags=["LeadType"],
    )
    def post(self, request):
        """
        Create a new lead type
        """
        serializer = my_serializers.LeadTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @extend_schema(
        responses={200: {"message": "Lead type deleted successfully"}},
        summary="Delete a lead type",
        description="Delete a lead type",
        tags=["LeadType"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Lead type UUID",
                required=True,
                type=str
            ),
        ],
    )
    def delete(self, request):
        """
        Delete a lead type
        """
        lead_type = models.LeadType.objects.get(uuid=request.query_params.get("uuid"))
        lead_type.is_active = False
        lead_type.save()
        return Response({"message": "Lead type deleted successfully"})
    
    @extend_schema(
        request=my_serializers.LeadTypeSerializer,
        responses={200: my_serializers.LeadTypeSerializer},
        summary="Update a lead type",
        description="Update a lead type",
        tags=["LeadType"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Lead type UUID",
                required=True,
                type=str
            ),
        ],
    )
    def patch(self, request):
        """
        Update a lead type
        """
        lead_type = models.LeadType.objects.get(uuid=request.query_params.get("uuid"))
        serializer = my_serializers.LeadTypeSerializer(lead_type, data=request.data, partial=True)  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
######################################
# Lead
######################################

class LeadApiView(APIView):

    @extend_schema(
        request=my_serializers.LeadSerializer,
        responses={200: my_serializers.LeadSerializer(many=True)},
        summary="Get all leads",
        description="Get all leads",
        tags=["Lead"],
        parameters=[
            OpenApiParameter(
                name="type",
                description="Type UUID",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="status",
                description="Status UUID",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="company_uuid",
                description="Company UUID",
                required=False,
                type=str
            ),
        ],  
    )
    def get(self, request):
        """
        Get all leads
        """
        leads = models.Lead.objects.filter(is_active=True)
        if request.query_params.get("type"):
            leads = leads.filter(type__uuid=request.query_params.get("type"))
        
        if request.query_params.get("status"):
            leads = leads.filter(type__status__uuid=request.query_params.get("status"))

        if request.query_params.get("company_uuid"):
            leads = leads.filter(type__company_uuid=request.query_params.get("company_uuid"))
            
        serializer = my_serializers.LeadSerializer(leads, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=my_serializers.LeadSerializer,
        responses={200: my_serializers.LeadSerializer},
        summary="Create a new lead",
        description="Create a new lead",
        tags=["Lead"],
    )
    def post(self, request):
        """
        Create a new lead
        """
        serializer = my_serializers.LeadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @extend_schema(
        responses={200: {"message": "Lead deleted successfully"}},
        summary="Delete a lead",
        description="Delete a lead",
        tags=["Lead"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Lead UUID",
                required=True,
                type=str
            ),
        ],
    )
    def delete(self, request):
        """
        Delete a lead
        """
        lead = models.Lead.objects.get(uuid=request.query_params.get("uuid"))
        lead.is_active = False
        lead.save()
        return Response({"message": "Lead deleted successfully"})
    
    @extend_schema(
        request=my_serializers.LeadSerializer,
        responses={200: my_serializers.LeadSerializer},
        summary="Update a lead",
        description="Update a lead",
        tags=["Lead"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Lead UUID",
                required=True,
                type=str
            ),
        ],
    )
    def patch(self, request):
        """
        Update a lead
        """
        lead = models.Lead.objects.get(uuid=request.query_params.get("uuid"))
        if request.data.get("type"):
            old_type = models.LeadType.objects.get(uuid=request.data.get("type"))
            if old_type != lead.type:
                models.LeadHistory.objects.create(
                    lead=lead,
                    type=old_type,
                    status=lead.type.status
                )
        serializer = my_serializers.LeadSerializer(lead, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

######################################
# LeadHistory
######################################

class LeadHistoryApiView(APIView):

    @extend_schema(
        responses={200: my_serializers.LeadHistorySerializer(many=True)},
        summary="Get all lead histories",
        description="Get all lead histories",
        parameters=[
            OpenApiParameter(
                name="page_size",
                description="Page size",
                required=False,
                type=int
            ),
            OpenApiParameter(
                name="page",
                description="Page number",
                required=False,
                type=int
            ),
        ],
        tags=["LeadHistory"],
    )
    def get(self, request):
        """
        Get all lead histories
        """
        lead_histories = models.LeadHistory.objects.filter(is_active=True)
        paginator = CustomPagination()
        paginator.page_size = request.query_params.get("page_size", 10)
        lead_histories = paginator.paginate_queryset(lead_histories, request)
        serializer = my_serializers.LeadHistorySerializer(lead_histories, many=True)
        return paginator.get_paginated_response(serializer.data)



















