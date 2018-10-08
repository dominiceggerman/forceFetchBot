# By Dominic Eggerman
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime

# Generate date range
def dateRangeGenerator():
    # Prepare start and end dates
    start_date = input("Start date (MM/DD/YYYY): ")
    month, day, year = map(int, start_date.split("/"))
    start_date = datetime.date(year, month, day)
    end_date = input("End date (MM/DD/YYYY): ")
    month, day, year = map(int, end_date.split("/"))
    end_date = datetime.date(year, month, day)

    # Return [range of dates] (inclusive)
    num_days = end_date - start_date
    return [(start_date + datetime.timedelta(days=d)).strftime("%m/%d/%Y") for d in range(0, num_days.days+1)]


# Check for jobs table  ?? some things in here are interacting strangely ??
def jobSelectCheck(pipe_id):
    # Try to select job table
    try:
        driver.find_element_by_css_selector("#reportResultTable")
        return True
    except:
        source_elem = driver.find_element_by_css_selector("#selFFPipeline")
        if int(pipe_id) != 122:  # ?? maybe change this logic
            source_elem.send_keys("250")
            time.sleep(0.1)
            source_elem.send_keys(Keys.RETURN)
        else:
            source_elem.send_keys("122")
            time.sleep(0.1)
            source_elem.send_keys(Keys.RETURN)
        return False

# Check for fetcher table
def tableChecker():
    # Try to switch driver to iframe and read status message
    try:
        driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[1])
        driver.find_element_by_class_name("statusMessageSuccess").text
        return True
    except:
        return False

# Run
if __name__ == '__main__':
    # List of strings for status of run
    log = []

    # Select pipeline
    pipe_id = input("Enter pipeline ID: ")
    # Check if int
    try:
        int(pipe_id)
    except ValueError:
        raise ValueError("The pipeline id you entered is not an integer.")

    # Select dataset
    dataset = input("Select dataset (opavail / gas_quality / no_notice etc.): ")
    if dataset not in ["opavail", "no_notice", "gas_quality", "segment_capacity", "index_of_customers"]:
        raise Exception("Select a dataset to force fetch (opavail, no_notice, gas_quality, segment_capacity, index_of_customers)")

    # Get the date range
    dates = dateRangeGenerator()

    try:
        # Start a Chrome driver
        driver = webdriver.Chrome("C:/Users/deggerman/chromedriver_win32/chromedriver.exe")
        # Navigate to page
        driver.get("http://gcc.genscape.com/GCCcontent/intranet/manual_normalization.php")
        # Wait and check for this string in title
        time.sleep(2)
        assert "Manual Operations" in driver.title

        # Select the job table for the source
        check_job_table = False
        while check_job_table is False:
            # Wait, find the source box, select source
            time.sleep(1)
            source_elem = driver.find_element_by_css_selector("#selFFPipeline")
            source_elem.send_keys("{0}".format(pipe_id))
            time.sleep(0.1)
            source_elem.send_keys(Keys.RETURN)
            check_job_table = jobSelectCheck(pipe_id)

        # Loop over the dates that were entered
        for date in dates:
            print("--- Excecuting manual operation for {0} ---".format(date))
            # Wait, find the date box, change date
            time.sleep(1)
            date_elem = driver.find_element_by_css_selector("#txtFFDateIn")
            driver.execute_script("arguments[0].setAttribute('value','{0}')".format(date), date_elem)
            # Wait, find the job with the desired dataset, click it
            time.sleep(2)
            job_table = driver.find_element_by_css_selector("#reportResultTable")
            jobs = job_table.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")  # Get table rows

            # Find job
            for j in jobs:
                # Get dataset text and arg text
                dset, arg = j.find_elements_by_tag_name("td")[0], j.find_elements_by_tag_name("td")[2]

                # opavail
                if dataset == "opavail":
                    if dset.text == dataset and arg.text == "manualRun=true":
                        # Select the job as an option
                        option = j.find_elements_by_tag_name("td")[0].find_element_by_tag_name("input")
                        # Click it
                        option.click()
                        break

                # no_notice
                elif dataset == "no_notice":
                    if dset.text == dataset and arg.text == "":
                        option = j.find_elements_by_tag_name("td")[0].find_element_by_tag_name("input")
                        option.click()
                        break

                # gas_quality
                elif dataset == "gas_quality":
                    if dset.text == dataset and arg.text == "":
                        option = j.find_elements_by_tag_name("td")[0].find_element_by_tag_name("input")
                        option.click()
                        break

                # segment_capacity
                elif dataset == "segment_capacity":
                    if dset.text == dataset and arg.text == "":
                        option = j.find_elements_by_tag_name("td")[0].find_element_by_tag_name("input")
                        option.click()
                        break
                
                # index_of_customers
                elif dataset == "index_of_customers":
                    if dset.text == dataset and arg.text == "":
                        option = j.find_elements_by_tag_name("td")[0].find_element_by_tag_name("input")
                        option.click()
                        break

                # Else break
                else:
                    print("No datasets matching {} found...".format(dataset))
                    break

            # Click fetch
            fetcher = driver.find_element_by_id("cmdFF")
            fetcher.click()
            
            # Loop until status is seen
            check_result = False
            while check_result is False:
                time.sleep(5)
                check_result = tableChecker()
                print("Waiting for fetcher to initialize...")  # Select dataset error

            # Wait to check for completed status message
            print("Waiting for fetcher / normalizer / loader to finish...")
            while driver.find_element_by_class_name("statusMessageSuccess").text in ("Not started yet", "Fetcher in Progress", "Normalizer in Progress", "Completed Normalizer", "Loader in Progress"):
                time.sleep(3)
                if driver.find_element_by_class_name("statusMessageSuccess").text is "Fetcher Error":
                    raise IOError("Fetcher encountered an error.")  # Change this ??

            # Get status message and details
            status_message = driver.find_element_by_class_name("statusMessageSuccess").text
            detail_message = driver.find_element_by_tag_name("textarea").text.split("|")[2].strip().split(";")
            total = detail_message[0].split("=")[1]
            num_duplicates = detail_message[1].split("=")[1]
            num_updates = detail_message[2].split("=")[1]
            num_inserts = detail_message[3].split("=")[1]
            num_errors = detail_message[4].split("=")[1]
            job_queue_id = detail_message[5].split("=")[1]

            # Append to log
            log.append("date:{0} | status message:{1} | total:{2} | duplicates:{3} | updates:{4} | inserts:{5} | errors:{6} | job_queue_id:{7}"
                        .format(date, status_message, total, num_duplicates, num_updates, num_inserts, num_errors, job_queue_id))

            # Switch to top-most content
            driver.switch_to_default_content()
            # Select close button (last anchor tag) and close modal window
            close_button = driver.find_elements_by_tag_name("a")[-1]
            close_button.click()
            time.sleep(1)
        
        # Print successful and unsuccessful jobs
        print("\nSuccessful Jobs:")
        for entry in log:
            # If no errors
            if int(entry.split("|")[6].strip().split(":")[1]) == 0:
                print(entry)
        
        print("\nUnsuccessful Jobs:")
        for entry in log:
            # If no errors
            if int(entry.split("|")[6].strip().split(":")[1]) != 0:
                print(entry)

        # Close driver
        driver.close()
    
    except KeyboardInterrupt:
        # Close the driver
        driver.close()