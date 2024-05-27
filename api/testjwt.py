import jwt

# Your JWT token
encoded_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcwNzcyMzA3LCJpYXQiOjE3MTY3NzIzMDcsImp0aSI6IjNlZWJjNzYyM2JiNTQ4OGI4ODFlNTA4Nzc2YTM3MDA3IiwidXNlcl9pZCI6MTUsImlzX3N0YWZmIjp0cnVlfQ.XwB2UAdq8vx6LuWbevq3O9_p0aS-m4FQR2JwQ7bQvNw'

# Decode the token without verification of the signature
decoded_payload = jwt.decode(encoded_token, options={"verify_signature": False})

# Print the content of the payload
print(decoded_payload)