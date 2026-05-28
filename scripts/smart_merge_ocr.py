import re

# Baseline RAW_EXHIBITORS from data.js
baseline = {
  "A2": "완도 청해진다원",
  "A3": "현암제다 / 무위다원",
  "A4": "한국제다",
  "A5": "제주차농 JEJU CHANONG",
  "A6": "차인연합회",
  "A7": "(사)세계기독교차문화협회 / 일양차문화연구회 회원 티플라워(디화) 전시회",
  "A8": "제주다원",
  "A9": "극락차파크 복합치유공간 (과천 청계산장)",
  "A10": "국제통상",
  "A11": "무유창작기가 살래요",
  "A12": "명인신광수차 _ 무도를 즐기는차(moocha)",
  "A13": "모두실에서만납차 / 적석곶이",
  "A14": "백자일상",
  "A15": "문경칠보산농원",
  "A16": "동국대학교 불교대학원 차문화콘텐츠학과",
  "A17": "가헌아트",
  "A18": "순천대학교 (사)고려천태국제선차 연구보존회",
  "A19": "장흥청태전(장흥다원)",
  "A21": "한국토기",
  "A22": "헬스베버리지",
  "A23": "문재필 옻칠갤러리",
  "A25": "트임 & 김진욱도예원",
  "A26": "매월초가",
  "A29": "토리",
  "A30": "연담",
  "A31": "하나실크로드티",
  "A32": "우기원",
  "A33": "안동착한농장 프로폴리스 꿀",
  "A34": "옥설차",
  "A35": "와락공방",
  "A36": "대림목공예",
  "A38": "주원안 (이든갤러리)",
  "A39": "청도천연염색연구회 감물드리",
  "A40": "꼬메",
  "A41": "보성천연염색협동조합 (자연담은 하늘수)",
  "A42": "천연염색 미주사랑",
  "A43": "풀과빛 (청도군 천연염색 연구회)",
  "A44": "승설재 · 무이성",
  "A45": "투디헌",
  "A46": "오차연각 / 청밀도방",
  "A47": "차문화협회",
  "A48": "(사)한국 싱잉볼 협회 / (주)젠테라피 내츄럴 힐링센터",
  "A49": "원유전통",
  
  "B1": "보성군 홍보관",
  "B2": "보성 (보향녹차)",
  "B3": "유기농 원당제다원 / 천보다원",
  "B4": "보성 유기농 운해다원 / 조태연가 죽로차",
  "B5": "보성제다",
  "B6": "징광잎차 / 장흥임하도예",
  "B8": "죽림다원 / 아이뜰리에",
  "B9": "보성 영천다원",
  "B10": "소아다원 / 백암요",
  "B11": "다재 / 다원다기",
  "B12": "보성녹차 선다원",
  "B13": "섬진다원",
  "B14": "한덕도선암경영연구원 • 차그리다",
  "B15": "우곡요",
  "B16": "효월",
  "B17": "토점가 (이조요) since1940",
  "B18": "황우요",
  "B19": "청타, 더 공유 / theou",
  "B20": "무결",
  "B21": "몽탄갤러리",
  "B22": "성도요 / 울산도예",
  "B23": "뚜띨로공방 / 이지헌도예연구소",
  "B25": "도정요",
  "B26": "대경도예",
  "B27": "도농도예",
  "B28": "자연으로 웅크려 / 한세은 도예공방",
  "B29": "차당업 / 봉정요",

  "C1": "나주",
  "C2": "연우제다",
  "C3": "티후",
  "C4": "하동아낙 (LADY HADONG)",
  "C5": "청석골감로다원",
  "C6": "로잔",
  "C7": "리산고산차",
  "C8": "쟈스민 TEA SHOP",
  "C9": "웃차",
  "C10": "찻잎마술/소암 초",
  "C11": "수제차전수관",
  "C12": "백학제다",
  "C14": "노련요",
  "C16": "황매산다원 허굴산방",
  "C18": "누보도예",
  "C19": "산이리",
  "C21": "보니다",
  "C22": "조은도예",
  "C23": "정요",
  "C24": "소선도예",
  "C25": "삐딱한 도자기 황계요",
  "C26": "문경 경록요",
  "C27": "천년보이차",
  "C28": "채담요",
  "C29": "봉정요",

  "D1": "일구다 & 요산당",
  "D2": "국천다원",
  "D3": "황아자 홍차 녹차",
  "D4": "혜원제, 혜원농원",
  "D5": "죽로은창",
  "D6": "삼신차 (발효차 전문다원)",
  "D8": "하늘 흙실선차 / 밀양요",
  "D9": "지당",
  "D10": "송하요",
  "D11": "도재명가",
  "D12": "관아수제차",
  "D13": "농업회사법인 지리산 상선암차",
  "D14": "무애 (MUAE TEA)",
  "D15": "금향다원",
  "D17": "산도방",
  "D18": "녹우요",
  "D19": "분당블루더 / 한밭제다 차공간 / 해내움",
  "D20": "민토 (최민옥)",
  "D21": "헌원요",
  "D23": "도유가",
  "D24": "김동민 도예 / 소랑요",
  "D26": "알천도예",
  "D28": "극단요, 성탄송운",
  "D29": "규림요 / 오름오르다",
  "D30": "동화도예",
  "D31": "영남요",
  "D32": "포암요",
  "D33": "기천공방",

  "E1": "대통령 표창 수상_꽃차 하늘바라기",
  "E2": "김전방짜유기 명인 이운형",
  "E4": "경기한빛꽃차협동조합",
  "E5": "열기손 금속전",
  "E6": "스튜디오 새온",
  "E7": "따띠 (뷰닉스테크)",
  "E8": "수니공방",
  "E9": "백산도예 연구소",
  "E10": "여송도예",
  "E11": "우방도예",
  "E12": "효원도예",
  "E13": "무무요",
  "E14": "청욱요",
  "E15": "김해예인요 / 도자기마을 (빛살)",
  "E16": "다솜공방 / 후계요",
  "E17": "삼정공방 / 예인요",
  "E18": "부산광역시 공예협동조합 토산요",
  "E19": "슬우재",
  "E20": "부산광역시 공예협동조합 다솔도예",
  "E21": "김욱진",
  "E22": "청담요",
  "E23": "금정공방",
  "E24": "도예명장 2023-01호 영산요",
  "E25": "더새드",
  "E26": "효향요",
  "E28": "도동요",
  "E30": "수도예",
  "E31": "화경도예",

  "F1": "자연을담다",
  "F2": "경위복지 (가인갤러리) / 연우제다",
  "F3": "Tea진공밀폐용기 에스락",
  "F4": "묘치",
  "F5": "교문공방",
  "F6": "강동현",
  "F7": "연세라믹",
  "F8": "우기세라믹",
  "F9": "날빛",
  "F10": "청기백기",
  "F11": "무유",
  "F12": "아람도자기",
  "F13": "나은크래프트 / 송화도예",
  "F14": "가람도예",
  "F15": "고도산방",
  "F16": "라세라미스타",
  "F17": "김해요",
  "F18": "다경요",
  "F19": "정호요",
  "F20": "연휘도방",
  "F21": "연우도예",
  "F22": "임의섭도예작업장",
  "F23": "이지헌도예연구소",
  "F24": "가야공방 / 박달요",
  "F25": "목향다원 / 모둥도예",
  "F26": "소월백자",
  "F27": "진곡요 / 연잎을 만드는 힐링푸드 두레연구품당",
  "F28": "드네플 (이종주의 도자기)",
  "F29": "심곡요",
  "F30": "침향나무",
  "F31": "모을 황선회도방",
  "F32": "HaDa design (하다디자인)",

  "G1": "(주)해올커뮤니케이션 / (주)해올 / (주)해올디앤씨",
  "G2": "티하우스 나니",
  "G3": "정산당",
  "G4": "재단법인 하동녹차연구소 / 하동녹차 & 바이오진흥원",
  "G5": "글럴피스",
  "G6": "대하고선방",
  "G7": "다연재",
  "G8": "차마고도 차상회",
  "G9": "지우명차",
  "G10": "다견원 / 한국 말차 격불 연구회",
  "G11": "향적당",
  "G12": "랑카티스 (스리랑카 홍차)",
  "G13": "틴치오보소올",
  "G14": "사계다향",
  "G15": "동정보이차 노반장홍",
  "G16": "차세상 (茶世上) / 유산차방 (遊山茶訪) 한국총판",
  "G17": "宜興永慶陶藝老書堂",
  "G18": "北京妙香緯業貿易有限公司",
  "G19": "동심명차",
  "G20": "송하요 / 포덤 티하우스",
  "G21": "尹家人 · YIN TEA",
  "G22": "상락구산지진차문화유한공사",
  "G24": "바이에드가",
  "G25": "초보보이",
  "G26": "보림원목 공방",
  "G27": "다승원 AFTR / 여원",
  "G28": "티 블렌즈",

  "H1": "보이차전문점 명가원",
  "H2": "차우림, 오래된 미래",
  "H3": "한차원",
  "H4": "예정",
  "H5": "선묘당 (善妙堂) CHINA TEA",
  "H6": "북향명차",
  "H7": "상명",
  "H9": "지당",
  "H10": "석가명차 오운산고차",
  "H11": "덕화코리아",
  "H12": "아원식 프리미엄 티라운지",
  "H13": "茗譪天下 x 흑유피련신 x 북경도사",
  "H14": "취죽진여실",
  "H15": "후다인",
  "H16": "宜興知丁文化創意有限公司",
  "H17": "일상다반사",
  "H18": "주식회사 인센스월드",
  "H19": "喜闈陶瓷公司",
  "H20": "경주 남산도예",
  "H21": "(주)차오마",
  "H22": "청도 천연염색연구회 쪽빛나라",
  "H24": "려진요",
  "H25": "고려문화",
  "H26": "계절사이로 (이오순 금침명인)",
  "H27": "반정고리"
}

