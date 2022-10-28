from main import create_app
from poll import DataPoll

app = create_app()
t = DataPoll()
t.start()