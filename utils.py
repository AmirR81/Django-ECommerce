from kavenegar import *


def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI('6F5078463173746E703155672F4D43326D4634774B336D416E43336D4249737A3663375766737A2F4F62593D')
		params = {
			'sender': '',
			'receptor': phone_number,
			'message': f'{code} کد تایید شما '
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)