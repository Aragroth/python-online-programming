from flask_mongoengine import MongoEngine

# держим расширения отдельно, чтобы избежать цикличного импорта
db = MongoEngine()
