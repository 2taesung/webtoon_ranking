import requests
from bs4 import BeautifulSoup

# url을 받아서 id를 구해준다 Ex) url 옴니버스 장르면 그 화면에 있는 모든 웹툰들의 아이디
def get_ids(url):
    try:
       
        response = requests.get(url)
        soup = BeautifulSoup(response.text ,'html.parser')
        li_list = soup.select('#content > div.list_area > ul > li')
        webtoon_id=[]
        for li in li_list:
            a_tag = li.select_one('dl > dt > a')
            id = a_tag['href'].split('=')[1]
            webtoon_id.append(id)
        return webtoon_id

    except :
        print('id 함수 문제')

# 장르의 url을 받아 완결되지 않은 웹툰의 [순위, 웹툰의 이름] 리스트와 연재 중인 웹툰들의 url을 리스트로 반환한다.
def not_finish_get_href(url,finish_id):
    response = requests.get(url)
    soup = BeautifulSoup(response.text ,'html.parser')
    li_list = soup.select('#content > div.list_area > ul > li')
    hrefs=[]
    name=[]
    img_url=[]
    id_list = []
    url_='https://comic.naver.com'
    for li in li_list:
        a_tag = li.select_one('dl > dt > a')
        a_img = li.select_one('div > a > img')
        id = a_tag['href'].split('=')[1]
        if id not in finish_id:
            hrefs.append(url_ + a_tag['href'])
            name.append(a_tag['title'])
            img_url.append(a_img['src'])
            id_list.append(id)
    total_not_finish = []
    for i in range(0, len(name)):
        total_not_finish.append([i+1,name[i]])
    return total_not_finish, hrefs, id_list
# total_not_finish = [[순위, 웹툰 이름], [ ], .... ] / hrefs = [href, href, ...]

# 웹툰 url 리스트를 받아 최근 5편의 별점 평균을 계산한 후 아이디와 별점점수 리스트 반환
def get_star(total_not_finish, not_finish_hrefs):
    total_star_list = []
    average_star = []
    for url in not_finish_hrefs:
        response = requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')
        star =[]
        count=1
        star_list=soup.select('div.rating_type > strong')
        if len(star_list) > 4:
            for strong in star_list:
                if count>5:
                    break
                else:
                    star.append(float(strong.get_text()))
                    count+=1
        else:
            for strong in star_list:
                star.append(float(strong.get_text()))
        average_star.append(sum(star) / len(star))
    for i in range(0, len(average_star)):
        total_star_list.append([total_not_finish[i][1],average_star[i]])
    return total_star_list
    # [[웹툰 이름, 별점 평균], [ ], .... ]

