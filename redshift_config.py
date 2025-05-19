import os

from dotenv import dotenv_values

# from sqlalchemy import create_engine
envs = dotenv_values(".env")
REDSHIFT_USER = envs['REDSHIFT_USER']
REDSHIFT_PW = envs['REDSHIFT_PW']
REDSHIFT_HOST = envs['REDSHIFT_HOST']
REDSHIFT_PORT = envs['REDSHIFT_PORT']
REDSHIFT_DB = envs['REDSHIFT_DB']
REDSHIFT_URL = (
    f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PW}"
    f"@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}"
)
REDSHIFT_PARAMS = {
    'host': REDSHIFT_HOST,
    'port': REDSHIFT_PORT,
    'dbname': REDSHIFT_DB,
    'user': REDSHIFT_USER,
    'password': REDSHIFT_PW
}
AWS_ACCESS_KEY = envs['AWS_ACCESS_KEY']
AWS_SECRET_KEY = envs['AWS_SECRET_KEY']
AWS_IAM_ROLE = envs['AWS_IAM_ROLE']
S3_BUCKET_NAME = envs['S3_BUCKET_NAME']
S3_PROJECT_PATH = envs['S3_PROJECT_PATH']
S3_URL = f"s3://{S3_BUCKET_NAME}/{S3_PROJECT_PATH}"

PATH_DOWNLOAD = 'data/download'
PATH_CSV = 'data/csv'
os.makedirs(PATH_DOWNLOAD, exist_ok=True)
os.makedirs(PATH_CSV, exist_ok=True)



addr_to_code={
    '서울': 'KR-11',
    '서울특별시': 'KR-11',
    '부산': 'KR-26',
    '부산광역시': 'KR-26',
    '대구': 'KR-27',
    '대구광역시': 'KR-27',
    '인천': 'KR-28',
    '인천광역시': 'KR-28',
    '광주': 'KR-29',
    '광주광역시': 'KR-29',
    '대전': 'KR-30',
    '대전광역시': 'KR-30',
    '울산': 'KR-31',
    '울산광역시': 'KR-31',
    '세종': 'KR-50',
    '세종특별자치시': 'KR-50',
    '경기': 'KR-41',
    '경기도': 'KR-41',
    '강원': 'KR-42',
    '강원도': 'KR-42',
    '강원특별자치도': 'KR-42',
    '충북': 'KR-43',
    '충청북도': 'KR-43',
    '충남': 'KR-44',
    '충청남도': 'KR-44',
    '전북': 'KR-45',
    '전라북도': 'KR-45',
    '전북특별자치도': 'KR-45',
    '전남': 'KR-46',
    '전라남도': 'KR-46',
    '경북': 'KR-47',
    '경상북도': 'KR-47',
    '경남': 'KR-48',
    '경상남도': 'KR-48',
    '제주': 'KR-49',
    '제주도': 'KR-49',
    '제주특별자치도': 'KR-49',
}

animal_hospital_schema = {
    'name': 'str',
    'phone_number': 'str',
    'addr': 'str',
    'id': 'str',
}

protected_animal_schema = {
    'id': 'str',  # 1
    'animal_id': 'str',  # 2
    'animal_type': 'str',  # 3
    'breed': 'str',  # 4
    'fur_color': 'str',  # 5
    'sex': 'str',  # 6
    'neutering': 'str',  # 7
    'feature': 'str',  # 8
    'rescue_day': 'str',  # 9
    'rescue_reason': 'str',  # 10
    'rescue_location': 'str',  # 11
    'notice_period': 'str',  # 12
    'protection_center': 'str',  # 13
    'exponent': 'str',  # 14
    'address': 'str',  # 15
    'phone_number': 'str',  # 16
}

to_atopt_animal_schema = {
    'id': 'str',  # 1
    'animal_id': 'str',  # 2
    'breed': 'str',  # 3
    'color': 'str',  # 4
    'sex': 'str',  # 5
    'neutering': 'str',  # 6
    'age_weight': 'str',  # 7
    'feature_rescue': 'str',  # 8
    'feature_social': 'str',  # 9
    'feature_health': 'str',  # 10
    'rescue_location': 'str',  # 11
    'reception_dt': 'str',  # 12
    'etc': 'str',  # 13
    'center': 'str',  # 14
    'status': 'str',  # 15
    'protection_center': 'str',  # 16
    'phone_number': 'str',  # 17
    'protection_addr': 'str'  # 18
}


download_files = {
    'animal_hospital': [animal_hospital_schema, 'https://www.animal.go.kr/front/awtis/shop/hospitalExcelList.do?csSignature=67u%2B8uPiv2kibyG3yR%2FNnw%3D%3D&boardId=shop&bizKnCd=&menuNo=5000000026&searchCoNm=&searchUprCd=&searchOrgCd=&searchPmsnNo=', ],
    'protected_animal': [protected_animal_schema, 'https://www.animal.go.kr/front/awtis/public/publicListExcel.do?csSignature=67u%2B8uPiv2kibyG3yR%2FNnw%3D%3D&boardId=&menuNo=1000000055&searchSDate=2025-01-01&searchEDate=2025-05-18&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd=&searchKindCd=&searchSexCd=&searchRfid=', ],
    'to_adopt_animal': [to_atopt_animal_schema, 'https://www.animal.go.kr/front/awtis/protection/protectionListExcel.do?csSignature=67u%2B8uPiv2kibyG3yR%2FNnw%3D%3D&boardId=&menuNo=1000000060&searchSDate=2025-01-01&searchEDate=2025-05-18&searchUprCd=&searchOrgCd=&searchCareRegNo=&searchUpKindCd=&searchKindCd=&searchSexCd=&searchRfid=', ],
}