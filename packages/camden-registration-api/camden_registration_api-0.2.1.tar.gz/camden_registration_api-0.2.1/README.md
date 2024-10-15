# Camden Registration Api Client


# About

Wrapper on requests api to simulate user actions
on the Camden Activity Registration portal


## Running environment

Python > 3.9

## Install from source code

```
git clone https://github.com/polovinko1980/camden-registration-api.git

pip install -r requirements.txt

```

# Player credentials

Supporting either passing list of credentials as yaml file config:

```

cd camden_registration_api

vi master.yml

players:
-   login: test@gmail.com
    password: password
-   login: test2@gmail.com
    password: password2
```

Or alternatively it's possible to pass single player credentials in the format:
<login>:<password>

```
--player login:password
```


# Usage examples

## To run test registration

```
python3 camden_api_client.py --player login:password --test

python3 camden_api_client.py --players-from-file master.yml --test
```


## To run actual registration

```

python3 camden_api_client.py --player login:password

python3 camden_api_client.py --players-from-file master.yml

python3 camden_api_client.py # will use master.yml by default

```


# Install as pip package

This is experimental feature and not tested yet, stay tuned

```
pip install camden_registration_api

from camden_registration_api import CamdenClient

api_client = CamdenClient(
        login=<your login>,
        password=<your password>,
    )

# to run test registration
api_client.test()


# to run actual registration
api_client.register()


```


## Other

To call Camden: 1-408-559-8553



## Special ask

Do not share with Alex K, let him train his fingers
