# camden-registration-api
wrapper on requests api to simulate user actions on the Camden Activity Registration portal


# Camden Registration

# About

Simple helper to automate the registration process
to Camden volleyball activities by simulating user actions.

# Running environment
Need python 3 to run

Need pip to install libraries



# Preconditions


Install ```pip install -r requirements.txt```

In ```master.yml``` file:

- update credentials in a list of players. List of players supported.

# Usage

To see all options
```python camden_api.py --help ```


To validate setup, run

```python camden_api.py --test ```

This option will only search for the next activity registration url and update
configuration file.

Make sure to validate updated url manually!


It is possible to use your own configuration file by passing its name:


```
python camden_api.py --config-file my-secret-file.yml
```



To run registration:

```
python camden_api.py
```


# Other

To call Camden: 1-408-559-8553



# Special ask

Do not share with Alex K, let him train his fingers
