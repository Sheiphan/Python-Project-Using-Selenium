from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://ai-jobs.net/')
k = 30
j = 200
for i in range(0, 14):

    # Click in the Job role
    driver.find_element(By.CSS_SELECTOR, f'[id=id_cat_{i}]').click()

    # Click on the search
    driver.find_element(By.CSS_SELECTOR, '[class ="btn btn-primary p2-3 px-sm-4 ms-1 ms-sm-2 my-auto"]').click()
    time.sleep(1)

    # To click the all the Load More in the page
    element = driver.find_element(By.CSS_SELECTOR, '[class="text-primary mt-2"]')
    a, b = 14000, 14900

    # Scroll to the element to make it visible
    while element.text == 'Load more':
        driver.execute_script(f"window.scrollTo({a},{b})")
        time.sleep(1)

        # Click the element
        element.click()
        time.sleep(2)
        try:
            driver.find_element(By.CSS_SELECTOR, '[class="text-primary mt-2"]')
            element = driver.find_element(By.CSS_SELECTOR, '[class="text-primary mt-2"]')
        except:
            break

        a = a + 14000
        b = b + 14620

    # Scroll to the top
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(1)

    # # Company Name
    # for div in driver.find_elements(By.CSS_SELECTOR, '.m-0'):
    #     print(div.text)
    #     time.sleep(1)

    # Job Name
    Job_names = []
    print("Job Name")
    for div in driver.find_elements(By.CSS_SELECTOR, '.h5'):
        print(div.text)
        Job_names.append(div.text)

    data = {'Job_name': Job_names}

    df = pd.DataFrame(data)
    df.to_json(f'Job_Name_{i}')

    Location = []
    Type = []
    Level = []
    Pay = []
    all_tag = []

    for job_name in driver.find_elements(By.CSS_SELECTOR, '[class="col pt-2 pb-3"]'):
        job_info = job_name.text
        job_info_split = job_info.split('\n')
        sentence_list = [sentence for sentence in job_info_split]
        print(sentence_list)
        Location.append(sentence_list[0])
        Type.append(sentence_list[1])
        Level.append(sentence_list[2])
        Pay.append(sentence_list[3])

        # Click on the job-name
        try:
            job_name.click()
            time.sleep(1)
        except Exception as e:
            print('Job name:', e)
            all_tag.append('')
            continue

        # Get the Tags in it.
        all_p_tags = driver.find_elements(By.CSS_SELECTOR, 'p')
        l = []
        for tag in all_p_tags:
            if "Tags: " in tag.text:
                for t in tag.find_elements(By.CSS_SELECTOR, '[class="badge rounded-pill text-bg-light"]'):
                    tagss = t.text.split('\n')
                    for z in tagss:
                        l.append(z)
            else:
                continue
            print(l)
            all_tag.append(l)

        # To go back
        driver.back()
        time.sleep(1)
        # 493, 959

        # Keep Scrolling the Page
        driver.execute_script(f"window.scrollTo({k},{j})")
        time.sleep(1)
        k += 150
        j += 150

        print('--------------------------------------------')

    # Save the Tags into JSON
    data2 = {'Tags': all_tag}
    df2 = pd.DataFrame(data2)
    df2.to_json('Tags.json')

    # Save the Descriptions into JSON
    data = {'Location': Location,
            'Type': Type,
            'Level': Level,
            'Pay': Pay}
    df = pd.DataFrame(data)
    df.to_json(f'Job_descriptions_{i}')

    # Scroll Back to the top
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(1)

    # To unselect the Job description.
    driver.find_element(By.CSS_SELECTOR, f'[id=id_cat_{i}]').click()
driver.quit()
