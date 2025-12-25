# Manual Acceptance Checks — Phase I

1. Add a task

   - Run app, choose Add, enter title and optional description.
   - Expect: success message and assigned ID.

2. View tasks

   - Choose View All.
   - Expect: list showing ID, completion status, title.

3. Mark complete/incomplete

   - Choose Mark, provide ID and confirm status.
   - Expect: task status updated when viewing.

4. Update task

   - Choose Update, provide ID, new title/description.
   - Expect: updated fields reflected in view.

5. Delete task

   - Choose Delete, provide ID, confirm.
   - Expect: task removed from list.

6. Invalid inputs
   - Provide empty title on Add/Update → Expect validation message.
   - Provide invalid/nonexistent ID → Expect friendly error.
