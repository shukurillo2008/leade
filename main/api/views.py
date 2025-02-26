from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from main import models
from . import serializers as my_serializers
from rest_framework import serializers as rest_serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter,inline_serializer
from main.api.utils import CustomPagination
from rest_framework import status
######################################
# Board
######################################


class BoardApiView(APIView):

    @extend_schema(
        request=my_serializers.BoardSerializer,
        responses={200: my_serializers.BoardSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="company_uuid",
                description="Company UUID",
                required=False,
                type=str
            ),
        ],
        summary="Get all boards",
        description="Get all boards",
        tags=["Board"],
    )
    def get(self, request):
        """
        Get all boards
        """
        company_uuid = request.GET.get("company_uuid")

        if company_uuid:
            boards = models.Board.objects.filter(is_active=True, company_uuid = company_uuid).order_by('id')
        else:
            boards = models.Board.objects.filter(is_active=True, company_uuid = request.user.id).order_by('id')

        serializer = my_serializers.BoardSerializer(boards, many=True)
        return Response(
            {
                "boards": serializer.data
            }
        )
    

    @extend_schema(
        request=my_serializers.BoardSerializer,
        responses={200: my_serializers.BoardSerializer},
        summary="Create a new board",
        description="Create a new board",
        tags=["Board"],
    )
    def post(self, request):
        """
        Create a new board
        """

        if request.data.get("company_uuid") == None:
            request.data["company_uuid"] = request.user.id
        else:
            request.data["company_uuid"] = request.data.get("company_uuid")

        serializer = my_serializers.BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    @extend_schema(
        responses={200: {"message": "Board deleted successfully"}},
        summary="Delete a board",
        description="Delete a board",
        tags=["Board"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Board UUID",
                required=True,
                type=str
            ),
        ],
    )   
    def delete(self, request):
        """
        Delete a board
        """
        board = models.Board.objects.get(uuid=request.query_params.get("uuid"))
        board.is_active = False
        board.save()
        return Response({"message": "Board deleted successfully"})
    

    @extend_schema(
        request=my_serializers.BoardSerializer,
        responses={200: my_serializers.BoardSerializer},
        summary="Update a board",
        description="Update a board",
        tags=["Board"],
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="Board UUID",
                required=True,
                type=str
            ),
        ],
    )
    def patch(self, request):
        """
        Update a board
        """
        board = models.Board.objects.get(uuid=request.query_params.get("uuid"))
        serializer = my_serializers.BoardSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
                name="board_uuid",
                description="Board UUID",
                required=True,
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
        
        if request.GET.get("board_uuid"):
            statuses = models.Status.objects.filter(is_active=True, board__uuid=request.query_params.get("board_uuid")).order_by('order')
        
        serializer = my_serializers.StatusSerializer(statuses, many=True)
        return Response(
            {
                "statuses": serializer.data
            }
        )

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
        if not request.data.get("order"):
            try:
                biggest_status = models.Status.objects.filter(board = request.data.get("board"), is_active = True).order_by('order').last()
                request.data['order'] = biggest_status.order + 1
            except:
                request.data['order'] = 1


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
                "board_uuid": rest_serializers.UUIDField(required=False),
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
                name="status_uuid",
                description="Status UUID",
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
        lead_types = models.LeadType.objects.filter(is_active=True, status__board__company_uuid = request.user.id).order_by('order')
        if request.query_params.get("status_uuid"):
            lead_types = lead_types.filter(status__uuid=request.query_params.get("status_uuid"))
        serializer = my_serializers.LeadTypeSerializer(lead_types, many=True)
        return Response(
            {
                "leadtypes":serializer.data
            }
        )

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
        if not request.data.get("order"):
            try:
                biggest_lead_type = models.LeadType.objects.filter(status = request.data.get("status"), is_active = True).order_by('order').last()
                request.data['order'] = biggest_lead_type.order + 1
            except:
                request.data['order'] = 1

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
    )
    def get(self, request):
        """
        Get all leads
        """

        leads = models.Lead.objects.filter(is_active=True, type__status__board__company_uuid = request.user.id)

        if request.query_params.get("type"):
            leads = leads.filter(type__uuid=request.query_params.get("type"))
        
        if request.query_params.get("status"):
            leads = leads.filter(type__status__uuid=request.query_params.get("status"))
        
        serializer = my_serializers.LeadSerializer(leads, many=True)
        return Response(
            {
                "leads": serializer.data
            }
        )
    
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
            lead_type = models.LeadType.objects.get(uuid=request.data.get("type"))
            if lead.type != lead_type:
                models.LeadHistory.objects.create(
                    lead=lead,
                    lead_type = lead_type,
                    status=lead_type.status
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


#####################################
# Actions
#####################################


class ChangeOrderApiView(APIView):

    def patch(self, request):
        """
        Change the order of a status
        """
        data = request.data.get("data")
        for item in data:
            status = models.Status.objects.get(uuid=item.get("uuid"))
            status.order = item.get("order")
            status.save()

        return Response({"message": "Status order changed successfully"})

class ClearApiView(APIView):

    @extend_schema(
        responses={200: {"message": "All lead types deleted successfully"}},
        summary="Clear a lead type",
        description="Clear a lead type",
        tags=["Actions"],
        parameters=[
            OpenApiParameter(
                name="board_uuid",
                description="Board UUID",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="status_uuid",
                description="Status UUID",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="leadtype_uuid",
                description="Lead type UUID",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="lead_uuid",
                description="Lead UUID",
                required=False,
                type=str
            ),
        ],
    )
    def delete(self, request):

        board_uuid = request.query_params.get("board_uuid")
        status_uuid = request.query_params.get("status_uuid")
        leadtype_uuid = request.query_params.get("leadtype_uuid")
        lead_uuid = request.query_params.get("lead_uuid")

        if board_uuid:
            board = models.Board.objects.get(uuid=board_uuid)
            board.is_active = False
            board.save()

        if status_uuid:
            status = models.Status.objects.get(uuid=status_uuid)
            status.is_active = False
            status.save()

        if leadtype_uuid:
            lead_type = models.LeadType.objects.get(uuid=leadtype_uuid)
            lead_type.is_active = False
            lead_type.save()

        if lead_uuid:
            lead = models.Lead.objects.get(uuid=lead_uuid)
            lead.is_active = False
            lead.save()

        return Response({"message": "All lead types deleted successfully"})




















