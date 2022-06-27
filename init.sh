#!/bin/sh

WORK_DIR=/home/jovyan/work
CLONE_DIR=${WORK_DIR}/repo-git
COURSE_DIR=${CLONE_DIR}/
FORMATION_DIR=${WORK_DIR}/playlist

# Clone course repository
REPO_URL=https://github.com/geoffreyaldebert/fetch-datasets.git
git clone --depth 1 $REPO_URL $CLONE_DIR

python ${CLONE_DIR}/fetch.py $1

mc cp --recursive ${WORK_DIR}/repo-git/$2/ s3/geoffrey/$2/

# Convert .md to .ipynb
pip install python-frontmatter jupytext
python $CLONE_DIR/utils/md-to-ipynb.py ${COURSE_DIR}/intro.md

# Put chapter data in the training dir
mkdir $FORMATION_DIR
cp ${COURSE_DIR}/intro.ipynb ${FORMATION_DIR}/

# Give write permissions
chown -R jovyan:users $FORMATION_DIR/

# Install additional packages if needed
REQUIREMENTS_FILE=${FORMATION_DIR}/requirements.txt
[ -f $REQUIREMENTS_FILE ] && pip install -r $REQUIREMENTS_FILE && rm $REQUIREMENTS_FILE

# Remove course Git repository
#rm -r $CLONE_DIR

# Open the relevant notebook when starting Jupyter Lab
echo "c.LabApp.default_url = '/lab/tree/playlist/intro.ipynb'" >> /home/jovyan/.jupyter/jupyter_server_config.py