# Common ID corrections
id_corrections = {
    "AIZ": "A17", "A!!": "A11", "A4S": "A45", "HI6": "H16", "HI3": "H13", "H2S": "H25",
    "HI2": "H12", "HI0": "H10", "HI8": "H18", "HI4": "H14", "HIs": "H15", "B1S": "B15",
    "BJ": "E1", "GI": "G1", "Cl": "C1", "CHI": "C11", "AS": "A5", "A2s": "A25",
    "814": "B14", "82": "B2", "89": "B9", "84": "B4", "826": "B26", "812": "B12",
    "87": "B7", "810": "B10", "813": "B13", "88": "B8", "86": "B6", "83": "B3",
    "BI": "B1", "A3!": "A31", "C33": "C23", "A4l": "A41", "D22": "D22", "449": "A49",
    "DI": "D1", "HIT": "H17", "C1O": "C10", "CIS": "C15", "A29": "A29", "A43": "A43",
    "E12": "E12", "E26": "E26", "313": "B13", "DI7": "D17", "A2S": "A25", "H2S": "H25",
    "HI": "H1", "HS": "H5", "E2!": "E21", "B2!": "B21"
}

log_path = "/Users/uchun1ee/.gemini/antigravity/brain/9c55d14c-dd38-45b4-8ae3-ec1af5913b15/.system_generated/tasks/task-602.log"

