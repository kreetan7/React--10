from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
tasks = []
task_id_counter = 1


# Home route
@app.route('/')
def home():
    return {"message": "Task Manager API is running 🚀"}


# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


# Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter

    data = request.get_json()
    task = {
        "id": task_id_counter,
        "title": data.get("title"),
        "completed": False
    }

    tasks.append(task)
    task_id_counter += 1

    return jsonify(task), 201


# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["completed"] = data.get("completed", task["completed"])
            return jsonify(task)

    return {"error": "Task not found"}, 404


# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]

    return {"message": "Task deleted"}


if __name__ == '__main__':
    app.run(debug=True)