# 웹툰 댓글 크롤러
'''
def comment_list(href_list,id_list):
    contents_list=[]

    for href,id in zip(href_list,id_list):
        try:
            response = requests.get(href)
            soup = BeautifulSoup(response.text ,'html.parser')
            epi_num = int(soup.select('td.title')[0].select_one('a')['href'].split('&')[1][3:])
            co_list=[]
            if epi_num>5:
                for i in range(5):
                    url = href + '&no=' + str(epi_num)
                    obj_id = id + "_" + str(epi_num)
                    get_comment(url,obj_id,co_list)
                    epi_num-=1
                contents_list.append(co_list)
            else:
                a=epi_num
                for i in range(epi_num):
                    if a != 0:
                        url = href + '&no=' + str(a)
                        obj_id = id + "_" + str(a)
                        get_comment(url,obj_id,co_list)
                        a-=1
                    else:
                        break
                contents_list.append(co_list)
        except :
            print(href)

    return contents_list

total_comments_list = get_comments()   
        

def get_comment(url,obj_id,contents_list):
    try:
        
        headers = {
            'referer': url,
        }

        params = (
            ('ticket', 'comic'),
            ('pool', 'cbox3'),
            ('lang', 'ko'),
            ('objectId', obj_id),
        )

        response = requests.get('https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json', headers=headers, params=params)

        idx=response.text.find('(') +1
        re=response.text[idx:]
        
        result=json.loads(re[:-2])
        comment_list=result['result']['commentList']

        for list in comment_list:
            comment=list['contents']
            contents_list.append(comment)
    except :
        print('댓글 긁기 문제')
'''
# 댓글 감정분석 결과.
episode_comments_score = [0.44582364, 0.4283107, 0.4431868, 0.54799104, 0.27183583, 0.40126446, 0.39778888, 0.4346631, 0.44238767, 0.44625786, 0.44454116, 0.51892364, 0.5754154, 0.36440837, 0.6513204, 0.49597123, 0.34918538, 0.44110745, 0.32799473, 0.3125381, 0.43530437, 0.39363334, 0.4380319, 0.7559797, 0.37864575, 0.4093229, 0.19624378, 0.4227675, 0.3835326, 0.322575, 0.33216202, 0.19577095]
omnibus_comments_score = [0.33407506, 0.3769576, 0.5178049, 0.3927674, 0.63748896, 0.36626205, 0.3823021, 0.43161827, 0.27108863, 0.56014484, 0.60556227, 0.38769692, 0.34178734]
# story_comments_score = [0.41392612, 0.42335984, 0.41584602, 0.30441797, 0.32819417, 0.44181988, 0.49200606, 0.40314934, 0.42360526, 0.48665234, 0.34661412, 0.3718951, 0.46582568, 0.2904135, 0.3293913, 0.22364894, 0.36705866, 0.49405494, 0.3874067, 0.3819858, 0.38955426, 0.43242776, 0.46278137, 0.3573703, 0.42506576, 0.44002837, 0.523549, 0.30575266, 0.48441374, 0.27414143, 0.46186915, 0.3784966, 0.37499714, 0.48857114, 0.24855307, 0.34011567, 0.46495017, 0.4987188, 0.39844483, 0.4004149, 0.14779153, 0.48683035, 0.45587882, 0.41666505, 0.46999565, 0.5685194, 0.41990426, 0.29783937, 0.5248795, 0.5006184, 0.5236481, 0.45203587, 0.32066005, 0.39071074, 0.38094285, 0.22046834, 0.47170433, 0.601937, 0.42305046, 0.43864322, 0.40762436, 0.5308628, 0.33207837, 0.21209629, 0.39061058, 0.42361107, 0.51954, 0.25223204, 0.28961354, 0.2503189, 0.28471804, 0.49403694, 0.42005444, 0.5, 0.384046, 0.4633852, 0.38354945, 0.18640444, 0.43756503, 0.3873757, 0.43831283, 0.3803602, 0.5262491, 0.34404182, 0.4861185, 0.42306176, 0.41880542, 0.28884938, 0.49829492, 0.4515239, 0.46863997, 0.48837718, 0.33763814, 0.39805198, 0.6254221, 0.5274894, 0.34873736, 0.45534152, 0.35887897, 0.18875572, 0.4135414, 0.4888159, 0.24622217, 0.5304364, 0.1282668, 0.45766354, 0.54252154, 0.38229033, 0.44601932, 0.23648813, 0.6272757, 0.18557186, 0.37168622, 0.2571017, 0.5535063, 0.43126297, 0.29189378, 0.5394913, 0.39950275, 0.37707034, 0.5628923, 0.25919712, 0.4989074, 0.3006881, 0.06527476, 0.44518337, 0.2531587, 0.5541031, 0.5293797, 0.6230622, 0.5931255, 0.17221361, 0.6572047, 0.5067751, 0.31239477, 0.22507524, 0.27824986, 0.48299956, 0.44566146, 0.3151209, 0.5287317, 0.44456863, 0.42756703, 0.19394325, 0.5690578, 0.31029224, 0.36617595, 0.3771612, 0.07623052, 0.35329542, 0.44394684, 0.5825952, 0.17906599, 0.43410987, 0.28511256, 0.308986, 0.41989267, 0.23948461, 0.42061096, 0.3768183, 0.42539284, 0.34097907, 0.41402978, 0.4184852, 0.07969564, 0.13626397, 0.45084172, 0.5522376, 0.41574356, 0.58435434, 0.54989487, 0.47526962, 0.49373773, 0.64815086, 0.38347843, 0.15758383, 0.4904503, 0.6242693, 0.18437672, 0.3675658, 0.42748928, 0.53471595, 0.39028466, 0.30811027, 0.24750721, 0.11994897, 0.13345987, 0.5388022, 0.2122373, 0.4242862, 0.42966953, 0.321881, 0.38424733, 0.37043774, 0.22162315, 0.3331424, 0.49257812, 0.55482775, 0.48513204, 0.17311954, 0.46358636, 0.35275006, 0.40182737, 0.24377067, 0.18845774, 0.4531533, 0.4329365, 0.3358048, 0.44996604, 0.5781627, 0.2770878, 0.18119098, 0.49205807, 0.48701692, 0.29830566, 0.38594487, 0.2928216, 0.2850643, 0.49081725, 0.33553433, 0.4512813, 0.2992505, 0.43528187, 0.27920127, 0.21601659, 0.31772903, 0.14453569, 0.2675604, 0.29242533, 0.2260574, 0.63447005, 0.4125265, 0.57184714, 0.31000957, 0.30253512, 0.31070298, 0.37339377, 0.6539565, 0.5527697, 0.26636302, 0.3769781, 0.13666697, 0.20700003, 0.4855844, 0.30153874, 0.4018412, 0.490527, 0.5703311, 0.20811254, 0.42287394, 0.4480192, 0.31041318, 0.45199957, 0.47729203, 0.31562224, 0.4887777, 0.3108881, 0.33968902, 0.17995901, 0.32885125, 0.38547722, 0.40618756, 0.4742279, 0.5288545, 0.4000683, 0.44486773, 0.5704473, 0.35710746, 0.28942868, 0.59333116, 0.4514856, 0.23047706, 0.49702933, 0.30367473, 0.39466515, 0.29920772, 0.32981881, 0.38226303, 0.23306736, 0.17870224, 0.5538376, 0.17805435, 0.28216165, 0.44253758]
story_comments_score = [0.36009964, 0.38116375, 0.36093274, 0.24880593, 0.28963643, 0.38936168, 0.40834677, 0.32703128, 0.3410514, 0.31934503, 0.40911618, 0.2841623, 0.38206512, 0.24227563, 0.28246814, 0.19538356, 0.31615174, 0.44425377, 0.313004, 0.22309303, 0.3134755, 0.38605613, 0.39086545, 0.28829277, 0.361966, 0.36240798, 0.4675913, 0.27388582, 0.42680454, 0.24231966, 0.4092879, 0.33095813, 0.37697557, 0.22596675, 0.32930347, 0.28933406, 0.42360914, 0.42836502, 0.349947, 0.33171862, 0.13951783, 0.46503422, 0.38890186, 0.34587532, 0.4411172, 0.48697305, 0.36787602, 0.36971328, 0.26062497, 0.43221736, 0.42992723, 0.47717622, 0.35422716, 0.35706067, 0.25570402, 0.3619095, 0.18731882, 0.42382154, 0.54660416, 0.4093328, 0.3491406, 0.47197795, 0.2868383, 0.1905149, 0.35592014, 0.41591412, 0.34255275, 0.21808273, 0.22756557, 0.24605343, 0.24313676, 0.3989927, 0.35287753, 0.5, 0.3473202, 0.44045216, 0.3585911, 0.16766535, 0.35746357, 0.33106616, 0.38642028, 0.4875674, 0.3352499, 0.31654158, 0.35938847, 0.24638706, 0.36291996, 0.40906742, 0.45095432, 0.37811193, 0.4218792, 0.3598473, 0.3691585, 0.53755534, 0.29558614, 0.3603344, 0.28367215, 0.44523454, 0.323926, 0.3598941, 0.16060856, 0.4444887, 0.44034776, 0.22329742, 0.21078296, 0.11235017, 0.4787396, 0.3825974, 0.40538287, 0.15817653, 0.31455374, 0.55573535, 0.30788624, 0.2248591, 0.05507217, 0.48861256, 0.3904317, 0.5071306, 0.20318796, 0.38328364, 0.47963306, 0.32738152, 0.40079513, 0.2208532, 0.26982537, 0.22765447, 0.36171758, 0.49853554, 0.47907037, 0.5324997, 0.49616468, 0.1390113, 0.46813458, 0.5912779, 0.1992246, 0.29688734, 0.38709873, 0.42644498, 0.27654612, 0.46431926, 0.37091553, 0.1724869, 0.36516488, 0.3000939, 0.5075292, 0.0740613, 0.27009448, 0.2837317, 0.34157646, 0.3734767, 0.5161188, 0.34759772, 0.27994454, 0.26056722, 0.3723051, 0.20501323, 0.14905213, 0.18855362, 0.34000492, 0.32007182, 0.07066809, 0.30026087, 0.3472986, 0.35112703, 0.3663788, 0.12161285, 0.518899, 0.32163826, 0.48288482, 0.37000084, 0.4566842, 0.39490962, 0.40257278, 0.3102912, 0.5751448, 0.41875947, 0.5648799, 0.13006154, 0.14122209, 0.1772074, 0.32090518, 0.32469392, 0.4865548, 0.10392085, 0.51826155, 0.3489955, 0.2443594, 0.26310855, 0.15979807, 0.3700434, 0.38365993, 0.2770207, 0.31954142, 0.28573126, 0.1966488, 0.3077517, 0.44230595, 0.48725975, 0.44055733, 0.15611032, 0.4082445, 0.3032674, 0.22283758, 0.40155914, 0.3617755, 0.355331, 0.42044213, 0.26061606, 0.16903609, 0.23704138, 0.5212318, 0.15266252, 0.42840123, 0.27693275, 0.44741082, 0.33216098, 0.24288155, 0.27740538, 0.42466217, 0.29387304, 0.39840907, 0.2708617, 0.32917348, 0.2500695, 0.19082494, 0.27877274, 0.12225566, 0.23875384, 0.20250286, 0.2631536, 0.60257155, 0.4928962, 0.34032553, 0.27906665, 0.27459818, 0.2850352, 0.35078445, 0.59180164, 0.47838074, 0.3375571, 0.22909628, 0.12597555, 0.1775192, 0.4265074, 0.26356608, 0.34437737, 0.44923577, 0.18454672, 0.49218854, 0.40143204, 0.4053942, 0.2051791, 0.455793, 0.41700143, 0.2803502, 0.44952312, 0.28059062, 0.31615007, 0.15546387, 0.43588912, 0.298356, 0.48164365, 0.339895, 0.30705664, 0.368072, 0.5516606, 0.41299915, 0.2396324, 0.28705904, 0.5015962, 0.45229098, 0.20474686, 0.46178454, 0.26928484, 0.35529152, 0.24528547, 0.28089365, 0.2165192, 0.15651208, 0.3369529, 0.4693681, 0.14653422, 0.23662275, 0.39286983, 0.2469665, 0.18176624, 0.2384326, 0.27186602, 0.39045528, 0.17682132, 0.29491448, 0.2784644, 0.1601976, 0.46975017, 0.5960243, 0.27716002, 0.03910205, 0.5]

