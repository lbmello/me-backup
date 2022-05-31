FROM python:3.10

WORKDIR /me_backup

COPY pyproject.toml .

RUN pip install .

CMD ["python3", "-m", "me_backup", "print_rsync"]
