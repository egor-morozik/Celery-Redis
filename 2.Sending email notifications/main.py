from tasks import send_welcome_email

result = send_welcome_email.delay('recipient@example.com', 'Алексей')

print(result.get(timeout=10))