# 03. Staff & Teacher Portal — XYZ AI

The **Staff & Teacher Portal** equips teachers with classroom management tools and an efficient, professional **Teaching Assistant** for rapid daily attendance marking and student reviews.

## Key Features
- **Conversational Voice Attendance Marker**: Speak or type *"Mark Rahul absent today"* to automatically update attendance and audit logs.
- **Class Roster**: Live roster for assigned classes (Grade 10-A) with one-click status toggles.
- **Entity Ownership Protection**: Teachers can only view and mark attendance for classes assigned to them (`teacher_class_links`).
- **Student Performance**: Instant alerts for students needing academic support or with low attendance.
- **3D Avatar & Speech**: Professional faculty AI persona with voice interaction.

## Running Locally
```bash
python -m http.server 3003 --directory 03_staff_portal
```
Visit: [http://localhost:3003](http://localhost:3003)
