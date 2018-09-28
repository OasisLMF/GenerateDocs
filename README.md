# GenerateDocs


## Building the Documentaion via Docker 
`docker build -f docker/Dockerfile.oasis_docbuilder -t oasis_doc_builder .`

`docker run -v $(pwd):/tmp/output oasis_doc_builder:latest`
Which creates a tar file in the the current dir `oasis_docs.tar.gz`

## Building Locally 

`./build.sh`
