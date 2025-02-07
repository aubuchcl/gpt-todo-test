import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get("/tasks");
      setTasks(response.data);
    } catch (error) {
      console.error("Error fetching tasks", error);
    }
  };

  const addTask = async () => {
    if (!newTask.trim()) return;
    try {
      await axios.post("/tasks", { title: newTask });
      setNewTask("");
      fetchTasks();
    } catch (error) {
      console.error("Error adding task", error);
    }
  };

  const toggleTask = async (id) => {
    try {
      await axios.put(`/tasks/${id}`);
      fetchTasks();
    } catch (error) {
      console.error("Error updating task", error);
    }
  };

  const deleteTask = async (id) => {
    try {
      await axios.delete(`/tasks/${id}`);
      fetchTasks();
    } catch (error) {
      console.error("Error deleting task", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h1 className="text-2xl font-bold mb-4">To-Do List</h1>
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            className="flex-1 p-2 border rounded"
            placeholder="New Task"
          />
          <button onClick={addTask} className="bg-blue-500 text-white px-4 py-2 rounded">
            Add
          </button>
        </div>
        <ul>
          {tasks.map((task) => (
            <li key={task.id} className="flex justify-between p-2 border-b">
              <span
                className={`${task.complete ? "line-through text-gray-500" : ""}`}
                onClick={() => toggleTask(task.id)}
              >
                {task.title}
              </span>
              <button onClick={() => deleteTask(task.id)} className="text-red-500">✘</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
