import requests, json

token_url = "https://sandbox86.tactiorpm7000.com/token.php"
api_url = "https://sandbox86.tactiorpm7000.com/tactio-clinician-api/1.1.4/"

client_id = "083e9a44a763473fbeb62fbf90b74551"
client_secret = "ba09798f0921456e8b4e5e4588ea536d"
user = "tactioClinician"
pw = "tactio"

data = {'grant_type':'password', 'username':user, 'password':pw}

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

token = json.loads(access_token_response.text)['access_token']

hds={'Authorization': 'Bearer ' + token}
patient_info = {}
codes = ['390896004',
         '289183008',
         '16890009',
         '767002',
         '77068002',
         '113079009',
         '104584009',
         '28036006',
         '60621009',
         '248300009',
         '276361009',
         '434912009',
         '302788006',
         '78564009',
         '75367002',
         '386725007',
         '136009',
         '103228002',
         '13644009',
         '312260007',
         '444780001',
         '38341003',
         '197315008',
         '14740000',
         '443911005',
         '408591000',
         '271065008',
         '72313002',
         '271650006',
         '364075005']


for i in range(58):
    f = open("patients_super" + str(i) + ".txt", 'a+')
    patient_pms = {'count':10, 'page':i}
    patient_data_request_json = requests.get(api_url + 'Patient', params=patient_pms, headers =hds).json()

    for patient in patient_data_request_json['entry']:
        patient_id = str(patient['resource']['id'])
        gender = str(patient['resource']['gender'])
        patient_info[patient_id] = {}
        flag=0
        for j in range(250):
            obs_pms = {'subject':patient_id, 'count':10, 'page':j, 'code': codes}
            patient_observation_request_json = requests.get(api_url + 'Observation', params=obs_pms, headers=hds)
            patient_observation_request_json = patient_observation_request_json.json()
            if flag==1:
                break
            try:
                for obs in patient_observation_request_json['entry']:
                        SNOMED_code = str(obs['resource']['code']['coding'][1]['code'])
                        SNOMED_display = str(obs['resource']['code']['coding'][1]['display'])
                        date=str(obs['resource']['effectiveDateTime'])
                        value = obs['resource']['valueQuantity']['value']
                        if SNOMED_code in patient_info[patient_id].keys():
                            if date in patient_info[patient_id][SNOMED_code].keys():
                                flag=1
                                print("hi")
                                break
                            else:
                                patient_info[patient_id][SNOMED_code][date]=[SNOMED_display,value]
                        else:
                            patient_info[patient_id][SNOMED_code]={}
                            patient_info[patient_id][SNOMED_code][date]=[SNOMED_display,value]

            except IndexError:
                pass
            except KeyError:
                pass
        flag=0
        print("Incoming!!!")
        f.write(patient_id + ',' + gender + '\n')
        for code in patient_info[patient_id]:
            for info in patient_info[patient_id].items():
                f.write(code+str(info[0]) + ',' + str(info[1]) + '\n')

    f.close()
