# https://github.com/nlmatics/nlm-ingestor?tab=readme-ov-file

# pip install nlm-ingestor
# run:
#   python -m nlm_ingestor.ingestion_daemon
# if error run the following:

import nltk
nltk.download('punkt')

# run docker desktop
# pull docker image:
#   docker pull ghcr.io/nlmatics/nlm-ingestor:latest
# run docker image (i ran through docker desktop just set port to 5010):
#   docker run -p 5010:5001 ghcr.io/nlmatics/nlm-ingestor:latest-<version>

