from django.urls import path, include, re_path
from news_app.views import *
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Default description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

# use it for additional if needed
router = DefaultRouter()
router.register('companies2', CompanyViewSet, 'companies')
router.register('users2', UserDetailViewSet, 'users')
router.register('posts2', PostViewSet, 'posts')


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('me/', UserMeViewSet.as_view({'get': 'get_me',
                                       'patch': 'partial_update',
                                       'delete': 'destroy',
                                       'put': 'update'})),
    path('users/', UserViewSet.as_view({'get': 'list',
                                        'post': 'create',
                                        'delete': 'destroy',
                                        'patch': 'partial_update',
                                        'put': 'update'})),
    path('users/<id>/', UserViewSet.as_view({'get': 'retrieve',
                                             'post': 'create',
                                             'patch': 'partial_update',
                                             'put': 'update'})),
    path('companies/', CompanyViewSet.as_view({'get': 'list',
                                               'post': 'create'})),
    path('companies/<id>/', CompanyViewSet.as_view({'get': 'retrieve',
                                                    'post': 'create',
                                                    'patch': 'partial_update',
                                                    'put': 'update'})),
    path('posts/', PostViewSet.as_view({'get': 'list',
                                        'post': 'my_create'})),
    path('posts/<id>/', PostViewSet.as_view({'get': 'retrieve',
                                             'post': 'create',
                                             'patch': 'partial_update',
                                             'put': 'update'})),
    path('companies_details/', CompaniesDetailsViewSet.as_view({'get': 'list'})),
    path('users_details/', UserDetailViewSet.as_view({'get': 'list'})),
    path('whoami/', WhoAmI.as_view()),
    path('my_company_posts/', MyCompanyPostsViewSet.as_view({'get': 'list'}))
]

urlpatterns += router.urls

