auth_headers = {
    "Authorization": "Basic Og==",
    "Content-Type": "application/x-www-form-urlencoded"
}

tasks_public_description = [
    {
        "_id": "Циклы",
        "tasks": [
            {
                "task_uuid": "a1bb7a0f-1e29-4428-9eda-8bef26eb88b1",
                "description": "Вводится два числа. Выведите все числа между ними включая последнее",
                "title": "Вывести числа",
                "examples": [
                    {
                        "input": "4\n8",
                        "output": "4\n5\n6\n7\n8\n"
                    }
                ],
                "short_title": "Вывести числа"
            }
        ]
    },
    {
        "_id": "Ввод и вывод",
        "tasks": [
            {
                "task_uuid": "81292eb1-1f24-4723-8f2f-feef58537f42",
                "description": "Вывести данные, переданные на стандартный ввод\r\n\r\nБла-бла-бла",
                "title": "Простой ввод данных",
                "examples": [
                    {
                        "input": "hello world",
                        "output": "hello world\n"
                    },
                    {
                        "input": "Всем привет!",
                        "output": "Всем привет!\n"
                    }
                ],
                "photo": "5fa8ed988240885111374c20",
                "short_title": "Задача А"
            }
        ]
    }
]

# @pytest.fixture
# async def mongo():
#     # TODO сделать отдельную базу для тестов, которую очищать
#     mongo = Database(settings.MONGODB_DATABASE_URI)
#     await mongo.delete_users_with_username("test")
#     await mongo.delete_logs("test")
#     await mongo.create_user("test", "test")
#     await mongo.add_to_completed("test", "f8gk230cvb23")
#     yield mongo


# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "username, password",
#     [
#         ["admin", "admin"],
#     ],
# )
# @pytest.mark.xfail(raises=ZeroDivisionError)
