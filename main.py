import pyodbc
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from jinja2 import Template
from bs4 import BeautifulSoup
from typing import Dict, List
import requests


app = FastAPI()

class Cars(BaseModel):
    Brand: str
    Model: str
    Year: int
    Price: float
@app.get("/Cars", response_class=HTMLResponse)
def get_data() -> List[Dict[str, str]]:
    url = 'https://vinfastotomiennam.com/bang-gia-2-31.html'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra trạng thái của yêu cầu HTTP
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi truy cập URL: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Trích xuất dữ liệu từ trang web
    data = []
    table = soup.find('table')
    if not table:
        raise HTTPException(status_code=404, detail="Không tìm thấy bảng dữ liệu")

    rows = table.find_all('tr')[1:]
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 2:
            car_info = {
                'Brand': cols[0].get_text(strip=True),
                'Model': cols[1].get_text(strip=True),
                'Year': cols[2].get_text(strip=True),
                'Price': cols[2].get_text(strip=True)
            }
            data.append(car_info)
    print(data)
    return data
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# uvicorn main:app --reload