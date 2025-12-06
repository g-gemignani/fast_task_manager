from nicegui import ui
import httpx # A modern, async HTTP client for Python

# The base URL for your FastAPI Task Manager
API_URL = "http://127.0.0.1:8000/tasks/"

async def load_tasks():
    """Fetches all tasks from the FastAPI backend."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API_URL)
            response.raise_for_status() # Raise an exception for bad status codes
            tasks = response.json()
            task_list.clear()
            # NEW: Interactive rendering using a Checkbox
            with task_list:
                for task in tasks:
                    with ui.row().classes('items-center justify-between w-full p-2 hover:bg-gray-100 rounded'):
                        # Create a checkbox tied to the task's current status
                        checkbox = ui.checkbox(
                            text=f"ID {task['id']}: {task['title']}", 
                            value=task['completed']
                        ).classes('text-lg')
                        
                        # When the checkbox is clicked (toggled), call the update function
                        checkbox.on('change', lambda e, id=task['id']: 
                            toggle_task_status(id, e.value)
                        )
                                                
                        # Add a visual indicator for completion status
                        ui.icon('done_all' if task['completed'] else 'pending').classes('text-green-600' if task['completed'] else 'text-yellow-600')
                    
        except httpx.HTTPError as e:
            ui.notify(f"Error connecting to API: {e}", color='negative')

async def add_task():
    """Sends a new task to the FastAPI backend."""
    new_title = title_input.value
    if not new_title:
        ui.notify("Title cannot be empty.", color='warning')
        return

    payload = {"title": new_title, "description": "Added via GUI"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            ui.notify(f"Task '{new_title}' created!", color='positive')
            title_input.value = ''
            await load_tasks() # Refresh the list
        except httpx.HTTPError as e:
            ui.notify(f"Failed to create task: {e}", color='negative')

def run_gui():
    # --- GUI Layout ---
    ui.page_title('FastAPI Task Manager GUI')

    with ui.card():
        ui.label('FastAPI Task Manager').classes('text-2xl font-bold')
        
        # Input for new task
        global title_input
        title_input = ui.input(label='New Task Title').classes('w-full')
        ui.button('Add Task', on_click=add_task).classes('w-full')
        
        ui.separator()
        ui.label('Current Tasks:').classes('text-xl mt-4')
        
        # Container to hold the list of tasks
        global task_list
        task_list = ui.column().classes('w-full')
        
    # Button to manually refresh and initial load
    ui.button('Refresh Tasks', on_click=load_tasks).classes('mt-4')

    # Schedule a single immediate call to load tasks after the UI starts.
    # `ui.run` forwards kwargs to the underlying server config and some
    # parameters like `on_startup` are not accepted there, which causes
    # a TypeError. Using `ui.timer(0, ...)` schedules an async call once
    # the UI loop is running and is compatible across NiceGUI versions.
    ui.timer(0, load_tasks, once=True)
    # Add logging around ui.run to ensure any exceptions are visible
    import traceback
    import sys

    print("[fast_task_manager.gui] launching ui.run()", flush=True)
    try:
        ui.run(title='Task GUI', port=8080)
    except Exception:
        print("[fast_task_manager.gui] ui.run() raised:", flush=True)
        traceback.print_exc()
        sys.exit(1)


# In gui.py
async def toggle_task_status(task_id: int, completed: bool):
    """Sends a PUT request to update a task's completion status."""
    # Note: We send 'completed' as a query parameter in the URL
    url = f"{API_URL}{task_id}/complete?completed={completed}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url)
            response.raise_for_status()
            status = "completed" if completed else "reopened"
            ui.notify(f"Task ID {task_id} successfully {status}!", color='info')
            await load_tasks() # Refresh the list immediately
        except httpx.HTTPError as e:
            ui.notify(f"Failed to update task {task_id}: {e}", color='negative')


if __name__ in {"__main__", "__mp_main__"}:
    # Allow the module to be executed with `python -m fast_task_manager.gui`
    # and to work correctly with multiprocessing start methods that set
    # __name__ to "__mp_main__" (recommended by NiceGUI docs).
    run_gui()
