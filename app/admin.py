from app.backend.session import async_engine
from app.models import *
from starlette_admin.contrib.sqla import ModelView, Admin
from starlette_admin import I18nConfig

admin = Admin(async_engine, title='FastApi Auth', route_name='admin', i18n_config=I18nConfig(default_locale='ru'))

# models
admin.add_view(ModelView(User, icon='fa-solid fa-users', name='Users', label='Users'))