finish_url = 'https://comic.naver.com/webtoon/finish.nhn'

webtoon_url = {'에피소드':'https://comic.naver.com/webtoon/genre.nhn?genre=episode',
'옴니버스':'https://comic.naver.com/webtoon/genre.nhn?genre=omnibus',
'스토리' :'https://comic.naver.com/webtoon/genre.nhn?genre=story'}

# 장르 입력을 받아서 genre에 저장
genre=input('장르를 입력해주세요(에피소드, 옴니버스, 스토리) :')
# 완결 웹툰의 id를 저장해놓기
finish_id=get_ids(finish_url)
# 완결웹툰 id와 입력받은 genre를 url딕셔너리에 넣어 장르에 맞는 url not_finish_get_href함수의 인풋으로 넣는다
# 그리고 output으론 각 장르의 완결이 아닌 웹툰의 url과 이름을 리스트로 반환한다.

total_not_finish, not_finish_hrefs, id_list = not_finish_get_href(webtoon_url[genre],finish_id)

total_star_list = get_star(total_not_finish, not_finish_hrefs)


if genre == '에피소드': total_comments_list = episode_comments_score
elif genre == '옴니버스': total_comments_list = omnibus_comments_score
else: total_comments_list = story_comments_score

# 별점 점수와, 원래 순위 점수와, 댓글 감정분석 점수로 최종 점수를 도출하는 모델
def rearrange_list(total_not_finish, total_star_list, total_comments_list): 
    new_score_list = []
    total_new_list = []
    rank_dif_list=[]
    rank_p_dif_list=[]
    rank_n_dif_list=[]
    search_dic ={}
    for i in range(0, len(total_not_finish)):
        popular_score = 1 - (total_not_finish[i][0]*1/len(total_not_finish))
        star_score = total_star_list[i][1]/10
        comments_score = total_comments_list[i]
        score = 0.4*popular_score + 0.4*star_score +0.2*comments_score
        new_score_list.append([total_not_finish[i][1], score])

    rearrange_list = sorted(new_score_list, key=lambda x:x[1], reverse=True)   
    
    for i in range(0, len(rearrange_list)):   
        total_new_list.append([i+1, rearrange_list[i][0], rearrange_list[i][1]])

    
    for list in total_new_list :
        search_dic[list[1]] = list[0]

    for list in total_not_finish:
        new_rank = search_dic[list[1]]
        rank_dif = list[0] - new_rank
        rank_dif_list.append(rank_dif)
        if rank_dif > 0 :  
            rank_p_dif_list.append(rank_dif)
            rank_n_dif_list.append(0)
        elif rank_dif < 0 :
            rank_p_dif_list.append(0)
            rank_n_dif_list.append(rank_dif)
        else:
            rank_p_dif_list.append(rank_dif)
            rank_n_dif_list.append(rank_dif)

    #print(total_new_list)
    return total_new_list, rank_dif_list, rank_n_dif_list, rank_p_dif_list

