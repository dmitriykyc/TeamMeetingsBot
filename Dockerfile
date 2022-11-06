FROM python:3.8

WORKDIR /TeamMeetings
COPY TeamMeetings/requirements.txt /TeamMeetings
RUN pip install -r requirements.txt
COPY TeamMeetings /TeamMeetings
