from flask import *
from database.models import *
import pandas as pd
import tempfile
from flask import send_file, abort, make_response 

app = Flask(__name__)
connection_string = f"postgresql+psycopg2://korep:@localhost:5432/korep"
engine = create_engine(connection_string)
# session=Session()
# Session = sessionmaker(bind = engine)

@app.route('/download/<book_id>')
def download_book_stats(book_id):
    query = f'SELECT borrow_id, date_start, date_end FROM borrows WHERE book_id = {book_id}'
    df = pd.read_sql(query, engine)
    if len(df) > 0:
        temp = tempfile.NamedTemporaryFile(suffix='.xlsx', dir="../../Downloads/Telegram Desktop", mode='w+t')
        df.to_excel(temp.name, sheet_name='new_sheet_name')
        return send_file(temp.name, as_attachment = True)
    else:
        return "Empty"
app.run("0.0.0.0", port=5000)