new_list, rank_dif_list, rank_n_dif_list, rank_p_dif_list = rearrange_list(total_not_finish, total_star_list, total_comments_list)
# 재배열 리스트 = [[순위, 제목, 점수], [], ..]

origin_list = []
for i in range(0, len(rank_dif_list)):
    origin_list.append([total_not_finish[i][0], total_not_finish[i][1], rank_dif_list[i]])

# origin_list = [[순위, 제목, 변동], [], ..]
# new_list = [[순위, 제목, 점수], [], ..]

# total_not_finish 와 total_new_list를 dataframe을 활용하여 시각화
import pandas as pd

df_origin = pd.DataFrame(origin_list)
df_origin.columns = ['순위', '제목', '변동']
df_origin = df_origin.set_index("순위")
df_new = pd.DataFrame(new_list)
df_new.columns = ['순위', ' 제목', '최종 점수']
df_new = df_new.set_index("순위")


df = pd.merge(df_origin, df_new, on='순위')
df.columns = ['기존 차트', '순위 변동', '새로운 차트', '최종 점수']

print(df)
# 시각화
ori_rank=[x[0] for x in total_not_finish]
import matplotlib.pyplot as plt

plt.bar(ori_rank,rank_n_dif_list,color='red')
plt.bar(ori_rank,rank_p_dif_list,color='blue')
plt.show()


