Test
===
Overview
---
This folder holds some simple tests. To run tests a Docker image is tried to be build. It bases on Ubuntu, installs the sylva-etl package and then, runs the tests. If the image can be build without an error, tests are successful.

Folder Structure
---
| Folder/File | Purpose |
| --- | --- |
| testdata/** | Contains some prepared example that can be used in tests. Examples will be provided in /home/sylva/testdata folder of the image. |
| tests/** | Contains tests (prefix: test-) and test preparation steps (prefix: prep-) that are call during build of image. |
| Dockerfile | Well, the Docker file. |
| setup-mongo | A simple script that sets up MongoDB during image build by creating the required users. |

Run tests
---
Put the Debian package to test in this folder an then, run 
```
docker build .
```


