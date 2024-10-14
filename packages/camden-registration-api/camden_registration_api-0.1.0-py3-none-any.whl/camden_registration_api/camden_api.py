import argparse
import logging
import random
import re
import threading
import time

import requests
import yaml

# Set up logging to stdout
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger
logger = logging.getLogger(__name__)


### Custom exceptions #########


class NotFoundCSRFToken(Exception):
    def __init__(self, message):
        logger.info(
            f"Unable to proceed without server returning CSRF token in html, "
            f"check server response: {yaml.dump(message)}"
        )


class UnauthorizedLogin(Exception):

    def __init__(self, message):
        logger.info(
            f"Unable to proceed without getting 200 response from login request, "
            f"check user credentials and server response: {yaml.dump(message)}"
        )


class NotFoundActivity(Exception):

    def __init__(self, search, output):
        logger.info(
            f"Unable to find activity using {search}. Server response: {yaml.dump(output)}"
        )


class NotOpenEnrollment(Exception):
    def __init__(self, message):
        logger.info(
            f"Unable to proceed without getting 200 response from enrollment call, "
            f"check server response: {yaml.dump(message)}"
        )


class UserNotSelected(Exception):
    def __init__(self, message):
        logger.info(
            f"Unable to proceed without getting 200 response from user selection call, "
            f"check server response: {yaml.dump(message)}"
        )


class ActivityNotAddedToCart(Exception):

    def __init__(self, message):
        logger.info(
            f"Unable to proceed without getting 200 response from add activity to cart, "
            f"check if all inputs to add activity are correct. Server response: {yaml.dump(message)}"
        )


class CheckoutFailed(Exception):
    def __init__(self, message):
        logger.info(
            f"Getting non-success response code for final submission, "
            f"please debug server response: {message}"
        )


