from flask import Flask, session, request, jsonify, send_file, Response
import uuid
import io
from datetime import datetime, timedelta, timezone
from maze_gen import Maze, bfs_shortest_path, gen_maze_image, depth_first_recursive_backtracker
import secrets
from threading import Lock


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

GRID_SIZE = 25
TASK_EXPIRY_TIME = timedelta(seconds=0.3)
REQUIRED_SOLUTIONS = 100

class MazeTask:
    def __init__(self, maze, solution, png_bytes, created_at):
        self.maze = maze
        self.solution = solution
        self.png_bytes = png_bytes
        self.created_at = created_at

    def __del__(self):
        del self.maze

tasks = {}
tasks_lock = Lock()


def create_task() -> str:
    size = session.get("maze_size", GRID_SIZE)

    maze = Maze(size, size)
    depth_first_recursive_backtracker(maze)

    solution = bfs_shortest_path(maze)
    png_io = gen_maze_image(maze, 'vova.png', 'portal.png')

    task_id = str(uuid.uuid4())
    task = MazeTask(maze, solution, png_io.getvalue(), datetime.now(timezone.utc))

    with tasks_lock:
        tasks[task_id] = task

    session["task_id"] = task_id
    session["maze_solved"] = False
    return task_id

def is_task_expired() -> bool:
    if "task_id" not in session:
        return True

    task_id = session["task_id"]

    with tasks_lock:
        task = tasks.get(task_id)
        solved = session.get("maze_solved", False)
        expired = (task is None or datetime.now(timezone.utc) >= task.created_at + TASK_EXPIRY_TIME)
        if solved:
            return True
        if expired:
            if task:
                del tasks[task_id]
            return True
    return False

@app.route("/maze", methods=["GET"])
def labyrinth():
    if session.get("maze_solved"):
        create_task()
        session["maze_solved"] = False

    if is_task_expired():
        create_task()
        session["solved_count"] = 0

    task_id = session.get("task_id")
    with tasks_lock:
        png_bytes = tasks[task_id].png_bytes

    return send_file(io.BytesIO(png_bytes), mimetype='image/png')

@app.route("/solve", methods=["POST"])
def solve():
    if is_task_expired():
        session.pop("task_id", None)
        session["maze_solved"] = False
        session["solved_count"] = 0
        return jsonify({"status": "fail", "reason": "expired_task"}), 400

    moves = request.json.get('moves', [])
    if type(moves) != list or any(type(step) != str for step in moves):
        return jsonify({"status": "fail", "reason": "invalid request"}), 400

    task_id = session["task_id"]
    with tasks_lock:
        task = tasks.get(task_id)
        if task is None:
            session.pop("task_id", None)
            return jsonify({"status": "fail", "reason": "task is none"}), 400

        if moves != task.solution:
            session["solved_count"] = 0
            return jsonify({"status": "fail", "reason": "incorrect moves"}), 400

        if "solved_count" not in session:
            session["solved_count"] = 0

        session["solved_count"] += 1
        session["maze_solved"] = True

        tasks.pop(task_id, None)
        session.pop("task_id", None)

    if session["solved_count"] >= REQUIRED_SOLUTIONS:
        with open("flag", "r", encoding="utf-8") as f:
            flag = f.read()
        return Response(flag, mimetype="text/plain")

    return jsonify({"status": "ok", "message": "Correct moves!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
