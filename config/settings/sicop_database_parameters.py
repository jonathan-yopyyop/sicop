import environ

env = environ.Env()
environ.Env.read_env()
# for production
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# for local
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
