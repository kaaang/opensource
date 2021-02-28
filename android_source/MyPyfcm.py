from pyfcm import FCMNotification

# Api_key is fixed value based on the firebase.
push_service = FCMNotification(api_key="AAAANwyTgsY:APA91bFTQwDKyQcozCiu9DJkmk8bZ2dZgQ9dZqxAyk5vTvYiFHjBR0AVkHGsAuCsUHNG8eCL1dqPwcRVgQv1NwtAVFn_Sku4TVTkcHA9leq0fMEbGHeFxEopSpbJKlIUEWAi25NH4nt0")

# Open "logcat.txt" to get registration_id.
# FCM Log has been written on first line of "logcat.txt".
# So, we use lines[0] to get it.
f = open("D:\\logcat.txt", 'r')
# If above line returns error:
# UnicodeDecodeError: 'cp949' codec can't decode byte 0xff in position 0: illegal multibyte sequence
# use this:
# f = open("D:\\logcat.txt", 'r', encoding='utf-16')
# it's because 'utf-16' can decode '0xff'
lines = f.readlines()
print(lines[0])
f.close()

# Find an index where string "Token" starts.
index = lines[0].find("Token")
print(index)

# Because lines[1] looks like "~~ FCM Token: ~~",
# we add 7 to index and read line to the end.
# (After "T", there are 7 characters "o k e n : ")
# Then, get rid of line feed '\n'.
registration_id = lines[0][index+7:].rstrip('\n')
print(registration_id)

message_title = "[Hydration Alert]"
message_body = "It's been an hour since you drank water."
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

print(result)
