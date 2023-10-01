from requests.exceptions import RequestException
from django.db import connection
from django.http import JsonResponse

from rest_framework.decorators import api_view


def rows_to_json(cursor, rows):
    keys = [i[0] for i in cursor.description]
    result_array = []
    for row in rows:
        result_array.append({k: v for k, v in zip(keys, row)})
    return {i+1: v for i, v in enumerate(result_array)}

def user_all_lessons(uid):
    q = """
SELECT DISTINCT l.code, l.name, ul.length_viewed, ul.is_viewed
FROM pages_userlesson ul
INNER JOIN pages_product_user pu
    ON ul.user_id = pu.user_id
INNER JOIN pages_lesson l
    ON ul.lesson_id = l.id
WHERE ul.user_id = %s
"""
    with connection.cursor() as cursor:
        cursor.execute(q % (uid))
        rows = cursor.fetchall()
        result = rows_to_json(cursor, rows)

    return JsonResponse(result)

def user_product_lessons(uid, pid):
    q = """
SELECT DISTINCT l.code, l.name, ul.length_viewed, ul.is_viewed, ul.last_viewed
FROM pages_userlesson ul
INNER JOIN pages_product_user pu
    ON ul.user_id = pu.user_id
INNER JOIN pages_lesson l
    ON ul.lesson_id = l.id
WHERE ul.user_id = %s
    AND pu.product_id = %s
    AND l.id in (
        SELECT lesson_id
        FROM pages_product_lesson
        WHERE product_id = %s
        )
"""
    with connection.cursor() as cursor:
        cursor.execute(q % (uid, pid, pid))
        rows = cursor.fetchall()
        result = rows_to_json(cursor, rows)

    return JsonResponse(result)

@api_view(['GET'])
def get_user_lessons(request):
    if ("user_id" not in request.GET) or (len(request.GET["user_id"]) == 0):
        raise RequestException("user_id is required")
    uid = request.GET["user_id"]
    print(f"UID: {uid}")
    if ("product_id" not in request.GET) or (len(request.GET["product_id"]) == 0):
        result = user_all_lessons(uid)
    else:
        pid = request.GET["product_id"]
        print(f"PID: {pid}")
        result = user_product_lessons(uid, pid)
    return result

@api_view(["GET"])
def get_stats(request):
    q = """
WITH watch_metadata AS (
    SELECT product_id,
        SUM(is_viewed) as full_views_by_users,
        SUM(length_viewed) as total_viewtime
    FROM pages_userlesson ul
    INNER JOIN pages_product_lesson pl
        ON ul.lesson_id = pl.lesson_id
    GROUP BY product_id
), student_metadata AS (
    SELECT product_id,
        COUNT(user_id) as user_purchased_count
    FROM pages_product_user
    GROUP BY product_id
)
SELECT
    wmd.*,
    smd.user_purchased_count,
    100.0 * smd.user_purchased_count / (SELECT COUNT(id) FROM pages_user) AS purchase_percentage
FROM watch_metadata wmd
INNER JOIN student_metadata smd
    ON wmd.product_id = smd.product_id
"""
    with connection.cursor() as cursor:
        cursor.execute(q)
        rows = cursor.fetchall()
        result = rows_to_json(cursor, rows)
    return JsonResponse(result)

@api_view(["GET"])
def get_users(request):
    q = """
WITH grp_products AS (
    SELECT user_id, GROUP_CONCAT(product_id, ", ") as purchased_products
    FROM pages_product_user pu
    INNER JOIN pages_user u
        ON pu.user_id = u.id
    GROUP BY user_id
)
SELECT u.username, u.name, u.date_of_registration, grp.purchased_products
FROM pages_user u
INNER JOIN grp_products grp 
    ON u.id = grp.user_id
"""
    with connection.cursor() as cursor:
        cursor.execute(q)
        rows = cursor.fetchall()
        result = rows_to_json(cursor, rows)
    return JsonResponse(result)

@api_view(["GET"])
def get_products_owners(request):
    q = """
SELECT 
    p.id as product_id,
    p.code as product_code,
    p.name as product_name,
    o.code as owner_code,
    o.name as owner_name
FROM pages_product p
INNER JOIN pages_owner o
    ON p.owner_id = o.id
"""
    with connection.cursor() as cursor:
        cursor.execute(q)
        rows = cursor.fetchall()
        result = rows_to_json(cursor, rows)
    return JsonResponse(result)

@api_view(["GET"])
def get_products_lessons(request):
    q = """
WITH lesson_with_id AS (
    SELECT 
        pl.lesson_id,
        pl.product_id,
        l.code as lesson_code,
        l.name as lesson_name, 
        l.length as lesson_length, 
        l.url as lesson_url
    FROM pages_lesson l
    INNER JOIN pages_product_lesson pl
        ON l.id = pl.lesson_id
)
SELECT 
    id as product_id,
    code as product_code, 
    name as product_name, 
    lesson_code, 
    lesson_name, 
    lesson_length, 
    lesson_url
FROM pages_product p
INNER JOIN lesson_with_id l
    ON p.id = l.product_id
"""
    with connection.cursor() as cursor:
        cursor.execute(q)
        rows = cursor.fetchall()
        result = rows_to_json(cursor, rows)
    return JsonResponse(result)