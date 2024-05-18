import pyodbc
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from jinja2 import Template
from bs4 import BeautifulSoup
from typing import Dict, List
import requests


# Thông tin kết nối
#server = 'ADMIN-PC'  # VD: 'localhost' hoặc '192.168.1.1'
#database = 'CarDatabase'
#username = 'sa'
#password = '123'
#connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


# Kết nối đến cơ sở dữ liệu
#def get_connection():
#    try:
#        conn = pyodbc.connect(connection_string)
#        return conn
#    except Exception as e:
#        print(f"Kết nối thất bại: {e}")
#        return None


# Tạo ứng dụng FastAPI
app = FastAPI()


# Định nghĩa mô hình dữ liệu
class Cars(BaseModel):
    Brand: str
    Model: str
    Year: int
    Price: float


# Template HTML dưới dạng chuỗi
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Car List</title>
    <style>
        table {
            width: 80%;
            border-collapse: collapse;
            margin: auto;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }
        .chart-container {
            width: 80%;
            margin: auto;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Car List</h1>
    <table>
        <tr>
            <th>Brand</th>
            <th>Model</th>
            <th>Year</th>
            <th>Price</th>
        </tr>
        {% for car in cars %}
        <tr>
            <td>{{ car.Brand }}</td>
            <td>{{ car.Model }}</td>
            <td>{{ car.Year }}</td>
            <td>{{ car.Price }}</td>
        </tr>
        {% endfor %}
    </table>
    <div class="chart-container">
        <canvas id="priceChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('priceChart').getContext('2d');
        const priceChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [{% for car in cars %}'{{ car.Model }}',{% endfor %}],
                datasets: [{
                    label: 'Car Prices',
                    data: [{% for car in cars %}{{ car.Price }},{% endfor %}],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def get_data() -> List[Dict[str, str]]:
    url = 'https://bonbanh.com/gia-xe-oto-vinfast'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra trạng thái của yêu cầu HTTP
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi truy cập URL: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Trích xuất dữ liệu từ trang web
    data = []

    # Giả sử bảng đầu tiên chứa dữ liệu mong muốn
    table = soup.find('table')
    if not table:
        raise HTTPException(status_code=404, detail="Không tìm thấy bảng dữ liệu")

    rows = table.find_all('tr')[1:]  # Bỏ qua hàng tiêu đề
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 2:  # Đảm bảo rằng hàng có đủ cột dữ liệu
            car_info = {
                'Brand': cols[0].get_text(strip=True),
                'Model': cols[1].get_text(strip=True),
                'Year': cols[2].get_text(strip=True),
                'Price': cols[2].get_text(strip=True)
            }
            data.append(car_info)

    # In dữ liệu để debug
    print(data)

    return data

    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

# uvicorn main:app --reload