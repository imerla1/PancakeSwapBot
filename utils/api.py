from utils.exceptions import VerifyApiException
from utils.logger import setup_logger
import requests
from requests.exceptions import ConnectionError
import sys
import traceback

api_logger = setup_logger("api_logger", "api_logger.log")

def verify_app():
    url = "http://imerla1.pythonanywhere.com/verify_token"
    print("Verifying APP .....")
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            api_logger.debug(f"Success Status with Status Code {resp.status_code} from {url}")
            text = resp.text
            if text == "HELLO":
                api_logger.debug("Api verified")
                print("App Verified Succesfully.")
                return True
            else:
                api_logger.critical(f"Api Can't Be verified !!!")
                print("Error IN API VERIFICATION")
                raise VerifyApiException("Somethin Went wrong in the Software Please Contact The <<<DEVELOPER>>>")
    except ConnectionError:
        api_logger.critical(f"Faild To establish Connection to {url} Check the Network Connection")
    except VerifyApiException:
        traceback.print_exc()
        sys.exit()

    
if __name__ == "__main__":
    verify_app()

    