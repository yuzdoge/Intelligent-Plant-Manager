from aip import AipSpeech

APP_ID = '19488249'  # 百度AI平台申请后换为自己的，下同
API_KEY = '2iDpdT90if2hfreWPTNfsxLC'
SECRET_KEY = 'sbxIDrKlfebLFr4qsc25EqDS8CBZPM1N'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def sound2text(file_path='temp.wav'):
    # sound to text function
    with open(file_path, 'rb') as fp:
        recog = client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1537})
        if recog['err_no'] not in [0, 3301]:
            return False, recog['err_no']
        elif recog['err_no'] == 3301:
            return True, ''
        return True, recog['result'][0].strip('。')
