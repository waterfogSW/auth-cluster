# Kubernetes Istio Envoy Filter(JWKS) Project

This project demonstrates the application of an Istio Envoy filter in a Kubernetes cluster. 
It intercepts JWTs (JSON Web Tokens), parses them to extract a 'username' claim, and passes it in the headers to downstream services.

## Pre-requisites

- Kubernetes (e.g., Minikube for a local setup), with Istio installed.
- Helm.
- Docker, if you are planning to build images manually.

## Operating Instructions with Minikube

1. Ensure that your Kubernetes cluster is operational: `minikube start --driver=hyperkit`
2. Deploy the helm chart: `helm install envoy-auth charts/`
3. Get the external IP address of the Istio ingress gateway: `minikube service istio-ingressgateway -n istio-system`
4. Log in to obtain a JWT token: Send a POST request to `{host}/api/auth/login`
5. Test if the setup is working: Send a GET request to `{host}/api/echo/echo_user_info`

The GET request should include the JWT from step 4 in an Authorization header: `Authorization: Bearer {token}`

## Services

The project includes two key services:

1. auth service - providing a login API and JWKs public key endpoint.
```python
@app.post("/login")
async def login(request: LoginRequest):
    payload = {
        "username": request.username,
        "iss": "fastapi-jwks",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # Valid for 1 hour
    }
    token = jwt.encode(payload, key_util.private_key_str, algorithm="RS256")
    return {"access_token": token}

@app.get("/.well-known/jwks.json")
async def jwks():
    numbers = key_util.public_key.public_numbers()
    n = base64url_encode(numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, 'big')).decode()
    e = base64url_encode(numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, 'big')).decode()
    jwk = {
        "alg": "RS256",
        "kty": "RSA",
        "use": "sig",
        "n": n,
        "e": e,
        "kid": "abc123"
    }
    return dict(keys=[jwk])
```


2. echo service - capable of verifying the presence of a 'username' header.

```python
@app.get("/echo_user_info")
async def echo_user_info(username: Optional[str] = Header(None)):
    return {"username": username }
```

## Conclusion

This project highlights the utility of Istio Envoy filters within a Kubernetes context, particularly with respect to handling JWTs and manipulating headers for downstream services.
 
Remember to include further information on dependencies, detailed setup instructions, environment configurations, or other considerations that might apply to a developer or user working with your project.