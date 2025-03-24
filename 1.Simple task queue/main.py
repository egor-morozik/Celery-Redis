from tasks import uppercase_string

result = uppercase_string.delay("hello")

print(result.get(timeout=10))  