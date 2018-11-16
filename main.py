import requests


def main():
    r = requests.post("http://127.0.0.1:5000/api/new_patient",
                      json={
                          "patient_id": 1,
                          "attending_email": "sharon.sangermano@duke.edu",
                          "user_age": 50,
                      })
    data = r.json()
    print(data)

    r2 = requests.post("http://127.0.0.1:5000/api/heart_rate",
                       json={
                          "patient_id": 1,
                          "heart_rate": 100,
                            })
    hr_data = r2.json()
    print(hr_data)

    r3 = requests.get("http://127.0.0.1:5000/api/status/1")
    status_data = r3.json()
    print(status_data)

    r4 = requests.get("http://127.0.0.1:5000/api/heart_rate/1")
    hr_list = r4.json()
    print(hr_list)

    r5 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/1")
    avg = r5.json()
    print(avg)

    r6 = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average",
                       json={
                           "patient_id": 1,
                           "heart_rate_average_since": "2018-03-09 11:00:"
                                                       "36.372339"
                       })
    ave_since = r6.json()
    print(ave_since)

    r7 = requests.post("http://127.0.0.1:5000/api/heart_rate",
                       json={
                           "patient_id": 2,
                           "heart_rate": 100,
                       })
    hr_data = r7.json()
    print(hr_data)

    r8 = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average",
                       json={
                           "patient_id": 2,
                           "heart_rate_average_since": "2018-03-09 11:00:"
                                                       "36.372339"
                       })
    ave_since = r8.json()
    print(ave_since)

    r9 = requests.get("http://127.0.0.1:5000/api/status/2")
    status_data = r9.json()
    print(status_data)

    r10 = requests.get("http://127.0.0.1:5000/api/heart_rate/2")
    hr_list = r10.json()
    print(hr_list)

    r11 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/2")
    avg = r11.json()
    print(avg)

    r12 = requests.post("http://127.0.0.1:5000/api/new_patient", json={
                          "patient_id": 1,
                          "attending_email": "sharon.sangermano@duke.edu",
                          "user_age": 50,
                      })
    data = r12.json()
    print(data)


if __name__ == "__main__":
    main()
