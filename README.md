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

### read approved interactions
`GET http://localhost:5000/api/v1/interaction/approve -H "X-Token: <token>"`
_example output:_
```json
{
  "data": [
    [
      1,
      "0x3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532",
      "0xA024A8ec4D9F2F26Add18E999E79648DcCd805CF",
      "0x7b22696e746572616374696f6e5f6964223a22307833613938356461373466653232356232303435633137326436626433393062643835356630383665336539643532356234366266653234353131343331353332222c227369676e6572223a22307841303234413865633444394632463236416464313845393939453739363438446343643830354346227d",
      "0xe9ba02d1c8397078cbe858e292814211376526cb5ee55634c349511d05f2eb40631eb2501aa8b588cbaf57aa0e0867ec46e374bac0a0529667664b907db5924b1b"
    ],
    [
      2,
      "0x3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532",
      "0x7f322968701F6e2388A3deBF8E2547104bc5105C",
      "0x7b22696e746572616374696f6e5f6964223a22307833613938356461373466653232356232303435633137326436626433393062643835356630383665336539643532356234366266653234353131343331353332222c227369676e6572223a22307837663332323936383730314636653233383841336465424638453235343731303462633531303543227d",
      "0x117a7635c6e4afc40f2f192fa46c104f7a17b5cd59ca3560848d1fafe515b0a019766663931c7cb211f2f10eea0ab81c472831dbca630fdd1af0d01753d0da511b"
    ]
  ],
  "success": true
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
