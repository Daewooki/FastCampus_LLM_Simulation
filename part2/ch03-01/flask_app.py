from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  # CORS 추가
import json

app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청을 허용

# Swagger 설정
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'  # 위에서 만든 swagger.json 엔드포인트

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Employee Management API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# employees
employees = [
    {
        "name": "대사",
        "id": "1",
        "age": 29,
        "work": "ML Engineer",
        "team": "AI Dev"
    },
    {
        "name": "대오",
        "id": "2",
        "age": 30,
        "work": "UI/UX Designer",
        "team": "AI Dev"
    },
    {
        "name": "대육",
        "id": "3",
        "age": 31,
        "work": "DevOps",
        "team": "Infra"
    }
]

# Swagger Documentation
@app.route("/swagger.json")
def swagger():
    swagger_info = {
        "swagger": "2.0",
        "info": {
            "title": "Employee Management API",
            "description": "This is a simple Employee API to manage employees.",
            "version": "1.0.0"
        },
        "host": "localhost:5000",  # 실제 서버의 호스트 이름
        "schemes": ["http"],
        "paths": {
            "/employees": {
                "get": {
                    "summary": "Get all employees",
                    "description": "Returns a list of all employees.",
                    "responses": {
                        "200": {
                            "description": "A list of employees",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/Employee"
                                }
                            }
                        }
                    }
                }
            },
            "/employees/{id}": {
                "get": {
                    "summary": "Get employee by ID",
                    "description": "Returns a single employee by ID.",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "string",
                            "description": "The employee's ID"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "A single employee",
                            "schema": {
                                "$ref": "#/definitions/Employee"
                            }
                        },
                        "404": {
                            "description": "Employee not found"
                        }
                    }
                },
                "put": {
                    "summary": "Update employee by ID",
                    "description": "Update the employee's team by ID.",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "string",
                            "description": "The employee's ID"
                        },
                        {
                            "name": "team",
                            "in": "body",
                            "required": True,
                            "description": "The updated team",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "team": {
                                        "type": "string"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "The employee was updated",
                            "schema": {
                                "$ref": "#/definitions/Employee"
                            }
                        },
                        "404": {
                            "description": "Employee not found"
                        }
                    }
                },
                "delete": {
                    "summary": "Delete employee by ID",
                    "description": "Delete an employee by ID.",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "string",
                            "description": "The employee's ID"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Employee was deleted"
                        },
                        "404": {
                            "description": "Employee not found"
                        }
                    }
                }
            },
            "/new_employees": {
                "post": {
                    "summary": "Add a new employee",
                    "description": "Add a new employee to the list.",
                    "parameters": [
                        {
                            "name": "employee",
                            "in": "body",
                            "required": True,
                            "description": "The employee to create",
                            "schema": {
                                "$ref": "#/definitions/Employee"
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Employee was created",
                            "schema": {
                                "$ref": "#/definitions/Employee"
                            }
                        }
                    }
                }
            }
        },
        "definitions": {
            "Employee": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "id": {
                        "type": "string"
                    },
                    "age": {
                        "type": "integer"
                    },
                    "work": {
                        "type": "string"
                    },
                    "team": {
                        "type": "string"
                    }
                }
            }
        }
    }
    return jsonify(swagger_info)

# API 엔드포인트들
@app.route('/employees', methods=['GET'])
def get_employees():
    response = json.dumps({'employees': employees}, ensure_ascii=False)
    print("\n--- 전체 직원 목록 ---")
    for emp in employees:
        print(f"ID: {emp['id']}, 이름: {emp['name']}, 나이: {emp['age']}, 직무: {emp['work']}, 팀: {emp['team']}")
    return response

@app.route('/employees/<string:id>', methods=['GET'])
def get_employees_with_id(id):
    for emp in employees:
        if id == emp['id']:
            print("\n--- 조회된 직원 ---")
            print(f"ID: {emp['id']}, 이름: {emp['name']}, 나이: {emp['age']}, 직무: {emp['work']}, 팀: {emp['team']}")
            return jsonify({'employees': emp})
    print(f"\n--- ID: {id} 일치 직원 없음 ---")
    return jsonify({'employees': '일치 직원 없음'})

@app.route('/new_employees', methods=['POST'])
def new_employees():
    if request.method == 'POST':
        params = request.get_json()
        for emp in employees:
            if emp['id'] == params['id']:
                print(f"\n--- ID: {params['id']} 이미 존재하는 직원 ---")
                return jsonify({'error': '이미 존재하는 ID입니다.'}), 400
        
        temp = {
            'name': params['name'],
            'id': params['id'],
            'age': params['age'],
            'work': params['work'],
            'team': params['team']
        }
        employees.append(temp)
        print("\n--- 새로 추가된 직원 ---")
        print(f"ID: {temp['id']}, 이름: {temp['name']}, 나이: {temp['age']}, 직무: {temp['work']}, 팀: {temp['team']}")
        print("\n--- 전체 직원 목록 ---")
        for emp in employees:
            print(f"ID: {emp['id']}, 이름: {emp['name']}, 나이: {emp['age']}, 직무: {emp['work']}, 팀: {emp['team']}")
        return jsonify({'New': temp}), 201

@app.route('/employees/<string:id>', methods=['PUT'])
def update_employees(id):
    params = request.get_json()
    for emp in employees:
        if id == emp['id']:
            emp['team'] = params['team']
            print("\n--- 업데이트된 직원 ---")
            print(f"ID: {emp['id']}, 이름: {emp['name']}, 나이: {emp['age']}, 직무: {emp['work']}, 팀: {emp['team']}")
            print("\n--- 전체 직원 목록 ---")
            for emp in employees:
                print(f"ID: {emp['id']}, 이름: {emp['name']}, 나이: {emp['age']}, 직무: {emp['work']}, 팀: {emp['team']}")
            return jsonify({'update': emp})
    print(f"\n--- ID: {id} 일치 직원 없음 ---")
    return jsonify({'update': '일치 직원 없음'})

@app.route('/employees/<string:id>', methods=['DELETE'])
def delete_employees(id):
    for emp in employees:
        if id == emp['id']:
            employees.remove(emp)
            print(f"\n--- 삭제된 직원 ID: {id} ---")
            print("\n--- 전체 직원 목록 ---")
            for emp in employees:
                print(f"ID: {emp['id']}, 이름: {emp['name']}, 나이: {emp['age']}, 직무: {emp['work']}, 팀: {emp['team']}")
            return jsonify({'delete': True})
    print(f"\n--- ID: {id} 일치 직원 없음 ---")
    return jsonify({'delete': '일치 직원 없음'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
