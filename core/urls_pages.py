from django.urls import path
from .views import LoginPageView
from .views import ApplyPageView
from .views import CompletePageView
from .views import HistoryPageView

urlpatterns = [ 
    path("login/", LoginPageView.as_view(), name="login"),
    path("apply/", ApplyPageView.as_view(), name="apply"),
    path("complete/", CompletePageView.as_view(), name="complete"),    
    path("history/", HistoryPageView.as_view(), name="history"), 
]
