/**
 * XYZ AI — Shared TypeScript Type Definitions
 * Used by student-portal, parent-portal, staff-portal, and management-portal
 */

export type UserRole = 'student' | 'parent' | 'teacher' | 'principal';

export type SupportedLanguage =
  | 'en' // English
  | 'hi' // Hindi
  | 'ta' // Tamil
  | 'te' // Telugu
  | 'mr' // Marathi
  | 'bn' // Bengali
  | 'gu' // Gujarati
  | 'pa' // Punjabi
  | 'kn' // Kannada
  | 'ml' // Malayalam
  | 'ur'; // Urdu

export interface UserProfile {
  id: string;
  auth_id: string;
  email: string;
  name: string;
  role: UserRole;
  phone?: string;
  preferred_language: SupportedLanguage;
  avatar_url?: string;
}

export interface StudentRecord {
  id: string;
  user_id: string;
  roll_number: string;
  name: string;
  class_id: string;
  class_name?: string;
  date_of_birth?: string;
  gender?: string;
}

export interface AttendanceRecord {
  id: string;
  student_id: string;
  student_name?: string;
  class_id: string;
  date: string;
  status: 'present' | 'absent' | 'late' | 'excused';
  remarks?: string;
}

export interface AttendanceSummary {
  student_id: string;
  student_name: string;
  total_days: number;
  present_days: number;
  absent_days: number;
  late_days: number;
  percentage: number;
  recent_records: AttendanceRecord[];
}

export interface GradeRecord {
  id: string;
  student_id: string;
  subject_id: string;
  subject_name: string;
  subject_code: string;
  exam_id: string;
  exam_name: string;
  marks_obtained: number;
  max_marks: number;
  grade: string;
  remarks?: string;
}

export interface FeeInvoice {
  id: string;
  student_id: string;
  term: string;
  academic_year: string;
  total_amount: number;
  amount_paid: number;
  due_date: string;
  status: 'paid' | 'partial' | 'unpaid' | 'overdue';
  receipt_no?: string;
}

export interface TimetableSlot {
  id: string;
  class_id: string;
  day_of_week: string;
  period_number: number;
  start_time: string;
  end_time: string;
  subject_name: string;
  teacher_name: string;
  room_number?: string;
}

export interface HomeworkItem {
  id: string;
  class_id: string;
  subject_name: string;
  teacher_name: string;
  title: string;
  description: string;
  assigned_date: string;
  due_date: string;
}

export interface SchoolNotice {
  id: string;
  title: string;
  body: string;
  posted_by_name: string;
  target_role: string;
  is_urgent: boolean;
  created_at: string;
}

export interface LeaveApplication {
  id: string;
  applicant_user_id: string;
  applicant_role: UserRole;
  student_id?: string;
  student_name?: string;
  start_date: string;
  end_date: string;
  reason: string;
  status: 'pending' | 'approved' | 'rejected';
  approved_by?: string;
  remarks?: string;
  created_at: string;
}

export interface EscalationTicket {
  id: string;
  requested_by_user_id: string;
  requested_by_role: UserRole;
  student_id?: string;
  target_entity: 'teacher' | 'management' | 'principal' | 'counselor';
  target_user_name?: string;
  reason: string;
  status: 'pending' | 'confirmed' | 'failed' | 'resolved';
  created_at: string;
  resolution_notes?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  tool_calls?: Array<{
    name: string;
    arguments: Record<string, any>;
    result?: any;
  }>;
  audio_url?: string;
  visemes?: Array<{ time: number; viseme: string }>;
  suggested_actions?: Array<{ label: string; action_type: string; payload?: any }>;
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  language?: SupportedLanguage;
}

export interface ChatResponse {
  response_text: string;
  session_id: string;
  language: SupportedLanguage;
  audio_base64?: string;
  visemes?: Array<{ time: number; viseme: string }>;
  suggested_actions?: Array<{ label: string; action_type: string; payload?: any }>;
  executed_tools?: string[];
}
