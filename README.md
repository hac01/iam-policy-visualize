# iam-policy-visualize
Python script to create a visualization of GCP Project IAM policy bindings

# Example 

```
# gcloud projects get-iam-policy gr-prod-1 --format json > iam-policy-bindings.json
python3 main.py iam-policy-bindings.json
```
![image](https://github.com/hac01/iam-policy-visualize/assets/70646122/c0d12bcc-7bda-40e3-9a56-dc30a2b9cea1)
