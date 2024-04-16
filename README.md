# backend

first-time set-up
```bash
docker network create backend
docker-compose -f docker-compose-pg.yml -f docker-compose.yml pull
```

on-schema change / postgres initialization fail
```bash
rm -rf volumes/postgres
```

each time, start postgres & pgadmin
```bash
docker-compose -f docker-compose-pg.yml up --build
```

each time, start backend
```bash
docker-compose -f docker-compose.yml up --build
```

<...>

now you should have endpoint with base_url=`http://localhost:5000/api/v1/...` up and running (sorry no openapi specs, for now) 

### add approval for interaction hash (any interaction hash is valid, you can approve interactions upfront)
`POST http://localhost:5000/api/v1/interaction/approve -H "Content-Type: application/json"`
_example:_
```json
{
  "message": {
    "timestamp": 1710231420,
    "signer": "0xB08124571b208E72307AF66e92c55cA373245946",
    "domain": "localhost:5000"
  },
  "signature": "0x68779eda626428dc74e4449d614b8c86d75e4837c3183e7ad2c95dcca27d20f31bacbbd047df73e5c02a06d0bcc79a0e5c065100c0af03c3fea09bdf73fadcd61c"
}
```

### create readonly access token 
`POST http://localhost:5000/api/v1/auth/token -H "Content-Type: application/json"` 
_example:_
```json
{
  "message": {
    "interaction_id": "0x3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532",
    "signer": "0xB08124571b208E72307AF66e92c55cA373245946"
  },
  "signature": "0x0104478a236779bc4826ca6519421ce79cbb5717abbd1480497080db71097b8a4771b10bf44ae40362214a6778d84c975a0d8d2dc0fde57e518047b6edf8af341b"
}
```

### read token payload (for the previously generated token) 
`GET http://localhost:5000/api/v1/auth/token/payload -H "X-Token: <token>"`
_example output:_
```json
{
  "payload": {
    "aud": "urn:autlabs:autid:holder",
    "exp": 1710235020,
    "iat": 1710231423,
    "iss": "urn:autlabs",
    "nbf": 1700000000,
    "sub": "0xB08124571b208E72307AF66e92c55cA373245946"
  }
}
```

## cheatsheet

gen private key
```bash
openssl rand -hex 32
```


# todo

! pg tx fetcher (moralis, on-demand load, for v1)
! tx root publisher (full rebuild, v1)

- extra prod deployments 
- find cloud provider
- pgpool / conn mgmt pg 
- logging
- openapi 
- alerting / prometheus + grafana 