with open(log_path, "r", encoding="utf-8") as f:
    content = f.read()

lines = []
in_block = False
for line in content.split("\n"):
    if "Grouped 227 rows:" in line:
        in_block = True
        continue
    if in_block:
        if line.strip():
            lines.append(line.strip())
        else:
            if len(lines) > 50:
                break

ocr_mappings = []

for line in lines:
    match = re.match(r"^\d+:\s*(.*)$", line)
    if not match:
        continue
    row_content = match.group(1).strip()
    words = row_content.split()
    if not words:
        continue
    
    # Try to see if there's a booth ID in the row
    booth_id = None
    name_start_idx = 0
    
    # Check first word
    w1 = words[0].strip()
    cleaned_w1 = id_corrections.get(w1, w1)
    if re.match(r"^[A-H]\d+$", cleaned_w1):
        booth_id = cleaned_w1
        name_start_idx = 1
    # Check if there is an ID anywhere else, e.g. "A18 (순처대학교..."
    else:
        for idx, w in enumerate(words):
            cleaned_w = id_corrections.get(w, w)
            if re.match(r"^[A-H]\d+$", cleaned_w):
                booth_id = cleaned_w
                # Name is everything else
                words_copy = list(words)
                words_copy.pop(idx)
                row_content = " ".join(words_copy)
                break
                
    if booth_id:
        name = " ".join(words[name_start_idx:]).strip() if name_start_idx > 0 else row_content.strip()
        ocr_mappings.append((booth_id, name))
    else:
        # No ID found, save name for fuzzy matching
        ocr_mappings.append((None, row_content))

