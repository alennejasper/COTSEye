"""
Django settings for configurations project.

Generated by "django-admin startproject" using Django 5.0.

For more information on this file, see https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see https://docs.djangoproject.com/en/5.0/ref/settings/
"""


from pathlib import Path

# import dj_database_url
import os


#Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


#Quick-start development settings - unsuitable for production
#See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
#SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vz!lj^+vf@!(6&07mgt6r*u72%!g-2@tqa*3fqc_g1y=!$x(hk"


#SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["*"]


#Application definition
INSTALLED_APPS = [
    "jazzmin",
    
    "django.contrib.admin",
    
    "django.contrib.auth",
    
    "django.contrib.contenttypes",
    
    "django.contrib.sessions",
    
    "django.contrib.messages",
    
    "django.contrib.staticfiles",
    
    "django.contrib.sites",
    
    "allauth",

    "allauth.account",
    
    "allauth.socialaccount",
    
    "allauth.socialaccount.providers.google",
    
    "allauth.socialaccount.providers.facebook",
    
    "authentications",
    
    "reports",

    "managements",
    
    "auxiliaries"
]


SITE_ID = 1


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    "django.contrib.sessions.middleware.SessionMiddleware",
    
    "django.middleware.common.CommonMiddleware",
    
    "django.middleware.csrf.CsrfViewMiddleware",
    
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    
    "django.contrib.messages.middleware.MessageMiddleware",
    
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    "allauth.account.middleware.AccountMiddleware",
]


ROOT_URLCONF = "configurations.urls"


TEMPLATES = [
    {   
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        
        "DIRS": [os.path.join(BASE_DIR, "statics/templates/")],
        
        "APP_DIRS": True,
        
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                
                "django.template.context_processors.request",
                
                "django.contrib.auth.context_processors.auth",
                
                "django.contrib.messages.context_processors.messages",
                
                "authentications.processors.coordinates",
            ],
            
        },

    },

]


WSGI_APPLICATION = "configurations.wsgi.application"


#Database
#https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        
        "OPTIONS": {
            "options": "-c search_path=cotseye_schema"
        },

        "NAME": "cotseye_yekg",
        
        "USER": "cotseye_yekg_user",
        
        "PASSWORD": "IXNRnNoWxcHGXCfbZzi7aUbraeOIkulw",
        
        "HOST": "dpg-cq2ffbrv2p9s73erneog-a.singapore-postgres.render.com",
        
        "PORT": "5432",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
        
#         "OPTIONS": {
#             "options": "-c search_path=cotseye_schema"
#         },

#         "NAME": "cotseye",
        
#         "USER": "postgres",
        
#         "PASSWORD": "lucyheaven",
        
#         "HOST": "localhost",
        
#         "PORT": "5432",
#     }
# }

# postgresql://cotseye_yekg_user:IXNRnNoWxcHGXCfbZzi7aUbraeOIkulw@dpg-cq2ffbrv2p9s73erneog-a.singapore-postgres.render.com/cotseye_yekg

# DATABASES["default"] = dj_database_url.parse("postgres://cotseye_9y7b_user:nveiDlWwh3jjBcHXHQmohACFWX2jWRf1@dpg-cpo4h788fa8c73bb5u50-a.singapore-postgres.render.com/cotseye_9y7b")

#Password validation
#https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    #{
    #    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    #},

    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    #{
    #    "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    #},

    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


#Internationalization
#https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Manila"

USE_I18N = True

USE_TZ = True

DATETIME_FORMAT = "%b. %j, %Y %I:%M %P"


#Static files (CSS, JavaScript, Images)
#https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "statics/"

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "statics")
# ]

STATIC_ROOT = os.path.join(BASE_DIR, "statics")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "assets/"

MEDIA_ROOT = os.path.join(BASE_DIR, "statics/assets")


#Default primary key field type
#https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "authentications.Account"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

SOCIALACCOUNT_ADAPTER = "authentications.adapters.SocialAccountAdapter"

SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_EMAIL_REQUIRED = False

SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_QUERY_EMAIL = False

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            
            "email",
        ],

        "AUTH_PARAMS": {
            "access_type": "online",
        }
    },

    "facebook": {
        "SCOPE": [
            "public_profile",
            
            "email",
        ],

        "AUTH_PARAMS": {
            "access_type": "online",
        }
    },
}

ACCOUNT_AUTHENTICATION_METHOD = "username"

ACCOUNT_EMAIL_REQUIRED = False

ACCOUNT_EMAIL_VERIFICATION = "none"

ACCOUNT_UNIQUE_EMAIL = False

ACCOUNT_USER_MODEL_EMAIL_FIELD = None


CSRF_FAILURE_VIEW = "authentications.views.ForgeryReadRedirect"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = "cotseye.information@gmail.com"

EMAIL_HOST_PASSWORD = "vqmurhtaaynudqku"

EMAIL_PORT = 587

EMAIL_USE_TLS = True


RECAPTCHA_PUBLIC_KEY = "6LeLKv0pAAAAAK9mrndyaPeMfKa7zrY6avR_2rlc"

RECAPTCHA_PRIVATE_KEY = "6LeLKv0pAAAAAGD_uAO92iSAh5VVkwMeNHPdG3ag"


JAZZMIN_SETTINGS = {
    "changeform_format": "horizontal_tabs",
        
    "copyright": "Team Rocket",

    "custom_css": "css/admin/control/index/index.css", 

    "navigation_expanded": False,

    "show_sidebar": False,

    "site_brand": "COTSEYE",
    
    "site_logo": "assets/icons/logo.jpg",

    "site_title": "Home",
}