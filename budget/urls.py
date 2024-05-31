from django.urls import path 

from budget import views

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import ObtainAuthToken

router = DefaultRouter()

# viewset view url
router.register("api/v1/expenses", views.ExpenseViewSetView, basename="expenses")


# print("======",router.urls)

urlpatterns = [
    # APIView urls
    path("api/budget/user/", views.SignUpView.as_view()),

    # Token generator call
    path("api/token/", ObtainAuthToken.as_view()),

    path("api/budget/expenses/", views.ExpenseListCreateAPIView.as_view()),
    path("api/budget/expenses/<int:pk>/", views.ExpenseDetailUpdateDestroyAPIView.as_view()),

    # Expense ListApiView and CreateApiView
    path("api/v2/expenses/", views.ExpenseListCreateView.as_view()),
    # Expense Retrieve, Update and DestroyApiView
    path("api/v2/expenses/<int:pk>/", views.ExpenseDetailUpdateDestroyView.as_view()),

    # Income ListApiView and CreateApiView
    path("api/v2/income/", views.IncomeListCreateView.as_view()),
    # Income Detail, Update and DestroyApiView
    path("api/v2/income/<int:pk>/", views.IncomeDetailUpdateDestroyView.as_view()),

    # Summary 
    path("api/v2/summary/", views.TransactionSummaryView.as_view())

    
] + router.urls