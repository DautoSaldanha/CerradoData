set -e

export PIP_DISABLE_PIP_VERSION_CHECK=1

python3 -m pip install --break-system-packages -r requirements.txt

python3 manage.py migrate --noinput

python3 manage.py ensure_superuser

python3 manage.py collectstatic --noinput --upload-unhashed-files