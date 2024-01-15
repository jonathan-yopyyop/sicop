import environ

env = environ.Env()
environ.Env.read_env()
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "sicop",
#         "USER": "myuser",
#         "PASSWORD": "mypass",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }
