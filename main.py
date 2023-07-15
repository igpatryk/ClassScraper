import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)


def get_env_vars():
    logging.info("Initializing settings...")
    variables = ['debug', 'url', 'all_answers']
    env_dict = {}

    for var in variables:
        try:
            value = os.getenv(var)
            env_dict[var] = value
        except Exception as e:
            logging.error(f"Error occurred while reading environment variable '{var}': {str(e)}")
            exit(2)

    logging.info(f"Settings initialized: {str(env_dict)}")
    return env_dict


def initialize_webdriver():
    try:
        logging.info("Initializing webdriver options...")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-dev-shm-usage')
        logging.info("Webdriver options initialized successfully.")
        logging.info("Initializing remote webdriver...")
        driver = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            options=options
        )
    except Exception as e:
        logging.error(f"Error during webdriver initialization: {str(e)}")
        exit(2)
    else:
        logging.info("Webdriver initialized successfully.")
        return driver


def scrap_test(driver, wait, output_file, question_number, all_answers):
    try:
        logging.debug(f"Scrapping question no. {str(question_number)}.")
        logging.debug("Waiting for checkboxes to appear.")
        checkbox = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '.ion-color.ion-color-secondary.md.in-item.interactive.hydrated')))
        logging.debug("Checkboxes appeared, trying to check-in the first box.")
        checkbox.click()
        logging.debug("Checked-in first checkbox.")

        logging.debug("Looking for continue button...")
        continue_button = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '[data-cy="continue-btn"]')))
        logging.debug("Found continue button, trying to click on it.")
        continue_button.click()
        logging.info("Clicked continue button.")

        logging.debug("Waiting for parent of question div.")
        question_parent_div = wait.until(EC.visibility_of_element_located((
            By.CSS_SELECTOR, '.ion-text-wrap.question-text')))
        logging.debug("Parent of question div found.")
        logging.debug("Looking for question div.")
        question_div = question_parent_div.find_element(By.CSS_SELECTOR, '.bbcode')
        logging.debug("Found question div, looking for it's content...")
        question = question_div.text
        logging.info(f"Got question: {question}, writing it to file.")
        logging.debug(f"{question_number}. {question}")
        output_file.write(f"{question_number}. {question}\n")
        logging.debug("Wrote question to file.")

        logging.debug("Looking for answers...")
        answers = driver.find_elements(
            By.CSS_SELECTOR, '.item.md.in-list.ion-activatable.ion-focusable.hydrated')
        for index, answer in enumerate(answers):
            logging.debug(f"Checking answer {index + 1}.")
            green_checks = answer.find_elements(
                By.CSS_SELECTOR, 'ion-icon.icon.icon-correct.circular-tick-holo.md.hydrated')
            if len(green_checks) > 0:
                logging.debug("This is correct answer - found holo icon. Fetching answer's value...")
                logging.debug("Trying to get answer div...")
                answer_div = answer.find_element(
                    By.CSS_SELECTOR, 'div[data-cy="question-option-text"]')
                logging.debug("Got answer div, obtaining it's content...")
                answer_text = answer_div.text
                logging.info(f"Found correct answer: {answer_text}")
                logging.debug("Writing answer to file...")
                if all_answers == "y":
                    output_file.write(f"RIGHT: {answer_text}\n")
                else:
                    output_file.write(f"{answer_text}\n")
                logging.info("Answer written to the file.")
            else:
                green_checks = answer.find_elements(
                    By.CSS_SELECTOR, 'ion-icon.icon.icon-correct.circular-tick.md.hydrated')
                if len(green_checks) > 0:
                    logging.debug("This is correct answer - found regular icon. Fetching answer's value...")
                    logging.debug("Trying to get answer div...")
                    answer_div = answer.find_element(By.CSS_SELECTOR, 'div[data-cy="question-option-text"]')
                    logging.debug("Got answer div, obtaining it's content...")
                    answer_text = answer_div.text
                    logging.info(f"Found correct answer: {answer_text}")
                    logging.debug("Writing answer to file...")
                    if all_answers == "y":
                        output_file.write(f"RIGHT: {answer_text}\n")
                    else:
                        output_file.write(f"{answer_text}\n")
                    logging.info("Answer written to the file.")
                elif all_answers == "y":
                    logging.debug("Did not found correct answer's icon. Fetching answer's value...")
                    logging.debug("Trying to get answer div...")
                    answer_div = answer.find_element(By.CSS_SELECTOR, 'div[data-cy="question-option-text"]')
                    logging.debug("Got answer div, obtaining it's content...")
                    answer_text = answer_div.text
                    logging.info(f"Found wrong answer: {answer_text}")
                    logging.debug("Writing answer to file...")
                    output_file.write(f"WRONG: {answer_text}\n")
                    logging.info("Answer written to the file.")

        logging.debug("Checking if it's the last question - looking for finish button.")
        finish_button = driver.find_elements(By.CSS_SELECTOR, '[data-cy="finish-btn"]')
        if len(finish_button) > 0:
            logging.info("This is the last question.")
            logging.debug("Closing driver...")
            driver.quit()
            logging.debug("Driver closed, closing file...")
            output_file.close()
            logging.debug("File closed.")
            logging.info("Exiting, bye!")
            exit(0)

        logging.debug("It is not the last question.")
        logging.debug("Looking for continue button.")
        continue_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-cy="continue-btn"]')))
        logging.info("Proceeding to the next question...")
        continue_button.click()
        logging.debug("Clicked continue button.")
        question_number += 1
        logging.debug("Invoking scrap_test function.")
        scrap_test(driver, wait, output_file, question_number, all_answers)
    except Exception as e:
        logging.error(f"Error during automation: {str(e)}")
        exit(2)


def main():
    logging.basicConfig(filename='./logs.txt', encoding='utf-8', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    settings = get_env_vars()
    if settings["debug"].lower() == "y":
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename='./logs.txt', encoding='utf-8', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    driver = initialize_webdriver()
    url = settings["url"]
    logging.info("Opening provided URL...")
    logging.debug(f"URL is {url}")
    try:
        driver.get(url)
        logging.info("Website opened.")
        logging.debug("Creating wait object...")
        wait = WebDriverWait(driver, 10)
        logging.debug("Created wait object.")
        logging.debug("Waiting for continue button to show up...")
        continue_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-cy="continue-btn"]')))
        logging.debug("Continue button showed up, attempting to click on it.")
        continue_button.click()
        logging.debug("Clicked continue button.")
        logging.info("Started test.")
        logging.info("Opening output file...")
        output_file = open("./output.txt", "w")
        logging.info("Output file opened.")
    except Exception as e:
        logging.error(f"Error during pre-automation tasks: {str(e)}")
        exit(2)
    scrap_test(driver, wait, output_file, 1, settings["all_answers"].lower())


if __name__ == '__main__':
    main()