# 장르 - 스토리 
# total_not_finish = [[1, '복학왕'], [2, '외모지상주의'], [3, '고수'], [4, '헬퍼 2 : 킬베로스'], [5, '여신강림'], [6, '싸움독학'], [7, '더 복서'], [8, '연애혁명'], [9, '갓 오브 하이스쿨'], [10, '호랑이형님'], ...]
# total_star_list = [['복학왕', 2.428], ['외모지상주의', 0.4419999999999984], ['고수', 0.12399999999999878], ['헬퍼 2 : 킬베로스', 5.792], ['여신강림', 1.1419999999999995], ['싸움독학', 0.6180000000000003], ['더 복서', 0.08000000000000007], ['연애혁명', 0.8019999999999996], ['갓 오브 하이스쿨', 0.958000000000002], ['호랑이형님', 0.03200000000000003],..]

# total_new_list 
# [[1, '고수'], [2, '더 복서'], [3, '호랑이형님'], [4, '전지적 독자 시점'], [5, '외모지상주의'], [6, '후기'], [7, '바른연애 길잡이'], [8, '취사병 전설이 되다'], [9, '이두나!'], [10, '프리드로우'],
# [11, '랜덤채팅의 그녀!'], [12, '싸움독학'], [13, '열렙전사'], [14, '파이게임'], [15, '소녀의 세계'], [16, '백수세끼'], [17, '뷰티풀 군바리'], [18, '개를 낳았다'], [19, '비질란테'], [20, '재혼 황후'], 
# [21, '1초'], [22, '연애혁명'], [23, '하루만 네가 되고 싶어'], [24, '경비 배두만'], [25, '헬58'], [26, '신도림'], [27, '사신소년'], [28, '갓 오브 하이스쿨'], [29, '운수 오진 날'], [30, '화이트 블러드'], 
# [31, '튜토리얼 탑의 고인물'], [32, '간 떨어지는 동거'], [33, 'POGO 공포단편선 - 혼집'], [34, '여신강림'], [35, '장씨세가 호위무사'], [36, '나노마신'], [37, '중증외상센터 : 골든 아워'], [38, '격기3반'], [39, '이번 생도 잘 부탁해'], [40, '소녀재판'], 
# [41, '초인의 시대'], [42, '가담항설'], [43, '여주실격!'], [44, '앵무살수'], [45, '하드캐리'], [46, '스터디그룹'], [47, '로어 올림푸스'], [48, '토끼대왕'], [49, '낙향문사전'], [50, '남주의 첫날밤을 가져버렸다'],
# [51, '윈드브레이커'], [52, '일렉시드'], [53, '피와 살'], [54, '유일무이 로맨스'], [55, '맘마미안'], [56, '캐슬'], [57, '빌드업'], [58, '걸어서 30분'], [59, '고삼무쌍'], [60, '전자오락수호대'],
# [61, '도망자'], [62, '선의의 경쟁'], [63, '원주민 공포만화'], [64, '꽃만 키우는데 너무강함'], [65, '난약'], [66, '복학왕'], [67, '민간인 통제구역'], [68, '판타지 여동생!'], [69, '신의 탑'], [70, '극야'], 
# [71, '에리타'], [72, '원수를 사랑하라'], [73, '무사만리행'], [74, '구남친이 내게 반했다'], [75, '피와 나비'], [76, '집이 없어'], [77, '관계의 종말'], [78, '트롤트랩'], [79, '광해의 연인'], [80, '체크포인트'], 
# [81, '상남자'], [82, '견우와 선녀'], [83, '가타부타타'], [84, '각자의 디데이'], [85, '평범한 8반'], [86, '냐한남자'], [87, '사냥개들'], [88, '현혹'], [89, '연놈'], [90, '당신의 과녁'], 
# [91, '귀곡의 문'], [92, '어글리 피플즈'], [93, '플레이어'], [94, '갓핑크'], [95, '두번째 생일'], [96, '행성인간'], [97, '갓물주'], [98, '사이드킥 2~3'], [99, '나를 바꿔줘'], [100, ' 이츠마인'], 
# [101, '쿠베라'], [102, '합격시켜주세용'], [103, '복학생 정순이'], [104, '링크보이'], [105, '땅 보고 걷는 아이'], [106, '용왕님의 셰프가 되었습니다'], [107, '레사 시즌2~3'], [108, '마법스크롤 상인 지오'], [109, '구름이 피워낸 꽃'], [110, '아홉수 우리들'],
# [111, '더 트웰브'], [112, '백년게임'], [113, '사장님을 잠금해제'], [114, '언메이크'], [115, '아도나이'], [116, '옆집친구'], [117, '더 게이 머'], [118, '친애하는 X'], [119, '소심한 팔레트'], [120, '신비'], 
# [121, '나이트런'], [122, '악마와 계약연애'], [123, '남자주인공의 여자사람친구입니다'], [124, '교환일기'], [125, '가슴털 로망스'], [126, '미래의 골동품 가게'], [127, '고래별'], [128, '침범'], [129, '정순애 식당'], [130, '최강전설 강해효'], 
# [131, '닥터 하운드'], [132, '3cm 헌터'], [133, '커피도둑'], [134, '아는 여자애'], [135, '금혼령-조선 혼인금지령'], [136, '문래빗'], [137, '인어를 위한 수영교실'], [138, '안녕, 이바다씨'], [139, '삶이 우리를 속일지라도'], [140, '제로게임'], 
# [141, '무모협지'], [142, '정년이'], [143, '집사레인저'], [144, '럭키언럭키'], [145, '그놈은 흑염룡'], [146, '셧업앤댄스'], [147, '새벽 두 시의 신데렐라'], [148, '압락사스'], [149, '공유몽'], [150, '얼굴천재'], [151, '탑코너'], [152, '이것도 친구라고'], [153, '일진이 
# 사나워'], [154, '별을 삼킨 너에게'], [155, '꿈의 기업'], [156, '열불 로맨스'], [157, '한강예찬'], [158, '가비지타임'], [159, '강남도깨비'], [160, '닥터 프로스트 시즌 3~4'], 
# [161, '안개무덤'], [162, '도롱이'], [163, '리턴 투 플레이어'], [164, '드로잉 레시피'], [165, '동트는 로맨스'], [166, '오파츠'], [167, '학교정벌'], [168, '신의 언어'], [169, '헬퍼 2 : 킬베로스'], [170, '은주의 방 2~3부'], 
# [171, '동네 몬스터'], [172, '위대한 방옥숙'], [173, '완벽한 가족'], [174, '텃밭부 사건일지'], [175, '저무는 해, 시린 눈'], [176, '어쩔꼰대'], [177, '피라미드 게임'], [178, '구독금지'], [179, '얌전한 사이'], [180, ' 피노키오 소녀'], 
# [181, '아르세니아의 마법사'], [182, '별이삼샵'], [183, '칼부림'], [184, '롤랑롤랑'], [185, '틴맘'], [186, '골든 체인지'], [187, '사우러스'], [188, '도플갱어의 게임'], [189, '와이키키 뱀 파이어'], [190, '올가미'], 
# [191, '피플'], [192, '데드라이프'], [193, '날 가져요'], [194, '숲속의 담'], [195, '스캔들'], [196, '너의 미소가 함정'], [197, '킬더킹'], [198, '소녀180'], [199, '그날 죽은 나는'], [200, '셈하는 사이'],
# [201, '겟라이프'], [202, '평행도시'], [203, '라일락 200%'], [204, '언데드'], [205, '정보전사 202'], [206, '나의 우주'], [207, '노력의 결과'], [208, '왕세자 입학도'], [209, '도를아십니까'], [210, '아테나 컴플렉스'], 
# [211, '별종'], [212, '손아귀'], [213, '구주의 시간'], [214, '너에게만 보이는'], [215, '괴물신부'], [216, '오버더문'], [217, '잉여특공대'], [218, '저세상 클라스!'], [219, '커넥트'], [220, '미드나잇 체이서'], 
# [221, '헬로도사'], [222, '스테어스'], [223, '스윗솔티'], [224, '안식의 밤'], [225, '여기 악마가 있어'], [226, '조선홍보대행사 조대박'], [227, '9등급 뒤집기'], [228, '필살VS로맨스'], [229, '버그'], [230, '감히'], 
# [231, '두근두근 네가 좋아서'], [232, '개미'], [233, '아이고 아이고'], [234, '나쁜 쪽으로'], [235, '지구멸망버튼'], [236, '온새미로'], [237, '꼬맹이를  부탁해!'], [238, '그 판타지 세계에서 사는 법'], [239, '하슬라'], [240, '불릿 6미리'], 
# [241, '신이 담긴 아이'], [242, '뱀파이어의 꽃'], [243, '천도'], [244, '장단에 맞춰줘!'], [245, '11me'], [246, '빛빛빛'], [247, '무주의 맹시'], [248, '거미'], [249, '꽃 피는 날'], [250, '소녀 해미'], [251, '천사가 아니야'], [252, '몽홀'], [253, '우주최강대스타'], [254, '합법해적 파르페'], [255, '기억흔적'], [256, '인싸 라이프'], [257, '여름은 뜨겁다'], [258, '갓도령스'], [259, '백호랑'], [260, '죽여주는 탐정님'], [261, '만찢남녀'], [262, '노선도'], [263, '꼬리 있는 연애'], [264, '밤하늘에 구름운'], [265, '그녀의 버킷리스트'], [266, 'Here U Are'], [267, '갑자기 커피'], [268, '물레'], [269, '에이머'], [270, '오늘도 사랑하세요'], [271, '열등의 조건'], [272, '스몰'], [273, '신선비'], [274, '모락모락 왕세자님'], [275, '하 우스키퍼'], [276, '결백한 사람은 없다'], [277, '위험한 신입사원'], [278, '함부로 대해줘'], [279, '도사 가온'], [280, 'FM보이'], [281, '깁스맨'], [282, '나의 첫번째 새벽'], [283, '방탈출'], [284, '누군가 의 로섬'], [285, '데이즈'], [286, '먹지마세요'], [287, '다이스(DICE)'], [288, '저승사자 출입금지'], [289, '선녀야 야옹해봐!'], [290, '인간의 온도'], [291, '오일머니'], [292, '마도'], [293, '법대로 사랑하라'], [294, '8월의 눈보라'], [295, '비스타'], [296, '블루투스']]