import sys
import os
import logging
from typing import Callable
from .utils import replace_domain
from .status import OK, WARNING, CRITICAL, UNKNOWN
import requests


# SCC_USE_TEST_SVR = 'http://testserver/'
SCC_USE_TEST_SVR = os.getenv("SCC_USE_TEST_SERVER")
if SCC_USE_TEST_SVR and not 'http' in SCC_USE_TEST_SVR:
    raise ValueError("SCC_USE_TEST_SERVER must be a valid URL")


def _terminate_check(status, msg):
    # -----------------------------------------   
    #   DO NOT MODIFY THIS FUNCTION
    # -----------------------------------------    
    print(f"{status} - {msg}")
    if status == OK:
        sys.exit(0)
    elif status == WARNING:
        sys.exit(1)
    elif status == CRITICAL:
        sys.exit(2)
    else:
        sys.exit(3)

  
def make_request(
    plugin_id: str,
    url, 
    method: str, 
    headers: dict = {}, 
    data:dict = {}, 
    verify=False, 
    terminate_check: Callable =_terminate_check,
    logger_name: str = "cmk-tools"
): 
    logger = logging.getLogger(logger_name)
    if not callable(terminate_check):
        raise ValueError("terminate_check must be a function")

    if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE']:
        return terminate_check(UNKNOWN, f"request API method >>{method}<< not supported")
    
    response = None
    try:
        if SCC_USE_TEST_SVR:
            new_url = replace_domain(url, SCC_USE_TEST_SVR)
            headers = {
                **headers, 
                'X-Plugin-Id': plugin_id
            }
            response = requests.request('POST', new_url, headers=headers, data=data, verify=verify)
        else:
            response = requests.request(method, url, headers=headers, data=data, verify=verify)
        response.raise_for_status()
        
    except requests.exceptions.ConnectTimeout:
        logger.warning(f"Timeout when connect to {url}", api_resp=response)
        terminate_check(UNKNOWN, f"Timeout when connect to {url}")
    except requests.exceptions.ReadTimeout:
        logger.warning(f"Timeout when connect to {url}", api_resp=response)
        terminate_check(UNKNOWN, f"Timeout when read data from {url}")
    except Exception as e:
        logger.critical(f"Timeout when connect to {url}", api_resp=response)
        terminate_check(UNKNOWN, f"Error when request to {url} with error: {e}")
    finally:
        return response