class GCS:
    SIGNED_URL_EXPIRE = 60 * 24

class RABBITMQ:
    HEART_BEAT = 60

class MESSAGES:
    class SUCCESS:
        ANALYZE = "영상 분석을 완료했습니다."
    class ERROR:
        NOT_FOUND_VIDEO = "영상을 찾을 수 없습니다."
        FAILED_ANALYZE = "영상 분석에 실패했습니다."
        FAILED_UPLOAD = "영상 저장에 실패했습니다."
        FAILED_GENERATE_URL = "액세스 링크 생성에 실패했습니다."
        FAILED_INSERT_SUBTITLE = "영상에 자막을 삽입하는 데 실패했습니다."
        FAILED_CREATE_SUBTITLE = "자막 파일 생성에 실패했습니다."
        FAILED_CONNECT_CHANNEL = "채널 연결에 실패했습니다."
        SERVER_ERROR = "서버 오류가 발생했습니다."

class CODE:
    class SUCCESSS:
        ANALYZE = "SUCCESS_ANALYZE"
    class FAILED:
        ANALYZE = "FAILED_ANALYZE"