# Output dictionary
final_exhibitors = {}

# 1. First pass: Assign exact ID matches
for bid, name in ocr_mappings:
    if bid:
        final_exhibitors[bid] = name

# 2. Second pass: Fuzzy match lines without IDs using baseline names
for bid, name in ocr_mappings:
    if not bid:
        # Let's clean the name for matching
        clean_name = re.sub(r"[^\w\s]", "", name).replace(" ", "")
        if not clean_name:
            continue
            
        best_match_id = None
        best_score = 0
        
        for base_id, base_name in baseline.items():
            clean_base = re.sub(r"[^\w\s]", "", base_name).replace(" ", "")
            # Simple substring matching
            overlap1 = clean_name in clean_base
            overlap2 = clean_base in clean_name
            if overlap1 or overlap2:
                # Find length of overlap
                score = min(len(clean_name), len(clean_base))
                if score > best_score:
                    best_score = score
                    best_match_id = base_id
                    
        if best_match_id and best_score >= 3:
            # We matched a baseline ID! Update name
            # If we don't have this ID filled yet, or the fuzzy match is better
            if best_match_id not in final_exhibitors:
                final_exhibitors[best_match_id] = name

# 3. Post-processing: Fill in missing baseline items from original values
# to ensure we don't lose any data
for base_id, base_name in baseline.items():
    if base_id not in final_exhibitors:
        # Use baseline
        final_exhibitors[base_id] = base_name

