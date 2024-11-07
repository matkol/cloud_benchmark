
you need to have a functioning google command line client and you need to be authenticated at GCS with it:
https://cloud.google.com/sdk/docs/install

You need to have a project on GCS created and activated as your default and you need to have the right permissions
 - Cloud Resource Manager API needs to be activated
 - Google Container Registry API
    - gcloud services enable artifactregistry.googleapis.com
    - gcloud artifacts repositories create cstr --repository-format=docker --location=europe-west10  --description="ConstellR Test Repo"
    - docker tag cstr_download_test europe-west10-docker.pkg.dev/constellr-test/cstr/cstr_download_test:0.1
    - gcloud auth configure-docker europe-west10-docker.pkg.dev (configure gcloud as credentials helper for docker push)
    - docker push europe-west10-docker.pkg.dev/constellr-test/cstr/cstr_download_test:0.1
 - Kubernetes Engine API needs to be activated
    - https://cloud.google.com/kubernetes-engine/docs/deploy-app-cluster?hl=de
    - 'gcloud container clusters create-auto cstr  --location=europe-west10'
    - 'gcloud container clusters get-credentials cstr --location=europe-west10' (Auth info abrufen)
    - 'kubectl create deployment'
 - Compute Service needs to be activated
 - 'storage.objects.get

in order to follow the operations instructions.





Location: europe-west10
