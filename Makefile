SHELL := /bin/bash
VERSION?=latest
TASK_IMAGES:=$(shell find tasks -name Dockerfile -printf '%h ')
REGISTRY=toddchaney
PROJECT=car_insurance
ARGO_NAMESPACE=argo

tasks/%: FORCE
	set -e ;\
	docker build -t $(PROJECT)_$(@F):$(VERSION) $@ ;\
	docker tag $(PROJECT)_$(@F):$(VERSION) $(REGISTRY)/$(PROJECT)_$(@F):$(VERSION) ;\
	docker push $(REGISTRY)/$(PROJECT)_$(@F):$(VERSION);\
	if [ $(@F) != base -a $(@F) != notebooks ]; then argo template create workflows/$(@F).yaml -n $(ARGO_NAMESPACE); fi
 
images: $(TASK_IMAGES)

run: images
	argo template create workflows/pipeline.yaml -n $(ARGO_NAMESPACE)
	argo submit --from=workflowtemplate/pipeline --watch -n $(ARGO_NAMESPACE)
	argo template delete --all -n $(ARGO_NAMESPACE)

start_notebooks:
	kubectl apply -f $(HOME)/ml/car-insurance/notebooks.yaml -n $(ARGO_NAMESPACE)

stop_notebooks:
	kubectl delete deployment jupyter-notebook -n $(ARGO_NAMESPACE)

FORCE: ;
