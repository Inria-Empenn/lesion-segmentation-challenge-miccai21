# Install, publish and use the example method

## Build the Docker image

To build the GPU version, run `docker build -f Dockerfile.gpu -t YOUR-USER-NAME/msseg-gpu-example .`
To build the CPU version, run `docker build -f Dockerfile.cpu -t YOUR-USER-NAME/msseg-cpu-example .`

## Run the Docker image

`docker run --entrypoint=/bin/sh --rm -v /path/to/flairs/:/data/ -v /path/to/miccai21/example_method/:/working-directory/ -w /working-directory/ arthurmassoninria/msseg-example:latest process.sh`

## Publish the Docker image

- Login to the Docker Hub using the command `docker login -u YOUR-USER-NAME`
- docker push YOUR-USER-NAME/msseg-cpu-example

## Publish the Boutiques descriptor

- Create an account on Zenodo, the publishing platform used by Boutiques. 
- Create a new personal access token on the [applications page](https://zenodo.org/account/settings/applications/) of your Zenodo account so that bosh can publish descriptors under your name.
- Publish the descriptor with your personal access token: `bosh publish --zenodo-token ACCESS_TOKEN msseg_example_method_cpu.json`

## Execute the method with Boutiques

- Change the paths in `example_invocation.json` to reflect your data paths
- Find the tool to get its zenodo.ID: `bosh search MSSeg`
- Execute the tool: `bosh exec launch -v /path/to/data/:/path/to/data/ zenodo.4769886 example_invocation.json`