# 4. Clean up names
def clean_exhibitor_name(name):
    # Remove duplicates like "소랑요 소랑요"
    words = name.split()
    if len(words) >= 2 and len(words) % 2 == 0:
        half = len(words) // 2
        if words[:half] == words[half:]:
            name = " ".join(words[:half])
            
    # Clean OCR artefacts
    name = name.replace(" • ", " · ")
    name = name.replace(" •", " ·")
    name = name.replace("• ", "· ")
    name = name.replace("•", " · ")
    
    # Specific Korean cleanups based on OCR typical misreadings
    name = name.replace("경기한방꽃차협동조합", "경기한빛꽃차협동조합")
    name = name.replace("지리산 상선암사", "지리산 상선암차")
    name = name.replace("문재필 육칠갤러리", "문재필 옻칠갤러리")
    name = name.replace("백학제다.", "백학제다")
    name = name.replace("도자기마을(빌살)", "도자기마을 (빛살)")
    name = name.replace("도자기마을(빛살)", "도자기마을 (빛살)")
    name = name.replace("드내뜰(이종주의 도자기)", "드네플 (이종주의 도자기)")
    name = name.replace("순처대학교", "순천대학교")
    name = name.replace("고려전태국제선자", "고려천태국제선차")
    name = name.replace("해*이죠슈미", "喜闈陶瓷公司")
    name = name.replace("껌 5xF x 휴코퍼레이션 x 북경도사", "茗譪天下 x 흑유피련신 x 북경도사")
    name = name.replace("일삼차(로스포) 피웃음조", "일상다반사")
    name = name.replace("a 조", "쪽빛나라")
    name = name.replace("대링목공예", "대림목공예")
    name = name.replace("독성명차", "동심명차")
    name = name.replace("동정보이차 노반차품", "동정보이차 노반장홍")
    name = name.replace("동정보이차 노반차품.", "동정보이차 노반장홍")
    name = name.replace("원유 •전통", "원유전통")
    name = name.replace("자연으로 몽크씨", "자연으로 웅크려")
    name = name.replace("재단법인 하동차&바이오진흥원", "하동녹차연구소 / 하동녹차 & 바이오진흥원")
    name = name.replace("정광잎차", "징광잎차")
    name = name.replace("조태연가 3로차", "조태연가 죽로차")
    name = name.replace("대통령 표창 수상 꽃차 하늘바라기", "꽃차 하늘바라기")
    name = name.replace("귀단요 성탄송운,", "귀단요 성탄송운")
    
    # Trim brackets, spaces, prefix noise
    name = name.strip()
    name = re.sub(r"^[\[\_\s\#\-\|\d\:\*]+", "", name)
    name = re.sub(r"[\]\,\s]+$", "", name)
    name = name.replace("A!! 우유장작가마 실래요 무유장작가마 살래요", "무유장작가마 살래요")
    name = name.replace("A29 토라 (토라", "토리")
    name = name.replace("A29 토라", "토리")
    name = name.replace("D9 조태연가 죽로차 조태연가 3로차", "조태연가 죽로차")
    name = name.replace("D9 조태연가 죽로차 조태연가 죽로차", "조태연가 죽로차")
    name = name.replace("E27 백암요 백암효", "백암요")
    name = name.replace("B2! 난강노예 언양도예", "언양도예")
    name = name.replace("222 [청담요", "청담요")
    name = name.replace("FI7 김해요", "김해요")
    name = name.replace("드내뜰(이종주의 도자기) 드내뜰(이종주의 도자기)", "드네플 (이종주의 도자기)")
    name = name.replace("월 2은 데 랑카티스(스리랑카 홍차)", "랑카티스 (스리랑카 홍차)")
    name = name.replace("조-YIN TEA", "尹家人 · YIN TEA")
    name = name.replace("선요당 (총0호) CHINA TEA", "선묘당 (善妙堂) CHINA TEA")
    name = name.replace("경위복차 (가인갤러리)", "경위복지 (가인갤러리)")
    name = name.replace("소랑요 소랑요", "소랑요")
    name = name.replace("소산도예 소산도예", "소산도예")
    name = name.replace("소아다원 소아다원", "소아다원")
    name = name.replace("대통령 표창 수상_꽃차 하늘바라기", "꽃차 하늘바라기")
    name = name.replace("언담", "연담")
    name = name.replace("가현아트", "가헌아트")
    name = name.replace("기린공방", "기천공방")
    name = name.strip()
    return name

final_dict = {}
for bid, name in final_exhibitors.items():
    final_dict[bid] = clean_exhibitor_name(name)

# Sort and output
sorted_ids = sorted(final_dict.keys(), key=lambda x: (x[0], int(x[1:])))

# Print as JS code block
print(f"// Parsed and merged {len(sorted_ids)} exhibitors.")
print("const RAW_EXHIBITORS = [")
sections = {
    'A': "SECTION A: 외곽 및 벽면 부스 (Perimeter)",
    'B': "SECTION B: 1열 (B 섬식 부스)",
    'C': "SECTION C: 2열 (C 섬식 부스)",
    'D': "SECTION D: 3열 (D 섬식 부스)",
    'E': "SECTION E: 4열 (E 섬식 부스)",
    'F': "SECTION F: 5열 (F 섬식 부스)",
    'G': "SECTION G: 6열 (G 섬식 부스)",
    'H': "SECTION H: 7열 (H 섬식 부스)"
}

current_sec = None
for bid in sorted_ids:
    sec = bid[0]
    if sec != current_sec:
        current_sec = sec
        print(f"\n  // {sections[sec]}")
    print(f'  {{ id: "{bid}", name: "{final_dict[bid]}" }},')
print("];")
