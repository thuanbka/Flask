import jwt
import base64
# token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRodWFubnYxMCIsInBhc3N3b3JkIjoidGVzdDEyMzQiLCJleHAiOjE2OTY0OTIzMzF9.wpCmuFJchpls32U0pCzGGBnZrWY7Wbyan60yi6q-Wc0'
# # Extract and decode the header part
# header_encoded = token.split('.')[0]
# header_padded = header_encoded + '=' * (4 - len(header_encoded) % 4)

# try:
#     decoded_header = base64.urlsafe_b64decode(header_padded).decode('utf-8')
#     print(f'Decoded Header: {decoded_header}')
# except Exception as e:
#     print(f'Error Decoding Header: {e}')

import base64

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRodWFubnYxMCIsInBhc3N3b3JkIjoidGVzdDEyMzQiLCJleHAiOjE2OTY0OTIzMzF9.wpCmuFJchpls32U0pCzGGBnZrWY7Wbyan60yi6q-Wc0'

# Extract and decode the header part
header_encoded = token.split('.')[0]
header_padded = header_encoded + '=' * (-len(header_encoded) % 4)  # Adjust padding calculation

try:
    decoded_header = base64.urlsafe_b64decode(header_padded).decode('utf-8')
    print(f'Decoded Header: {decoded_header}')
except Exception as e:
    print(f'Error Decoding Header: {e}')
# print(f'Received Token: {token}')

# try:
#     decoded_payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
#     print(f'Decoded Payload: {decoded_payload}')
# except jwt.ExpiredSignatureError:
#     print('Token has expired')
# except jwt.InvalidTokenError as e:
#     print(f'Invalid token: {str(e)}')