class CamdenClient:
    """
    Class to act as a client for the
    Camden Volleyball registration.
    """

    # use them only for the initial call to initiate
    # user session and get csrf token
    NOT_AUTHENTICATED_HEADERS = {
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/129.0.0.0 Safari/537.36",
            ]
        ),
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "host": "anc.apm.activecommunities.com",
        "referer": "https://anc.apm.activecommunities.com/",
        "upgrade-insecure-requests": "1",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-user": "1",
        "Sec-Fetch-Site": "same-site",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept": "*/*",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    }

    # use them for making requests to api endpoints (REST)
    API_HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "connection": "keep-alive",
        "content-type": "application/json;charset=utf-8",
        "host": "anc.apm.activecommunities.com",
        "origin": "https://anc.apm.activecommunities.com",
        "page_info": '{"page_number":1,"total_records_per_page":20}',
        "referer": 'https://anc.apm.activecommunities.com/sanjoseparksandrec/signin?onlineSiteId=0&locale=en-US&from_original_cui=true&override_partial_error=False&custom_amount=False&params=aHR0cHM6Ly9hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL3Nhbmpvc2VwYXJrc2FuZHJlYy9BY3RpdmVOZXRfSG9tZT9GaWxlTmFtZT1hY2NvdW50b3B0aW9ucy5zZGkmZnJvbUxvZ2luUGFnZT10cnVl',
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/129.0.0.0 Safari/537.36",
            ]
        ),
        "x-csrf-token": None,  # make sure to update after getting token
        "x-requested-with": "XMLHttpRequest",
    }

    def __init__(
        self,
        login,
        password,
        keywords,
        activity_date,
    ):
        self.user_login = login
        self.user_password = password
        self.keywords = keywords
        self.activity_date = activity_date

        # placeholders
        self.session = requests.session()
        self.session.cookies = requests.cookies.RequestsCookieJar()
        self.csrf_token = None
        self.start_time = time.perf_counter()

    def register(self):

        self._get_csrf_token()

        self._update_cookies_after_login()

        self._search_for_activity(test_mode=False)

        self._simulate_enroll_action()

        self._simulate_select_user_action()

        self._simulate_add_to_cart_action()

        self._simulate_checkout_action()

        logger.info(
            f"User {self.user_login} registered in "
            f"{round(time.perf_counter() - self.start_time, 2)} seconds"
        )

        return True

    def test(self):

        self._get_csrf_token()

        self._update_cookies_after_login()

        self._search_for_activity(test_mode=True)

        self._simulate_enroll_action()

        self._simulate_select_user_action()

        self._simulate_add_to_cart_action()

        tests.append(f"User {self.user_login} test PASSED")

        logger.info(
            f"User {self.user_login} completed test in "
            f"{round(time.perf_counter() - self.start_time, 2)} seconds"
        )

        return True

    ############# Private methods ################

    def _get_csrf_token(self):
        """ """
        logger.info(f"User {self.user_login} requested csrf token")

        res = self.session.get(
            (
                "https://anc.apm.activecommunities.com/sanjoseparksandrec/signin?"
                "onlineSiteId=0&locale=en-US&"
                "from_original_cui=true&"
                "override_partial_error=False&"
                "custom_amount=False&"
                "params=aHR0cHM6Ly9hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL3Nhbmpvc2VwYXJrc2FuZHJlYy9BY3RpdmVOZXRfSG9tZT9GaWxlTmFtZT1hY2NvdW50b3B0aW9ucy5zZGkmZnJvbUxvZ2luUGFnZT10cnVl"
            ),
            headers=CamdenClient.NOT_AUTHENTICATED_HEADERS,
        )

        # Regex pattern to extract the CSRF token
        csrf_token_pattern = r'window\.__csrfToken = "([a-f0-9-]+)"'

        # Applying the regex pattern to extract the CSRF token
        csrf_token_match = re.search(csrf_token_pattern, res.text)

        # Check if the regex match was successful
        if csrf_token_match:
            csrf_token = csrf_token_match.group(1)
            logger.info(f"User {self.user_login} CSRF Token: {csrf_token}")
            self.csrf_token = csrf_token

        else:
            raise NotFoundCSRFToken(res.text)

        self.session.cookies.update(res.cookies)

    def _update_cookies_after_login(self):

        if not self.user_login and not self.user_password:
            raise Exception("Unable to proceed without credentials")

        logger.info(f"User {self.user_login} simulate login and update session cookies")

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,ru;q=0.8",
            "connection": "keep-alive",
            "content-type": "application/json;charset=utf-8",
            "host": "anc.apm.activecommunities.com",
            "origin": "https://anc.apm.activecommunities.com",
            "page_info": '{"page_number":1,"total_records_per_page":20}',
            "referer": 'https://anc.apm.activecommunities.com/sanjoseparksandrec/signin?onlineSiteId=0&locale=en-US&from_original_cui=true&override_partial_error=False&custom_amount=False&params=aHR0cHM6Ly9hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL3Nhbmpvc2VwYXJrc2FuZHJlYy9BY3RpdmVOZXRfSG9tZT9GaWxlTmFtZT1hY2NvdW50b3B0aW9ucy5zZGkmZnJvbUxvZ2luUGFnZT10cnVl',
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": " ".join(
                [
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                    "AppleWebKit/537.36 (KHTML, like Gecko)",
                    "Chrome/129.0.0.0 Safari/537.36",
                ]
            ),
            "x-csrf-token": self.csrf_token,
            "x-requested-with": "XMLHttpRequest",
        }

        payload = {
            "login_name": self.user_login,
            "password": self.user_password,
            "recaptcha_response": "",
            "signin_source_app": "0",
            "locale": "en-US",
            "ak_properties": None,
        }

        res = self.session.post(
            "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/user/signin?locale=en-US",
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            self.customer_id = res.json()["body"]["result"]["customer"]["customer_id"]
            self.session.cookies.update(res.cookies)
            logger.info(f"User {self.user_login} got customerId: {self.customer_id}")
        else:
            raise UnauthorizedLogin(res.text)

    def _search_for_activity(self, test_mode=False):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "activity_search_pattern": {
                "skills": [],
                "time_after_str": "",
                "days_of_week": "0010100",
                "activity_select_param": 2,
                "center_ids": [],
                "time_before_str": "",
                "open_spots": None,
                "activity_id": None,
                "activity_category_ids": [],
                "date_before": self.activity_date,
                "min_age": 18,
                "date_after": self.activity_date,
                "activity_type_ids": [],
                "site_ids": [],
                "for_map": False,
                "geographic_area_ids": [],
                "season_ids": [],
                "activity_department_ids": [],
                "activity_other_category_ids": [],
                "child_season_ids": [],
                "activity_keyword": self.keywords,
                "instructor_ids": [],
                "max_age": "45",
                "custom_price_from": "0",
                "custom_price_to": "0",
            },
            "activity_transfer_pattern": {},
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activities/list?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        all_activities = []

        if res.status_code == 200:
            all_activities = res.json()["body"]["activity_items"]

        if not all_activities:
            raise NotFoundActivity(self.keywords, res.text)

        logger.info(
            f"User {self.user_login} search returned "
            f"{len(all_activities)} activities using keywords {self.keywords}"
        )

        # For testing only
        if test_mode:
            activity = random.choice(all_activities)
            logger.info(
                f"User {self.user_login} selected randomly: {activity.get('desc')[:22]}"
            )
        else:
            # filter out paid activities
            all_activities = [
                activity
                for activity in all_activities
                if activity["fee"]["label"] == "Free"
            ]

            activity = all_activities[0]
            logger.info(
                f"User {self.user_login} selected first activity: {activity.get('desc')[:22]}"
            )

        self.activity = activity

    def _simulate_enroll_action(self):
        """
        Requires valid activity id

        Possible cases:

        - not open for enrollment

        """

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "activity_id": self.activity["id"],
            "transfer_out_transaction_id": 0,
            "reg_type": 0,
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            logger.info(
                f"User {self.user_login} was enrolled after {time.perf_counter() - self.start_time}"
            )
            self.session.cookies.update(res.cookies)
        else:
            raise NotOpenEnrollment(res.json())

    def _simulate_select_user_action(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "reno": 1,
            "customer_id": self.customer_id,
            "overrides": [],
            "is_edit_transfer": False,
            "transfer_out_transaction_id": 0,
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment/participant?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            self.session.cookies.update(res.cookies)
            logger.info(
                f"User {self.user_login} was selected after {time.perf_counter() - self.start_time}"
            )
        else:
            raise UserNotSelected(res.text)

    def _simulate_add_to_cart_action(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "reno": 1,
            "participant_note": "",
            "question_answers": [
                {
                    "reno": 1,
                    "question_id": 2,
                    "customquestion_index": "1",
                    "parent_question_id": 0,
                    "user_entry_answer": "None",
                    "answer_id": [],
                },
                {
                    "reno": 1,
                    "question_id": 157,
                    "customquestion_index": "2",
                    "parent_question_id": 0,
                    "user_entry_answer": "",
                    "answer_id": [1031],
                },
            ],
            "donation_param": [],
            "waivers": [],
            "pickup_customers": [],
            "participant_usa_hockey_number": {
                "usah_code": "",
                "position_id": 1,
            },
            "token": "",
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment/addtocart?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if not res.status_code == 200:
            raise ActivityNotAddedToCart(res.text)
        else:
            logger.info(
                f"User {self.user_login} added to cart after {time.perf_counter() - self.start_time}"
            )

    def _simulate_checkout_action(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "waiver_initials_online_text": True,
            "online_waiver_initials": "",
            "initials": [],
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/checkout?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            logger.info(
                f"User {self.user_login} checked out after {time.perf_counter() - self.start_time}"
            )
        else:
            raise CheckoutFailed(res.text)

    #### Not required for registration, just FYI #########

    def _get_user_account(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/myaccount?locale=en-US"

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

    def _get_enrollment_details(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/detail/118875?locale=en-US&ui_random=1728771949835"

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

    def _get_login_check(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/common/logincheck?locale=en-US"

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)


tests = []


def process_single_player(
    login,
    password,
    activity_date,
    test_mode,
):

    logger.info(f"Processing in test mode: {test_mode}")
    if test_mode:

        attempts = 3

        camden_client = CamdenClient(
            login=login,
            password=password,
            keywords="",
            activity_date="",
        )

        while attempts > 0:
            try:
                if camden_client.test():
                    attempts = -1
            except Exception as e:
                logger.info(e)
            time.sleep(1)
            attempts -= 1

        if attempts == 0:
            tests.append(f"User {login} test FAILED")
    else:

        attempts = 2
        camden_client = CamdenClient(
            login=login,
            password=password,
            keywords="Drop In Volleyball",
            activity_date=activity_date,
        )

        while attempts > 0:
            try:
                if camden_client.register():
                    attempts = 0
            except Exception as e:
                logger.info(e)

            time.sleep(1)
            attempts -= 1


def main():

    parser = argparse.ArgumentParser(
        description="Automate user actions to register player for the next Camden volleyball activity",
        epilog=(
            """
            EXAMPLES:

            The following command will execute script with all default values,
            use config file to navigate to registration url, use user credentials to login
            and trigger registration:
                % python camden.py

            The following command will use custom configuration file:
                % python camden.py --config-file my-file.yml

            The following command will use custom configuration file:
                % python camden.py --config-file my-file.yml --test


            """
        ),
    )

    parser.add_argument(
        "--test",
        help="If true, will login and exit",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--config-file",
        help="If specified, will override default config.yml file",
        action="store",
        default="master.yml",
    )

    parser.add_argument(
        "--activity-date",
        help="If specified, will search only activities for that date",
        action="store",
        default="2024-10-15",
    )

    args, unknown = parser.parse_known_args()

    activity_date = args.activity_date
    test_mode = args.test

    with open(args.config_file) as f:
        config = yaml.safe_load(f.read())

    players = config.get("players")

    for player in players:

        t = threading.Thread(
            target=process_single_player,
            args=(
                player.get("login"),
                player.get("password"),
                activity_date,
                test_mode,
            ),
        )

        t.start()
        t.join()

    if test_mode:
        logger.info("#" * 100 + "\n")
        logger.info(yaml.dump({"TEST RESULTS": tests}, indent=4))
        logger.info("#" * 100)


if __name__ == "__main__":
    main()
