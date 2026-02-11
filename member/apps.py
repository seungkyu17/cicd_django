from django.apps import AppConfig


class MemberConfig(AppConfig):
    name = 'member'

    #'Django' 앱 로딩이 완료되면, 자동으로 실행되는 '초기화 함수' 입니다.
    def ready(self):
        #'import' 가 되어야 '@receiver 데코레이터' 가 실행 됩니다.
        import member.signals