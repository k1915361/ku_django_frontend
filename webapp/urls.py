from django.urls import path

from . import views

app_name = 'webapp'
urlpatterns = [
    path("login/", views.login, name="login view"),
    path("", views.index, name="index"),
    # path("profile/", views.profile_view, name="profile"),
    # path("logout/", views.logout_view, name="logout"),
    # path("login-retry-view/", views.login_retry_view, name="login retry view"),
    # path("login-view/login/", views.login_user, name="login"),
    # path("login-retry-view/login/", views.login_user, name="retry login"),
    # path("register-view/", views.register_view, name="register view"),
    # path("register-retry-view/", views.register_retry_view, name="register retry view"),
    # path("register-view/register/", views.register, name="register"),
    # path("register-retry-view/register/", views.register, name="register retry "),
    # path("upload-model/", views.upload_model, name="upload model form"),
    # path("upload-folder/", views.upload_folder, name="upload folder view"),
    # path("public-dataset-list-view/", views.public_dataset_list_view, name="public dataset list view"),
    # path("public-model-list-view/", views.public_model_list_view, name="public model list view"),
    # path("public-dataset-data-view:<int:pk>/", views.public_dataset_list_view, name="public-dataset-data-view"),
    # path("private-dataset-list-view/", views.private_dataset_list_view, name="private-dataset-list-view"),
    # path("private-model-list-view/", views.private_model_list_view, name="private-model-list-view"),
    # path("user_dataset_list_path_view/", views.user_dataset_list_path_view, name="user_dataset_list_path_view"),
    # path("process-model-options/", views.process_model_options_view, name="process model options"),
    # path("human-reinforced-feedback/", views.human_reinforced_feedback_view, name="human reinforced feedback view"),
    # path("final-task-analytics/", views.final_task_analytics_view, name="final task analytics"),
    # path("previous-tasks/", views.previous_tasks_view, name="previous tasks"),
    # path("personal-model-repo/", views.personal_model_repo_view, name="personal model repo"),
    # path("personal-dataset-repo/", views.personal_dataset_repo_view, name="personal dataset repo"),
    # path("personal-dataset-analysis/", views.personal_dataset_analysis_view, name="personal dataset analysis"),
]
