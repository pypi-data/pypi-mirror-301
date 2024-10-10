import os
import argparse
from utils_hj3415 import noti, utils
from scraper_hj3415.nfscraper import run as nfs_run
# import pprint

from utils_hj3415.helpers import SettingsManager


def unittest_setUp_test_server_setting() -> dict:
    """
    unittest의 setUp 함수에서 db 주소를 임시로 테스트 서버로 변경하는 함수
    :return: original sever setting dictionary
    """
    test_server_addr = {
        'mongo': "mongodb+srv://Cluster13994:Rnt3Q1hrZnFT@cluster13994.vhtfyhr.mongodb.net/",
        'redis': "localhost",
    }
    setting_manager = DbSettingsManager()
    original_settings_dict = setting_manager.load_settings()
    # print("<< original settings >>")
    # pprint.pprint(original_settings_dict)

    print("<< 테스트 서버의 주소로 변경합니다. >>")
    for db_type, address in test_server_addr.items():
        setting_manager.set_address(db_type, address, verbose=False)
    # pprint.pprint(test_server_addr)

    return original_settings_dict

def unittest_tearDown_test_server_setting(original_settings_dict: dict):
    """
    unittest의 tearDown 함수에서 임시로 변경된 db 주소를 다시 원래로 돌리는 함수
    :return:
    """
    print("<< 원래의 서버 주소로 복원합니다. >>")
    setting_manager = DbSettingsManager()
    for k, v in original_settings_dict.items():
        setting_manager.set_address(k, v, verbose=False)
    # pprint.pprint(setting_manager.load_settings())


class DbSettingsManager(SettingsManager):
    DEFAULT_SETTING = {
        'mongo': 'mongodb://hj3415:piyrw421@localhost:27017',
        'redis': 'localhost',
    }
    DB_TYPE = DEFAULT_SETTING.keys()

    def __init__(self):
        settings_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'settings.json')
        super().__init__(settings_file)

    def set_address(self, db_type: str, address: str, verbose = True):
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        self.settings_dict[db_type] = address
        self.save_settings()
        if db_type == 'mongo':
            from db_hj3415 import mymongo
            mymongo.Base.mongo_client = mymongo.connect_to_mongo(address)
        elif db_type == 'redis':
            from db_hj3415 import myredis
            myredis.Base.redis_client = myredis.connect_to_redis(address)

        if verbose:
            print(f"{db_type} 주소가 저장되었으며 데이터베이스의 연결 주소도 변경되었습니다.: {address}")

    def get_address(self, db_type: str) -> str:
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        return self.settings_dict.get(db_type, self.DEFAULT_SETTING[db_type])

    def reset_address(self, db_type: str, verbose = True):
        assert db_type in self.DB_TYPE, f"db_type 인자는 {self.DB_TYPE} 중에 있어야 합니다."
        self.set_address(db_type, self.DEFAULT_SETTING[db_type], verbose=False)
        if verbose:
            print(f"{db_type} 주소가 기본값 ({self.DEFAULT_SETTING[db_type]}) 으로 초기화 되었습니다.")

def db_manager():
    settings_manager = DbSettingsManager()

    parser = argparse.ArgumentParser(description="데이터베이스 주소 관리 프로그램")
    db_subparsers = parser.add_subparsers(dest='db_type', help='데이터베이스 종류를 지정하세요(mongo, redis)', required=True)

    # 'mongo' 명령어 서브파서
    mongo_parser = db_subparsers.add_parser('mongo', help=f"mongodb 데이터베이스")
    mongo_subparser = mongo_parser.add_subparsers(dest='command', help='mongodb 데이터베이스 관련된 명령')

    # mongo - save 파서
    mongo_save_parser = mongo_subparser.add_parser('save', help=f"mongodb 주소를 저장합니다.")
    mongo_save_parser.add_argument('address', type=str, help=f"저장할 데이터베이스 주소를 입력하세요.")

    # mongo - print 파서
    mongo_subparser.add_parser('print', help=f"mongodb 주소를 출력합니다.")

    # mongo - repair 파서
    mongo_repair_parser = mongo_subparser.add_parser('repair', help=f"mongodb의 모든 종목의 컬렉션 유효성을 확인하고 없으면 채웁니다.")
    mongo_repair_parser.add_argument('targets', nargs='*', type=str, help="대상 종목 코드를 입력하세요. 'all'을 입력하면 전체 종목을 대상으로 합니다.")
    mongo_repair_parser.add_argument('-n', '--noti', action='store_true', help='작업 완료 후 메시지 전송 여부')

    # mongo - reset 파서
    mongo_subparser.add_parser('reset', help=f"mongodb 주소를 기본값으로 초기화합니다.")

    # 'redis' 명령어 서브파서
    redis_parser = db_subparsers.add_parser('redis', help=f"redis 데이터베이스")
    redis_subparser = redis_parser.add_subparsers(dest='command', help='redisdb 데이터베이스 관련된 명령')

    # redis - save 파서
    redis_save_parser = redis_subparser.add_parser('save', help=f"redisdb 주소를 저장합니다.")
    redis_save_parser.add_argument('address', type=str, help=f"저장할 데이터베이스 주소를 입력하세요.")

    # redis - print 파서
    redis_subparser.add_parser('print', help=f"redis 주소를 출력합니다.")

    # redis - reset 파서
    redis_subparser.add_parser('reset', help=f"redis 주소를 기본값으로 초기화합니다.")

    args = parser.parse_args()

    if args.db_type in ['mongo', 'redis']:
        if args.command == 'save':
            settings_manager.set_address(args.db_type, args.address)
        elif args.command == 'print':
            address = settings_manager.get_address(args.db_type)
            print(f"{args.db_type} 주소: {address}")
        elif args.command == 'reset':
            settings_manager.reset_address(args.db_type)
        elif args.db_type == 'mongo' and args.command == 'repair':
            from db_hj3415 import mymongo
            if len(args.targets) == 1 and args.targets[0] == 'all':
                all_codes_in_db = mymongo.Corps.list_all_codes()
                print(f"**** 모든 종목({len(all_codes_in_db)})의 데이터베이스를 검사합니다. ****")
                missing_dict = mymongo.Corps.chk_integrity(*all_codes_in_db)
            else:
                # 입력된 종목 코드 유효성 검사
                invalid_codes = [code for code in args.targets if not utils.is_6digit(code)]
                if invalid_codes:
                    print(f"다음 종목 코드의 형식이 잘못되었습니다: {', '.join(invalid_codes)}")
                    return
                print(f"**** {args.targets} 종목의 데이터베이스를 검사합니다. ****")
                missing_dict = mymongo.Corps.chk_integrity(*args.targets)

            repairable_codes = list(missing_dict.keys())
            if len(repairable_codes) != 0:
                print(f"**** {repairable_codes} 종목에서 이상이 발견되어서 스크랩하겠습니다. ****")
                nfs_run.all_spider(*repairable_codes)
                if args.noti:
                    noti.telegram_to('manager', f"{repairable_codes}의 데이터베이스를 수리했습니다.")
        else:
            parser.print_help()
    else:
        parser.print_help()
