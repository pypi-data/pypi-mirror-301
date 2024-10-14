import requests
import math
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_weather(nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    service_key = 'RnHtwPf0XSCKZubIqPj6+oESQSSd89MrtrItNcs/TcSBd36t+rT332mwXAK28bC42NUoV60aMnPUCJD+1nyzaA=='
    
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = now.strftime("%H%M")

    params = {
        'serviceKey': service_key,
        'pageNo': '1',
        'numOfRows': '10',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"API Response: {data}")
        
        if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
            items = data['response']['body']['items']['item']
            
            weather_info = {}
            for item in items:
                category = item['category']
                value = item['obsrValue']
                
                if category == 'T1H':
                    weather_info['temperature'] = f"{value}°C"
                elif category == 'REH':
                    weather_info['humidity'] = f"{value}%"
                elif category == 'PTY':
                    weather_info['precipitation'] = get_precipitation_type(value)
                elif category == 'WSD':
                    weather_info['wind_speed'] = f"{value}m/s"
            
            weather_description = (
                f"오늘날씨는 {weather_info.get('precipitation', '알 수 없음')}이고, "
                f"현재 기온은 {weather_info.get('temperature', '알 수 없음')}입니다, "
                f"습도는 {weather_info.get('humidity', '알 수 없음')}이고. "
                
                f"풍속은 {weather_info.get('wind_speed', '알 수 없음')}입니다."
            )
            
            return weather_description
        else:
            logger.error(f"Unexpected API response structure: {data}")
            return "날씨 정보 구조가 예상과 다릅니다."
    
    except requests.RequestException as e:
        logger.error(f"API 요청 중 오류 발생: {str(e)}")
        return "날씨 정보를 가져오는데 실패했습니다."
    except KeyError as e:
        logger.error(f"API 응답 파싱 중 오류 발생: {str(e)}")
        return "날씨 정보 파싱에 실패했습니다."
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {str(e)}")
        return "날씨 정보 처리 중 오류가 발생했습니다."

def get_precipitation_type(value):
    precipitation_types = {
        '0': '맑음',
        '1': '비',
        '2': '비/눈',
        '3': '눈',
        '4': '소나기',
        '5': '빗방울',
        '6': '빗방울/눈날림',
        '7': '눈날림'
    }
    return precipitation_types.get(value, '알 수 없음')

def convert_grid(lat, lon):
    RE = 6371.00877  # 지구 반경(km)
    GRID = 5.0  # 격자 간격(km)
    SLAT1 = 30.0  # 투영 위도1(degree)
    SLAT2 = 60.0  # 투영 위도2(degree)
    OLON = 126.0  # 기준점 경도(degree)
    OLAT = 38.0  # 기준점 위도(degree)
    XO = 43  # 기준점 X좌표(GRID)
    YO = 136  # 기준점 Y좌표(GRID)

    DEGRAD = math.pi / 180.0
    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)

    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn

    nx = int(ra * math.sin(theta) + XO + 0.5)
    ny = int(ro - ra * math.cos(theta) + YO + 0.5)

    return nx, ny