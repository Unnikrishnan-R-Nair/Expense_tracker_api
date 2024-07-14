from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework import serializers

from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from budget.serializers import UserSerializer, ExpenseSerializer, IncomeSerializer
from budget.models import Expense, Income
from budget.permissions import IsOwnerOrIsAdmin

from django.utils import timezone
from django.db.models import Sum


class SignUpView(APIView):

    def post(self, request, *args, **kwargs):

        data = request.data 

        serializer_instance = UserSerializer(data=data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)
    

# APIView
class ExpenseListCreateAPIView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwnerOrIsAdmin]

    def get(self, request, *args, **kwargs):

        qs = Expense.objects.filter(owner=request.user)

        serializer_instance = ExpenseSerializer(qs, many=True)

        return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):

        serializer_instance = ExpenseSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
        
        return Response(data=serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ExpenseDetailUpdateDestroyAPIView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        expense_obj = Expense.objects.get(id=kwargs.get("pk"))

        serializer_instance = ExpenseSerializer(expense_obj)

        return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
    

    def put(self, request, *args, **kwargs):
        
        expense_obj = Expense.objects.get(id=kwargs.get("pk"))
        serializer_instance = ExpenseSerializer(data=request.data, instance=expense_obj)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
        return Response(data=serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        
        expense_obj = Expense.objects.get(id=kwargs.get("pk"))

        expense_obj.delete()

        return Response(data={"message": "resource deleted."})
    


class ExpenseViewSetView(ViewSet):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdmin]

    def list(self, request, *args, **kwargs):
        qs = Expense.objects.filter(owner=request.user)
        serializer_instance = ExpenseSerializer(qs, many=True)
        return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer_instance = ExpenseSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        qs = Expense.objects.get(id=kwargs.get("pk"))
        serializer_instance = ExpenseSerializer(qs)
        return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        obj = Expense.objects.get(id=kwargs.get("pk"))
        serializer_instance = ExpenseSerializer(data=request.data, instance=obj)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data, status=status.HTTP_200_OK)
        return Response(data=serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        obj = Expense.objects.get(id=kwargs.get("pk"))
        obj.delete()
        return Response(data={"message": "resource deleted"})



class ExpenseListCreateView(ListAPIView, CreateAPIView):
    
    serializer_class = ExpenseSerializer

    queryset = Expense.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        if 'month' in self.request.query_params:
            month = self.request.query_params.get('month')
            year = self.request.query_params.get('year')
            return Expense.objects.filter(
                owner = self.request.user, 
                created_date__month=month,
                created_date__year=year,
                ).order_by('-id') 
        return Expense.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    
class ExpenseDetailUpdateDestroyView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):

    serializer_class = ExpenseSerializer

    queryset = Expense.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdmin]



class IncomeListCreateView(ListAPIView, CreateAPIView):

    serializer_class = IncomeSerializer

    queryset = Income.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdmin]

    def  get_queryset(self):
        # print(self.request.query_params)
        if 'month' in self.request.query_params:
            month = self.request.query_params.get('month')
            year = self.request.query_params.get('year')
            return Income.objects.filter(
                owner = self.request.user, 
                created_date__month=month,
                created_date__year=year,
                ).order_by('-id')
        return Income.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    
class IncomeDetailUpdateDestroyView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):

    serializer_class = IncomeSerializer

    queryset = Income.objects.all()

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdmin]



class TransactionSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrIsAdmin]

    def get(self, request, *args, **kwargs):

        # cur_year = timezone.now().year
        # cur_month = timezone.now().month

        print(request.query_params)

        cur_year = request.query_params.get('year')
        cur_month = request.query_params.get('month')

        all_expenses = Expense.objects.filter(owner=request.user, created_date__year=cur_year, created_date__month=cur_month)

        all_incomes = Income.objects.filter(owner=request.user, created_date__year=cur_year, created_date__month=cur_month)

        expense_total = all_expenses.values("amount").aggregate(total=Sum("amount"))
        income_total = all_incomes.values("amount").aggregate(total=Sum("amount"))

        expense_summary = list(all_expenses.values("category").annotate(total=Sum("amount")))
        income_summary = list(all_incomes.values("category").annotate(total=Sum("amount")))

        total_income = income_total["total"] or 0
        total_expense = expense_total["total"] or 0
        savings = total_income - total_expense

        summary = {
                    "expense_total": total_expense, 
                    "expense_summary": expense_summary, 
                    "income_total": total_income,
                    "income_summary": income_summary,
                    "current_month_savings": savings
                    
                    }
        
        # print("expense_total", expense_total)
        # print("income_total", income_total)
        # print("expense_summary", expense_summary)
        # print("income_summary", income_summary)
        # print("savings", savings)
        

        return Response(data=summary)
    



