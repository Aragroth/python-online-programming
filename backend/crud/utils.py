import time


def cache_timeout(timeout: int):
    """
    Кэширующий декоратор для запросов к базе данных, параметра timeout
    указывается в секундах (написан для асинхронных методов)
    """

    def cache_wrapper(func):
        cache_value = None
        time_start = time.time()

        async def cacher(self, *args, **kwargs):
            nonlocal cache_value, time_start

            if cache_value is None:
                cache_value = await func(self, *args, **kwargs)

            elif time.time() - time_start >= timeout:
                cache_value = await func(self, *args, **kwargs)
                time_start = time.time()

            return cache_value

        return cacher

    return cache_wrapper


all_tasks_query = [
    {
        "$lookup": {
            "from": "sections",
            "localField": "section_name",
            "foreignField": "_id",
            "as": "section_name"
        }
    },
    {
        "$project": {
            "description": 1,
            "title": 1,
            "examples": 1,
            "photo": 1,
            "short_title": 1,
            "section_name": {"$arrayElemAt": ["$section_name", 0]},
        }
    },
    {
        "$project": {
            "description": 1,
            "title": 1,
            "examples": 1,
            "photo": 1,
            "short_title": 1,
            "section_name": "$section_name.section_name"
        },
    },
    {
        "$sort": {"section_name": 1, "short_title": 1}
    },
    {
        "$group": {
            "_id": "$section_name",
            "tasks": {
                "$push": {
                    "task_uuid": "$_id",
                    "description": "$description",
                    "title": "$title",
                    "examples": "$examples",
                    "photo": "$photo",
                    "short_title": "$short_title",
                }
            }
        }
    },
    {
        "$project": {
            "tasks.examples.is_answer_empty": 0,
        },
    },
]
