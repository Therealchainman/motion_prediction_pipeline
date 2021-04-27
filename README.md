# Notes

argo ui

```sh
kubectl -n argo port-forward deployment/argo-server 2746:2746
```

These are some notes on what I've changed,
for this to work there are some changes you have to make to the code.  

You need to add the ARGO_NAMESPACE environment variable to your environment.  
Also you need to rename the registry in makefile to that of yours, so like for me it is
toddchaney because that is my username in docker hub.  I could create an environment variable for
this as well.  

Most of this effort, which is poorly documented in my first pass, I can improve on it when I tear down and reinstall
Then I will know what I'm doing on my second installation 


[volumes](<https://blog.container-solutions.com/understanding-volumes-docker>)


\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes


## creating the hostPath volume

The architecture of this I drew out, but this is what it looks like, 
I need to create the persistentvolume, persistentvolumeclaim, and create the hostpath by ssh into my single node, which is just going to be 

```sh
minikube ssh
```

But I don't need to do that, I don't need to create the directory, it will if it doesn't exist.  

I created a very basic pv and pvc for the cluster to have the /data as a hostPath. This will allow me to persist files in my cluster so I can work from a pod and continue the work from the pod
later on.  

Of course if this node crashes for some reason I will lose all my data, I need to consider this as a problem.  But for now I'm
fine, and in fact the only real trouble for me is actually trying to save it to a github repo potentially periodically yeah that would be nice.  Fortunately all of the images are built atop of python3.7 which contains git installed.  So I can manually run jupyterlab and do all the git commands in my single node.  

TODO:  Add github action workflow to push the information to there from the /data file in the node.  

create a jupyterlab deployment and service, the reason for the deployment is it will create a pod that will continually be running that has the jupyter lab inside of the pod.  All I need to do is exec into the pod and I can see that jupyter is running or run the logs and see that jupyterlab is running.  The thing is it will say it cannot find a browser.  That is because it is not exposed to my localhost.  So I portforward from the pod to my laptop.  So that now I can actually see web app in my browser locally.  However, while this does sound very nice and all.  It still leaves some very gigantic holes to be covered.  For instance, one of the problems or issues is that i lost my train of thought.  Regardless boom I have this jupyter labs where the pod is connected to hostpath, so it should be able to see the data that I plop into that local hostpath, now all I need is the following.  I need the ability to be able to yeah and I can run from jupyter lab and everything, not sure if it will actually be connected though.  But this is definitely worth a shot.  The other thing that can be tried is the following though.  I can also try something else.  Regardless you see the general concept.  I don't know if this will work.  also I'm basically just running the code in the jupyter lab pod.  I mean why do I even need my pipeline with argo.  IDK, maybe so I can run code and isolate certain areas, for when it breaks there.  I guess. I don't know how necessary Argo will be, but having jupyter will be nice, and it is nice that I can attach anything in Argo to the volumes.  

Investigate this link to create deployments later

https://argoproj.github.io/argo-events/tutorials/04-standard-k8s-resources/

For now I'm happy with this state of events, where I am running jupyter lab inside here and so on.  

Seems good and I can run other trainings in argo workflows.  I don't know why yet haha.  But maybe it will be helpful breaking down into components, and then
but ofcourse if it fails anywhere I just have to rerun the entire workflow.  Oh you know what it could help with parallelization if I run two pods at same time.  potentially by scheduling it.  In addition I think I can schedule these so I will continue researching this later. 


The other thing I'm working on is the following 


## Setting up the MLFlow in here

\\wsl$\Ubuntu-20.04

Get set up with [conda](<https://www.bradleysawler.com/engineering/python-conda-wsl-2-ubuntu-setup-on-windows-10/>)

Working through MLFlow has been fun so far, but I have not configured exactly where I'd want it,  so far I feel one of the best
strengths of it would be the ability to do hyperparameter tuning potentially.  As such I may add it into this product. 

I would need to figure out how to parallelize it I suppose.  

## Setting up the Apache spark 

Let's update my plan of attack for this task, and so I know what I want to focus on tomorrow.  

Finish tonight: Reading more on Apache Spark

Learn strongly vs loosely typed data types

Why apache spark ,  because it uses in-memory pcomputation procssing where data is kept in RAM instead of slow disk drives, and processed in parallel.  
how do I do this?? 

What is a spark executor pod:  

kubernetes apiserver:  The core of the kubernetes control plane is the api server.  Let's components communicate with one another. 

control plane:  COL that exposes the api and interfaces to define, deploy and manage the lifecycle of containers

scheduler:  Find sthe best node for that pod, if it discovers a pod is not running on any nodes.  The default one is the kube-scheduler

Create a spark driver and then creates executors that all communicate back to the spark driver.

executor pods are run when executing application code, and once complete, they are terminated and cleaned up.  But the driver pod persists logs and remaines completed state in kubernetes api.

In the completed state the driver pod does not use any computation resources. 

> Make certain to set the spark.kubernetes.driver.pod.name to the name of thepod of the spark driver, that way the executor pods are garbage collected.  

Can mount following types of kubernetes volumes into the driver and executor pods, hostPath and nfs

What is the spark operator? 

let's use the spark-submit for right now.

So here is what we have basically 

Kubernetes takes this request and starts the Spark driver in a k8s pod,  The spark driver an directly talk back to kubernetes master to request execotur pods, scaling them up and down at runtime according to load dynamic allocation is enabled.  

I need the dynamic allocation and cluster level autoscaling,  

spark operator is opensouded by google, and it runs a single pod on the cluster that will turn Spark applications into CRDs, which can be described like other kubernetes objects,  

a k8s operator for managing the lifecycle of apache spark apps on k8s. 


## Starting jupyterlab

```sh
make start_notebooks
```

```sh
kubectl port-forward <pod running jupyterlabs> 8888:8888 -n argo
```

```sh
make stop_notebooks
```

TODO: How am I going to save the data that I'm saving to the single node in my k8s cluster?  If I want to save to github, I need to have git cli installed.  
I can create workflow, connect to the volume in the node, and copy the files to local computer in the workflow and then run git commands to create git repo and so on.  

## testing something

I want to achieve the following, that is I am going to basically try to get this part to work.  

I need to create the workflows 


## come back to later

Exploring how to use hard-wired artifact like git

[example 1](<https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/test/e2e/functional/git-clone-test.yaml>)
[example 2](<https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/ci.yaml>)
[example 3](<https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/ci-output-artifact.yaml>)
[example 4](<https://github.com/argoproj/argo-workflows/blob/91c08cdd83386bfcf48fcb237dd05216bc61b7a0/.github/workflows/ci-build.yaml>)
[example 5](<https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/influxdb-ci.yaml>)


## running workflow

run build.sh in the base directory to build the base image containing python3. 

TODO: fix the fact that you have to run argo template create before you can submit it.  
I have to first create a workflowtemplate with 
argo template create path/to/workflow
note I added name

note running the make clone_repo will not work if your repository is private, it needs to be public, this will be resolved when I used the git repository and include credentials.

TODO: fix the fact that every single time you need to reset the git config user.name and user.email git config --global 

TODO: Can I run jupyterlabs from inside a notebook?? 

## Issues

A potential issue occurred when running 2 intense workflows, and deleting both of them at once with the delete --all command, and it seems there may have
been a memory leak potentially, because the VM continued to have high memory usage.  

also I deleted the workflowtemplate for the workflow that was running, 

## Future


This is the best method to create a kubernetes ssh secret.  

Create your kubernetes ssh secret for using the pipeline git components. 
```sh
 kubectl create secret generic ssh-secret --from-file=ssh-privatekey=${HOME}/.ssh/id_ed25519 --from-file=ssh-publickey=${HOME}/.ssh/id_ed25519.pub -n argo
```

Need to include .ssh files inside the base directory




ERRORS:

MESSAGE:


helpful message for example of a helpful error message: 
2021/04/26 17:37:42 Failed to parse workflow template: json: cannot unmarshal array into Go struct field Parameter.spec.templates.inputs.parameters.name of type string

Example of a horrendous error message that does not help debug whatsoever. 
```sh
argo template create workflows/pipeline.yaml -n argo
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x1a2207e]

goroutine 1 [running]:
github.com/argoproj/argo-workflows/v3/workflow/validate.validateDAGTaskArgumentDependency(0xc000709040, 0x1, 0x4, 0x0, 0x0, 0x0, 0xc000b26c00, 0x3, 0x3, 0x0, ...)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/workflow/validate/validate.go:1266 +0x15e
github.com/argoproj/argo-workflows/v3/workflow/validate.(*templateValidationCtx).validateDAG(0xc0005157c0, 0xc0008eb1a0, 0xc000515800, 0xc0008ed440, 0xc0008ee658, 0x0)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/workflow/validate/validate.go:1241 +0x1016
github.com/argoproj/argo-workflows/v3/workflow/validate.(*templateValidationCtx).validateTemplate(0xc0005157c0, 0xc0008ecd80, 0xc000515800, 0x32bac40, 0x42b31f0, 0xc0008ecd80, 0x0)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/workflow/validate/validate.go:372 +0xb35
github.com/argoproj/argo-workflows/v3/workflow/validate.(*templateValidationCtx).validateTemplateHolder(0xc0005157c0, 0x32ba8c0, 0xc0008f42c0, 0xc0007beeb8, 0x32bac40, 0x42b31f0, 0x0, 0x0, 0x0)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/workflow/validate/validate.go:456 +0x157
github.com/argoproj/argo-workflows/v3/workflow/validate.ValidateWorkflow(0x32a5000, 0xc0008f2110, 0x32a4fe0, 0xc0008f2130, 0xc000100800, 0x1913600, 0x0, 0x0, 0x100, 0x2299b60, ...)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/workflow/validate/validate.go:203 +0x1257
github.com/argoproj/argo-workflows/v3/workflow/validate.ValidateWorkflowTemplate(0x32a5000, 0xc0008f2110, 0x32a4fe0, 0xc0008f2130, 0xc0008f6000, 0x8, 0x2000, 0x0)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/workflow/validate/validate.go:256 +0x12f
github.com/argoproj/argo-workflows/v3/server/workflowtemplate.(*WorkflowTemplateServer).CreateWorkflowTemplate(0xc0007fe2c0, 0x33007c0, 0xc000770c30, 0xc000515780, 0x40, 0x7f87987b7560, 0xc000515780)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/server/workflowtemplate/workflow_template_server.go:36 +0x285
github.com/argoproj/argo-workflows/v3/pkg/apiclient.(*argoKubeWorkflowTemplateServiceClient).CreateWorkflowTemplate(0xc0007fe2d0, 0x33007c0, 0xc000770c30, 0xc000515780, 0x0, 0x0, 0x0, 0x40, 0x23ff8c0, 0xc000867c01)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/pkg/apiclient/argo-kube-workflow-template-service-client.go:19 +0x51
github.com/argoproj/argo-workflows/v3/pkg/apiclient.(*errorTranslatingWorkflowTemplateServiceClient).CreateWorkflowTemplate(0xc0007fe2e0, 0x33007c0, 0xc000770c30, 0xc000515780, 0x0, 0x0, 0x0, 0x1, 0xc0002ff5e0, 0xc0007bfaa0)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/pkg/apiclient/error-translating-workflow-template-service-client.go:20 +0x69
github.com/argoproj/argo-workflows/v3/cmd/argo/commands/template.CreateWorkflowTemplates(0xc0000369c0, 0x1, 0x3, 0xc00012e580)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/cmd/argo/commands/template/create.go:68 +0x3ff
github.com/argoproj/argo-workflows/v3/cmd/argo/commands/template.NewCreateCommand.func1(0xc0000342c0, 0xc0000369c0, 0x1, 0x3)
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/cmd/argo/commands/template/create.go:33 +0x51
github.com/spf13/cobra.(*Command).execute(0xc0000342c0, 0xc000036990, 0x3, 0x3, 0xc0000342c0, 0xc000036990)
        /Users/sbeharyutk/go/pkg/mod/github.com/spf13/cobra@v1.0.0/command.go:846 +0x2c2
github.com/spf13/cobra.(*Command).ExecuteC(0xc000132840, 0xc00007c778, 0xc0007bff78, 0x406325)
        /Users/sbeharyutk/go/pkg/mod/github.com/spf13/cobra@v1.0.0/command.go:950 +0x375
github.com/spf13/cobra.(*Command).Execute(...)
        /Users/sbeharyutk/go/pkg/mod/github.com/spf13/cobra@v1.0.0/command.go:887
main.main()
        /Users/sbeharyutk/go/src/github.com/argoproj/argo-workflows/cmd/argo/main.go:14 +0x2b
```

RESOLUTION: 

MESSAGE: 2021/04/26 18:46:35 No workflow template found in given files

The file has the env as a dictionary in the image, but it should be in the container
container
-image
--env
but should be 
container
-image
-env
```yaml
apiVersion: argoproject.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: clone-repo
spec:
  entrypoint: clone
  volumes:
  - name: workspace
    persistentVolumeClaim:
      claimName: pvc-data
  arguments:
    parameters:
    - name: email
      value: email@example.com
    - name: user
      value: john
  templates:
  - name: clone-repo
    inputs:
      parameters: [{name: email}, {name: user}]
    container: 
      image: toddchaney/car_insurance_clone_repo
        env: 
        - name: EMAIL
          value: "{{inputs.parameters.email}}"
        - name: USER
          value: "{{inputs.parameters.user}}"}]
      command: [bash]
      args: ["/run.sh"]
      volumeMounts:
      - mountPath: /data
        name: workspace
  - name: clone
    dag:
      tasks:
      - name: clone-repo
        template: clone-repo
        arguments: 
          parameters: [{name: email, value: "{{workflow.parameters.email}}"}, {name: user, value: "{{workflow.parameters.user}}"}]
```

## Generating ssh
Choose directory to save it, and choose no passphrase.  
```sh
ssh-keygen
```

Then add it to your github account, the public key with .pub extension

copy to your directory that contains Dockerfile 
```sh
cp -a ~/.ssh/id_rsa tasks/base/.ssh
```

debug trick 

RUN ssh -Tv git@github.com 

add your known host as well from .ssh and you should be set now. 



