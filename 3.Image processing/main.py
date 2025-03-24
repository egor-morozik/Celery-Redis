from tasks import resize_image

result = resize_image.delay('test_image.jpg')

print(result.get(timeout=10))